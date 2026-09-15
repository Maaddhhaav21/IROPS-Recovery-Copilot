import pandas as pd

from app.database.connection import Base, engine, SessionLocal

from app.database.models import (
    Airport,
    AirportCapacity,
    Aircraft,
    Flight,
    FlightRotation,
    Passenger,
    Connection,
    Crew,
    CrewQualification,
    CrewAssignment,
    Maintenance,
    Weather,
    Disruption,
)


DATA_DIR = "data"


def seed_database():

    print()
    print("=" * 60)
    print("SEEDING IROPS DATABASE")
    print("=" * 60)
    print()

    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # AIRPORTS
        # ----------------------------------------------------

        airports = pd.read_csv(
            f"{DATA_DIR}/airports.csv"
        )

        for _, row in airports.iterrows():

            db.add(
                Airport(
                    airport_code=row["iata_code"],
                    name=row["name"],
                    city=row["city"],
                    country=row["country"],
                )
            )

        print(
            f"Loaded {len(airports)} airports"
        )

        # ----------------------------------------------------
        # AIRPORT CAPACITY
        # ----------------------------------------------------

        airport_capacity = pd.read_csv(
            f"{DATA_DIR}/airport_capacity.csv"
        )

        for _, row in airport_capacity.iterrows():

            db.add(
                AirportCapacity(
                    airport_code=row[
                        "airport_code"
                    ],
                    airport_type=row[
                        "airport_type"
                    ],
                    max_daily_movements=int(
                        row[
                            "max_daily_movements"
                        ]
                    ),
                    available_slots=int(
                        row[
                            "available_slots"
                        ]
                    ),
                )
            )

        print(
            f"Loaded {len(airport_capacity)} airport capacity records"
        )

        # ----------------------------------------------------
        # AIRCRAFT
        # ----------------------------------------------------

        aircraft = pd.read_csv(
            f"{DATA_DIR}/aircraft.csv"
        )

        for _, row in aircraft.iterrows():

            db.add(
                Aircraft(
                    aircraft_id=row[
                        "aircraft_id"
                    ],
                    aircraft_type=row[
                        "aircraft_type"
                    ],
                    capacity=int(
                        row["capacity"]
                    ),
                    current_airport=row[
                        "current_airport"
                    ],
                    status=row["status"],
                )
            )

        print(
            f"Loaded {len(aircraft)} aircraft"
        )

        # ----------------------------------------------------
        # FLIGHTS
        # ----------------------------------------------------

        flights = pd.read_csv(
            f"{DATA_DIR}/flights.csv"
        )

        for _, row in flights.iterrows():

            db.add(
                Flight(
                    flight_id=row[
                        "flight_id"
                    ],
                    origin=row["origin"],
                    destination=row[
                        "destination"
                    ],
                    departure=str(
                        row["departure"]
                    ),
                    arrival=str(
                        row["arrival"]
                    ),
                    aircraft_id=row[
                        "aircraft_id"
                    ],
                    capacity=int(
                        row["capacity"]
                    ),
                    occupied_seats=int(
                        row["occupied_seats"]
                    ),
                    available_seats=int(
                        row["available_seats"]
                    ),
                    status=row["status"],
                )
            )

        print(
            f"Loaded {len(flights)} flights"
        )

        # ----------------------------------------------------
        # FLIGHT ROTATIONS
        # ----------------------------------------------------

        rotations = pd.read_csv(
            f"{DATA_DIR}/flight_rotations.csv"
        )

        for _, row in rotations.iterrows():

            db.add(
                FlightRotation(
                    rotation_id=row[
                        "rotation_id"
                    ],
                    aircraft_id=row[
                        "aircraft_id"
                    ],
                    flight_id=row[
                        "flight_id"
                    ],
                    leg_number=int(
                        row["leg_number"]
                    ),
                )
            )

        print(
            f"Loaded {len(rotations)} flight rotations"
        )

        # ----------------------------------------------------
        # PASSENGERS
        # ----------------------------------------------------

        passengers = pd.read_csv(
            f"{DATA_DIR}/passengers.csv"
        )

        for _, row in passengers.iterrows():

            db.add(
                Passenger(
                    passenger_id=row[
                        "passenger_id"
                    ],
                    name=row["name"],
                    flight_id=row[
                        "flight_id"
                    ],
                    origin=row["origin"],
                    destination=row[
                        "destination"
                    ],
                    passenger_type=row[
                        "passenger_type"
                    ],
                    cabin=row["cabin"],
                    fare_class=row[
                        "fare_class"
                    ],
                    special_assistance=str(
                        row[
                            "special_assistance"
                        ]
                    ),
                    priority_level=row[
                        "priority_level"
                    ],
                    status=row["status"],
                )
            )

        print(
            f"Loaded {len(passengers)} passengers"
        )

        # ----------------------------------------------------
        # CONNECTIONS
        # ----------------------------------------------------

        connections = pd.read_csv(
            f"{DATA_DIR}/connections.csv"
        )

        for _, row in connections.iterrows():

            db.add(
                Connection(
                    connection_id=row[
                        "connection_id"
                    ],
                    passenger_id=row[
                        "passenger_id"
                    ],
                    first_flight_id=row[
                        "first_flight_id"
                    ],
                    second_flight_id=row[
                        "second_flight_id"
                    ],
                    connection_airport=row[
                        "connection_airport"
                    ],
                    arrival_time=str(
                        row["arrival_time"]
                    ),
                    next_departure_time=str(
                        row[
                            "next_departure_time"
                        ]
                    ),
                    connection_minutes=int(
                        row[
                            "connection_minutes"
                        ]
                    ),
                )
            )

        print(
            f"Loaded {len(connections)} connections"
        )

        # ----------------------------------------------------
        # CREW
        # ----------------------------------------------------

        crew = pd.read_csv(
            f"{DATA_DIR}/crew.csv"
        )

        for _, row in crew.iterrows():

            db.add(
                Crew(
                    crew_id=row[
                        "crew_id"
                    ],
                    name=row["name"],
                    role=row["role"],
                    aircraft_type=row[
                        "aircraft_type"
                    ],
                    base_airport=row[
                        "base_airport"
                    ],
                    current_airport=row[
                        "current_airport"
                    ],
                    duty_hours=float(
                        row["duty_hours"]
                    ),
                    rest_hours=float(
                        row["rest_hours"]
                    ),
                    status=row["status"],
                )
            )

        print(
            f"Loaded {len(crew)} crew members"
        )

        # ----------------------------------------------------
        # CREW QUALIFICATIONS
        # ----------------------------------------------------

        qualifications = pd.read_csv(
            f"{DATA_DIR}/crew_qualifications.csv"
        )

        for _, row in qualifications.iterrows():

            db.add(
                CrewQualification(
                    crew_id=row[
                        "crew_id"
                    ],
                    aircraft_type=row[
                        "aircraft_type"
                    ],
                    qualification_level=row[
                        "qualification_level"
                    ],
                    valid_until=str(
                        row["valid_until"]
                    ),
                )
            )

        print(
            f"Loaded {len(qualifications)} crew qualifications"
        )

        # ----------------------------------------------------
        # CREW ASSIGNMENTS
        # ----------------------------------------------------

        assignments = pd.read_csv(
            f"{DATA_DIR}/crew_assignments.csv"
        )

        for _, row in assignments.iterrows():

            db.add(
                CrewAssignment(
                    assignment_id=row[
                        "assignment_id"
                    ],
                    crew_id=row[
                        "crew_id"
                    ],
                    flight_id=row[
                        "flight_id"
                    ],
                    role=row["role"],
                    status=row["status"],
                )
            )

        print(
            f"Loaded {len(assignments)} crew assignments"
        )

        # ----------------------------------------------------
        # MAINTENANCE
        # ----------------------------------------------------

        maintenance = pd.read_csv(
            f"{DATA_DIR}/maintenance.csv"
        )

        for _, row in maintenance.iterrows():

            db.add(
                Maintenance(
                    maintenance_id=row[
                        "maintenance_id"
                    ],
                    aircraft_id=row[
                        "aircraft_id"
                    ],
                    maintenance_type=row[
                        "maintenance_type"
                    ],
                    status=row["status"],
                    start_time=str(
                        row["start_time"]
                    ),
                    end_time=str(
                        row["end_time"]
                    ),
                )
            )

        print(
            f"Loaded {len(maintenance)} maintenance records"
        )

        # ----------------------------------------------------
        # WEATHER
        # ----------------------------------------------------

        weather = pd.read_csv(
            f"{DATA_DIR}/weather.csv"
        )

        for _, row in weather.iterrows():

            db.add(
                Weather(
                    weather_id=row[
                        "weather_id"
                    ],
                    airport_code=row[
                        "airport_code"
                    ],
                    date=str(
                        row["date"]
                    ),
                    condition=row[
                        "condition"
                    ],
                    severity=row[
                        "severity"
                    ],
                    visibility_km=float(
                        row[
                            "visibility_km"
                        ]
                    ),
                    wind_speed_kmh=float(
                        row[
                            "wind_speed_kmh"
                        ]
                    ),
                )
            )

        print(
            f"Loaded {len(weather)} weather records"
        )

        # ----------------------------------------------------
        # DISRUPTIONS
        # ----------------------------------------------------

        disruptions = pd.read_csv(
            f"{DATA_DIR}/disruptions.csv"
        )

        for _, row in disruptions.iterrows():

            db.add(
                Disruption(
                    disruption_id=row[
                        "disruption_id"
                    ],
                    flight_id=row[
                        "flight_id"
                    ],
                    type=row["type"],
                    severity=row["severity"],
                    status=row["status"],
                    description=row[
                        "description"
                    ],
                )
            )

        print(
            f"Loaded {len(disruptions)} disruptions"
        )

        # ----------------------------------------------------
        # COMMIT
        # ----------------------------------------------------

        db.commit()

        print()
        print("=" * 60)
        print("DATABASE SEEDING COMPLETE")
        print("=" * 60)
        print()

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


if __name__ == "__main__":
    seed_database()