# Structure Timers II

An app for keeping track of Eve Online structure timers with Alliance Auth and Discord.

[![release](https://img.shields.io/pypi/v/aa-structuretimers?label=release)](https://pypi.org/project/aa-structuretimers/)
[![python](https://img.shields.io/pypi/pyversions/aa-structuretimers)](https://pypi.org/project/aa-structuretimers/)
[![django](https://img.shields.io/pypi/djversions/aa-structuretimers?label=django)](https://pypi.org/project/aa-structuretimers/)
[![pipeline](https://gitlab.com/ErikKalkoken/aa-structuretimers/badges/master/pipeline.svg)](https://gitlab.com/ErikKalkoken/aa-structuretimers/-/pipelines)
[![codecov](https://codecov.io/gl/ErikKalkoken/aa-structuretimers/branch/master/graph/badge.svg?token=J4PKTXSOBM)](https://codecov.io/gl/ErikKalkoken/aa-structuretimers)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/aa-structuretimers/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/zmh52wnfvM)

## Contents

- [Overview](#overview)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Settings](#settings)
- [Notification Rules](#notification-rules)
- [Permissions](#permissions)
- [Management commands](#management-commands)
- [Change Log](CHANGELOG.md)

## Overview

*Structure Timers II* is an enhanced version of the Alliance Auth's Structure Timers app, with many additional useful features and an improved UI. Here is a overview of it's main features in comparison to Auth's basic variant.

Feature | Auth | Structure Timer II
--|--|--
Create and edit timers for structures | x | x
See all pending timers at a glance and with live countdowns | x | x
Restrict timer access to your corporation | x | x
Restrict ability to create and delete timers to certain users | x | x
Get automatic notifications about upcoming timers on Discord  | - | x
Define a timer type (e.g. armor or hull)| - | x
Restrict timer access to your alliance | - | x
Restrict timer access to people with special clearance ("OPSEC") | - | x
Add screenshots to timers (e.g. with the structure's fitting)| - | x
Create timers more quickly and precisely with autocomplete for solar system and structure types| - | x
Find timers more quickly with filters and full text search | - | x
Automatic cleanup of elapsed timers | - | x

## Screenshots

### List of timers

![timerboard](https://i.imgur.com/MNa2IGl.png)

### Details for a timer

![timerboard](https://i.imgur.com/ZEbl2Vc.png)

### Creating a new timer

![timerboard](https://i.imgur.com/LPCEQNr.png)

### Notification on Discord

![notification](https://i.imgur.com/Knq2bif.png)

## Installation

### Step 1 - Check Preconditions

Please make sure you meet all preconditions before proceeding:

1. Structure Timers is a plugin for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth). If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/auth/allianceauth/) for details)

2. Structure Timers needs the app [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse) to function. Please make sure it is installed, before continuing.

Note that Structure Timers is compatible with Alliance Auth's Structure Timer app and can be installed in parallel.

### Step 2 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the newest release from PyPI:

```bash
pip install aa-structuretimers
```

### Step 3 - Configure settings

Configure your Auth settings (`local.py`) as follows:

- Add `'structuretimers'` to `INSTALLED_APPS`
- Add the following lines to your settings file:

```python
CELERYBEAT_SCHEDULE['structuretimers_housekeeping'] = {
    'task': 'structuretimers.tasks.housekeeping',
    'schedule': crontab(minute=0, hour=3),
}
```

- Optional: Add additional settings if you want to change any defaults. See [Settings](#settings) for the full list.

### Step 4 - Finalize installation

Run migrations & copy static files

```bash
python manage.py migrate
python manage.py collectstatic
```

Restart your supervisor services for Auth

### Step 5 - Preload Eve Universe data

In order to be able to select solar systems and structure types for timers you need to preload some data from ESI once. If you already have run those commands previously you can skip this step.

Load Eve Online map:

```bash
python manage.py eveuniverse_load_data map
```

```bash
python manage.py structuretimers_load_eve
```

You may want to wait until the data loading is complete before starting to create new timers.

### Step 6 - Migrate existing timers

If you have already been using the classic app from Auth, you can migrate your existing timers over to **Structure Timers II**. Just run the following command:

```bash
python manage.py structuretimers_migrate_timers
```

Note: We suggest migration timers before setting up notification rules to avoid potential notification spam for migrated timers.

### Step 7 - Setup notification rules

If you want to receive notifications about timers on Discord you can setup notification rules on the admin site. e.g. you can setup a rule to sent notifications 60 minutes before a timer elapses. Please see [Notification Rules](#notification-rules) for details.

### Step 8 - Setup permissions

Another important step is to setup permissions, to ensure the right people have access features. Please see [Permissions](#permissions) for an overview of all permissions.

## Settings

Here is a list of available settings for this app. They can be configured by adding them to your Auth settings file (`local.py`).

Note that all settings are optional and the app will use the documented default settings if they are not used.

Name | Description | Default
-- | -- | --
`STRUCTURETIMERS_MAX_AGE_FOR_NOTIFICATIONS`| Will not sent notifications for timers, which event time is older than the given minutes | `60`
`STRUCTURETIMERS_NOTIFICATIONS_ENABLED`| Wether notifications for timers are scheduled at all | `True`
`STRUCTURETIMERS_TIMERS_OBSOLETE_AFTER_DAYS`| Minimum age in days for a timer to be considered obsolete. Obsolete timers will automatically be deleted. If you want to keep all timers, set to `None` | `30`
`STRUCTURETIMERS_DEFAULT_PAGE_LENGTH`| Default page size for timerboard. Must be an integer value from the available options in the app. | `10`
`STRUCTURETIMERS_PAGING_ENABLED`| Wether paging is enabled on the timerboard. | `True`

## Notification Rules

In *Structure Timers II* you can receive automatic notifications on Discord for timers by setting up notification rules. Notification rules allow you to define in detail what event and which kind of timers should trigger notifications.

Note that in general all rules are independent from each other and all enabled rules will be executed for every timer one by one.

### Example setup

Here is an example for a basic setup of rules:

#### Example 1: Notify about new every newly created timer without ping (e.g. into a scouts channel)

- Trigger: New timer created
- Scheduled Time: -
- Webhook: YOUR-WEBHOOK
- Ping Type: (no ping)

#### Example 2: Notify 45 minutes before any timer elapses with ping (e.g. into the FC channel)

- Trigger: Scheduled timer reached
- Scheduled Time: T - 45 minutes
- Webhook: YOUR-WEBHOOK
- Ping Type: @here

### Key concepts

Here are some key concepts. For all details please see the onscreen help text when creating rules.

#### Triggers

Notifications can be triggered by two kinds of events:

- When a new timers is created
- When the remaining time of timer has reached a defined threshold (e.g. 10 minutes before timer elapses)

#### Webhooks

Each rule has exactly one webhook. You can of course define multiple rules for the same webhook or define rules for different webhooks.

#### Timer clauses

Almost every property of a timer can be used to define rules. For example you can define to get notifications only for timers which hostile objective or only for final timers.

Note that setting a timer clause is optional and clauses that are not set, it will always match any.

## Permissions

Here are all relevant permissions:

Codename | Description
-- | --
`general - Can access this app and see timers` | Basic permission required by anyone to access this app. Gives access to the list of timers (which timers a user sees can depend on other permissions and settings for a timers)
`general - Can create new timers and edit own timers` | Users with this permission can create new timers and edit or delete their own timers.
`general - Can edit and delete any timer` | Users with this permission can edit and delete any timer.
`general - Can create and see opsec timers` | Users with this permission can create and view timers that are opsec restricted.

## Management commands

The following management commands are available:

- **structuretimers_load_eve**: Preload all eve objects required for this app to function
- **structuretimers_migrate_timers**: Migrate pending timers from Auth's Structure Timers apps
