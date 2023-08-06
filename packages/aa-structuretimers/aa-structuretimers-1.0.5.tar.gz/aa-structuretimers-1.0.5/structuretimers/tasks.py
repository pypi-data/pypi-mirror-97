from datetime import timedelta

from celery import shared_task

from django.contrib.auth.models import User
from django.db import transaction, DatabaseError
from django.utils.timezone import now

from allianceauth.notifications import notify
from allianceauth.services.hooks import get_extension_logger
from allianceauth.services.tasks import QueueOnce

from . import __title__
from .models import DiscordWebhook, NotificationRule, ScheduledNotification, Timer
from app_utils.logging import LoggerAddTag


logger = LoggerAddTag(get_extension_logger(__name__), __title__)
TASK_PRIO_HIGH = 4


@shared_task(base=QueueOnce, acks_late=True)
def send_messages_for_webhook(webhook_pk: int) -> None:
    """sends all currently queued messages for given webhook to Discord"""
    try:
        webhook = DiscordWebhook.objects.get(pk=webhook_pk)
    except DiscordWebhook.DoesNotExist:
        logger.error(
            "DiscordWebhook with pk = %s does not exist. Aborting.", webhook_pk
        )
    else:
        if not webhook.is_enabled:
            logger.info(
                "Tracker %s: DiscordWebhook disabled - skipping sending", webhook
            )
            return

        logger.info("Started sending messages to webhook %s", webhook)
        webhook.send_queued_messages()
        logger.info("Completed sending messages to webhook %s", webhook)


@shared_task(base=QueueOnce, bind=True, acks_late=True)
def send_scheduled_notification(self, scheduled_notification_pk: int) -> None:
    """Sends a scheduled notification for a timer based on a notification rule"""
    with transaction.atomic():
        try:
            scheduled_notification = (
                ScheduledNotification.objects.select_for_update().get(
                    pk=scheduled_notification_pk
                )
            )
        except (ScheduledNotification.DoesNotExist, DatabaseError):
            logger.info(
                "ScheduledNotification with pk = %s does not / no longer exist "
                "or is being processed by another task. Discarding.",
                scheduled_notification_pk,
                exc_info=True,
            )
            return
        logger.debug(
            "Delete scheduled_notification in task_id = %s: %r",
            self.request.id,
            scheduled_notification,
        )
        scheduled_notification.delete()

    timer = scheduled_notification.timer
    notification_rule = scheduled_notification.notification_rule
    if scheduled_notification.celery_task_id != self.request.id:
        logger.info(
            "Discarded outdated scheduled notification: %r",
            scheduled_notification,
        )
    elif not notification_rule.is_enabled:
        logger.info(
            "Discarded scheduled notification based on disabled rule: %r",
            scheduled_notification,
        )
    else:
        logger.info(
            "Sending notifications for timer '%s' and rule '%s'",
            timer,
            notification_rule,
        )
        webhook = notification_rule.webhook
        if webhook.is_enabled:
            minutes = round((timer.date - now()).total_seconds() / 60)
            mod_text = "**important** " if timer.is_important else ""
            content = (
                f"The following {mod_text}structure timer will elapse "
                f"in less than **{minutes:,}** minutes:"
            )
            timer.send_notification(
                webhook=webhook,
                content=notification_rule.prepend_ping_text(content),
            )
            send_messages_for_webhook.apply_async(
                args=[webhook.pk], priority=TASK_PRIO_HIGH
            )
        else:
            logger.warning(
                "Webhook not enabled for %r. Discarding.", scheduled_notification
            )


@shared_task
def notify_about_new_timer(timer_pk: int, notification_rule_pk: int) -> None:
    try:
        timer = Timer.objects.get(pk=timer_pk)
        notification_rule = NotificationRule.objects.select_related("webhook").get(
            pk=notification_rule_pk
        )
    except Timer.DoesNotExist:
        logger.error("Timer with pk = %s does not exist. Aborting.", timer_pk)
    except NotificationRule.DoesNotExist:
        logger.error(
            "NotificationRule with pk = %s does not exist. Aborting.",
            notification_rule_pk,
        )
    else:
        if notification_rule.is_enabled and notification_rule.webhook.is_enabled:
            content = f"New timer added by **{timer.eve_character}**:"
            timer.send_notification(
                webhook=notification_rule.webhook,
                content=notification_rule.prepend_ping_text(content),
            )
            send_messages_for_webhook.apply_async(
                args=[notification_rule.webhook.pk], priority=TASK_PRIO_HIGH
            )


def _schedule_notification_for_timer(
    timer: Timer, notification_rule: NotificationRule
) -> ScheduledNotification:
    logger.info(
        "Scheduling fresh notification for timer #%d, rule #%d",
        timer.pk,
        notification_rule.pk,
    )
    notification_date = timer.date - timedelta(minutes=notification_rule.scheduled_time)
    scheduled_notification, _ = ScheduledNotification.objects.update_or_create(
        timer=timer,
        notification_rule=notification_rule,
        defaults={"timer_date": timer.date, "notification_date": notification_date},
    )
    result = send_scheduled_notification.apply_async(
        kwargs={"scheduled_notification_pk": scheduled_notification.pk},
        eta=timer.date - timedelta(minutes=notification_rule.scheduled_time),
        priority=TASK_PRIO_HIGH,
    )
    scheduled_notification.celery_task_id = result.task_id
    scheduled_notification.save()

    return scheduled_notification


