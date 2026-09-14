import pandas as pd
from pathlib import Path
import random
from datetime import datetime, timedelta
from faker import Faker

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

fake = Faker()

random.seed(42)
Faker.seed(42)

AIRPORTS = [
    {
        "iata_code": "DXB",
        "name": "Dubai International Airport",
        "city": "Dubai",
        "country": "UAE",
    },
    {
        "iata_code": "LHR",
        "name": "London Heathrow Airport",
        "city": "London",
        "country": "UK",
    },
    {
        "iata_code": "JFK",
        "name": "John F. Kennedy International Airport",
        "city": "New York",
        "country": "USA",
    },
    {
        "iata_code": "BOM",
        "name": "Chhatrapati Shivaji Maharaj International Airport",
        "city": "Mumbai",
        "country": "India",
    },
    {
        "iata_code": "DEL",
        "name": "Indira Gandhi International Airport",
        "city": "Delhi",
        "country": "India",
    },
    {
        "iata_code": "SIN",
        "name": "Singapore Changi Airport",
        "city": "Singapore",
        "country": "Singapore",
    },
    {
        "iata_code": "DOH",
        "name": "Hamad International Airport",
        "city": "Doha",
        "country": "Qatar",
    },
    {
        "iata_code": "FRA",
        "name": "Frankfurt Airport",
        "city": "Frankfurt",
        "country": "Germany",
    },
    {
        "iata_code": "CDG",
        "name": "Charles de Gaulle Airport",
        "city": "Paris",
        "country": "France",
    },
    {
        "iata_code": "AMS",
        "name": "Amsterdam Schiphol Airport",
        "city": "Amsterdam",
        "country": "Netherlands",
    },
    {
        "iata_code": "IST",
        "name": "Istanbul Airport",
        "city": "Istanbul",
        "country": "Turkey",
    },
    {
        "iata_code": "HKG",
        "name": "Hong Kong International Airport",
        "city": "Hong Kong",
        "country": "Hong Kong",
    },
    {
        "iata_code": "SYD",
        "name": "Sydney Kingsford Smith Airport",
        "city": "Sydney",
        "country": "Australia",
    },
    {
        "iata_code": "MEL",
        "name": "Melbourne Airport",
        "city": "Melbourne",
        "country": "Australia",
    },
    {
        "iata_code": "BKK",
        "name": "Suvarnabhumi Airport",
        "city": "Bangkok",
        "country": "Thailand",
    },
    {
        "iata_code": "NRT",
        "name": "Narita International Airport",
        "city": "Tokyo",
        "country": "Japan",
    },
    {
        "iata_code": "ICN",
        "name": "Incheon International Airport",
        "city": "Seoul",
        "country": "South Korea",
    },
    {
        "iata_code": "ORD",
        "name": "Chicago O'Hare International Airport",
        "city": "Chicago",
        "country": "USA",
    },
    {
        "iata_code": "LAX",
        "name": "Los Angeles International Airport",
        "city": "Los Angeles",
        "country": "USA",
    },
    {
        "iata_code": "SFO",
        "name": "San Francisco International Airport",
        "city": "San Francisco",
        "country": "USA",
    },
]

AIRCRAFT_TYPES = {
    "A380": 484,
    "B777": 396,
    "A350": 325,
    "B787": 300,
    "A320": 180,
    "A321": 220,
}

ROUTES = [
    ("DXB", "LHR"),
    ("DXB", "JFK"),
    ("DXB", "BOM"),
    ("DXB", "DEL"),
    ("DXB", "SIN"),
    ("DXB", "DOH"),
    ("DXB", "FRA"),
    ("DXB", "CDG"),

    ("LHR", "JFK"),
    ("LHR", "FRA"),
    ("LHR", "CDG"),
    ("LHR", "AMS"),
    ("LHR", "BOM"),

    ("DOH", "LHR"),
    ("DOH", "JFK"),
    ("DOH", "SIN"),

    ("SIN", "SYD"),
    ("SIN", "MEL"),
    ("SIN", "BKK"),

    ("FRA", "JFK"),
    ("FRA", "SIN"),

    ("CDG", "JFK"),
    ("CDG", "DXB"),

    ("NRT", "LAX"),
    ("NRT", "SIN"),

    ("LAX", "JFK"),
    ("LAX", "SFO"),

    ("JFK", "SFO"),
    ("ORD", "LAX"),
]
FLIGHT_DURATIONS = {
    ("DXB", "LHR"): 8,
    ("DXB", "JFK"): 14,
    ("DXB", "BOM"): 3,
    ("DXB", "DEL"): 3,
    ("DXB", "SIN"): 7,
    ("DXB", "DOH"): 1,
    ("DXB", "FRA"): 7,
    ("DXB", "CDG"): 7,

    ("LHR", "JFK"): 8,
    ("LHR", "FRA"): 2,
    ("LHR", "CDG"): 2,
    ("LHR", "AMS"): 2,
    ("LHR", "BOM"): 9,

    ("DOH", "LHR"): 7,
    ("DOH", "JFK"): 14,
    ("DOH", "SIN"): 8,

    ("SIN", "SYD"): 8,
    ("SIN", "MEL"): 8,
    ("SIN", "BKK"): 2,

    ("FRA", "JFK"): 9,
    ("FRA", "SIN"): 12,

    ("CDG", "JFK"): 9,
    ("CDG", "DXB"): 7,

    ("NRT", "LAX"): 10,
    ("NRT", "SIN"): 7,

    ("LAX", "JFK"): 6,
    ("LAX", "SFO"): 1,

    ("JFK", "SFO"): 6,
    ("ORD", "LAX"): 4,
}


