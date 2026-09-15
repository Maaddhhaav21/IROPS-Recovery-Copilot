import pandas as pd

from app.agents.disruption_agent import DisruptionAgent

from app.optimization.constraints import (
    get_affected_passengers,
    find_alternative_flights,
)

from app.optimization.model import optimize_rebooking


def analyze_disruption(flight_id):
    """
    Analyze a disruption using the Disruption Agent.
    """

    agent = DisruptionAgent()

    return agent.analyze(flight_id)


def generate_recovery_plan(flight_id):
    """
    Generate an optimized recovery plan.
    """

    # -----------------------------------------
    # STEP 1: DISRUPTION AGENT
    # -----------------------------------------

    analysis = analyze_disruption(flight_id)

    if analysis["status"] != "DISRUPTION_FOUND":
        return analysis

    # -----------------------------------------
    # STEP 2: GET AFFECTED PASSENGERS
    # -----------------------------------------

    affected = get_affected_passengers(
        flight_id
    )

    # -----------------------------------------
    # STEP 3: FIND ALTERNATIVE FLIGHTS
    # -----------------------------------------

    alternatives = find_alternative_flights(
        flight_id
    )

    # -----------------------------------------
    # STEP 4: OPTIMIZE REBOOKING
    # -----------------------------------------

    (
        results,
        feasible_options,
        solver_status,
    ) = optimize_rebooking(
        affected,
        alternatives,
    )

    # -----------------------------------------
    # STEP 5: RETURN RECOVERY PLAN
    # -----------------------------------------

    return {
        "status": "RECOVERY_PLAN_GENERATED",
        "flight_id": flight_id,
        "disruption_type": analysis[
            "disruption_type"
        ],
        "severity": analysis[
            "severity"
        ],
        "disruption_status": analysis[
            "disruption_status"
        ],
        "affected_passengers": len(
            affected
        ),
        "alternative_flights": len(
            alternatives
        ),
        "solver_status": solver_status,
        "rebooking_results": results,
        "feasible_options": feasible_options,
    }