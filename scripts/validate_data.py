import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")


def load_data():
    """Load all generated CSV files."""

    airports = pd.read_csv(DATA_DIR / "airports.csv")
    aircraft = pd.read_csv(DATA_DIR / "aircraft.csv")
    flights = pd.read_csv(DATA_DIR / "flights.csv")
    passengers = pd.read_csv(DATA_DIR / "passengers.csv")
    connections = pd.read_csv(DATA_DIR / "connections.csv")
    crew = pd.read_csv(DATA_DIR / "crew.csv")
    disruptions = pd.read_csv(DATA_DIR / "disruptions.csv")

    return (
        airports,
        aircraft,
        flights,
        passengers,
        connections,
        crew,
        disruptions
    )


def validate_airports(airports):
    """Validate airport data."""

    print("\nChecking airports...")

    # Airport codes should be unique
    if airports["iata_code"].duplicated().any():
        print("❌ Duplicate airport codes found")
        return False

    print("✓ Airport codes are unique")

    return True


def validate_aircraft(aircraft, airports):
    """Validate aircraft data."""

    print("\nChecking aircraft...")

    valid_airports = set(airports["iata_code"])

    invalid_airports = set(
        aircraft["current_airport"]
    ) - valid_airports

    if invalid_airports:
        print(
            f"❌ Aircraft contain invalid airports: "
            f"{invalid_airports}"
        )
        return False

    print("✓ All aircraft airports are valid")

    if aircraft["aircraft_id"].duplicated().any():
        print("❌ Duplicate aircraft IDs found")
        return False

    print("✓ Aircraft IDs are unique")

    return True


def validate_flights(flights, aircraft, airports):
    """Validate flight data."""

    print("\nChecking flights...")

    valid_airports = set(airports["iata_code"])
    valid_aircraft = set(aircraft["aircraft_id"])

    # Check origins
    invalid_origins = set(
        flights["origin"]
    ) - valid_airports

    if invalid_origins:
        print(
            f"❌ Invalid flight origins: "
            f"{invalid_origins}"
        )
        return False

    print("✓ All flight origins are valid")

    # Check destinations
    invalid_destinations = set(
        flights["destination"]
    ) - valid_airports

    if invalid_destinations:
        print(
            f"❌ Invalid flight destinations: "
            f"{invalid_destinations}"
        )
        return False

    print("✓ All flight destinations are valid")

    # Check aircraft
    invalid_aircraft = set(
        flights["aircraft_id"]
    ) - valid_aircraft

    if invalid_aircraft:
        print(
            f"❌ Invalid aircraft references: "
            f"{invalid_aircraft}"
        )
        return False

    print("✓ All flights reference valid aircraft")

    # Origin cannot equal destination
    if (flights["origin"] == flights["destination"]).any():
        print("❌ Some flights have the same origin and destination")
        return False

    print("✓ No flight has identical origin/destination")

    # Check times
    flights["departure"] = pd.to_datetime(
        flights["departure"]
    )

    flights["arrival"] = pd.to_datetime(
        flights["arrival"]
    )

    if (flights["arrival"] <= flights["departure"]).any():
        print("❌ Some flights arrive before they depart")
        return False

    print("✓ Flight times are valid")

    return True


def validate_passengers(passengers, flights):
    """Validate passenger data."""

    print("\nChecking passengers...")

    valid_flights = set(
        flights["flight_id"]
    )

    invalid_flights = set(
        passengers["flight_id"]
    ) - valid_flights

    if invalid_flights:
        print(
            f"❌ Passengers reference invalid flights: "
            f"{invalid_flights}"
        )
        return False

    print("✓ All passengers reference valid flights")

    if passengers["passenger_id"].duplicated().any():
        print("❌ Duplicate passenger IDs found")
        return False

    print("✓ Passenger IDs are unique")

    return True


