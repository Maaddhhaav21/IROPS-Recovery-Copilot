import pandas as pd


CREW_PATH = "data/crew.csv"


def load_crew():
    return pd.read_csv(CREW_PATH)


def get_available_crew(origin):
    crew = load_crew()

    return crew[
        (crew["current_airport"] == origin)
        & (crew["status"] == "AVAILABLE")
    ].copy()


def get_matching_crew(origin, aircraft_type):
    crew = get_available_crew(origin)

    return crew[
        crew["aircraft_type"]
        == aircraft_type
    ].copy()


def get_crew_member(crew_id):
    crew = load_crew()

    member = crew[
        crew["crew_id"] == crew_id
    ]

    if member.empty:
        return None

    return member.iloc[0].to_dict()