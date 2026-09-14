import pandas as pd
from pathlib import Path


DATA_DIR = Path("data/demo")


# ============================================================
# 1. FIND AFFECTED PASSENGERS
# ============================================================

def get_affected_passengers(flight_id):
    """
    Return all passengers booked on the disrupted flight.
    """

    passengers = pd.read_csv(
        DATA_DIR / "passengers.csv"
    )

    affected = passengers[
        passengers["flight_id"] == flight_id
    ].copy()

    return affected


# ============================================================
# 2. FIND ALTERNATIVE FLIGHTS
# ============================================================

def find_alternative_flights(flight_id):
    """
    Find later flights operating on the same route
    as the disrupted flight.
    """

    flights = pd.read_csv(
        DATA_DIR / "flights.csv"
    )

    flights["departure"] = pd.to_datetime(
        flights["departure"]
    )

    flights["arrival"] = pd.to_datetime(
        flights["arrival"]
    )

    # Find disrupted flight
    disrupted = flights[
        flights["flight_id"] == flight_id
    ]

    if disrupted.empty:
        return pd.DataFrame()

    disrupted = disrupted.iloc[0]

    origin = disrupted["origin"]
    destination = disrupted["destination"]
    departure = disrupted["departure"]

    # Same origin + same destination
    # + departure after disrupted flight
    alternatives = flights[
        (flights["origin"] == origin)
        & (flights["destination"] == destination)
        & (flights["departure"] > departure)
        & (flights["flight_id"] != flight_id)
        & (flights["status"] == "SCHEDULED")
    ].copy()

    return alternatives


# ============================================================
# 3. CHECK CAPACITY
# ============================================================

def check_capacity(
    alternative_flight,
    passengers_count
):
    """
    Check whether an alternative flight has
    enough available seats for the passengers.
    """

    available_seats = int(
        alternative_flight["available_seats"]
    )

    return available_seats >= passengers_count


# ============================================================
# 4. CHECK CONNECTION
# ============================================================

def check_connection(
    passenger_id,
    alternative_flight_id
):
    """
    Check whether a passenger can take an
    alternative flight without missing
    their connecting flight.
    """

    connections = pd.read_csv(
        DATA_DIR / "connections.csv"
    )

    flights = pd.read_csv(
        DATA_DIR / "flights.csv"
    )

    flights["departure"] = pd.to_datetime(
        flights["departure"]
    )

    flights["arrival"] = pd.to_datetime(
        flights["arrival"]
    )

    # Find passenger connection
    passenger_connection = connections[
        connections["passenger_id"] == passenger_id
    ]

    # No connection
    if passenger_connection.empty:
        return {
            "valid": True,
            "reason": "No connecting flight"
        }

    connection = passenger_connection.iloc[0]

    # Find passenger's next flight
    next_flight = flights[
        flights["flight_id"]
        == connection["second_flight_id"]
    ]

    if next_flight.empty:
        return {
            "valid": False,
            "reason": "Connecting flight not found"
        }

    next_flight = next_flight.iloc[0]

    # Find proposed alternative
    alternative = flights[
        flights["flight_id"]
        == alternative_flight_id
    ]

    if alternative.empty:
        return {
            "valid": False,
            "reason": "Alternative flight not found"
        }

    alternative = alternative.iloc[0]

    # Alternative must arrive at
    # the connecting airport
    if (
        alternative["destination"]
        != connection["connection_airport"]
    ):
        return {
            "valid": False,
            "reason": "Wrong connection airport"
        }

    # Calculate time available
    connection_minutes = (
        next_flight["departure"]
        - alternative["arrival"]
    ).total_seconds() / 60

    connection_minutes = int(
        connection_minutes
    )

    # Connecting flight already departed
    if connection_minutes < 0:
        return {
            "valid": False,
            "reason": "Connecting flight already departed",
            "connection_minutes": connection_minutes
        }

    # Minimum connection requirement
    MIN_CONNECTION_TIME = 60

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
# ============================================================
# 5. FIND FEASIBLE REBOOKING
# ============================================================

def find_feasible_rebooking(passenger, alternatives):
    """
    Find the first alternative flight that satisfies
    both capacity and connection constraints.
    """

    passenger_id = passenger["passenger_id"]

    for _, flight in alternatives.iterrows():

        # Check capacity
        if flight["available_seats"] <= 0:
            continue

        # Check connection
        connection_result = check_connection(
            passenger_id,
            flight["flight_id"]
        )

        if not connection_result["valid"]:
            continue

        return {
            "passenger_id": passenger_id,
            "passenger_name": passenger["name"],
            "original_flight": passenger["flight_id"],
            "new_flight": flight["flight_id"],
            "status": "REBOOKED",
            "reason": connection_result["reason"]
        }

    return {
        "passenger_id": passenger_id,
        "passenger_name": passenger["name"],
        "original_flight": passenger["flight_id"],
        "new_flight": None,
        "status": "NO_FEASIBLE_FLIGHT",
        "reason": "No alternative satisfies constraints"
    }

