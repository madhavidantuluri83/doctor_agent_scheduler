def detect_intent(user_input):

    user_input = user_input.lower()

    # ---------------------------------------
    # BOOKING INTENT
    # ---------------------------------------

    booking_keywords = [
        "book",
        "schedule",
        "appointment",
        "reserve"
    ]

    for word in booking_keywords:

        if word in user_input:
            return "booking"

    # ---------------------------------------
    # AVAILABILITY INTENT
    # ---------------------------------------

    availability_keywords = [
        "available",
        "free",
        "availability"
    ]

    for word in availability_keywords:

        if word in user_input:
            return "availability"

    return "unknown"