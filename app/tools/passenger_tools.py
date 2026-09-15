import pandas as pd


PASSENGERS_PATH = "data/passengers.csv"
CONNECTIONS_PATH = "data/connections.csv"


def load_passengers():
    return pd.read_csv(PASSENGERS_PATH)


def load_connections():
    return pd.read_csv(CONNECTIONS_PATH)


def get_affected_passengers(flight_id):
    passengers = load_passengers()

    return passengers[
        passengers["flight_id"] == flight_id
    ].copy()


def get_connecting_passengers(flight_id):
    passengers = load_passengers()
    connections = load_connections()

    connecting_ids = set(
        connections[
            connections["first_flight_id"]
            == flight_id
        ]["passenger_id"]
    )

    return passengers[
        passengers["passenger_id"].isin(
            connecting_ids
        )
    ].copy()


def get_passenger_connections(passenger_id):
    connections = load_connections()

    return connections[
        connections["passenger_id"]
        == passenger_id
    ].copy()