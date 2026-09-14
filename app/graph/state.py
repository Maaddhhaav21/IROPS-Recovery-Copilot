from typing import TypedDict, Any


class IROPSState(TypedDict, total=False):
    """
    Shared state passed between all IROPS recovery agents/nodes.
    """

    # ─────────────────────────────────────────
    # DISRUPTION
    # ─────────────────────────────────────────

    flight_id: str
    disruption_type: str
    severity: str

    # ─────────────────────────────────────────
    # PASSENGERS
    # ─────────────────────────────────────────

    affected_passengers: Any
    connecting_passengers: Any

    # ─────────────────────────────────────────
    # FLIGHTS
    # ─────────────────────────────────────────

    alternative_flights: Any
    feasible_options: Any

    # ─────────────────────────────────────────
    # OPTIMIZATION
    # ─────────────────────────────────────────

    solver_status: str
    rebooking_results: Any

    # ─────────────────────────────────────────
    # FINAL OUTPUT
    # ─────────────────────────────────────────

    recovery_plan: Any
    briefing: str