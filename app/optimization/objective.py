import pandas as pd


def build_objective(alternatives, decision_vars):
    """
    Build the OR-Tools objective.

    Priority:
    1. Rebook as many passengers as possible.
    2. Prefer earlier arrival.
    3. Slightly prefer flights with more available seats.
    """

    flight_lookup = (
        alternatives
        .set_index("flight_id")
        .to_dict("index")
    )

    objective_terms = []

    for (passenger_id, flight_id), variable in (
        decision_vars.items()
    ):
        flight = flight_lookup[flight_id]

        arrival = pd.to_datetime(
            flight["arrival"]
        )

        arrival_minutes = int(
            (
                arrival
                - pd.Timestamp("2026-10-01")
            ).total_seconds() / 60
        )

        available_seats = int(
            flight["available_seats"]
        )

        rebooking_reward = 1_000_000
        delay_cost = arrival_minutes * 100

        seat_cost = max(
            0,
            500 - available_seats
        )

        coefficient = (
            rebooking_reward
            - delay_cost
            - seat_cost
        )

        objective_terms.append(
            coefficient * variable
        )

    return objective_terms
