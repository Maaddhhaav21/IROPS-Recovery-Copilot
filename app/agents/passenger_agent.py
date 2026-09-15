from app.tools.passenger_tools import (
    get_affected_passengers,
    get_connecting_passengers,
)


class PassengerAgent:

    def analyze(self, flight_id):

        affected = get_affected_passengers(flight_id)
        connecting = get_connecting_passengers(flight_id)

        if not affected:
            return {
                "status": "NO_AFFECTED_PASSENGERS",
                "flight_id": flight_id,
                "affected_passengers": [],
                "connecting_passengers": [],
            }

        connecting_ids = {
            passenger["passenger_id"]
            for passenger in connecting
        }

        for passenger in affected:
            passenger["has_connection"] = (
                passenger["passenger_id"] in connecting_ids
            )

        connecting_with_flag = [
            passenger
            for passenger in affected
            if passenger["has_connection"]
        ]

        return {
            "status": "PASSENGERS_FOUND",
            "flight_id": flight_id,
            "affected_passengers": affected,
            "connecting_passengers": connecting_with_flag,
        }