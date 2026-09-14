import pandas as pd
from pathlib import Path

DEMO_DIR = Path("data/demo")
DEMO_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. FLIGHTS
# ============================================================

flights = pd.DataFrame([
    # --------------------------------------------------------
    # DISRUPTED FLIGHT
    # DXB -> DOH
    # --------------------------------------------------------
    {
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 14:00:00",
        "arrival": "2026-10-10 15:00:00",
        "status": "CANCELLED",
        "available_seats": 0
    },

    # --------------------------------------------------------
    # PASSENGERS' ONWARD FLIGHT
    # DOH -> LHR
    # Leaves at 16:30
    # --------------------------------------------------------
    {
        "flight_id": "DEMO002",
        "origin": "DOH",
        "destination": "LHR",
        "departure": "2026-10-10 16:30:00",
        "arrival": "2026-10-10 21:00:00",
        "status": "SCHEDULED",
        "available_seats": 80
    },

    # --------------------------------------------------------
    # ALTERNATIVE 1
    # Arrives 15:30
    # 60 minutes before onward flight
    # VALID
    # --------------------------------------------------------
    {
        "flight_id": "ALT001",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 14:30:00",
        "arrival": "2026-10-10 15:30:00",
        "status": "SCHEDULED",
        "available_seats": 20
    },

    # --------------------------------------------------------
    # ALTERNATIVE 2
    # Arrives 16:15
    # Only 15 minutes before onward flight
    # INVALID CONNECTION
    # --------------------------------------------------------
    {
        "flight_id": "ALT002",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 15:15:00",
        "arrival": "2026-10-10 16:15:00",
        "status": "SCHEDULED",
        "available_seats": 80
    },

    # --------------------------------------------------------
    # ALTERNATIVE 3
    # Arrives 17:00
    # Onward flight already departed
    # INVALID CONNECTION
    # --------------------------------------------------------
    {
        "flight_id": "ALT003",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 16:00:00",
        "arrival": "2026-10-10 17:00:00",
        "status": "SCHEDULED",
        "available_seats": 80
    },

    # --------------------------------------------------------
    # ALTERNATIVE 4
    # Only 2 seats available
    # 8 passengers affected
    # INVALID CAPACITY
    # --------------------------------------------------------
    {
        "flight_id": "ALT004",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 14:45:00",
        "arrival": "2026-10-10 15:45:00",
        "status": "SCHEDULED",
        "available_seats": 2
    }
])

flights.to_csv(
    DEMO_DIR / "flights.csv",
    index=False
)


# ============================================================
# 2. PASSENGERS
# ============================================================

passengers = pd.DataFrame([
    {
        "passenger_id": "DEMO_P001",
        "name": "Rahul Sharma",
        "passenger_type": "CONNECTING",
        "cabin": "Economy",
        "fare_class": "Y",
        "special_assistance": True,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "LHR"
    },

    {
        "passenger_id": "DEMO_P002",
        "name": "Emma Wilson",
        "passenger_type": "CONNECTING",
        "cabin": "Economy",
        "fare_class": "M",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "LHR"
    },

    {
        "passenger_id": "DEMO_P003",
        "name": "James Anderson",
        "passenger_type": "CONNECTING",
        "cabin": "Business",
        "fare_class": "J",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "LHR"
    },

    {
        "passenger_id": "DEMO_P004",
        "name": "Sofia Martin",
        "passenger_type": "CONNECTING",
        "cabin": "Economy",
        "fare_class": "B",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "LHR"
    },

    {
        "passenger_id": "DEMO_P005",
        "name": "Daniel Brown",
        "passenger_type": "CONNECTING",
        "cabin": "Economy",
        "fare_class": "Y",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "LHR"
    },

    {
        "passenger_id": "DEMO_P006",
        "name": "Arjun Patel",
        "passenger_type": "DIRECT",
        "cabin": "Economy",
        "fare_class": "Y",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "DOH"
    },

    {
        "passenger_id": "DEMO_P007",
        "name": "Olivia Taylor",
        "passenger_type": "DIRECT",
        "cabin": "Economy",
        "fare_class": "M",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "DOH"
    },

    {
        "passenger_id": "DEMO_P008",
        "name": "Michael Davis",
        "passenger_type": "DIRECT",
        "cabin": "Business",
        "fare_class": "J",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "DOH"
    }
])

passengers.to_csv(
    DEMO_DIR / "passengers.csv",
    index=False
)


# ============================================================
# 3. CONNECTIONS
# ============================================================

connections = pd.DataFrame([
    {
        "connection_id": "DEMO_C001",
        "passenger_id": "DEMO_P001",
        "first_flight_id": "DEMO001",
        "second_flight_id": "DEMO002",
        "connection_airport": "DOH",
        "arrival_time": "2026-10-10 15:00:00",
        "next_departure_time": "2026-10-10 16:30:00",
        "connection_minutes": 90
    },

    {
        "connection_id": "DEMO_C002",
        "passenger_id": "DEMO_P002",
        "first_flight_id": "DEMO001",
        "second_flight_id": "DEMO002",
        "connection_airport": "DOH",
        "arrival_time": "2026-10-10 15:00:00",
        "next_departure_time": "2026-10-10 16:30:00",
        "connection_minutes": 90
    },

    {
        "connection_id": "DEMO_C003",
        "passenger_id": "DEMO_P003",
        "first_flight_id": "DEMO001",
        "second_flight_id": "DEMO002",
        "connection_airport": "DOH",
        "arrival_time": "2026-10-10 15:00:00",
        "next_departure_time": "2026-10-10 16:30:00",
        "connection_minutes": 90
    },

    {
        "connection_id": "DEMO_C004",
        "passenger_id": "DEMO_P004",
        "first_flight_id": "DEMO001",
        "second_flight_id": "DEMO002",
        "connection_airport": "DOH",
        "arrival_time": "2026-10-10 15:00:00",
        "next_departure_time": "2026-10-10 16:30:00",
        "connection_minutes": 90
    },

    {
        "connection_id": "DEMO_C005",
        "passenger_id": "DEMO_P005",
        "first_flight_id": "DEMO001",
        "second_flight_id": "DEMO002",
        "connection_airport": "DOH",
        "arrival_time": "2026-10-10 15:00:00",
        "next_departure_time": "2026-10-10 16:30:00",
        "connection_minutes": 90
    }
])

connections.to_csv(
    DEMO_DIR / "connections.csv",
    index=False
)


# ============================================================
# DONE
# ============================================================

print("=" * 60)
print("DEMO DATA CREATED")
print("=" * 60)

print()
print("Disrupted flight : DEMO001")
print("Onward flight    : DEMO002")
print("Affected         : 8 passengers")
print("Connecting       : 5 passengers")
print("Direct           : 3 passengers")

print()
print("Alternatives:")
print("ALT001 → 20 seats → 60 min connection → VALID")
print("ALT002 → 80 seats → 15 min connection → INVALID")
print("ALT003 → 80 seats → connection departed → INVALID")
print("ALT004 → 2 seats  → capacity failure → INVALID")

print()
print("Files created in data/demo/")