def generate_airports():
    df = pd.DataFrame(AIRPORTS)
    df.to_csv(DATA_DIR / "airports.csv", index=False)

    print(f"Generated {len(df)} airports")

def generate_aircraft(count=30):
    aircraft = []
    airport_codes = [airport["iata_code"] for airport in AIRPORTS]

    for i in range(1, count + 1):
        aircraft_type = random.choice(list(AIRCRAFT_TYPES.keys()))
        aircraft.append({
            "aircraft_id": f"AC{i:03d}",
            "aircraft_type": aircraft_type,
            "capacity": AIRCRAFT_TYPES[aircraft_type],
            "current_airport": random.choice(airport_codes),
            "status": random.choice([
                "AVAILABLE",
                "AVAILABLE",
                "AVAILABLE",
                "MAINTENANCE"
            ])
        })

    df = pd.DataFrame(aircraft)

    df.to_csv(
        DATA_DIR / "aircraft.csv",
        index=False
    )

    print(f"Generated {len(df)} aircraft")

def generate_flights(count=200):

    aircraft_df = pd.read_csv(DATA_DIR / "aircraft.csv")

    flights = []

    start_date = datetime(2026, 10, 1)

    # ============================================================
    # GUARANTEED IROPS TEST SCENARIO
    # ============================================================

    scenario_flights = [
        {
            "flight_id": "FL0001",
            "origin": "NRT",
            "destination": "SIN",
            "departure": datetime(2026, 10, 1, 10, 0),
            "duration": 7,
            "status": "SCHEDULED"
        },
        {
            "flight_id": "FL0002",
            "origin": "NRT",
            "destination": "SIN",
            "departure": datetime(2026, 10, 1, 11, 0),
            "duration": 7,
            "status": "SCHEDULED"
        },
        {
            "flight_id": "FL0003",
            "origin": "NRT",
            "destination": "SIN",
            "departure": datetime(2026, 10, 1, 12, 30),
            "duration": 7,
            "status": "SCHEDULED"
        },
        {
            "flight_id": "FL0004",
            "origin": "NRT",
            "destination": "SIN",
            "departure": datetime(2026, 10, 1, 18, 0),
            "duration": 7,
            "status": "SCHEDULED"
        },
        {
            "flight_id": "FL0005",
            "origin": "SIN",
            "destination": "BKK",
            "departure": datetime(2026, 10, 1, 20, 30),
            "duration": 2,
            "status": "SCHEDULED"
        }
    ]

    for flight in scenario_flights:

        aircraft = aircraft_df.sample(1).iloc[0]

        capacity = int(aircraft["capacity"])

        # Give alternatives enough seats, but keep some constraints
        if flight["flight_id"] == "FL0002":
            occupied_seats = capacity - 8

        elif flight["flight_id"] == "FL0003":
            occupied_seats = capacity - 5

        elif flight["flight_id"] == "FL0004":
            occupied_seats = capacity - 2

        else:
            occupied_seats = random.randint(
                int(capacity * 0.50),
                int(capacity * 0.80)
            )

        available_seats = capacity - occupied_seats

        arrival = flight["departure"] + timedelta(
            hours=flight["duration"]
        )

        flights.append({
            "flight_id": flight["flight_id"],
            "origin": flight["origin"],
            "destination": flight["destination"],
            "departure": flight["departure"],
            "arrival": arrival,
            "aircraft_id": aircraft["aircraft_id"],
            "capacity": capacity,
            "occupied_seats": occupied_seats,
            "available_seats": available_seats,
            "status": flight["status"]
        })

    # ============================================================
    # RANDOM FLIGHTS
    # ============================================================

    for i in range(6, count + 1):

        origin, destination = random.choice(ROUTES)

        duration = FLIGHT_DURATIONS[(origin, destination)]

        flight_day = random.randint(0, 6)

        departure_hour = random.choice([
            6, 7, 8, 9,
            10, 11, 12,
            13, 14, 15,
            16, 17, 18,
            19, 20, 21
        ])

        departure_minute = random.choice([
            0, 15, 30, 45
        ])

        departure = start_date + timedelta(
            days=flight_day,
            hours=departure_hour,
            minutes=departure_minute
        )

        arrival = departure + timedelta(hours=duration)

        aircraft = aircraft_df.sample(1).iloc[0]

        capacity = int(aircraft["capacity"])

        occupied_seats = random.randint(
            int(capacity * 0.50),
            int(capacity * 0.90)
        )

        available_seats = capacity - occupied_seats

        flights.append({
            "flight_id": f"FL{i:04d}",
            "origin": origin,
            "destination": destination,
            "departure": departure,
            "arrival": arrival,
            "aircraft_id": aircraft["aircraft_id"],
            "capacity": capacity,
            "occupied_seats": occupied_seats,
            "available_seats": available_seats,
            "status": "SCHEDULED"
        })

    df = pd.DataFrame(flights)

    df.to_csv(
        DATA_DIR / "flights.csv",
        index=False
    )

    print(f"Generated {len(df)} flights")
    
