import pandas as pd


class PassengerAgent:
    """
    Agent responsible for identifying passengers affected
    by a disrupted flight and their connection status.
    """

    def __init__(
        self,
        passengers_path="data/passengers.csv",
        connections_path="data/connections.csv",
    ):
        self.passengers_path = passengers_path
        self.connections_path = connections_path

    def analyze(self, flight_id):
        """
        Find passengers affected by the disrupted flight
        and identify which of them have onward connections.
        """

        passengers = pd.read_csv(
            self.passengers_path
        )

        connections = pd.read_csv(
            self.connections_path
        )

        # Find passengers booked on the disrupted flight
        affected = passengers[
            passengers["flight_id"] == flight_id
        ].copy()

        if affected.empty:
            return {
                "status": "NO_AFFECTED_PASSENGERS",
                "flight_id": flight_id,
                "affected_passengers": [],
                "connecting_passengers": [],
            }

        # Find passengers who have an onward connection
        connecting_ids = set(
            connections[
                connections["first_flight_id"]
                == flight_id
            ]["passenger_id"]
        )

        affected["has_connection"] = (
            affected["passenger_id"]
            .isin(connecting_ids)
        )

        connecting = affected[
            affected["has_connection"]
        ].copy()

        return {
            "status": "PASSENGERS_FOUND",
            "flight_id": flight_id,
            "affected_passengers": affected,
            "connecting_passengers": connecting,
        }