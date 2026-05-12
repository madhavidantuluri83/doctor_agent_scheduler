from tools.google_calendar_tool import GoogleCalendarTool
from utils.datetime_parser import extract_datetime

import dateparser
import datetime
import re

calendar_tool = GoogleCalendarTool()


def check_doctor_availability(user_input):

    # ----------------------------------------
    # EXTRACT DATE/TIME
    # ----------------------------------------

    parsed_date = extract_datetime(user_input)

    if not parsed_date:
        return "Sorry, I could not understand the date/time."

    # ----------------------------------------
    # CREATE SLOT
    # ----------------------------------------

    start_time = parsed_date

    end_time = start_time + datetime.timedelta(minutes=30)

    # ----------------------------------------
    # CHECK CALENDAR
    # ----------------------------------------

    available = calendar_tool.check_availability(
        start_time,
        end_time
    )

    # ----------------------------------------
    # RESPONSE
    # ----------------------------------------

    formatted_time = start_time.strftime(
        "%d %B %Y at %I:%M %p"
    )

    if available:

        return (
            f"Doctor is available on {formatted_time}"
        )

    return (
        f"Doctor is NOT available on {formatted_time}"
    )