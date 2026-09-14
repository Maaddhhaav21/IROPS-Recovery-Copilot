import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")


# ============================================================
# LOAD EXISTING DATA
# ============================================================

flights = pd.read_csv(DATA_DIR / "flights.csv")
passengers = pd.read_csv(DATA_DIR / "passengers.csv")
connections = pd.read_csv(DATA_DIR / "connections.csv")
aircraft = pd.read_csv(DATA_DIR / "aircraft.csv")
disruptions = pd.read_csv(DATA_DIR / "disruptions.csv")


# ============================================================
# 1. ADD DEMO AIRCRAFT
# ============================================================

demo_aircraft = pd.DataFrame([
    {
        "aircraft_id": "DEMO_AC01",
        "aircraft_type": "A320",
        "capacity": 180,
        "current_airport": "DXB",
        "status": "AVAILABLE"
    },
    {
        "aircraft_id": "DEMO_AC02",
        "aircraft_type": "A320",
        "capacity": 180,
        "current_airport": "DOH",
        "status": "AVAILABLE"
    },
    {
        "aircraft_id": "DEMO_AC03",
        "aircraft_type": "A320",
        "capacity": 180,
        "current_airport": "DXB",
        "status": "AVAILABLE"
    },
    {
        "aircraft_id": "DEMO_AC04",
        "aircraft_type": "A320",
        "capacity": 180,
        "current_airport": "DXB",
        "status": "AVAILABLE"
    },
    {
        "aircraft_id": "DEMO_AC05",
        "aircraft_type": "A320",
        "capacity": 180,
        "current_airport": "DXB",
        "status": "AVAILABLE"
    }
])

aircraft = pd.concat(
    [aircraft, demo_aircraft],
    ignore_index=True
)


# ============================================================
# 2. ADD DEMO FLIGHTS
# ============================================================

demo_flights = pd.DataFrame([
    
    # ORIGINAL FLIGHT - DISRUPTED
    {
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 14:00:00",
        "arrival": "2026-10-10 15:00:00",
        "aircraft_id": "DEMO_AC01",
        "status": "CANCELLED",
        "capacity": 180,
        "occupied_seats": 20,
        "available_seats": 160
    },

    # PASSENGERS' CONNECTING FLIGHT
    {
        "flight_id": "DEMO002",
        "origin": "DOH",
        "destination": "LHR",
        "departure": "2026-10-10 16:30:00",
        "arrival": "2026-10-10 21:00:00",
        "aircraft_id": "DEMO_AC02",
        "status": "SCHEDULED",
        "capacity": 180,
        "occupied_seats": 100,
        "available_seats": 80
    },

    # --------------------------------------------------------
    # ALTERNATIVE 1
    # Arrives at 15:30
    # Connection flight leaves at 16:30
    # 60 minutes connection
    # SHOULD PASS
    # --------------------------------------------------------
    {
        "flight_id": "ALT001",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 14:30:00",
        "arrival": "2026-10-10 15:30:00",
        "aircraft_id": "DEMO_AC03",
        "status": "SCHEDULED",
        "capacity": 180,
        "occupied_seats": 160,
        "available_seats": 20
    },

    # --------------------------------------------------------
    # ALTERNATIVE 2
    # Arrives at 16:15
    # Connection flight leaves at 16:30
    # Only 15 minutes
    # SHOULD FAIL CONNECTION CHECK
    # --------------------------------------------------------
    {
        "flight_id": "ALT002",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 15:15:00",
        "arrival": "2026-10-10 16:15:00",
        "aircraft_id": "DEMO_AC04",
        "status": "SCHEDULED",
        "capacity": 180,
        "occupied_seats": 100,
        "available_seats": 80
    },

    # --------------------------------------------------------
    # ALTERNATIVE 3
    # Arrives at 17:00
    # Connection flight already left at 16:30
    # SHOULD FAIL
    # --------------------------------------------------------
    {
        "flight_id": "ALT003",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 16:00:00",
        "arrival": "2026-10-10 17:00:00",
        "aircraft_id": "DEMO_AC05",
        "status": "SCHEDULED",
        "capacity": 180,
        "occupied_seats": 100,
        "available_seats": 80
    },

    # --------------------------------------------------------
    # ALTERNATIVE 4
    # Only 2 seats available
    # 8 passengers need seats
    # SHOULD FAIL CAPACITY CHECK
    # --------------------------------------------------------
    {
        "flight_id": "ALT004",
        "origin": "DXB",
        "destination": "DOH",
        "departure": "2026-10-10 14:45:00",
        "arrival": "2026-10-10 15:45:00",
        "aircraft_id": "DEMO_AC03",
        "status": "SCHEDULED",
        "capacity": 180,
        "occupied_seats": 178,
        "available_seats": 2
    }
])

