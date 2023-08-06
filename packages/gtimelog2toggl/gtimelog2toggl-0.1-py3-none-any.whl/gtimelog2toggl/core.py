
import datetime
import sys
import time

from gtimelog.timelog import TimeLog, Entry
from gtimelog.settings import Settings
from toggl.TogglPy import Toggl, Endpoints

from . import config as g2t_config


toggl = None     # type: Toggl
gtimelog = None  # type: TimeLog
category_map = {}


def setup():
    """
    Sets up gtimelog and toggl.
    Creates project map.
    """
    config = g2t_config.load()

    # Setup toggl
    global toggl
    toggl = Toggl()
    toggl.setAPIKey(config.api_key)

    # Setup gtimelog
    global gtimelog
    settings = Settings()
    gtimelog = TimeLog(settings.get_timelog_file(), settings.virtual_midnight)

    # Create mapping for gtimelog category -> toggl client/project
    # TODO: Cache these results?
    for category, (client, project) in config.mappings.items():
        try:
            project = toggl.getClientProject(client, project)
        except UnboundLocalError:  # TogglPy is a bit buggy
            continue
        if project:
            category_map[category] = project["data"]["id"]


def _window_for_week(date):
    """
    Reimplementation of window_for_week() but with sunday being the first day of the week.
    """
    monday = date - datetime.timedelta(date.weekday())
    sunday = monday - datetime.timedelta(1)
    min = datetime.datetime.combine(sunday, gtimelog.virtual_midnight)
    max = min + datetime.timedelta(7)
    window = gtimelog.window_for(min, max)
    return window


def _create_time_entry(duration, description, projectid, start):
    """
    This is a reimplementation of toggl.createTimeEntry() because the original code is a bit
    buggy, and doesn't allow for one to just provide a start datetime.

    Better handles timezones as well.
    """
    data = {
        "time_entry": {
            "description": description,
            "start": start.astimezone().isoformat(),
            "duration": duration,  # duration in seconds
            "pid": projectid,
            "created_with": "gtimelog2toggl",
        }
    }
    response = toggl.postRequest(Endpoints.TIME_ENTRIES, parameters=data)
    return toggl.decodeJSON(response)


def upload_entries(work_day=None, dry_run=False):
    if not work_day:
        work_day = datetime.datetime.now()
    window = _window_for_week(work_day)

    for entry in window.all_entries():
        project_id = None
        description = entry.entry
        if "**" in description or description.strip() in ("arrive", "arrived", "start"):
            continue

        category, description = gtimelog.split_category(description)
        if category:
            try:
                project_id = category_map[category]
            except KeyError:
                description = entry.entry  # Restore description

        print((
            f"[{description}]: {entry.start} -> {entry.start + entry.duration}  <{project_id}>"
        ))

        # TODO: Add a custom tag so we know it came from this script.
        #   This will help for synchronization in the future.)
        # TODO: Add checks to make sure we don't create duplicate entries.
        if not dry_run:
            _create_time_entry(
                entry.duration.seconds,
                description=description,
                projectid=project_id,
                start=entry.start,  # TODO: Do we need to adjust for timezone?
            )
            # Must sleep or Toggl complains we are going to fast.
            time.sleep(0.3)
