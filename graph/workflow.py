from langgraph.graph import StateGraph, END

from graph.state import AppointmentState

from agents.intent_agent import detect_intent
from agents.availability_agent import availability_agent
from agents.booking_agent import booking_agent

workflow = StateGraph(AppointmentState)

workflow.add_node("intent", detect_intent)

workflow.add_node("availability", availability_agent)

workflow.add_node("booking", booking_agent)

def router(state):

    intent = state["intent"]

    if intent == "check_availability":
        return "availability"

    if intent == "create_appointment":
        return "booking"

    return END

workflow.set_entry_point("intent")

workflow.add_conditional_edges(
    "intent",
    router
)

workflow.add_edge("availability", END)

workflow.add_edge("booking", END)

graph = workflow.compile()