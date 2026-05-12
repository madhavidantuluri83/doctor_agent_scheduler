from utils.datetime_parser import (
    extract_datetime,
    has_explicit_time
)

from tools.google_calendar_tool import calendar_tool


def book_appointment(user_input):

    print(f"\n[Booking Input]: {user_input}")

    # -------------------------------------
    # CHECK TIME
    # -------------------------------------

    if not has_explicit_time(user_input):

        return {
            "needs_followup": True,
            "response": (
                "What time would you like "
                "to book the appointment?"
            )
        }

    # -------------------------------------
    # PARSE DATETIME
    # -------------------------------------

    parsed_date = extract_datetime(user_input)

    if not parsed_date:

        return {
            "needs_followup": False,
            "response": (
                "Sorry, I could not "
                "understand the appointment time."
            )
        }

    # -------------------------------------
    # APPOINTMENT WINDOW
    # -------------------------------------

    start_time = parsed_date

    from datetime import timedelta

    end_time = start_time + timedelta(minutes=30)

    # -------------------------------------
    # CHECK AVAILABILITY
    # -------------------------------------

    available = calendar_tool.check_availability(
        start_time,
        end_time
    )

    if not available:

        return {
            "needs_followup": False,
            "response": (
                f"Doctor is NOT available on "
                f"{start_time.strftime('%d %B %Y at %I:%M %p')}"
            )
        }

    # -------------------------------------
    # CREATE EVENT
    # -------------------------------------

    calendar_tool.create_event(
        summary="Doctor Appointment",
        start_time=start_time,
        end_time=end_time
    )
    # -------------------------------------
    # SUCCESS
    # -------------------------------------

    return {
        "needs_followup": False,
        "response": (
            f"Appointment booked successfully for "
            f"{start_time.strftime('%d %B %Y at %I:%M %p')}"
        )
    }