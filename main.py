from agents.intent_agent import detect_intent
from agents.booking_agent import book_appointment
from agents.availability_agent import check_doctor_availability


def chatbot():

    print("\nDoctor AI Scheduler Started\n")

    while True:

        user_input = input("You: ")

        # -------------------------------------
        # EXIT
        # -------------------------------------

        if user_input.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        # -------------------------------------
        # DETECT INTENT
        # -------------------------------------

        intent = detect_intent(user_input)

        # -------------------------------------
        # ROUTE TO AGENT
        # -------------------------------------

        if intent == "booking":

            result = book_appointment(user_input)

        elif intent == "availability":

            result = check_doctor_availability(user_input)

        else:

            result = (
                "Sorry, I could not understand your request."
            )

        # -------------------------------------
        # RESPONSE
        # -------------------------------------

        print(f"\nBot: {result}\n")


if __name__ == "__main__":

    chatbot()