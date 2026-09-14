import pandas as pd

from app.optimization.constraints import (
    get_affected_passengers,
    find_alternative_flights,
)

from app.optimization.model import optimize_rebooking


def analyze_disruption(flight_id):
    """
    Analyze a disrupted flight and prepare recovery inputs.
    """

    disruptions = pd.read_csv("data/disruptions.csv")

    disruption = disruptions[
        disruptions["flight_id"] == flight_id
    ]

    if disruption.empty:
        return {
            "status": "NO_DISRUPTION",
            "flight_id": flight_id,
        }

    disruption = disruption.iloc[0]

    affected = get_affected_passengers(flight_id)

    alternatives = find_alternative_flights(flight_id)

    return {
        "status": "DISRUPTION_FOUND",
        "flight_id": flight_id,
        "disruption_type": disruption["type"],
        "severity": disruption["severity"],
        "affected_passengers": affected,
        "alternative_flights": alternatives,
    }


def generate_recovery_plan(flight_id):
    """
    Generate an optimized passenger recovery plan.
    """

    analysis = analyze_disruption(flight_id)

    if analysis["status"] != "DISRUPTION_FOUND":
        return analysis

    affected = analysis["affected_passengers"]
    alternatives = analysis["alternative_flights"]

    results, feasible_options, solver_status = (
        optimize_rebooking(
            affected,
            alternatives,
        )
    )

    return {
        "status": "RECOVERY_PLAN_GENERATED",
        "flight_id": flight_id,
        "disruption_type": analysis["disruption_type"],
        "severity": analysis["severity"],
        "affected_passengers": len(affected),
        "alternative_flights": len(alternatives),
        "solver_status": solver_status,
        "rebooking_results": results,
        "feasible_options": feasible_options,
    }