def generate_passengers(count=2000):

    flights_df = pd.read_csv(
        DATA_DIR / "flights.csv"
    )

    flights_df["departure"] = pd.to_datetime(
        flights_df["departure"]
    )

    flights_df["arrival"] = pd.to_datetime(
        flights_df["arrival"]
    )

    passengers = []

    # ============================================================
    # GUARANTEED IROPS SCENARIO
    # ============================================================

    disrupted_flight = flights_df[
        flights_df["flight_id"] == "FL0001"
    ].iloc[0]

    # First 10 passengers are connecting
    for i in range(1, 11):

        cabin = random.choices(
            ["Economy", "Business", "First"],
            weights=[80, 17, 3]
        )[0]

        if cabin == "Economy":
            fare_class = random.choice(["Y", "M", "B"])
        elif cabin == "Business":
            fare_class = random.choice(["J", "C"])
        else:
            fare_class = "F"

        passengers.append({
            "passenger_id": f"P{i:05d}",
            "name": fake.name(),
            "flight_id": "FL0001",
            "origin": "NRT",
            "destination": "BKK",
            "passenger_type": "CONNECTING",
            "cabin": cabin,
            "fare_class": fare_class,
            "special_assistance": random.random() < 0.05
        })

    # Next 5 passengers are direct
    for i in range(11, 16):

        cabin = random.choices(
            ["Economy", "Business", "First"],
            weights=[80, 17, 3]
        )[0]

        if cabin == "Economy":
            fare_class = random.choice(["Y", "M", "B"])
        elif cabin == "Business":
            fare_class = random.choice(["J", "C"])
        else:
            fare_class = "F"

        passengers.append({
            "passenger_id": f"P{i:05d}",
            "name": fake.name(),
            "flight_id": "FL0001",
            "origin": "NRT",
            "destination": "SIN",
            "passenger_type": "DIRECT",
            "cabin": cabin,
            "fare_class": fare_class,
            "special_assistance": random.random() < 0.05
        })

    # ============================================================
    # REMAINING RANDOM PASSENGERS
    # ============================================================

    for i in range(16, count + 1):

        flight = flights_df.sample(1).iloc[0]

        passenger_type = random.choices(
            ["DIRECT", "CONNECTING"],
            weights=[70, 30]
        )[0]

        cabin = random.choices(
            ["Economy", "Business", "First"],
            weights=[80, 17, 3]
        )[0]

        if cabin == "Economy":
            fare_class = random.choice(["Y", "M", "B"])

        elif cabin == "Business":
            fare_class = random.choice(["J", "C"])

        else:
            fare_class = "F"

        passengers.append({
            "passenger_id": f"P{i:05d}",
            "name": fake.name(),
            "flight_id": flight["flight_id"],
            "origin": flight["origin"],
            "destination": flight["destination"],
            "passenger_type": passenger_type,
            "cabin": cabin,
            "fare_class": fare_class,
            "special_assistance": random.random() < 0.05
        })

    df = pd.DataFrame(passengers)

    df.to_csv(
        DATA_DIR / "passengers.csv",
        index=False
    )

    print(
        f"Generated {len(df)} passengers"
    )

