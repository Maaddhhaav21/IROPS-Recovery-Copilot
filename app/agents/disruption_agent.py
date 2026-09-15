import pandas as pd


class DisruptionAgent:
    """
    Agent responsible for identifying and analyzing
    an airline disruption.
    """

    def __init__(self, data_path="data/disruptions.csv"):
        self.data_path = data_path

    def analyze(self, flight_id):
        """
        Analyze the disruption affecting a flight.
        """

        disruptions = pd.read_csv(self.data_path)

        disruption = disruptions[
            disruptions["flight_id"] == flight_id
        ]

        if disruption.empty:
            return {
                "status": "NO_DISRUPTION",
                "flight_id": flight_id,
            }

        disruption = disruption.iloc[0]

        return {
            "status": "DISRUPTION_FOUND",
            "flight_id": flight_id,
            "disruption_type": disruption["type"],
            "severity": disruption["severity"],
            "disruption_status": disruption["status"],
            "description": disruption["description"],
        }