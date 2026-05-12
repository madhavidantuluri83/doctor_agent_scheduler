from graph.doctor_graph import doctor_graph


# -------------------------------------------------
# CONVERSATION MEMORY
# -------------------------------------------------

conversation_state = {

    "pending_action": "",
    "partial_datetime": ""
}


# -------------------------------------------------
# CHATBOT
# -------------------------------------------------

def chatbot():

    print("\nDoctor AI Scheduler Started\n")

    while True:

        user_input = input("You: ")

        # -----------------------------------------
        # EXIT
        # -----------------------------------------

        if user_input.lower() in ["exit", "quit"]:

            print("\nGoodbye!")
            break

        # -----------------------------------------
        # FOLLOW-UP HANDLING
        # -----------------------------------------

        if conversation_state["pending_action"] == "booking":

            print("\n[Using Previous Context]\n")

            original_request = conversation_state[
                "partial_datetime"
            ]

            # Merge ONLY temporarily
            merged_input = (
                f"{original_request} {user_input}"
            )

            print(f"[Merged Input]: {merged_input}")

            user_input = merged_input

        # -----------------------------------------
        # GRAPH INVOCATION
        # -----------------------------------------

        result = doctor_graph.invoke({

            "user_input": user_input,

            "pending_action":
                conversation_state["pending_action"],

            "partial_datetime":
                conversation_state["partial_datetime"]
        })

        # -----------------------------------------
        # STORE / CLEAR MEMORY
        # -----------------------------------------

        conversation_state["pending_action"] = result.get(
            "pending_action",
            ""
        )

        conversation_state["partial_datetime"] = result.get(
            "partial_datetime",
            ""
        )

        # -----------------------------------------
        # RESPONSE
        # -----------------------------------------

        print(f"\nBot: {result['response']}\n")


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------

if __name__ == "__main__":

    chatbot()