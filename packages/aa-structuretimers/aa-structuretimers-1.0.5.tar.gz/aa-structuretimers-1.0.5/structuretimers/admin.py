from typing import Any, Dict, Optional

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.db.models.functions import Lower
from django.utils.timezone import now
from django.utils.safestring import mark_safe

from allianceauth.eveonline.models import EveAllianceInfo, EveCorporationInfo

from .models import DiscordWebhook, NotificationRule, ScheduledNotification, Timer
from . import tasks


@admin.register(DiscordWebhook)
class DiscordWebhookAdmin(admin.ModelAdmin):
    list_display = ("name", "is_enabled", "_messages_in_queue")
    list_filter = ("is_enabled",)
    ordering = ("name",)

    def _messages_in_queue(self, obj):
        return obj.queue_size()

    actions = ["send_test_message", "purge_messages"]

    def purge_messages(self, request, queryset):
        actions_count = 0
        killmails_deleted = 0
        for webhook in queryset:
            killmails_deleted += webhook.clear_queue()
            actions_count += 1

        self.message_user(
            request,
            f"Purged queued messages for {actions_count} webhooks, "
            f"deleting a total of {killmails_deleted} messages.",
        )

    purge_messages.short_description = "Purge queued messages of selected webhooks"

    def send_test_message(self, request, queryset):
        actions_count = 0
        for webhook in queryset:
            tasks.send_test_message_to_webhook.delay(webhook.pk, request.user.pk)
            actions_count += 1

        self.message_user(
            request,
            f"Initiated sending of {actions_count} test messages to "
            f"selected webhooks. You will receive a notification with the result.",
        )

    send_test_message.short_description = "Send test message to selected webhooks"


def field_nice_display(name: str) -> str:
    return name.replace("_", " ").capitalize()


class NotificationRuleAdminForm(forms.ModelForm):
    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        self._validate_not_same_options_chosen(
            cleaned_data,
            "require_timer_types",
            "exclude_timer_types",
            lambda x: NotificationRule.get_multiselect_display(x, Timer.TYPE_CHOICES),
        )
        self._validate_not_same_options_chosen(
            cleaned_data,
            "require_objectives",
            "exclude_objectives",
            lambda x: NotificationRule.get_multiselect_display(
                x, Timer.OBJECTIVE_CHOICES
            ),
        )
        self._validate_not_same_options_chosen(
            cleaned_data,
            "require_visibility",
            "exclude_visibility",
            lambda x: NotificationRule.get_multiselect_display(
                x, Timer.VISIBILITY_CHOICES
            ),
        )
        self._validate_not_same_options_chosen(
            cleaned_data,
            "require_corporations",
            "exclude_corporations",
        )
        self._validate_not_same_options_chosen(
            cleaned_data,
            "require_alliances",
            "exclude_alliances",
        )
        if (
            cleaned_data["trigger"] == NotificationRule.TRIGGER_SCHEDULED_TIME_REACHED
            and cleaned_data["scheduled_time"] is None
        ):
            raise ValidationError(
                {
                    "scheduled_time": (
                        "You need to specify scheduled time for "
                        "the `Scheduled time reached` trigger"
                    )
                }
            )

        if cleaned_data["trigger"] == NotificationRule.TRIGGER_NEW_TIMER_CREATED:
            cleaned_data["scheduled_time"] = None

        return cleaned_data

    @staticmethod
    def _validate_not_same_options_chosen(
        cleaned_data, field_name_1, field_name_2, display_func=lambda x: x
    ) -> None:
        same_options = set(cleaned_data[field_name_1]).intersection(
            set(cleaned_data[field_name_2])
        )
        if same_options:
            same_options_text = ", ".join(
                map(
                    str,
                    [display_func(x) for x in same_options],
                )
            )
            raise ValidationError(
                f"Can not choose same options for {field_nice_display(field_name_1)} "
                f"& {field_nice_display(field_name_2)}: {same_options_text}"
            )


