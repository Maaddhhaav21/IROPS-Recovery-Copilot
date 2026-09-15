from langgraph.graph import StateGraph, END

from app.graph.state import IROPSState

from app.agents.disruption_agent import DisruptionAgent
from app.agents.passenger_agent import PassengerAgent
from app.agents.rebooking_agent import RebookingAgent
from app.agents.crew_agent import CrewAgent
from app.agents.briefing_agent import BriefingAgent


def disruption_node(state: IROPSState):

    flight_id = state["flight_id"]

    agent = DisruptionAgent()
    result = agent.analyze(flight_id)

    return {
        "flight_id": result["flight_id"],
        "disruption_type": result.get("disruption_type"),
        "severity": result.get("severity"),
        "disruption_status": result.get("disruption_status"),
        "recovery_plan": result,
    }


def passenger_node(state: IROPSState):

    flight_id = state["flight_id"]

    agent = PassengerAgent()
    result = agent.analyze(flight_id)

    return {
        "affected_passengers": result["affected_passengers"],
        "connecting_passengers": result["connecting_passengers"],
    }


def rebooking_node(state: IROPSState):

    flight_id = state["flight_id"]

    affected_passengers = state.get(
        "affected_passengers",
        []
    )

    agent = RebookingAgent()

    result = agent.analyze(
        flight_id,
        affected_passengers
    )

    return {
        "solver_status": result.get("solver_status"),
        "feasible_options": result.get("feasible_options", {}),
        "rebooking_results": result.get("results", []),
        "alternative_flights": result.get("results", []),
        "recovery_plan": result,
    }


def crew_node(state: IROPSState):

    flight_id = state["flight_id"]

    agent = CrewAgent()
    result = agent.analyze(flight_id)

    return {
        "crew_analysis": result,
    }


def briefing_node(state: IROPSState):

    agent = BriefingAgent()
    result = agent.generate(state)

    return {
        "briefing": result["briefing"],
    }


def build_workflow():

    workflow = StateGraph(IROPSState)

    workflow.add_node(
        "disruption_agent",
        disruption_node
    )

    workflow.add_node(
        "passenger_agent",
        passenger_node
    )

    workflow.add_node(
        "rebooking_agent",
        rebooking_node
    )

    workflow.add_node(
        "crew_agent",
        crew_node
    )

    workflow.add_node(
        "briefing_agent",
        briefing_node
    )

    workflow.set_entry_point(
        "disruption_agent"
    )

    workflow.add_edge(
        "disruption_agent",
        "passenger_agent"
    )

    workflow.add_edge(
        "passenger_agent",
        "rebooking_agent"
    )

    workflow.add_edge(
        "rebooking_agent",
        "crew_agent"
    )

    workflow.add_edge(
        "crew_agent",
        "briefing_agent"
    )

    workflow.add_edge(
        "briefing_agent",
        END
    )

    return workflow.compile()


recovery_workflow = build_workflow()