def validate_connections(
    connections,
    passengers,
    flights
):
    """Validate passenger connections."""

    print("\nChecking connections...")

    valid_passengers = set(
        passengers["passenger_id"]
    )

    valid_flights = set(
        flights["flight_id"]
    )

    # Check passenger references
    invalid_passengers = set(
        connections["passenger_id"]
    ) - valid_passengers

    if invalid_passengers:
        print(
            f"❌ Invalid passenger references: "
            f"{invalid_passengers}"
        )
        return False

    print("✓ All connection passengers are valid")

    # Check first flights
    invalid_first = set(
        connections["first_flight_id"]
    ) - valid_flights

    if invalid_first:
        print(
            f"❌ Invalid first flight references: "
            f"{invalid_first}"
        )
        return False

    print("✓ All first flights are valid")

    # Check second flights
    invalid_second = set(
        connections["second_flight_id"]
    ) - valid_flights

    if invalid_second:
        print(
            f"❌ Invalid second flight references: "
            f"{invalid_second}"
        )
        return False

    print("✓ All second flights are valid")

    # Load flight information
    flight_lookup = flights.set_index("flight_id")

    for _, connection in connections.iterrows():

        first = flight_lookup.loc[
            connection["first_flight_id"]
        ]

        second = flight_lookup.loc[
            connection["second_flight_id"]
        ]

        # Destination of first flight must equal
        # origin of second flight
        if first["destination"] != second["origin"]:

            print(
                "❌ Invalid connection airport: "
                f"{connection['connection_id']}"
            )

            return False

        # Second flight must depart after first arrives
        if second["departure"] <= first["arrival"]:

            print(
                "❌ Second flight departs before "
                f"first flight arrives: "
                f"{connection['connection_id']}"
            )

            return False

        # Minimum connection time
        connection_minutes = (
            second["departure"] - first["arrival"]
        ).total_seconds() / 60

        if connection_minutes < 60:

            print(
                "❌ Connection time below 60 minutes: "
                f"{connection['connection_id']}"
            )

            return False

    print("✓ All connections are valid")

    return True


def validate_crew(crew, airports):
    """Validate crew data."""

    print("\nChecking crew...")

    valid_airports = set(
        airports["iata_code"]
    )

    invalid_base = set(
        crew["base_airport"]
    ) - valid_airports

    invalid_current = set(
        crew["current_airport"]
    ) - valid_airports

    if invalid_base:
        print(
            f"❌ Invalid crew base airports: "
            f"{invalid_base}"
        )
        return False

    if invalid_current:
        print(
            f"❌ Invalid crew current airports: "
            f"{invalid_current}"
        )
        return False

    print("✓ Crew airports are valid")

    if crew["crew_id"].duplicated().any():
        print("❌ Duplicate crew IDs found")
        return False

    print("✓ Crew IDs are unique")

    return True


def validate_disruptions(disruptions, flights):
    """Validate disruption data."""

    print("\nChecking disruptions...")

    valid_flights = set(
        flights["flight_id"]
    )

    invalid_flights = set(
        disruptions["flight_id"]
    ) - valid_flights

    if invalid_flights:
        print(
            f"❌ Disruptions reference invalid flights: "
            f"{invalid_flights}"
        )
        return False

    print("✓ All disruptions reference valid flights")

    if disruptions["disruption_id"].duplicated().any():
        print("❌ Duplicate disruption IDs found")
        return False

    print("✓ Disruption IDs are unique")

    return True


def main():

    print("=" * 50)
    print("IROPS DATA VALIDATION")
    print("=" * 50)

    try:
        (
            airports,
            aircraft,
            flights,
            passengers,
            connections,
            crew,
            disruptions
        ) = load_data()

    except FileNotFoundError as e:

        print(f"\n❌ Missing data file: {e}")
        print("Run generate_data.py first.")
        return

    results = []

    results.append(
        validate_airports(airports)
    )

    results.append(
        validate_aircraft(
            aircraft,
            airports
        )
    )

    results.append(
        validate_flights(
            flights,
            aircraft,
            airports
        )
    )

    results.append(
        validate_passengers(
            passengers,
            flights
        )
    )

    results.append(
        validate_connections(
            connections,
            passengers,
            flights
        )
    )

    results.append(
        validate_crew(
            crew,
            airports
        )
    )

    results.append(
        validate_disruptions(
            disruptions,
            flights
        )
    )

    print("\n" + "=" * 50)

    if all(results):

        print("✅ DATA VALIDATION PASSED")
        print("=" * 50)

    else:

        print("❌ DATA VALIDATION FAILED")
        print("=" * 50)


if __name__ == "__main__":
    main()