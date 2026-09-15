import pandas as pd


AIRCRAFT_PATH = "data/aircraft.csv"


def load_aircraft():
    return pd.read_csv(AIRCRAFT_PATH)


def get_aircraft(aircraft_id):
    aircraft = load_aircraft()

    result = aircraft[
        aircraft["aircraft_id"]
        == aircraft_id
    ]

    if result.empty:
        return None

    return result.iloc[0].to_dict()


def get_aircraft_type(aircraft_id):
    aircraft = get_aircraft(aircraft_id)

    if aircraft is None:
        return None

    return aircraft["aircraft_type"]


def get_aircraft_capacity(aircraft_id):
    aircraft = get_aircraft(aircraft_id)

    if aircraft is None:
        return None

    return int(aircraft["capacity"])
