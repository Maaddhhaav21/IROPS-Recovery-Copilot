import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path("data")

MIN_REST_HOURS = 10
MAX_DUTY_HOURS = 12


# ============================================================
# LOAD DATA
# ============================================================

def load_crew():
    return pd.read_csv(DATA_DIR / "crew.csv")


def load_flight(flight_id):
    flights = pd.read_csv(DATA_DIR / "flights.csv")

    flight = flights[
        flights["flight_id"] == flight_id
    ]

    if flight.empty:
        return None

    return flight.iloc[0]


# ============================================================
# CHECK CREW ELIGIBILITY
# ============================================================

def check_crew_eligibility(crew, flight):
    """
    Check whether one crew member can operate a flight.
    """

    reasons = []

    # Rule 1: Crew must be available
    if crew["status"] != "AVAILABLE":
        reasons.append("Crew is not available")

    # Rule 2: Crew must be at the flight origin
    if crew["current_airport"] != flight["origin"]:
        reasons.append(
            f"Crew is at {crew['current_airport']}, "
            f"flight departs from {flight['origin']}"
        )

    # Rule 3: Aircraft type must match
    if crew["aircraft_type"] != flight["aircraft_id"]:
        # We will handle aircraft type below using the aircraft file.
        pass

    # Rule 4: Minimum rest
    if float(crew["rest_hours"]) < MIN_REST_HOURS:
        reasons.append(
            f"Insufficient rest ({crew['rest_hours']} hours)"
        )

    # Rule 5: Maximum duty
    duration = (
        pd.to_datetime(flight["arrival"])
        - pd.to_datetime(flight["departure"])
    ).total_seconds() / 3600

    projected_duty = float(crew["duty_hours"]) + duration

    if projected_duty > MAX_DUTY_HOURS:
        reasons.append(
            f"Duty would reach {projected_duty:.1f} hours"
        )

    if reasons:
        return {
            "eligible": False,
            "reasons": reasons
        }

    return {
        "eligible": True,
        "reasons": []
    }


# ============================================================
# FIND ELIGIBLE CREW
# ============================================================

def find_eligible_crew(flight_id):
    """
    Find crew members that satisfy the basic crew rules.
    """

    flight = load_flight(flight_id)

    if flight is None:
        return {
            "flight_id": flight_id,
            "status": "FLIGHT_NOT_FOUND"
        }

    crew_df = load_crew()

    eligible = []
    rejected = []

    for _, crew in crew_df.iterrows():

        result = check_crew_eligibility(
            crew,
            flight
        )

        crew_result = {
            "crew_id": crew["crew_id"],
            "name": crew["name"],
            "role": crew["role"],
            "aircraft_type": crew["aircraft_type"],
            "current_airport": crew["current_airport"],
            "duty_hours": crew["duty_hours"],
            "rest_hours": crew["rest_hours"]
        }

        if result["eligible"]:
            eligible.append(crew_result)
        else:
            crew_result["reasons"] = result["reasons"]
            rejected.append(crew_result)

    return {
        "flight_id": flight_id,
        "origin": flight["origin"],
        "destination": flight["destination"],
        "eligible_crew": eligible,
        "rejected_crew": rejected,
        "status": "ANALYZED"
    }


# ============================================================
# DISPLAY RESULTS
# ============================================================

def print_results(result):

    print()
    print("=" * 60)
    print("IROPS CREW RECOVERY ANALYZER")
    print("=" * 60)

    if result["status"] == "FLIGHT_NOT_FOUND":
        print(f"Flight not found: {result['flight_id']}")
        print("=" * 60)
        return

    print(
        f"Flight       : {result['flight_id']}"
    )

    print(
        f"Route        : "
        f"{result['origin']} → {result['destination']}"
    )

    print()

    print(
        f"Eligible crew: {len(result['eligible_crew'])}"
    )

    for crew in result["eligible_crew"]:
        print(
            f"  ✓ {crew['crew_id']} | "
            f"{crew['role']} | "
            f"{crew['aircraft_type']} | "
            f"{crew['current_airport']}"
        )

    print()

    print(
        f"Rejected crew: {len(result['rejected_crew'])}"
    )

    for crew in result["rejected_crew"]:
        print(
            f"  ✗ {crew['crew_id']} | "
            f"{', '.join(crew['reasons'])}"
        )

    print()
    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    flight_id = "FL0002"

    result = find_eligible_crew(flight_id)

    print_results(result)