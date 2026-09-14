from langgraph.graph import StateGraph, END

from app.graph.state import IROPSState
from app.graph.nodes import generate_recovery_plan


def recovery_node(state: IROPSState):
    """
    Run the complete recovery engine.
    """

    flight_id = state["flight_id"]

    plan = generate_recovery_plan(flight_id)

    return {
        "disruption_type": plan.get("disruption_type"),
        "severity": plan.get("severity"),
        "affected_passengers": plan.get(
            "affected_passengers"
        ),
        "alternative_flights": plan.get(
            "alternative_flights"
        ),
        "solver_status": plan.get(
            "solver_status"
        ),
        "rebooking_results": plan.get(
            "rebooking_results"
        ),
        "feasible_options": plan.get(
            "feasible_options"
        ),
        "recovery_plan": plan,
    }


def build_workflow():
    """
    Build the IROPS recovery workflow.
    """

    workflow = StateGraph(IROPSState)

    workflow.add_node(
        "recovery",
        recovery_node
    )

    workflow.set_entry_point("recovery")

    workflow.add_edge(
        "recovery",
        END
    )

    return workflow.compile()


recovery_workflow = build_workflow()