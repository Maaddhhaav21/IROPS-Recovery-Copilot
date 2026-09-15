import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

random.seed(42)
Faker.seed(42)

fake = Faker()

START_DATE = datetime(2026, 10, 1)

NUM_AIRCRAFT = 120
NUM_FLIGHTS = 3000
NUM_PASSENGERS = 30000
NUM_CREW = 600
NUM_DISRUPTIONS = 150


# ============================================================
# AIRPORTS
# ============================================================

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
    {
        "iata_code": "SEA",
        "name": "Seattle-Tacoma International Airport",
        "city": "Seattle",
        "country": "USA",
    },
    {
        "iata_code": "BOS",
        "name": "Boston Logan International Airport",
        "city": "Boston",
        "country": "USA",
    },
    {
        "iata_code": "ATL",
        "name": "Hartsfield-Jackson Atlanta International Airport",
        "city": "Atlanta",
        "country": "USA",
    },
    {
        "iata_code": "DFW",
        "name": "Dallas Fort Worth International Airport",
        "city": "Dallas",
        "country": "USA",
    },
    {
        "iata_code": "YYZ",
        "name": "Toronto Pearson International Airport",
        "city": "Toronto",
        "country": "Canada",
    },
    {
        "iata_code": "YVR",
        "name": "Vancouver International Airport",
        "city": "Vancouver",
        "country": "Canada",
    },
    {
        "iata_code": "GRU",
        "name": "Sao Paulo Guarulhos International Airport",
        "city": "Sao Paulo",
        "country": "Brazil",
    },
    {
        "iata_code": "MEX",
        "name": "Mexico City International Airport",
        "city": "Mexico City",
        "country": "Mexico",
    },
    {
        "iata_code": "JNB",
        "name": "O.R. Tambo International Airport",
        "city": "Johannesburg",
        "country": "South Africa",
    },
    {
        "iata_code": "CAI",
        "name": "Cairo International Airport",
        "city": "Cairo",
        "country": "Egypt",
    },
    {
        "iata_code": "RUH",
        "name": "King Khalid International Airport",
        "city": "Riyadh",
        "country": "Saudi Arabia",
    },
    {
        "iata_code": "AUH",
        "name": "Zayed International Airport",
        "city": "Abu Dhabi",
        "country": "UAE",
    },
    {
        "iata_code": "KUL",
        "name": "Kuala Lumpur International Airport",
        "city": "Kuala Lumpur",
        "country": "Malaysia",
    },
    {
        "iata_code": "CGK",
        "name": "Soekarno-Hatta International Airport",
        "city": "Jakarta",
        "country": "Indonesia",
    },
    {
        "iata_code": "TPE",
        "name": "Taiwan Taoyuan International Airport",
        "city": "Taipei",
        "country": "Taiwan",
    },
    {
        "iata_code": "PEK",
        "name": "Beijing Capital International Airport",
        "city": "Beijing",
        "country": "China",
    },
    {
        "iata_code": "PVG",
        "name": "Shanghai Pudong International Airport",
        "city": "Shanghai",
        "country": "China",
    },
    {
        "iata_code": "HND",
        "name": "Tokyo Haneda Airport",
        "city": "Tokyo",
        "country": "Japan",
    },
    {
        "iata_code": "AKL",
        "name": "Auckland Airport",
        "city": "Auckland",
        "country": "New Zealand",
    },
    {
        "iata_code": "PER",
        "name": "Perth Airport",
        "city": "Perth",
        "country": "Australia",
    },
]


# ============================================================
# AIRCRAFT
# ============================================================

AIRCRAFT_TYPES = {
    "A380": 484,
    "B777": 396,
    "A350": 325,
    "B787": 300,
    "A320": 180,
    "A321": 220,
}


# ============================================================
# ROUTES
# ============================================================