def _revoke_notification_for_timer(
    scheduled_notification: ScheduledNotification,
) -> None:
    logger.info(
        "Removing stale notification for timer #%d, rule #%d",
        scheduled_notification.timer.pk,
        scheduled_notification.notification_rule.pk,
    )
    scheduled_notification.delete()


@shared_task(acks_late=True)
def schedule_notifications_for_timer(timer_pk: int, is_new: bool = False) -> None:
    """Schedules notifications for this timer based on notification rules"""
    try:
        timer = Timer.objects.get(pk=timer_pk)
    except Timer.DoesNotExist:
        logger.error("Timer with pk = %s does not exist. Aborting.", timer_pk)
    else:
        if timer.date > now():
            # trigger: newly created
            if is_new:
                rules = (
                    NotificationRule.objects.select_related("webhook")
                    .filter(
                        is_enabled=True,
                        trigger=NotificationRule.TRIGGER_NEW_TIMER_CREATED,
                        webhook__is_enabled=True,
                    )
                    .conforms_with_timer(timer)
                )
                if rules:
                    for rule in rules:
                        notify_about_new_timer.apply_async(
                            kwargs={
                                "timer_pk": timer.pk,
                                "notification_rule_pk": rule.pk,
                            },
                            priority=TASK_PRIO_HIGH,
                        )

            # trigger: timer elapses soon
            with transaction.atomic():
                # remove existing scheduled notifications if date has changed
                for obj in ScheduledNotification.objects.filter(timer=timer).exclude(
                    timer_date=timer.date
                ):
                    _revoke_notification_for_timer(scheduled_notification=obj)

                # schedule new notifications
                for notification_rule in NotificationRule.objects.filter(
                    is_enabled=True,
                    trigger=NotificationRule.TRIGGER_SCHEDULED_TIME_REACHED,
                ).conforms_with_timer(timer):
                    _schedule_notification_for_timer(
                        timer=timer, notification_rule=notification_rule
                    )
        else:
            logger.warning("Can not schedule notification for past timer: %s", timer)


@shared_task(acks_late=True)
def schedule_notifications_for_rule(notification_rule_pk: int) -> None:
    """Schedules notifications for all timers confirming with this rule.
    Will recreate all existing and still pending notifications
    """
    try:
        notification_rule = NotificationRule.objects.get(pk=notification_rule_pk)
    except NotificationRule.DoesNotExist:
        logger.error(
            "NotificationRule with pk = %s does not exist. Aborting.",
            notification_rule_pk,
        )
    else:
        if notification_rule.trigger == NotificationRule.TRIGGER_NEW_TIMER_CREATED:
            logger.error(
                "NotificationRule with pk = %s has the wrong trigger. Aborting.",
                notification_rule_pk,
            )
        else:
            logger.debug(
                "Checking scheduled notifications for: %s",
                notification_rule,
            )
            with transaction.atomic():
                for obj in notification_rule.schedulednotification_set.filter(
                    timer_date__gt=now()
                ):
                    _revoke_notification_for_timer(scheduled_notification=obj)

                for timer in Timer.objects.filter(
                    date__gt=now()
                ).conforms_with_notification_rule(notification_rule):
                    _schedule_notification_for_timer(
                        timer=timer, notification_rule=notification_rule
                    )


@shared_task
def send_test_message_to_webhook(webhook_pk: int, user_pk: int = None) -> None:
    """send a test message to given webhook.
    Optional inform user about result if user ok is given
    """
    try:
        webhook = DiscordWebhook.objects.get(pk=webhook_pk)
        if user_pk:
            user = User.objects.get(pk=user_pk)
        else:
            user = None
    except DiscordWebhook.DoesNotExist:
        logger.error(
            "DiscordWebhook with pk = %s does not exist. Aborting.", webhook_pk
        )
    except User.DoesNotExist:
        logger.warning("User with pk = %s does not exist. Aborting.", user_pk)
    else:
        logger.info("Sending test message to webhook %s", webhook)
        error_text, success = webhook.send_test_message(user)

        if user:
            message = (
                f"Error text: {error_text}\nCheck log files for details."
                if not success
                else "No errors"
            )
            level = "success" if success else "error"
            notify(
                user=user,
                title=(
                    f"{__title__}: Result of test message to webhook {webhook}: "
                    f"{level.upper()}"
                ),
                message=message,
                level=level,
            )


@shared_task
def housekeeping() -> None:
    """Perform housekeeping tasks"""
    logger.info("Performing housekeeping")
    deleted_count = Timer.objects.delete_obsolete()
    logger.info(f"Deleted {deleted_count:,} obsolete timers.")
