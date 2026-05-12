import re
import dateparser

from datetime import datetime, timedelta


WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def get_next_weekday(target_day):

    today = datetime.now()

    today_weekday = today.weekday()

    days_ahead = target_day - today_weekday

    if days_ahead <= 0:
        days_ahead += 7

    return today + timedelta(days=days_ahead)


def extract_datetime(text):

    # ---------------------------------------
    # LOWERCASE
    # ---------------------------------------

    text = text.lower()

    # ---------------------------------------
    # REMOVE INTENT WORDS
    # ---------------------------------------

    words_to_remove = [
        "schedule",
        "book",
        "appointment",
        "doctor",
        "visit",
        "meeting",
        "consultation",
        "is",
        "available",
        "free",
        "check",
    ]

    for word in words_to_remove:
        text = text.replace(word, "")

    # ---------------------------------------
    # CLEAN SPACES
    # ---------------------------------------

    text = re.sub(r"\s+", " ", text).strip()

    # ---------------------------------------
    # EXTRACT TIME
    # ---------------------------------------

    time_match = re.search(
        r'(\d{1,2})(:\d{2})?\s*(am|pm)',
        text
    )

    extracted_time = None

    if time_match:

        extracted_time = time_match.group(0)

        text = text.replace(extracted_time, "").strip()

    # ---------------------------------------
    # HANDLE WEEKDAYS
    # ---------------------------------------

    parsed_date = None

    for weekday_name, weekday_num in WEEKDAYS.items():

        if weekday_name in text:

            parsed_date = get_next_weekday(weekday_num)

            break

    # ---------------------------------------
    # FALLBACK DATE PARSER
    # ---------------------------------------

    if not parsed_date:

        parsed_date = dateparser.parse(
            text,
            settings={
                "PREFER_DATES_FROM": "future"
            }
        )

    if not parsed_date:
        return None

    # ---------------------------------------
    # APPLY TIME
    # ---------------------------------------

    if extracted_time:

        parsed_time = dateparser.parse(extracted_time)

        parsed_date = parsed_date.replace(
            hour=parsed_time.hour,
            minute=parsed_time.minute,
            second=0,
            microsecond=0
        )

    return parsed_date