ROUTES = [
    ("DXB", "LHR"),
    ("DXB", "JFK"),
    ("DXB", "BOM"),
    ("DXB", "DEL"),
    ("DXB", "SIN"),
    ("DXB", "DOH"),
    ("DXB", "FRA"),
    ("DXB", "CDG"),
    ("DXB", "NRT"),
    ("DXB", "ICN"),

    ("LHR", "JFK"),
    ("LHR", "FRA"),
    ("LHR", "CDG"),
    ("LHR", "AMS"),
    ("LHR", "BOM"),
    ("LHR", "NRT"),

    ("DOH", "LHR"),
    ("DOH", "JFK"),
    ("DOH", "SIN"),
    ("DOH", "BOM"),
    ("DOH", "DEL"),

    ("SIN", "SYD"),
    ("SIN", "MEL"),
    ("SIN", "BKK"),
    ("SIN", "KUL"),
    ("SIN", "CGK"),
    ("SIN", "NRT"),

    ("FRA", "JFK"),
    ("FRA", "SIN"),
    ("FRA", "NRT"),

    ("CDG", "JFK"),
    ("CDG", "DXB"),
    ("CDG", "NRT"),

    ("NRT", "LAX"),
    ("NRT", "SIN"),
    ("NRT", "ICN"),
    ("NRT", "HND"),
    ("NRT", "BKK"),

    ("ICN", "NRT"),
    ("ICN", "LAX"),
    ("ICN", "SIN"),

    ("LAX", "JFK"),
    ("LAX", "SFO"),
    ("LAX", "ORD"),

    ("JFK", "SFO"),
    ("JFK", "LHR"),
    ("JFK", "BOS"),

    ("ORD", "LAX"),
    ("ORD", "JFK"),
    ("ORD", "DFW"),

    ("SYD", "MEL"),
    ("SYD", "AKL"),
    ("MEL", "PER"),

    ("BOM", "DEL"),
    ("BOM", "SIN"),
    ("BOM", "DXB"),

    ("DEL", "BOM"),
    ("DEL", "DXB"),
    ("DEL", "SIN"),

    ("HKG", "NRT"),
    ("HKG", "SIN"),
    ("HKG", "SYD"),

    ("AMS", "LHR"),
    ("AMS", "CDG"),
    ("AMS", "FRA"),
]


# ============================================================
# FLIGHT DURATIONS
# ============================================================

