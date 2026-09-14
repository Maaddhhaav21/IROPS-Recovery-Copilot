import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")


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

def passenger_priority(passenger):
    """
    Higher priority passengers are processed first.

    Priority:
    1. Connecting + special assistance
    2. Connecting
    3. Special assistance
    4. First
    5. Business
    6. Economy

    Lower returned value = higher priority.
    """

    score = 0

    if passenger["passenger_type"] == "CONNECTING":
        score += 100

    if passenger["special_assistance"]:
        score += 50

    if passenger["cabin"] == "First":
        score += 30
    elif passenger["cabin"] == "Business":
        score += 20

    return -score


# ============================================================
# 5. OR-TOOLS OPTIMIZATION
# ============================================================

from ortools.sat.python import cp_model


def build_feasible_options(affected, alternatives):
    """
    Build all passenger -> flight assignments that satisfy
    the hard operational constraints.

    A pair is feasible only if:
    1. The alternative flight has a seat.
    2. The passenger can make their connection.
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


def optimize_rebooking(affected, alternatives):
    """
    Find the best overall rebooking plan using OR-Tools CP-SAT.

    Hard constraints:
    - Every passenger is assigned to at most one flight.
    - A passenger can only use a feasible flight.
    - A flight cannot receive more passengers than its available seats.

    Objective:
    - Rebook as many passengers as possible.
    - Minimize passenger arrival delay.
    - Preserve scarce seats by applying a small penalty to flights
      with fewer available seats.
    """

    model = cp_model.CpModel()

    feasible_options = build_feasible_options(
        affected,
        alternatives
    )

    # --------------------------------------------------------
    # Create decision variables
    # --------------------------------------------------------
    #
    # x[p, f] = 1 means passenger p is assigned to flight f.
    #
    # x[p, f] = 0 means they are not assigned to that flight.
    # --------------------------------------------------------

    decision_vars = {}

    for _, passenger in affected.iterrows():
        passenger_id = passenger["passenger_id"]

        for flight_id in feasible_options[passenger_id]:
            decision_vars[
                (passenger_id, flight_id)
            ] = model.NewBoolVar(
                f"x_{passenger_id}_{flight_id}"
            )

    # --------------------------------------------------------
    # Constraint 1:
    # Each passenger can receive at most one flight.
    # --------------------------------------------------------

    for _, passenger in affected.iterrows():
        passenger_id = passenger["passenger_id"]

        variables = [
            decision_vars[(passenger_id, flight_id)]
            for flight_id in feasible_options[passenger_id]
        ]

        if variables:
            model.Add(sum(variables) <= 1)

    # --------------------------------------------------------
    # Constraint 2:
    # Flight capacity cannot be exceeded.
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Objective
    # --------------------------------------------------------
    #
    # We use a weighted objective:
    #
    # 1. Strongly reward every successful rebooking.
    # 2. Among solutions with the same number of rebookings,
    #    prefer earlier passenger arrival.
    # 3. Slightly prefer flights with more available seats.
    #
    # The rebooking reward is deliberately much larger than
    # the delay cost, so leaving a passenger unresolved is
    # always worse than accepting a reasonable delay.
    # --------------------------------------------------------

    flight_lookup = (
        alternatives
        .set_index("flight_id")
        .to_dict("index")
    )

    objective_terms = []

    for (passenger_id, flight_id), variable in decision_vars.items():

        flight = flight_lookup[flight_id]

        arrival = pd.to_datetime(
            flight["arrival"]
        )

        # Minutes from the disruption date.
        arrival_minutes = int(
            (
                arrival - pd.Timestamp("2026-10-01")
            ).total_seconds() / 60
        )

        available_seats = int(
            flight["available_seats"]
        )

        # Main reward for rebooking.
        rebooking_reward = 1_000_000

        # Earlier arrival is better.
        delay_cost = arrival_minutes * 100

        # Small tie-breaker to avoid consuming scarce capacity
        # when another equally good flight exists.
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

    if objective_terms:
        model.Maximize(
            sum(objective_terms)
        )

    # --------------------------------------------------------
    # Solve
    # --------------------------------------------------------

    solver = cp_model.CpSolver()

    # Keep the result deterministic and easy to reproduce.
    solver.parameters.num_search_workers = 1

    status = solver.Solve(model)

    if status not in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    ):
        return [], feasible_options, "NO_SOLUTION"

    # --------------------------------------------------------
    # Extract solution
    # --------------------------------------------------------

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
                "reason": "No feasible assignment in optimized solution"
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

    return results, feasible_options, solver.StatusName(status)


# ============================================================
# 6. FIND GOOD TEST FLIGHT
# ============================================================

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

        flight_connections = connections[
            connections["first_flight_id"] == flight_id
        ]

        for _, connection in flight_connections.iterrows():

            next_flight = flights[
                flights["flight_id"]
                == connection["second_flight_id"]
            ].iloc[0]

            alternatives = flights[
                (flights["origin"] == first_flight["origin"])
                & (flights["destination"] == first_flight["destination"])
                & (flights["departure"] > first_flight["departure"])
                & (flights["status"] == "SCHEDULED")
            ]

            for _, alternative in alternatives.iterrows():

                minutes = (
                    next_flight["departure"]
                    - alternative["arrival"]
                ).total_seconds() / 60

                if minutes >= 60:
                    return flight_id

    return connection_counts.index[0]


# ============================================================
# 7. MAIN TEST
# ============================================================

if __name__ == "__main__":

    # Automatically select a useful test disruption
    # containing at least one valid and one invalid connection.
    flight_id = find_good_test_flight()

    print("=" * 60)
    print("IROPS RECOVERY ENGINE - OR-TOOLS")
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
        raise SystemExit

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
    # OR-Tools optimized rebooking
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("OR-TOOLS OPTIMIZED REBOOKING")
    print("=" * 60)

    rebooking_results, feasible_options, solver_status = (
        optimize_rebooking(
            affected,
            alternatives
        )
    )

    print(
        f"Solver status: {solver_status}"
    )

    # Track seats after the optimized assignment.
    remaining_seats = {
        flight["flight_id"]: int(
            flight["available_seats"]
        )
        for _, flight in alternatives.iterrows()
    }

    for result in rebooking_results:

        if result["status"] == "REBOOKED":

            remaining_seats[
                result["new_flight"]
            ] -= 1

            print(
                f'{result["passenger_id"]} '
                f'({result["passenger_name"]}) '
                f'→ {result["new_flight"]} '
                f'| ✓ REBOOKED'
            )

        else:

            print(
                f'{result["passenger_id"]} '
                f'({result["passenger_name"]}) '
                f'→ NO FLIGHT '
                f'| ✗ NO FEASIBLE OPTION'
            )

    # --------------------------------------------------------
    # Recovery summary
    # --------------------------------------------------------

    successful_rebookings = sum(
        result["status"] == "REBOOKED"
        for result in rebooking_results
    )

    unresolved_passengers = (
        len(rebooking_results)
        - successful_rebookings
    )

    print("\n" + "=" * 60)
    print("RECOVERY SUMMARY")
    print("=" * 60)

    print(
        f"Total affected passengers : "
        f"{len(affected)}"
    )

    print(
        f"Successfully rebooked     : "
        f"{successful_rebookings}"
    )

    print(
        f"Unresolved passengers     : "
        f"{unresolved_passengers}"
    )

    if unresolved_passengers == 0:
        print(
            "Status                    : "
            "✓ ALL PASSENGERS REBOOKED"
        )
    else:
        print(
            "Status                    : "
            "✗ SOME PASSENGERS UNRESOLVED"
        )

    # --------------------------------------------------------
    # Remaining seats
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("REMAINING SEATS")
    print("=" * 60)

    for flight_id, seats in remaining_seats.items():

        print(
            f"{flight_id} | "
            f"Remaining seats: {seats}"
        )

    print("\n" + "=" * 60)
    print("END OF TEST")
    print("=" * 60)
