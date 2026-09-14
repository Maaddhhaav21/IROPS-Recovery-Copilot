import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")
MIN_CONNECTION_TIME = 60


def load_flights():
    """Load flights and parse time columns."""
    flights = pd.read_csv(DATA_DIR / "flights.csv")

    flights["departure"] = pd.to_datetime(
        flights["departure"]
    )
    flights["arrival"] = pd.to_datetime(
        flights["arrival"]
    )

    return flights


def get_affected_passengers(flight_id):
    """Return passengers booked on the disrupted flight."""
    passengers = pd.read_csv(
        DATA_DIR / "passengers.csv"
    )

    return passengers[
        passengers["flight_id"] == flight_id
    ].copy()


def find_alternative_flights(flight_id):
    """
    Find later scheduled flights on the same route.
    """

    flights = load_flights()

    disrupted = flights[
        flights["flight_id"] == flight_id
    ]

    if disrupted.empty:
        return pd.DataFrame()

    disrupted = disrupted.iloc[0]

    alternatives = flights[
        (flights["origin"] == disrupted["origin"])
        & (
            flights["destination"]
            == disrupted["destination"]
        )
        & (
            flights["departure"]
            > disrupted["departure"]
        )
        & (flights["flight_id"] != flight_id)
        & (flights["status"] == "SCHEDULED")
    ].copy()

    return alternatives


def check_capacity(alternative_flight, passengers_count):
    """Check whether a flight has enough available seats."""
    return (
        int(alternative_flight["available_seats"])
        >= passengers_count
    )


def check_connection(passenger_id, alternative_flight_id):
    """
    Check whether a passenger can take an alternative
    flight without missing their onward connection.
    """

    connections = pd.read_csv(
        DATA_DIR / "connections.csv"
    )
    flights = load_flights()

    passenger_connection = connections[
        connections["passenger_id"] == passenger_id
    ]

    if passenger_connection.empty:
        return {
            "valid": True,
            "reason": "No connecting flight"
        }

    connection = passenger_connection.iloc[0]

    next_flight = flights[
        flights["flight_id"]
        == connection["second_flight_id"]
    ]

    if next_flight.empty:
        return {
            "valid": False,
            "reason": "Connecting flight not found"
        }

    alternative = flights[
        flights["flight_id"]
        == alternative_flight_id
    ]

    if alternative.empty:
        return {
            "valid": False,
            "reason": "Alternative flight not found"
        }

    next_flight = next_flight.iloc[0]
    alternative = alternative.iloc[0]

    if (
        alternative["destination"]
        != connection["connection_airport"]
    ):
        return {
            "valid": False,
            "reason": "Wrong connection airport"
        }

    connection_minutes = int(
        (
            next_flight["departure"]
            - alternative["arrival"]
        ).total_seconds() / 60
    )

    if connection_minutes < 0:
        return {
            "valid": False,
            "reason": "Connecting flight already departed",
            "connection_minutes": connection_minutes
        }

    if connection_minutes < MIN_CONNECTION_TIME:
        return {
            "valid": False,
            "reason": (
                f"Only {connection_minutes} "
                "minutes available"
            ),
            "connection_minutes": connection_minutes
        }

    return {
        "valid": True,
        "reason": "Connection time is sufficient",
        "connection_minutes": connection_minutes
    }


def build_feasible_options(affected, alternatives):
    """
    Build feasible passenger -> flight assignments.

    A pair is feasible only when:
    - the alternative flight has a seat
    - the passenger can make their connection
    """

    feasible_options = {}

    for _, passenger in affected.iterrows():
        passenger_id = passenger["passenger_id"]
        feasible_options[passenger_id] = []

        for _, flight in alternatives.iterrows():
            flight_id = flight["flight_id"]

            if int(flight["available_seats"]) <= 0:
                continue

            connection_result = check_connection(
                passenger_id,
                flight_id
            )

            if connection_result["valid"]:
                feasible_options[passenger_id].append(
                    flight_id
                )

    return feasible_options
