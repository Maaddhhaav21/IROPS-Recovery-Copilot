from typing import TypedDict, Any


class IROPSState(TypedDict, total=False):
    flight_id: str
    disruption_type: str
    severity: str
    disruption_status: str
    
    affected_passengers: Any
    connecting_passengers: Any

    alternative_flights: Any
    feasible_options: Any

    solver_status: str
    rebooking_results: Any

    crew_analysis: Any

    recovery_plan: Any
    briefing: str