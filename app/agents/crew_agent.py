import pandas as pd


class CrewAgent:
    def __init__(
        self,
        crew_path="data/crew.csv",
        flights_path="data/flights.csv",
        aircraft_path="data/aircraft.csv",
    ):
        self.crew_path = crew_path
        self.flights_path = flights_path
        self.aircraft_path = aircraft_path

    def analyze(self, flight_id):
        # Load data
        crew = pd.read_csv(self.crew_path)
        flights = pd.read_csv(self.flights_path)
        aircraft = pd.read_csv(self.aircraft_path)

        # Find the flight
        flight = flights[flights["flight_id"] == flight_id]

        if flight.empty:
            return {
                "status": "FLIGHT_NOT_FOUND",
                "flight_id": flight_id,
                "available_crew": [],
                "matching_crew": [],
            }

        flight = flight.iloc[0]

        # Find the aircraft assigned to this flight
        aircraft_info = aircraft[
            aircraft["aircraft_id"] == flight["aircraft_id"]
        ]

        if aircraft_info.empty:
            return {
                "status": "AIRCRAFT_NOT_FOUND",
                "flight_id": flight_id,
                "available_crew": [],
                "matching_crew": [],
            }

        aircraft_info = aircraft_info.iloc[0]

        # IMPORTANT:
        # aircraft.csv uses "aircraft_type"
        aircraft_type = aircraft_info["aircraft_type"]

        # Find available crew at the flight's origin
        available_crew = crew[
            (crew["current_airport"] == flight["origin"])
            & (crew["status"] == "AVAILABLE")
        ].copy()

        # Keep only crew qualified for this aircraft type
        matching_crew = available_crew[
            available_crew["aircraft_type"] == aircraft_type
        ].copy()

        return {
            "status": "CREW_ANALYSIS_COMPLETED",
            "flight_id": flight_id,
            "origin": flight["origin"],
            "destination": flight["destination"],
            "aircraft_type": aircraft_type,
            "available_crew": available_crew,
            "matching_crew": matching_crew,
        }