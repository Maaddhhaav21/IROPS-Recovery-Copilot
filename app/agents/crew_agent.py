from app.tools.flight_tools import get_flight
from app.tools.aircraft_tools import get_aircraft
from app.tools.crew_tools import get_available_crew


class CrewAgent:

    def analyze(self, flight_id):

        flight = get_flight(flight_id)

        if flight is None:
            return {
                "status": "FLIGHT_NOT_FOUND",
                "flight_id": flight_id,
                "available_crew": [],
                "matching_crew": [],
            }

        aircraft_id = flight["aircraft_id"]

        aircraft = get_aircraft(aircraft_id)

        if aircraft is None:
            return {
                "status": "AIRCRAFT_NOT_FOUND",
                "flight_id": flight_id,
                "available_crew": [],
                "matching_crew": [],
            }

        aircraft_type = aircraft["aircraft_type"]
        origin = flight["origin"]

        available_crew = get_available_crew(origin)

        matching_crew = [
            crew
            for crew in available_crew
            if crew["aircraft_type"] == aircraft_type
        ]

        return {
            "status": "CREW_ANALYSIS_COMPLETED",
            "flight_id": flight_id,
            "origin": origin,
            "destination": flight["destination"],
            "aircraft_type": aircraft_type,
            "available_crew": available_crew,
            "matching_crew": matching_crew,
        }