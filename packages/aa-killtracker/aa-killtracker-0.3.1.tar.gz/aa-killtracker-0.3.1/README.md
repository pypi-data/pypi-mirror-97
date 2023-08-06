# killtracker

An app for running killmail trackers with Alliance Auth and Discord

[![release](https://img.shields.io/pypi/v/aa-killtracker?label=release)](https://pypi.org/project/aa-killtracker/)
[![python](https://img.shields.io/pypi/pyversions/aa-killtracker)](https://pypi.org/project/aa-killtracker/)
[![django](https://img.shields.io/pypi/djversions/aa-killtracker?label=django)](https://pypi.org/project/aa-killtracker/)
[![pipeline](https://gitlab.com/ErikKalkoken/aa-killtracker/badges/master/pipeline.svg)](https://gitlab.com/ErikKalkoken/aa-killtracker/-/pipelines)
[![codecov](https://codecov.io/gl/ErikKalkoken/aa-killtracker/branch/\x6d6173746572/graph/badge.svg?token=ZTGEX30YIN)](https://codecov.io/gl/ErikKalkoken/aa-killtracker)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/aa-killtracker/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/mevDXbxp4R)

## Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Trackers](#trackers)
- [Settings](#settings)
- [Change Log](CHANGELOG.md)

## Overview

Killtracker is an app for running killmail based trackers with Alliance Auth and Discord. Trackers are small programs that automatically select killmails based on a set of pre-defined conditions and then post them to a Discord channel as soon as they appear on zKillboard.

The main advantage of the Killtracker app over similar apps is it's high customizability, which allows you to cut through the noise of many false positives and only get the results you are really interested in.

For example you may want to know when a larger group is roaming through your area? Set up a tracker that shows all kills within 10 jumps of your staging that has more than 20 attackers. It will even ping you if you want.

Or you maybe want to be informed about any capitals being active within your jump range? Just setup a tracker for capital kills within 6 LY of your staging.

## Key Features

- Automatically post killmails conforming with a set of conditions to a Discord channel as soon as they arrive on zKillboard
- Use 20+ clauses to define exactly what you want to track incl. clauses for location, organization and ship types
- Clauses for "ship types" include ships, structures, customs offices, fighters and excavator drones
- Optional channel and group pinging for matching killmails
- Designed for fast response times, high throughput and low resource requirements
- Get additional insights about killmails like distance from staging
- See which fleets / groups are active in your area of interest
- Customize killmail messages with titles and colors

## Screenshots

Here is an example for settings up a new tracker:

![Tracker1](https://i.imgur.com/fkCOmGM.png)

And here is how posted killmails look on Discord:

![Discord](https://i.imgur.com/zCCzEpU.png)

## Installation

### Step 1 - Check preconditions

1. Killtracker is a plugin for Alliance Auth. If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/auth/allianceauth/) for details)

2. Killtracker needs the app [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse) to function. Please make sure it is installed, before continuing.

### Step 2 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the newest release from PyPI:

```bash
pip install aa-killtracker
```

### Step 3 - Configure settings

Configure your Auth settings (`local.py`) as follows:

- Add `'killtracker'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
CELERYBEAT_SCHEDULE['killtracker_run_killtracker'] = {
    'task': 'killtracker.tasks.run_killtracker',
    'schedule': crontab(minute='*/1'),
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

### Step 5 - Load Eve Universe map data

In order to be able to select solar systems and types for trackers you need to load that data from ESI once.

Load Eve Online map: (If you already have run this command with another app you can skip this step)

```bash
python manage.py eveuniverse_load_data map
```

Load app specific types:

```bash
python manage.py killtracker_load_eve
```

You may want to wait until the loading is complete before starting to create new trackers.

### Step 6 - Setup trackers

The setup and configuration for trackers is done on the admin page under **Killtracker**.

First need to add the Discord webhook that points to the channel you want your killmail to appear to **Webhooks**. You can use one webhook for all trackers, but it is usually better to create a new channel / webhook for each tracker.

To test that your webhook works correctly you can send a test notification.

Next you can create your trackers under **Tracker**. Make sure you link each tracker to the right webhook. Once you save a tracker that is **enabled** it will start working.

As final test that your setup is correct you may want to create a "Catch all" tracker. for that just create a new tracker without any conditions and it will forward all killmails to your Discord channel as they are received.

Congratulations you are now ready to use killtracker!

## Trackers

All trackers are setup and configured on the admin site under **Killtracker**.

Each tracker has a name, is linked to a webhook and has a set of conditions that define which killmails are selected and shown in the Discord channel. Note that if you define a tracker without any conditions tan you got a "catch all" tracker, that will post any killmail on Discord.

Each of the 20+ conditions belongs to one of two categories and they are named accordingly:

- **require**: Require conditions must be fulfilled by a killmail. e.g. a tracker with the condition **require min attackers = 10** will post only killmails on Discord that have at least 10 attackers.
- **exclude**: Exclude conditions are the opposite of require. Killmails that fulfil this condition will never be posted by this tracker. e.g. a tracker with **exclude high sec** will never show any killmails from high sec.

You can combine multiple conditions to create the tracker you want. Note that conditions are always combined together with a boolean AND. For example: if your tracker has **require min attackers** set to 10 and **exclude high sec** enabled, then you will only get killmails that both have at least 10 attackers and are not in high sec.

Here is a list of all currently supported conditions for each tracker:

Name | Description
-- | --
require max jumps|Require all killmails to be max x jumps away from origin solar system
require max distance|Require all killmails to be max x LY away from origin solar system
require min attackers|Require killmails to have at least given number of attackers
require max attackers|Require killmails to have no more than max number of attackers
exclude high sec|exclude killmails from high sec. Also exclude high sec systems in route finder for jumps from origin.
exclude low sec|exclude killmails from low sec
exclude null sec|exclude killmails from null sec
exclude w space|exclude killmails from WH space
require min value|Require killmail's value to be greater or equal to the given value in M ISK
exclude npc kills|exclude npc kills
require npc kills|only include killmails that are npc kills
exclude attacker alliances|exclude killmails with attackers from one of these alliances
exclude attacker corporations|exclude killmails with attackers from one of these corporations
require attacker alliances|only include killmails with attackers from one of these alliances
require attacker corporations|only include killmails with attackers from one of these corporations
require victim alliances|only include killmails where the victim belongs to one of these alliances
require victim corporations|only include killmails where the victim belongs to one of these corporations
require regions|Only include killmails that occurred in one of these regions
require constellations|Only include killmails that occurred in one of these regions
require solar systems|Only include killmails that occurred in one of these regions
require attackers ship groups|Only include killmails where at least one attacker is flying one of these ship groups
require attackers ship types|Only include killmails where at least one attacker is flying one of these ship types
require victim ship groups|Only include killmails where victim is flying one of these ship groups
require victim ship types|Only include killmails where victim is flying one of these ship types

## Settings

Here is a list of available settings for this app. They can be configured by adding them to your AA settings file (`local.py`).

Note that all settings are optional and the app will use the documented default settings if they are not used.

Name | Description | Default
-- | -- | --
`KILLTRACKER_KILLMAIL_MAX_AGE_FOR_TRACKER`| Ignore killmails that are older than the given number in minutes. Sometimes killmails appear belated on ZKB, this feature ensures they don't create new alerts | `60`
`KILLTRACKER_MAX_KILLMAILS_PER_RUN`| Maximum number of killmails retrieved from ZKB by task run. This value should be set such that the task that fetches new killmails from ZKB every minute will reliable finish within one minute. To test this run a "Catch all" tracker and see how many killmails your system is capable of processing. Note that you can get that information from the worker's log file. It will look something like this: `Total killmails received from ZKB in 49 secs: 251`   | `250`
`KILLTRACKER_PURGE_KILLMAILS_AFTER_DAYS`| Killmails older than set number of days will be purged from the database. If you want to keep all killmails set this to 0. Note that this setting is only relevant if you have storing killmails enabled.  | `30`
`KILLTRACKER_WEBHOOK_SET_AVATAR`| Wether app sets the name and avatar icon of a webhook. When False the webhook will use it's own values as set on the platform  | `True`
`KILLTRACKER_STORING_KILLMAILS_ENABLED`| If set to true Killtracker will automatically store all received killmails in the local database. This can be useful if you want to run analytics on killmails etc. However, please note that Killtracker itself currently does not use stored killmails in any way.  | `False`
