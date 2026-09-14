import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path("data")


# ============================================================
# LOAD DISRUPTION
# ============================================================

def get_disruption(flight_id):
    """
    Find the disruption record for a given flight.
    """

    disruptions = pd.read_csv(DATA_DIR / "disruptions.csv")

    disruption = disruptions[
        disruptions["flight_id"] == flight_id
    ]

    if disruption.empty:
        return None

    return disruption.iloc[0]


# ============================================================
# GET AFFECTED PASSENGERS
# ============================================================

def get_affected_passengers(flight_id):
    """
    Return all passengers booked on the disrupted flight.
    """

    passengers = pd.read_csv(DATA_DIR / "passengers.csv")

    return passengers[
        passengers["flight_id"] == flight_id
    ]


# ============================================================
# GET CONNECTING PASSENGERS
# ============================================================

def get_connecting_passengers(flight_id):
    """
    Return passengers whose disrupted flight is the first
    flight in their connection.
    """

    connections = pd.read_csv(DATA_DIR / "connections.csv")

    return connections[
        connections["first_flight_id"] == flight_id
    ]


# ============================================================
# DETERMINE SEVERITY
# ============================================================

def determine_severity(disruption_type):
    """
    Determine operational severity from the disruption type.
    """

    high_severity = {
        "WEATHER",
        "AIRCRAFT_FAILURE",
        "AIRPORT_CLOSURE",
        "CREW_UNAVAILABLE"
    }

    medium_severity = {
        "ATC_RESTRICTION"
    }

    if disruption_type in high_severity:
        return "HIGH"

    if disruption_type in medium_severity:
        return "MEDIUM"

    return "LOW"


# ============================================================
# RECOMMENDED ACTION
# ============================================================

def determine_action(severity, affected_count):
    """
    Determine the recommended recovery action.
    """

    if affected_count == 0:
        return "NO_ACTION"

    if severity == "HIGH":
        return "REBOOK"

    if severity == "MEDIUM":
        return "REBOOK_OR_DELAY"

    return "MONITOR"


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze_disruption(flight_id):
    """
    Analyze a flight disruption and return a structured
    operational summary.
    """

    disruption = get_disruption(flight_id)

    if disruption is None:
        return {
            "flight_id": flight_id,
            "status": "NO_DISRUPTION_FOUND"
        }

    # The CSV column is called "type", not "disruption_type".
    disruption_type = str(disruption["type"])

    affected = get_affected_passengers(flight_id)

    connecting = get_connecting_passengers(flight_id)

    # Use the severity already generated in disruptions.csv.
    severity = str(disruption["severity"])

    action = determine_action(
        severity,
        len(affected)
    )

    return {
        "flight_id": flight_id,
        "disruption_type": disruption_type,
        "severity": severity,
        "affected_passengers": len(affected),
        "connecting_passengers": len(connecting),
        "recommended_action": action,
        "status": "DISRUPTION_FOUND"
    }


# ============================================================
# DISPLAY ANALYSIS
# ============================================================

def print_analysis(result):
    """
    Print the disruption analysis in a readable format.
    """

    print()
    print("=" * 60)
    print("IROPS DISRUPTION ANALYZER")
    print("=" * 60)

    if result["status"] == "NO_DISRUPTION_FOUND":
        print(f"Flight              : {result['flight_id']}")
        print("Status              : No disruption found")
        print("=" * 60)
        return

    print(f"Flight              : {result['flight_id']}")
    print(f"Disruption type     : {result['disruption_type']}")
    print(f"Severity            : {result['severity']}")
    print(f"Affected passengers : {result['affected_passengers']}")
    print(f"Connecting          : {result['connecting_passengers']}")
    print(f"Recommended action  : {result['recommended_action']}")

    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    flight_id = "FL0001"

    result = analyze_disruption(flight_id)

    print_analysis(result)