def generate_connections():

    flights_df = pd.read_csv(
        DATA_DIR / "flights.csv"
    )

    passengers_df = pd.read_csv(
        DATA_DIR / "passengers.csv"
    )

    flights_df["departure"] = pd.to_datetime(
        flights_df["departure"]
    )

    flights_df["arrival"] = pd.to_datetime(
        flights_df["arrival"]
    )

    connections = []

    connection_id = 1

    # ============================================================
    # GUARANTEED CONNECTIONS FOR IROPS SCENARIO
    # ============================================================

    guaranteed_passengers = passengers_df[
        (passengers_df["flight_id"] == "FL0001") &
        (passengers_df["passenger_type"] == "CONNECTING")
    ]

    first_flight = flights_df[
        flights_df["flight_id"] == "FL0001"
    ].iloc[0]

    second_flight = flights_df[
        flights_df["flight_id"] == "FL0005"
    ].iloc[0]

    connection_minutes = int(
        (second_flight["departure"] - first_flight["arrival"])
        .total_seconds() / 60
    )

    for _, passenger in guaranteed_passengers.iterrows():

        connections.append({
            "connection_id": f"C{connection_id:05d}",
            "passenger_id": passenger["passenger_id"],
            "first_flight_id": "FL0001",
            "second_flight_id": "FL0005",
            "connection_airport": "SIN",
            "arrival_time": first_flight["arrival"],
            "next_departure_time": second_flight["departure"],
            "connection_minutes": connection_minutes
        })

        connection_id += 1

    # ============================================================
    # RANDOM CONNECTIONS FOR OTHER PASSENGERS
    # ============================================================

    connecting_passengers = passengers_df[
        (passengers_df["passenger_type"] == "CONNECTING") &
        (passengers_df["flight_id"] != "FL0001")
    ]

    for _, passenger in connecting_passengers.iterrows():

        first_flight = flights_df[
            flights_df["flight_id"] == passenger["flight_id"]
        ].iloc[0]

        possible_connections = flights_df[
            (flights_df["origin"] == first_flight["destination"]) &
            (flights_df["departure"] > first_flight["arrival"])
        ].copy()

        if possible_connections.empty:
            continue

        possible_connections["connection_minutes"] = (
            possible_connections["departure"]
            - first_flight["arrival"]
        ).dt.total_seconds() / 60

        possible_connections = possible_connections[
            (possible_connections["connection_minutes"] >= 90) &
            (possible_connections["connection_minutes"] <= 240)
        ]

        if possible_connections.empty:
            continue

        second_flight = possible_connections.sample(1).iloc[0]

        connection_minutes = int(
            second_flight["connection_minutes"]
        )

        connections.append({
            "connection_id": f"C{connection_id:05d}",
            "passenger_id": passenger["passenger_id"],
            "first_flight_id": first_flight["flight_id"],
            "second_flight_id": second_flight["flight_id"],
            "connection_airport": first_flight["destination"],
            "arrival_time": first_flight["arrival"],
            "next_departure_time": second_flight["departure"],
            "connection_minutes": connection_minutes
        })

        connection_id += 1

        passenger_index = passengers_df.index[
            passengers_df["passenger_id"] == passenger["passenger_id"]
        ][0]

        passengers_df.loc[
            passenger_index,
            "destination"
        ] = second_flight["destination"]

    # ============================================================
    # SAVE CONNECTIONS
    # ============================================================

    connections_df = pd.DataFrame(connections)

    connections_df.to_csv(
        DATA_DIR / "connections.csv",
        index=False
    )

    passengers_df.to_csv(
        DATA_DIR / "passengers.csv",
        index=False
    )

    print(
        f"Generated {len(connections_df)} connections"
    )
def generate_crew(count=100):
    crew = []
    airport_codes = [
        airport["iata_code"]
        for airport in AIRPORTS
    ]

    aircraft_types = list(AIRCRAFT_TYPES.keys())

    roles = [
        "CAPTAIN",
        "FIRST_OFFICER",
        "CABIN_CREW"
    ]

    for i in range(1, count + 1):

        role = random.choices(
            roles,
            weights=[15, 20, 65]
        )[0]

        aircraft_type = random.choice(
            aircraft_types
        )

        base_airport = random.choice(
            airport_codes
        )

        current_airport = random.choice(
            airport_codes
        )

        duty_hours = round(
            random.uniform(0, 10),
            1
        )

        rest_hours = round(
            random.uniform(8, 16),
            1
        )

        status = random.choices(
            ["AVAILABLE", "ON_DUTY", "RESTING"],
            weights=[60, 25, 15]
        )[0]

        crew.append({
            "crew_id": f"C{i:05d}",
            "name": fake.name(),
            "role": role,
            "aircraft_type": aircraft_type,
            "base_airport": base_airport,
            "current_airport": current_airport,
            "duty_hours": duty_hours,
            "rest_hours": rest_hours,
            "status": status
        })

    df = pd.DataFrame(crew)

    df.to_csv(
        DATA_DIR / "crew.csv",
        index=False
    )

    print(f"Generated {len(df)} crew members")