flights = pd.concat(
    [flights, demo_flights],
    ignore_index=True
)


# ============================================================
# 3. ADD DEMO PASSENGERS
# ============================================================

demo_passengers = pd.DataFrame([
    {
        "passenger_id": "DEMO_P001",
        "name": "Demo Passenger 1",
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
        "name": "Demo Passenger 2",
        "passenger_type": "CONNECTING",
        "cabin": "Economy",
        "fare_class": "Y",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "LHR"
    },

    {
        "passenger_id": "DEMO_P003",
        "name": "Demo Passenger 3",
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
        "name": "Demo Passenger 4",
        "passenger_type": "CONNECTING",
        "cabin": "Economy",
        "fare_class": "M",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "LHR"
    },

    {
        "passenger_id": "DEMO_P005",
        "name": "Demo Passenger 5",
        "passenger_type": "CONNECTING",
        "cabin": "Economy",
        "fare_class": "B",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "LHR"
    },

    {
        "passenger_id": "DEMO_P006",
        "name": "Demo Passenger 6",
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
        "name": "Demo Passenger 7",
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
        "name": "Demo Passenger 8",
        "passenger_type": "DIRECT",
        "cabin": "Business",
        "fare_class": "J",
        "special_assistance": False,
        "flight_id": "DEMO001",
        "origin": "DXB",
        "destination": "DOH"
    }
])

passengers = pd.concat(
    [passengers, demo_passengers],
    ignore_index=True
)


# ============================================================
# 4. ADD CONNECTIONS
# ============================================================

demo_connections = pd.DataFrame([
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

connections = pd.concat(
    [connections, demo_connections],
    ignore_index=True
)


# ============================================================
# 5. ADD DISRUPTION
# ============================================================

demo_disruption = pd.DataFrame([
    {
        "disruption_id": "DEMO_D001",
        "flight_id": "DEMO001",
        "disruption_type": "AIRCRAFT_FAILURE",
        "severity": "HIGH",
        "description": "Aircraft technical failure before departure",
        "status": "ACTIVE"
    }
])

disruptions = pd.concat(
    [disruptions, demo_disruption],
    ignore_index=True
)


# ============================================================
# 6. SAVE EVERYTHING
# ============================================================

aircraft.to_csv(
    DATA_DIR / "aircraft.csv",
    index=False
)

flights.to_csv(
    DATA_DIR / "flights.csv",
    index=False
)

passengers.to_csv(
    DATA_DIR / "passengers.csv",
    index=False
)

connections.to_csv(
    DATA_DIR / "connections.csv",
    index=False
)

disruptions.to_csv(
    DATA_DIR / "disruptions.csv",
    index=False
)


# ============================================================
# DONE
# ============================================================

print("=" * 60)
print("DEMO IROPS SCENARIO CREATED")
print("=" * 60)

print()
print("Disrupted flight : DEMO001")
print("Connecting flight: DEMO002")

print()
print("Alternative flights:")
print("  ALT001 → GOOD CONNECTION")
print("  ALT002 → CONNECTION TOO SHORT")
print("  ALT003 → CONNECTION ALREADY DEPARTED")
print("  ALT004 → NOT ENOUGH SEATS")

print()
print("Demo passengers  : 8")
print("Connecting       : 5")
print("Direct           : 3")

print()
print("Scenario ready!")