@admin.register(NotificationRule)
class NotificationRuleAdmin(admin.ModelAdmin):
    form = NotificationRuleAdminForm
    list_display = (
        "id",
        "is_enabled",
        "trigger",
        "_time",
        "webhook",
        "ping_type",
        "_timer_clauses",
    )
    list_filter = ("is_enabled", "trigger")
    ordering = ("id",)

    def _time(self, obj) -> Optional[str]:
        if obj.scheduled_time is None:
            return None
        else:
            return obj.get_scheduled_time_display()

    _time.admin_order_field = "scheduled time"

    def _timer_clauses(self, obj) -> list:
        clauses = list()
        for field, func, choices in [
            ("require_timer_types", self._add_to_clauses_1, Timer.TYPE_CHOICES),
            ("exclude_timer_types", self._add_to_clauses_1, Timer.TYPE_CHOICES),
            ("require_objectives", self._add_to_clauses_1, Timer.OBJECTIVE_CHOICES),
            ("exclude_objectives", self._add_to_clauses_1, Timer.OBJECTIVE_CHOICES),
            ("require_visibility", self._add_to_clauses_1, Timer.VISIBILITY_CHOICES),
            ("exclude_visibility", self._add_to_clauses_1, Timer.VISIBILITY_CHOICES),
            ("require_corporations", self._add_to_clauses_2, None),
            ("exclude_corporations", self._add_to_clauses_2, None),
            ("require_alliances", self._add_to_clauses_2, None),
            ("exclude_alliances", self._add_to_clauses_2, None),
            ("is_important", self._add_to_clauses_3, None),
            ("is_opsec", self._add_to_clauses_3, None),
        ]:
            func(clauses, obj, field, choices)

        return mark_safe("<br>".join(clauses)) if clauses else None

    def _add_to_clauses_1(self, clauses, obj, field, choices):
        if getattr(obj, field):
            text = ", ".join(
                map(
                    str,
                    [
                        NotificationRule.get_multiselect_display(x, choices)
                        for x in getattr(obj, field)
                    ],
                )
            )
            self._append_field_to_clauses(clauses, field, text)

    def _add_to_clauses_2(self, clauses, obj, field, choices=None):
        if getattr(obj, field).count() > 0:
            text = ", ".join(map(str, getattr(obj, field).all()))
            self._append_field_to_clauses(clauses, field, text)

    def _add_to_clauses_3(self, clauses, obj, field, choices=None):
        if getattr(obj, field) != NotificationRule.CLAUSE_ANY:
            text = getattr(obj, f"get_{field}_display")()
            self._append_field_to_clauses(clauses, field, text)

    def _append_field_to_clauses(self, clauses, field, text):
        clauses.append(f"{field_nice_display(field)} = {text}")

    actions = ["enable_rule", "disable_rule"]

    def enable_rule(self, request, queryset):
        queryset.update(is_enabled=True)
        self.message_user(request, f"Enabled {queryset.count()} notification rules.")

    enable_rule.short_description = "Enable selected notification rules"

    def disable_rule(self, request, queryset):
        queryset.update(is_enabled=False)
        self.message_user(request, f"Disabled {queryset.count()} notification rules.")

    disable_rule.short_description = "Disable selected notification rules"

    filter_horizontal = (
        "require_alliances",
        "exclude_alliances",
        "require_corporations",
        "exclude_corporations",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "trigger",
                    "scheduled_time",
                    "webhook",
                    "ping_type",
                    "is_enabled",
                )
            },
        ),
        (
            "Timer clauses",
            {
                "classes": ("collapse",),
                "fields": (
                    "require_timer_types",
                    "exclude_timer_types",
                    "require_objectives",
                    "exclude_objectives",
                    "require_corporations",
                    "exclude_corporations",
                    "require_alliances",
                    "exclude_alliances",
                    "require_visibility",
                    "exclude_visibility",
                    "is_important",
                    "is_opsec",
                ),
            },
        ),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """overriding this formfield to have sorted lists in the form"""
        if db_field.name in {"require_alliances", "exclude_alliances"}:
            kwargs["queryset"] = EveAllianceInfo.objects.all().order_by(
                Lower("alliance_name")
            )

        elif db_field.name in {"require_corporations", "exclude_corporations"}:
            kwargs["queryset"] = EveCorporationInfo.objects.all().order_by(
                Lower("corporation_name")
            )

        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(ScheduledNotification)
class ScheduledNotificationAdmin(admin.ModelAdmin):
    list_select_related = ("timer", "notification_rule")
    list_display = ("notification_date", "timer", "notification_rule", "celery_task_id")
    list_filter = ("notification_rule",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(notification_date__gt=now()).order_by("notification_date")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    list_select_related = ("eve_solar_system", "structure_type", "user")
    list_filter = (
        "timer_type",
        ("eve_solar_system", admin.RelatedOnlyFieldListFilter),
        ("structure_type", admin.RelatedOnlyFieldListFilter),
        "objective",
        "owner_name",
        ("user", admin.RelatedOnlyFieldListFilter),
        "is_opsec",
    )
    ordering = ("-date",)
    autocomplete_fields = ["eve_solar_system", "structure_type"]

    """
    def _scheduled_notifications(self, obj):
        return sorted(
            [
                x["notification_date"].strftime(DATETIME_FORMAT)
                for x in ScheduledNotification.objects.filter(
                    timer=obj, notification_date__gt=now()
                ).values("notification_date", "notification_rule_id")
            ]
        )
    """
    actions = ["send_test_notification"]

    def send_test_notification(self, request, queryset):
        for timer in queryset:
            for webhook in DiscordWebhook.objects.filter(is_enabled=True):
                timer.send_notification(
                    webhook=webhook,
                    content=f"Test notification sent by **{request.user}**",
                )

            self.message_user(
                request, f"Initiated sending test notification for timer: {timer}"
            )

        for webhook in DiscordWebhook.objects.filter(is_enabled=True):
            tasks.send_messages_for_webhook.delay(webhook.pk)

    send_test_notification.short_description = (
        "Send test notification for selected timers to all enabled webhooks"
    )
