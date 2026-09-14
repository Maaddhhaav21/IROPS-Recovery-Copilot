import pandas as pd
from ortools.sat.python import cp_model

from .constraints import build_feasible_options
from .objective import build_objective


def optimize_rebooking(affected, alternatives):
    """
    Optimize passenger rebooking using OR-Tools CP-SAT.

    Returns:
        results, feasible_options, solver_status
    """

    model = cp_model.CpModel()

    feasible_options = build_feasible_options(
        affected,
        alternatives
    )

    decision_vars = {}

    # Create one binary variable for every feasible
    # passenger -> alternative flight assignment.
    for _, passenger in affected.iterrows():
        passenger_id = passenger["passenger_id"]

        for flight_id in feasible_options[passenger_id]:
            decision_vars[(passenger_id, flight_id)] = (
                model.NewBoolVar(
                    f"x_{passenger_id}_{flight_id}"
                )
            )

    # Each passenger can be assigned to at most one flight.
    for _, passenger in affected.iterrows():
        passenger_id = passenger["passenger_id"]

        variables = [
            decision_vars[(passenger_id, flight_id)]
            for flight_id in feasible_options[passenger_id]
            if (passenger_id, flight_id) in decision_vars
        ]

        if variables:
            model.Add(sum(variables) <= 1)

    # Flight capacity constraints.
    for _, flight in alternatives.iterrows():
        flight_id = flight["flight_id"]

        variables = [
            decision_vars[(passenger_id, flight_id)]
            for passenger_id in feasible_options
            if (passenger_id, flight_id) in decision_vars
        ]

        if variables:
            model.Add(
                sum(variables)
                <= int(flight["available_seats"])
            )

    # Objective is kept in a separate module.
    objective_terms = build_objective(
        alternatives,
        decision_vars
    )

    if objective_terms:
        model.Maximize(sum(objective_terms))

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1

    status = solver.Solve(model)

    if status not in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    ):
        return [], feasible_options, "NO_SOLUTION"

    # Extract solution.
    results = []

    for _, passenger in affected.iterrows():
        passenger_id = passenger["passenger_id"]
        assigned_flight = None

        for flight_id in feasible_options[passenger_id]:
            variable = decision_vars[
                (passenger_id, flight_id)
            ]

            if solver.Value(variable) == 1:
                assigned_flight = flight_id
                break

        if assigned_flight is None:
            results.append({
                "passenger_id": passenger_id,
                "passenger_name": passenger["name"],
                "original_flight": passenger["flight_id"],
                "new_flight": None,
                "status": "NO_FEASIBLE_FLIGHT",
                "reason": (
                    "No feasible assignment in "
                    "optimized solution"
                )
            })
        else:
            results.append({
                "passenger_id": passenger_id,
                "passenger_name": passenger["name"],
                "original_flight": passenger["flight_id"],
                "new_flight": assigned_flight,
                "status": "REBOOKED",
                "reason": "OR-Tools optimized assignment"
            })

    return (
        results,
        feasible_options,
        solver.StatusName(status)
    )
