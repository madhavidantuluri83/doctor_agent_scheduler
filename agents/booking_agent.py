from tools.google_calendar_tool import GoogleCalendarTool
from utils.datetime_parser import extract_datetime

import re
import datetime


calendar_tool = GoogleCalendarTool()


def book_appointment(user_input):

    # -----------------------------------------
    # EXTRACT DATE/TIME
    # -----------------------------------------

    parsed_date = extract_datetime(user_input)

    if not parsed_date:
        return "Sorry, I could not understand the appointment time."

    # -----------------------------------------
    # APPOINTMENT SLOT
    # -----------------------------------------

    start_time = parsed_date

    end_time = start_time + datetime.timedelta(minutes=30)

    # -----------------------------------------
    # CHECK AVAILABILITY
    # -----------------------------------------

    available = calendar_tool.check_availability(
        start_time,
        end_time
    )

    if not available:

        return (
            f"Doctor is NOT available on "
            f"{start_time.strftime('%d %B %Y at %I:%M %p')}"
        )

    # -----------------------------------------
    # CREATE EVENT
    # -----------------------------------------

    event = calendar_tool.create_event(
        summary="Doctor Appointment",
        start_time=start_time,
        end_time=end_time
    )

    # -----------------------------------------
    # RESPONSE
    # -----------------------------------------

    return (
        f"Appointment booked successfully for "
        f"{start_time.strftime('%d %B %Y at %I:%M %p')}"
    )