def find_good_test_flight():

    connections = pd.read_csv(
        DATA_DIR / "connections.csv"
    )

    flights = pd.read_csv(
        DATA_DIR / "flights.csv"
    )

    flights["departure"] = pd.to_datetime(
        flights["departure"]
    )

    flights["arrival"] = pd.to_datetime(
        flights["arrival"]
    )

    # Count connecting passengers per first flight
    connection_counts = (
        connections
        .groupby("first_flight_id")
        .size()
        .sort_values(ascending=False)
    )

    for flight_id in connection_counts.index:

        first_flight = flights[
            flights["flight_id"] == flight_id
        ].iloc[0]

        # Find this flight's connections
        flight_connections = connections[
            connections["first_flight_id"] == flight_id
        ]

        for _, connection in flight_connections.iterrows():

            next_flight = flights[
                flights["flight_id"]
                == connection["second_flight_id"]
            ].iloc[0]

            # Find alternate flights
            alternatives = flights[
                (flights["origin"]
                 == first_flight["origin"]) &
                (flights["destination"]
                 == first_flight["destination"]) &
                (flights["departure"]
                 > first_flight["departure"]) &
                (flights["status"] == "SCHEDULED")
            ]

            for _, alternative in alternatives.iterrows():

                # How much time would remain
                # for the connection?
                minutes = (
                    next_flight["departure"]
                    - alternative["arrival"]
                ).total_seconds() / 60

                # We found a useful scenario:
                # at least one alternative works
                # and at least one doesn't.
                if minutes >= 60:

                    return flight_id

    # Fallback
    return connection_counts.index[0]

# ============================================================
# 5. MAIN TEST
# ============================================================

if __name__ == "__main__":

    # We intentionally selected FL0037
    # because it has 7 connecting passengers.
    flight_id = find_good_test_flight()

    print("=" * 60)
    print("IROPS RECOVERY ENGINE")
    print("=" * 60)

    # --------------------------------------------------------
    # Affected passengers
    # --------------------------------------------------------

    affected = get_affected_passengers(
        flight_id
    )

    print(
        f"\nDisrupted flight: {flight_id}"
    )

    print(
        f"Affected passengers: {len(affected)}"
    )

    print(
        affected[
            [
                "passenger_id",
                "name",
                "origin",
                "destination",
                "passenger_type",
                "cabin",
                "fare_class",
                "special_assistance"
            ]
        ].to_string(index=False)
    )

    # --------------------------------------------------------
    # Alternative flights
    # --------------------------------------------------------

    alternatives = find_alternative_flights(
        flight_id
    )

    print(
        f"\nAlternative flights found: "
        f"{len(alternatives)}"
    )

    if alternatives.empty:

        print("No alternative flights found.")

        exit()

    print(
        alternatives[
            [
                "flight_id",
                "origin",
                "destination",
                "departure",
                "arrival",
                "available_seats"
            ]
        ].to_string(index=False)
    )

    # --------------------------------------------------------
    # Capacity check
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CAPACITY CHECK")
    print("=" * 60)

    for _, flight in alternatives.iterrows():

        feasible = check_capacity(
            flight,
            len(affected)
        )

        print(
            f"{flight['flight_id']} | "
            f"Available seats: "
            f"{flight['available_seats']} | "
            f"Passengers: {len(affected)} | "
            f"{'✓ FEASIBLE' if feasible else '✗ NOT ENOUGH SEATS'}"
        )

    # --------------------------------------------------------
    # Connection check
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CONNECTION CHECK")
    print("=" * 60)

    for _, passenger in affected.iterrows():

        print(
            f"\n{passenger['passenger_id']} "
            f"({passenger['name']})"
        )

        for _, flight in alternatives.iterrows():

            result = check_connection(
                passenger["passenger_id"],
                flight["flight_id"]
            )

            if result["valid"]:

                print(
                    f"  → {flight['flight_id']} | "
                    f"✓ {result['reason']}"
                )

            else:

                print(
                    f"  → {flight['flight_id']} | "
                    f"✗ {result['reason']}"
                )
        # --------------------------------------------------------
    # Rebooking decisions
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("REBOOKING DECISIONS")
    print("=" * 60)

    rebooking_results = []

    for _, passenger in affected.iterrows():

        result = find_feasible_rebooking(
            passenger,
            alternatives
        )

        rebooking_results.append(result)

        if result["status"] == "REBOOKED":
            print(
                f"{result['passenger_id']} "
                f"({result['passenger_name']}) "
                f"→ {result['new_flight']} "
                f"| ✓ REBOOKED"
            )
        else:
            print(
                f"{result['passenger_id']} "
                f"({result['passenger_name']}) "
                f"→ NO FLIGHT "
                f"| ✗ NO FEASIBLE OPTION"
            )
        
    print("\n" + "=" * 60)
    print("END OF TEST")
    print("=" * 60)