FLIGHT_DURATIONS = {
    ("DXB", "LHR"): 8,
    ("DXB", "JFK"): 14,
    ("DXB", "BOM"): 3,
    ("DXB", "DEL"): 3,
    ("DXB", "SIN"): 7,
    ("DXB", "DOH"): 1,
    ("DXB", "FRA"): 7,
    ("DXB", "CDG"): 7,
    ("DXB", "NRT"): 10,
    ("DXB", "ICN"): 9,

    ("LHR", "JFK"): 8,
    ("LHR", "FRA"): 2,
    ("LHR", "CDG"): 2,
    ("LHR", "AMS"): 2,
    ("LHR", "BOM"): 9,
    ("LHR", "NRT"): 11,

    ("DOH", "LHR"): 7,
    ("DOH", "JFK"): 14,
    ("DOH", "SIN"): 8,
    ("DOH", "BOM"): 4,
    ("DOH", "DEL"): 4,

    ("SIN", "SYD"): 8,
    ("SIN", "MEL"): 8,
    ("SIN", "BKK"): 2,
    ("SIN", "KUL"): 1,
    ("SIN", "CGK"): 2,
    ("SIN", "NRT"): 7,

    ("FRA", "JFK"): 9,
    ("FRA", "SIN"): 12,
    ("FRA", "NRT"): 11,

    ("CDG", "JFK"): 9,
    ("CDG", "DXB"): 7,
    ("CDG", "NRT"): 12,

    ("NRT", "LAX"): 10,
    ("NRT", "SIN"): 7,
    ("NRT", "ICN"): 3,
    ("NRT", "HND"): 1,
    ("NRT", "BKK"): 7,

    ("ICN", "NRT"): 3,
    ("ICN", "LAX"): 11,
    ("ICN", "SIN"): 7,

    ("LAX", "JFK"): 6,
    ("LAX", "SFO"): 1,
    ("LAX", "ORD"): 4,

    ("JFK", "SFO"): 6,
    ("JFK", "LHR"): 8,
    ("JFK", "BOS"): 1,

    ("ORD", "LAX"): 4,
    ("ORD", "JFK"): 2,
    ("ORD", "DFW"): 2,

    ("SYD", "MEL"): 2,
    ("SYD", "AKL"): 3,
    ("MEL", "PER"): 4,

    ("BOM", "DEL"): 2,
    ("BOM", "SIN"): 6,
    ("BOM", "DXB"): 3,

    ("DEL", "BOM"): 2,
    ("DEL", "DXB"): 3,
    ("DEL", "SIN"): 6,

    ("HKG", "NRT"): 4,
    ("HKG", "SIN"): 4,
    ("HKG", "SYD"): 9,

    ("AMS", "LHR"): 2,
    ("AMS", "CDG"): 2,
    ("AMS", "FRA"): 2,
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_cabin():
    return random.choices(
        ["Economy", "Business", "First"],
        weights=[80, 17, 3],
    )[0]


def random_fare_class(cabin):
    if cabin == "Economy":
        return random.choice(["Y", "M", "B"])
    if cabin == "Business":
        return random.choice(["J", "C"])
    return "F"


def random_departure():
    day = random.randint(0, 6)
    hour = random.choice(
        [
            5, 6, 7, 8, 9, 10, 11,
            12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23,
        ]
    )
    minute = random.choice([0, 15, 30, 45])

    return START_DATE + timedelta(
        days=day,
        hours=hour,
        minutes=minute,
    )


def generate_seat_data(capacity, forced_available=None):
    if forced_available is not None:
        available = min(forced_available, capacity - 1)
        occupied = capacity - available
        return occupied, available

    load_factor = random.uniform(0.50, 0.92)

    occupied = int(capacity * load_factor)
    available = capacity - occupied

    return occupied, available


# ============================================================
# AIRPORT GENERATION
# ============================================================

def generate_airports():
    df = pd.DataFrame(AIRPORTS)

    df.to_csv(
        DATA_DIR / "airports.csv",
        index=False,
    )

    print(f"Generated {len(df)} airports")


# ============================================================
# AIRPORT CAPACITY
# ============================================================

def generate_airport_capacity():
    rows = []

    airport_types = [
        "HUB",
        "MAJOR",
        "REGIONAL",
    ]

    for airport in AIRPORTS:
        code = airport["iata_code"]

        if code in [
            "DXB",
            "LHR",
            "JFK",
            "SIN",
            "NRT",
            "FRA",
            "CDG",
            "DOH",
            "HKG",
            "ICN",
        ]:
            airport_type = "HUB"
            max_movements = random.randint(80, 140)
        elif code in [
            "BOM",
            "DEL",
            "LAX",
            "ORD",
            "SYD",
            "MEL",
            "AMS",
        ]:
            airport_type = "MAJOR"
            max_movements = random.randint(50, 90)
        else:
            airport_type = "REGIONAL"
            max_movements = random.randint(25, 60)

        rows.append(
            {
                "airport_code": code,
                "airport_type": airport_type,
                "max_daily_movements": max_movements,
                "available_slots": random.randint(
                    int(max_movements * 0.55),
                    int(max_movements * 0.90),
                ),
            }
        )

    df = pd.DataFrame(rows)

    df.to_csv(
        DATA_DIR / "airport_capacity.csv",
        index=False,
    )

    print(f"Generated {len(df)} airport capacity records")


# ============================================================
# AIRCRAFT GENERATION
# ============================================================

def generate_aircraft(count=NUM_AIRCRAFT):
    aircraft = []

    airport_codes = [
        airport["iata_code"]
        for airport in AIRPORTS
    ]

    for i in range(1, count + 1):

        aircraft_type = random.choice(
            list(AIRCRAFT_TYPES.keys())
        )

        status = random.choices(
            [
                "AVAILABLE",
                "AVAILABLE",
                "AVAILABLE",
                "MAINTENANCE",
            ],
            weights=[35, 35, 20, 10],
        )[0]

        aircraft.append(
            {
                "aircraft_id": f"AC{i:03d}",
                "aircraft_type": aircraft_type,
                "capacity": AIRCRAFT_TYPES[aircraft_type],
                "current_airport": random.choice(
                    airport_codes
                ),
                "status": status,
            }
        )

    df = pd.DataFrame(aircraft)

    df.to_csv(
        DATA_DIR / "aircraft.csv",
        index=False,
    )

    print(f"Generated {len(df)} aircraft")

    return df


# ============================================================
# FLIGHT GENERATION
# ============================================================

def generate_flights(count=NUM_FLIGHTS):
    aircraft_df = pd.read_csv(
        DATA_DIR / "aircraft.csv"
    )

    flights = []

    # --------------------------------------------------------
    # GUARANTEED IROPS SCENARIO
    # --------------------------------------------------------

    scenario_flights = [
        {
            "flight_id": "FL0001",
            "origin": "NRT",
            "destination": "SIN",
            "departure": datetime(
                2026, 10, 1, 10, 0
            ),
            "duration": 7,
            "status": "SCHEDULED",
            "available_seats": 0,
        },
        {
            "flight_id": "FL0002",
            "origin": "NRT",
            "destination": "SIN",
            "departure": datetime(
                2026, 10, 1, 11, 0
            ),
            "duration": 7,
            "status": "SCHEDULED",
            "available_seats": 8,
        },
        {
            "flight_id": "FL0003",
            "origin": "NRT",
            "destination": "SIN",
            "departure": datetime(
                2026, 10, 1, 12, 30
            ),
            "duration": 7,
            "status": "SCHEDULED",
            "available_seats": 5,
        },
        {
            "flight_id": "FL0004",
            "origin": "NRT",
            "destination": "SIN",
            "departure": datetime(
                2026, 10, 1, 18, 0
            ),
            "duration": 7,
            "status": "SCHEDULED",
            "available_seats": 2,
        },
        {
            "flight_id": "FL0005",
            "origin": "SIN",
            "destination": "BKK",
            "departure": datetime(
                2026, 10, 1, 20, 30
            ),
            "duration": 2,
            "status": "SCHEDULED",
            "available_seats": 100,
        },
    ]

    for flight in scenario_flights:

        aircraft = aircraft_df[
            aircraft_df["status"] == "AVAILABLE"
        ].sample(1).iloc[0]

        capacity = int(
            aircraft["capacity"]
        )

        available = min(
            flight["available_seats"],
            capacity - 1,
        )

        occupied = capacity - available

        arrival = (
            flight["departure"]
            + timedelta(
                hours=flight["duration"]
            )
        )

        flights.append(
            {
                "flight_id": flight["flight_id"],
                "origin": flight["origin"],
                "destination": flight["destination"],
                "departure": flight["departure"],
                "arrival": arrival,
                "aircraft_id": aircraft["aircraft_id"],
                "capacity": capacity,
                "occupied_seats": occupied,
                "available_seats": available,
                "status": flight["status"],
            }
        )

    # --------------------------------------------------------
    # Additional guaranteed NRT → SIN alternatives
    # --------------------------------------------------------

    for number, hour in enumerate(
        [8, 14, 16, 19, 21, 22],
        start=6,
    ):

        aircraft = aircraft_df[
            aircraft_df["status"] == "AVAILABLE"
        ].sample(1).iloc[0]

        capacity = int(
            aircraft["capacity"]
        )

        available = random.randint(
            20,
            min(80, capacity - 1),
        )

        occupied = capacity - available

        departure = datetime(
            2026,
            10,
            1,
            hour,
            0,
        )

        arrival = departure + timedelta(
            hours=7
        )

        flights.append(
            {
                "flight_id": f"FL{number:04d}",
                "origin": "NRT",
                "destination": "SIN",
                "departure": departure,
                "arrival": arrival,
                "aircraft_id": aircraft["aircraft_id"],
                "capacity": capacity,
                "occupied_seats": occupied,
                "available_seats": available,
                "status": "SCHEDULED",
            }
        )

    # --------------------------------------------------------
    # Random flights
    # --------------------------------------------------------

    for i in range(12, count + 1):

        origin, destination = random.choice(
            ROUTES
        )

        duration = FLIGHT_DURATIONS[
            (origin, destination)
        ]

        departure = random_departure()

        arrival = (
            departure
            + timedelta(
                hours=duration
            )
        )

        available_aircraft = aircraft_df[
            aircraft_df["status"] == "AVAILABLE"
        ]

        aircraft = available_aircraft.sample(
            1
        ).iloc[0]

        capacity = int(
            aircraft["capacity"]
        )

        occupied, available = (
            generate_seat_data(capacity)
        )

        flights.append(
            {
                "flight_id": f"FL{i:04d}",
                "origin": origin,
                "destination": destination,
                "departure": departure,
                "arrival": arrival,
                "aircraft_id": aircraft["aircraft_id"],
                "capacity": capacity,
                "occupied_seats": occupied,
                "available_seats": available,
                "status": "SCHEDULED",
            }
        )

    df = pd.DataFrame(flights)

    df = df.sort_values(
        "departure"
    ).reset_index(drop=True)

    df.to_csv(
        DATA_DIR / "flights.csv",
        index=False,
    )

    print(f"Generated {len(df)} flights")

    return df


# ============================================================
# PASSENGER GENERATION
# ============================================================

def generate_passengers(
    count=NUM_PASSENGERS,
):
    flights_df = pd.read_csv(
        DATA_DIR / "flights.csv"
    )

    passengers = []

    # --------------------------------------------------------
    # GUARANTEED FL0001 SCENARIO
    # --------------------------------------------------------

    for i in range(1, 26):

        if i <= 13:
            passenger_type = "CONNECTING"
            destination = "BKK"
        else:
            passenger_type = "DIRECT"
            destination = "SIN"

        cabin = random_cabin()

        passengers.append(
            {
                "passenger_id": f"P{i:05d}",
                "name": fake.name(),
                "flight_id": "FL0001",
                "origin": "NRT",
                "destination": destination,
                "passenger_type": passenger_type,
                "cabin": cabin,
                "fare_class": random_fare_class(cabin),
                "special_assistance": (
                    random.random() < 0.05
                ),
                "priority_level": random.choice(
                    ["NORMAL", "NORMAL", "HIGH"]
                ),
                "status": "ACTIVE",
            }
        )

    # --------------------------------------------------------
    # RANDOM PASSENGERS
    # --------------------------------------------------------

    for i in range(26, count + 1):

        flight = flights_df.sample(
            1
        ).iloc[0]

        passenger_type = random.choices(
            [
                "DIRECT",
                "CONNECTING",
            ],
            weights=[70, 30],
        )[0]

        cabin = random_cabin()

        passengers.append(
            {
                "passenger_id": f"P{i:05d}",
                "name": fake.name(),
                "flight_id": flight["flight_id"],
                "origin": flight["origin"],
                "destination": flight["destination"],
                "passenger_type": passenger_type,
                "cabin": cabin,
                "fare_class": random_fare_class(cabin),
                "special_assistance": (
                    random.random() < 0.05
                ),
                "priority_level": random.choice(
                    [
                        "NORMAL",
                        "NORMAL",
                        "NORMAL",
                        "HIGH",
                    ]
                ),
                "status": "ACTIVE",
            }
        )

    df = pd.DataFrame(passengers)

    df.to_csv(
        DATA_DIR / "passengers.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} passengers"
    )

    return df


# ============================================================
# CONNECTION GENERATION
# ============================================================

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

    # --------------------------------------------------------
    # GUARANTEED FL0001 CONNECTIONS
    # --------------------------------------------------------

    guaranteed = passengers_df[
        (
            passengers_df["flight_id"]
            == "FL0001"
        )
        & (
            passengers_df["passenger_type"]
            == "CONNECTING"
        )
    ]

    first_flight = flights_df[
        flights_df["flight_id"] == "FL0001"
    ].iloc[0]

    second_flight = flights_df[
        flights_df["flight_id"] == "FL0005"
    ].iloc[0]

    connection_minutes = int(
        (
            second_flight["departure"]
            - first_flight["arrival"]
        ).total_seconds()
        / 60
    )

    for _, passenger in guaranteed.iterrows():

        connections.append(
            {
                "connection_id": (
                    f"C{connection_id:06d}"
                ),
                "passenger_id": passenger[
                    "passenger_id"
                ],
                "first_flight_id": "FL0001",
                "second_flight_id": "FL0005",
                "connection_airport": "SIN",
                "arrival_time": first_flight[
                    "arrival"
                ],
                "next_departure_time": (
                    second_flight[
                        "departure"
                    ]
                ),
                "connection_minutes": (
                    connection_minutes
                ),
            }
        )

        connection_id += 1

    # --------------------------------------------------------
    # RANDOM CONNECTIONS
    # --------------------------------------------------------

    connecting_passengers = passengers_df[
        (
            passengers_df[
                "passenger_type"
            ]
            == "CONNECTING"
        )
        & (
            passengers_df[
                "flight_id"
            ]
            != "FL0001"
        )
    ]

    for _, passenger in connecting_passengers.iterrows():

        first_matches = flights_df[
            flights_df["flight_id"]
            == passenger["flight_id"]
        ]

        if first_matches.empty:
            continue

        first_flight = first_matches.iloc[0]

        possible = flights_df[
            (
                flights_df["origin"]
                == first_flight["destination"]
            )
            & (
                flights_df["departure"]
                > first_flight["arrival"]
            )
            & (
                flights_df["status"]
                == "SCHEDULED"
            )
        ].copy()

        if possible.empty:
            continue

        possible["connection_minutes"] = (
            (
                possible["departure"]
                - first_flight["arrival"]
            ).dt.total_seconds()
            / 60
        )

        possible = possible[
            (
                possible[
                    "connection_minutes"
                ]
                >= 90
            )
            & (
                possible[
                    "connection_minutes"
                ]
                <= 360
            )
        ]

        if possible.empty:
            continue

        second_flight = possible.sample(
            1
        ).iloc[0]

        connections.append(
            {
                "connection_id": (
                    f"C{connection_id:06d}"
                ),
                "passenger_id": passenger[
                    "passenger_id"
                ],
                "first_flight_id": (
                    first_flight[
                        "flight_id"
                    ]
                ),
                "second_flight_id": (
                    second_flight[
                        "flight_id"
                    ]
                ),
                "connection_airport": (
                    first_flight[
                        "destination"
                    ]
                ),
                "arrival_time": (
                    first_flight["arrival"]
                ),
                "next_departure_time": (
                    second_flight[
                        "departure"
                    ]
                ),
                "connection_minutes": int(
                    second_flight[
                        "connection_minutes"
                    ]
                ),
            }
        )

        connection_id += 1

    df = pd.DataFrame(connections)

    df.to_csv(
        DATA_DIR / "connections.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} connections"
    )

    return df


# ============================================================
# CREW GENERATION
# ============================================================

def generate_crew(count=NUM_CREW):
    crew = []

    airport_codes = [
        airport["iata_code"]
        for airport in AIRPORTS
    ]

    roles = [
        "CAPTAIN",
        "FIRST_OFFICER",
        "CABIN_CREW",
    ]

    aircraft_types = list(
        AIRCRAFT_TYPES.keys()
    )

    # --------------------------------------------------------
    # GUARANTEE qualified A321 crew at NRT
    # --------------------------------------------------------

    for i in range(1, 9):

        role = (
            "CAPTAIN"
            if i <= 2
            else "FIRST_OFFICER"
            if i <= 4
            else "CABIN_CREW"
        )

        crew.append(
            {
                "crew_id": f"C{i:05d}",
                "name": fake.name(),
                "role": role,
                "aircraft_type": "A321",
                "base_airport": "NRT",
                "current_airport": "NRT",
                "duty_hours": round(
                    random.uniform(0, 6),
                    1,
                ),
                "rest_hours": round(
                    random.uniform(12, 16),
                    1,
                ),
                "status": "AVAILABLE",
            }
        )

    # --------------------------------------------------------
    # Remaining crew
    # --------------------------------------------------------

    for i in range(9, count + 1):

        role = random.choices(
            roles,
            weights=[15, 20, 65],
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
            random.uniform(0, 12),
            1,
        )

        rest_hours = round(
            random.uniform(6, 18),
            1,
        )

        status = random.choices(
            [
                "AVAILABLE",
                "ON_DUTY",
                "RESTING",
            ],
            weights=[60, 25, 15],
        )[0]

        crew.append(
            {
                "crew_id": f"C{i:05d}",
                "name": fake.name(),
                "role": role,
                "aircraft_type": aircraft_type,
                "base_airport": base_airport,
                "current_airport": current_airport,
                "duty_hours": duty_hours,
                "rest_hours": rest_hours,
                "status": status,
            }
        )

    df = pd.DataFrame(crew)

    df.to_csv(
        DATA_DIR / "crew.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} crew members"
    )

    return df


# ============================================================
# CREW QUALIFICATIONS
# ============================================================

def generate_crew_qualifications():
    crew_df = pd.read_csv(
        DATA_DIR / "crew.csv"
    )

    rows = []

    for _, crew_member in crew_df.iterrows():

        primary_type = crew_member[
            "aircraft_type"
        ]

        rows.append(
            {
                "crew_id": crew_member[
                    "crew_id"
                ],
                "aircraft_type": primary_type,
                "qualification_level": "PRIMARY",
                "valid_until": "2028-12-31",
            }
        )

        # Some crew are qualified for a second type
        if random.random() < 0.25:

            additional_type = random.choice(
                [
                    aircraft_type
                    for aircraft_type
                    in AIRCRAFT_TYPES
                    if aircraft_type
                    != primary_type
                ]
            )

            rows.append(
                {
                    "crew_id": crew_member[
                        "crew_id"
                    ],
                    "aircraft_type": additional_type,
                    "qualification_level": "SECONDARY",
                    "valid_until": "2028-12-31",
                }
            )

    df = pd.DataFrame(rows)

    df.to_csv(
        DATA_DIR / "crew_qualifications.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} crew qualification records"
    )


# ============================================================
# CREW ASSIGNMENTS
# ============================================================

def generate_crew_assignments():
    crew_df = pd.read_csv(
        DATA_DIR / "crew.csv"
    )

    flights_df = pd.read_csv(
        DATA_DIR / "flights.csv"
    )

    available_crew = crew_df[
        crew_df["status"] == "ON_DUTY"
    ]

    rows = []

    assignment_id = 1

    for _, crew_member in available_crew.iterrows():

        if random.random() > 0.35:
            continue

        possible_flights = flights_df[
            flights_df["origin"]
            == crew_member[
                "current_airport"
            ]
        ]

        if possible_flights.empty:
            continue

        flight = possible_flights.sample(
            1
        ).iloc[0]

        rows.append(
            {
                "assignment_id": (
                    f"CA{assignment_id:06d}"
                ),
                "crew_id": crew_member[
                    "crew_id"
                ],
                "flight_id": flight[
                    "flight_id"
                ],
                "role": crew_member[
                    "role"
                ],
                "status": "ASSIGNED",
            }
        )

        assignment_id += 1

    df = pd.DataFrame(rows)

    df.to_csv(
        DATA_DIR / "crew_assignments.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} crew assignments"
    )


# ============================================================
# MAINTENANCE
# ============================================================

def generate_maintenance():
    aircraft_df = pd.read_csv(
        DATA_DIR / "aircraft.csv"
    )

    rows = []

    maintenance_id = 1

    for _, aircraft in aircraft_df.iterrows():

        if (
            aircraft["status"]
            == "MAINTENANCE"
        ):
            maintenance_status = "IN_PROGRESS"
        else:
            maintenance_status = random.choice(
                [
                    "COMPLETED",
                    "COMPLETED",
                    "SCHEDULED",
                ]
            )

        start_date = (
            START_DATE
            + timedelta(
                days=random.randint(
                    -5,
                    20,
                )
            )
        )

        duration = random.randint(
            2,
            12,
        )

        end_date = (
            start_date
            + timedelta(
                hours=duration
            )
        )

        rows.append(
            {
                "maintenance_id": (
                    f"M{maintenance_id:06d}"
                ),
                "aircraft_id": aircraft[
                    "aircraft_id"
                ],
                "maintenance_type": random.choice(
                    [
                        "A_CHECK",
                        "B_CHECK",
                        "C_CHECK",
                        "UNSCHEDULED",
                    ]
                ),
                "status": maintenance_status,
                "start_time": start_date,
                "end_time": end_date,
            }
        )

        maintenance_id += 1

    df = pd.DataFrame(rows)

    df.to_csv(
        DATA_DIR / "maintenance.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} maintenance records"
    )


# ============================================================
# WEATHER
# ============================================================

def generate_weather():
    airport_codes = [
        airport["iata_code"]
        for airport in AIRPORTS
    ]

    weather_types = [
        "CLEAR",
        "CLOUDY",
        "RAIN",
        "STORM",
        "SNOW",
        "FOG",
        "HIGH_WINDS",
    ]

    rows = []

    weather_id = 1

    for day in range(7):

        date = START_DATE + timedelta(
            days=day
        )

        for airport in airport_codes:

            condition = random.choices(
                weather_types,
                weights=[
                    35,
                    20,
                    15,
                    8,
                    7,
                    8,
                    7,
                ],
            )[0]

            severity = (
                "HIGH"
                if condition
                in [
                    "STORM",
                    "SNOW",
                    "FOG",
                    "HIGH_WINDS",
                ]
                and random.random() < 0.35
                else "LOW"
                if condition == "CLEAR"
                else "MEDIUM"
            )

            rows.append(
                {
                    "weather_id": (
                        f"W{weather_id:06d}"
                    ),
                    "airport_code": airport,
                    "date": date.date(),
                    "condition": condition,
                    "severity": severity,
                    "visibility_km": round(
                        random.uniform(
                            1,
                            20,
                        ),
                        1,
                    ),
                    "wind_speed_kmh": random.randint(
                        5,
                        80,
                    ),
                }
            )

            weather_id += 1

    df = pd.DataFrame(rows)

    df.to_csv(
        DATA_DIR / "weather.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} weather records"
    )


# ============================================================
# FLIGHT ROTATIONS
# ============================================================

def generate_flight_rotations():
    flights_df = pd.read_csv(
        DATA_DIR / "flights.csv"
    )
    flights_df["departure"] = pd.to_datetime(flights_df["departure"])
    flights_df["arrival"] = pd.to_datetime(flights_df["arrival"])

    

    flights_df = flights_df.sort_values(
        "departure"
    )


    rows = []

    rotation_id = 1

    for aircraft_id, group in flights_df.groupby(
        "aircraft_id"
    ):

        group = group.sort_values(
            "departure"
        )

        previous_flight = None

        for _, flight in group.iterrows():

            if previous_flight is None:

                leg_number = 1

            else:

                if (
                    flight["departure"]
                    >= previous_flight["arrival"]
                ):
                    leg_number += 1
                else:
                    leg_number = 1

            rows.append(
                {
                    "rotation_id": (
                        f"R{rotation_id:06d}"
                    ),
                    "aircraft_id": aircraft_id,
                    "flight_id": flight[
                        "flight_id"
                    ],
                    "leg_number": leg_number,
                }
            )

            previous_flight = flight
            rotation_id += 1

    df = pd.DataFrame(rows)

    df.to_csv(
        DATA_DIR / "flight_rotations.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} flight rotation records"
    )


# ============================================================
# DISRUPTIONS
# ============================================================

def generate_disruptions(
    count=NUM_DISRUPTIONS,
):
    flights_df = pd.read_csv(
        DATA_DIR / "flights.csv"
    )

    disruption_types = [
        "AIRCRAFT_FAILURE",
        "WEATHER",
        "CREW_UNAVAILABLE",
        "ATC_RESTRICTION",
        "AIRPORT_CLOSURE",
        "SECURITY",
    ]

    disruptions = []

    # --------------------------------------------------------
    # GUARANTEED FL0001 DISRUPTION
    # --------------------------------------------------------

    disruptions.append(
        {
            "disruption_id": "D000001",
            "flight_id": "FL0001",
            "type": "WEATHER",
            "severity": "HIGH",
            "status": "CANCELLED",
            "description": (
                "Severe weather causing "
                "cancellation of flight FL0001"
            ),
        }
    )

    # --------------------------------------------------------
    # Additional disruptions
    # --------------------------------------------------------

    available_flights = flights_df[
        flights_df["flight_id"] != "FL0001"
    ]

    selected_flights = (
        available_flights.sample(
            min(
                count - 1,
                len(available_flights),
            ),
            random_state=42,
        )
    )

    for index, (_, flight) in enumerate(
        selected_flights.iterrows(),
        start=2,
    ):

        disruption_type = random.choice(
            disruption_types
        )

        if disruption_type in [
            "AIRCRAFT_FAILURE",
            "CREW_UNAVAILABLE",
            "AIRPORT_CLOSURE",
            "SECURITY",
        ]:
            severity = random.choice(
                ["MEDIUM", "HIGH"]
            )
            status = random.choice(
                ["DELAYED", "CANCELLED"]
            )

        elif disruption_type == "WEATHER":
            severity = random.choice(
                [
                    "LOW",
                    "MEDIUM",
                    "HIGH",
                ]
            )

            status = random.choice(
                [
                    "DELAYED",
                    "CANCELLED",
                ]
            )

        else:
            severity = random.choice(
                [
                    "MEDIUM",
                    "HIGH",
                ]
            )

            status = "DELAYED"

        disruptions.append(
            {
                "disruption_id": (
                    f"D{index:06d}"
                ),
                "flight_id": flight[
                    "flight_id"
                ],
                "type": disruption_type,
                "severity": severity,
                "status": status,
                "description": (
                    f"{disruption_type.replace('_', ' ').title()} "
                    f"affecting flight "
                    f"{flight['flight_id']}"
                ),
            }
        )

    df = pd.DataFrame(disruptions)

    df.to_csv(
        DATA_DIR / "disruptions.csv",
        index=False,
    )

    print(
        f"Generated {len(df)} disruptions"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("IROPS SYNTHETIC DATA GENERATOR")
    print("=" * 60)
    print()

    generate_airports()

    generate_airport_capacity()

    generate_aircraft()

    generate_flights()

    generate_passengers()

    generate_connections()

    generate_crew()

    generate_crew_qualifications()

    generate_crew_assignments()

    generate_maintenance()

    generate_weather()

    generate_flight_rotations()

    generate_disruptions()

    print()
    print("=" * 60)
    print("DATA GENERATION COMPLETE")
    print("=" * 60)
    print()