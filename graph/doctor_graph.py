from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.intent_agent import detect_intent
from agents.booking_agent import book_appointment
from agents.availability_agent import check_doctor_availability


# -------------------------------------------------
# SHARED STATE
# -------------------------------------------------

class DoctorState(TypedDict):

    user_input: str
    intent: str
    response: str

    pending_action: str
    partial_datetime: str


# -------------------------------------------------
# INTENT NODE
# -------------------------------------------------

def intent_node(state):

    user_input = state["user_input"]

    intent = detect_intent(user_input)

    print(f"\n[Intent Detected]: {intent}")

    return {
        "intent": intent
    }


# -------------------------------------------------
# BOOKING NODE
# -------------------------------------------------

def booking_node(state):

    user_input = state["user_input"]

    result = book_appointment(user_input)

    print("\n[Booking Agent Executed]")

    # -------------------------------------
    # FOLLOW-UP REQUIRED
    # -------------------------------------

    if result.get("needs_followup"):

        return {

            "response": result["response"],

            "pending_action": "booking",

            # Preserve ORIGINAL incomplete request
            "partial_datetime":
                state.get("partial_datetime")
                or user_input
        }

    # -------------------------------------
    # SUCCESS
    # -------------------------------------

    return {

        "response": result["response"],

        # CLEAR STATE
        "pending_action": "",

        "partial_datetime": ""
    }

# -------------------------------------------------
# AVAILABILITY NODE
# -------------------------------------------------

def availability_node(state):

    user_input = state["user_input"]

    response = check_doctor_availability(user_input)

    print("\n[Availability Agent Executed]")

    return {
        "response": response
    }


# -------------------------------------------------
# ROUTER
# -------------------------------------------------

def route_intent(state):

    intent = state["intent"]

    if intent == "booking":

        return "booking"

    elif intent == "availability":

        return "availability"

    return END


# -------------------------------------------------
# BUILD GRAPH
# -------------------------------------------------

graph_builder = StateGraph(DoctorState)

# Nodes
graph_builder.add_node(
    "intent_node",
    intent_node
)

graph_builder.add_node(
    "booking_node",
    booking_node
)

graph_builder.add_node(
    "availability_node",
    availability_node
)

# Entry
graph_builder.set_entry_point(
    "intent_node"
)

# Conditional Routing
graph_builder.add_conditional_edges(
    "intent_node",
    route_intent,
    {
        "booking": "booking_node",
        "availability": "availability_node",
    }
)

# End Connections
graph_builder.add_edge(
    "booking_node",
    END
)

graph_builder.add_edge(
    "availability_node",
    END
)

# Compile Graph
doctor_graph = graph_builder.compile()