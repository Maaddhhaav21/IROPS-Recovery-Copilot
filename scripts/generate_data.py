import pandas as pd
from pathlib import Path
import random
from datetime import datetime, timedelta

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

random.seed(42)

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

    for i in range(1, count + 1):

        origin, destination = random.choice(ROUTES)

        duration = FLIGHT_DURATIONS[(origin, destination)]

        departure = start_date + timedelta(
            days=random.randint(0, 6),
            hours=random.randint(0, 23),
            minutes=random.choice([0, 15, 30, 45])
        )

        arrival = departure + timedelta(hours=duration)

        aircraft = aircraft_df.sample(1).iloc[0]

        flights.append({
            "flight_id": f"FL{i:04d}",
            "origin": origin,
            "destination": destination,
            "departure": departure,
            "arrival": arrival,
            "aircraft_id": aircraft["aircraft_id"],
            "status": "SCHEDULED"
        })

    df = pd.DataFrame(flights)

    df.to_csv(
        DATA_DIR / "flights.csv",
        index=False
    )

    print(f"Generated {len(df)} flights")

if __name__ == "__main__":
    generate_airports()
    generate_aircraft()
    generate_flights()
