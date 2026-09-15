import pandas as pd


FLIGHTS_PATH = "data/flights.csv"


def load_flights():
    flights = pd.read_csv(FLIGHTS_PATH)

    flights["departure"] = pd.to_datetime(
        flights["departure"]
    )

    flights["arrival"] = pd.to_datetime(
        flights["arrival"]
    )

    return flights


def get_flight(flight_id):
    flights = load_flights()

    flight = flights[
        flights["flight_id"] == flight_id
    ]

    if flight.empty:
        return None

    return flight.iloc[0].to_dict()


def get_alternative_flights(flight_id):
    flights = load_flights()

    flight = get_flight(flight_id)

    if flight is None:
        return pd.DataFrame()

    alternatives = flights[
        (flights["origin"] == flight["origin"])
        & (
            flights["destination"]
            == flight["destination"]
        )
        & (
            flights["departure"]
            > flight["departure"]
        )
        & (
            flights["flight_id"]
            != flight_id
        )
        & (
            flights["status"]
            == "SCHEDULED"
        )
    ].copy()

    return alternatives


def get_flight_status(flight_id):
    flight = get_flight(flight_id)

    if flight is None:
        return None

    return flight["status"]