def generate_crew(count=100):

    crew = []

    airport_codes = [
        airport["iata_code"]
        for airport in AIRPORTS
    ]

    aircraft_types = list(AIRCRAFT_TYPES.keys())

    roles = [
        "CAPTAIN",
        "FIRST_OFFICER",
        "CABIN_CREW"
    ]

    for i in range(1, count + 1):

        role = random.choices(
            roles,
            weights=[15, 20, 65]
        )[0]

        aircraft_type = random.choice(
            aircraft_types
        )

        base_airport = random.choice(
            airport_codes
        )

        current_airport = random.choice(
            airport_codes
        )

        duty_hours = round(
            random.uniform(0, 10),
            1
        )

        rest_hours = round(
            random.uniform(8, 16),
            1
        )

        status = random.choices(
            ["AVAILABLE", "ON_DUTY", "RESTING"],
            weights=[60, 25, 15]
        )[0]

        crew.append({
            "crew_id": f"C{i:05d}",
            "name": fake.name(),
            "role": role,
            "aircraft_type": aircraft_type,
            "base_airport": base_airport,
            "current_airport": current_airport,
            "duty_hours": duty_hours,
            "rest_hours": rest_hours,
            "status": status
        })

    df = pd.DataFrame(crew)

    df.to_csv(
        DATA_DIR / "crew.csv",
        index=False
    )

    print(f"Generated {len(df)} crew members")

def generate_disruptions(count=20):
    flights_df = pd.read_csv(DATA_DIR / "flights.csv")

    disruption_types = [
        "AIRCRAFT_FAILURE",
        "WEATHER",
        "CREW_UNAVAILABLE",
        "ATC_RESTRICTION",
        "AIRPORT_CLOSURE"
    ]

    disruptions = []

    # ============================================================
    # GUARANTEED IROPS TEST SCENARIO
    # ============================================================
    # FL0001 is the flight used by the recovery engine.
    # Always create a disruption for it so every component
    # of the project works with the same test scenario.
    # ============================================================

    disrupted_flight = flights_df[
        flights_df["flight_id"] == "FL0001"
    ].iloc[0]

    disruptions.append({
        "disruption_id": "D00001",
        "flight_id": "FL0001",
        "type": "WEATHER",
        "severity": "HIGH",
        "status": "CANCELLED",
        "description": "Severe weather causing cancellation of flight FL0001"
    })

    # ============================================================
    # RANDOM ADDITIONAL DISRUPTIONS
    # ============================================================

    for i in range(2, count + 1):

        # Avoid creating another disruption for FL0001.
        available_flights = flights_df[
            flights_df["flight_id"] != "FL0001"
        ]

        flight = available_flights.sample(1).iloc[0]

        disruption_type = random.choice(disruption_types)

        if disruption_type in [
            "AIRCRAFT_FAILURE",
            "CREW_UNAVAILABLE",
            "AIRPORT_CLOSURE"
        ]:
            severity = "HIGH"
            status = "CANCELLED"

        elif disruption_type == "WEATHER":
            severity = random.choice(["MEDIUM", "HIGH"])
            status = random.choice(["DELAYED", "CANCELLED"])

        else:
            severity = "MEDIUM"
            status = "DELAYED"

        disruptions.append({
            "disruption_id": f"D{i:05d}",
            "flight_id": flight["flight_id"],
            "type": disruption_type,
            "severity": severity,
            "status": status,
            "description": (
                f"{disruption_type.replace('_', ' ').title()} "
                f"affecting flight {flight['flight_id']}"
            )
        })

    df = pd.DataFrame(disruptions)

    df.to_csv(
        DATA_DIR / "disruptions.csv",
        index=False
    )

    print(f"Generated {len(df)} disruptions")


if __name__ == "__main__":
    generate_airports()
    generate_aircraft()
    generate_flights()
    generate_passengers()
    generate_connections()
    generate_crew()
    generate_disruptions()