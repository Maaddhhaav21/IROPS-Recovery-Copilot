from app.optimization.constraints import (
    find_alternative_flights,
)

from app.optimization.model import (
    optimize_rebooking,
)

class RebookingAgent:
    """
    Agent responsible for finding the best possible
    rebooking plan for passengers affected by a disruption.
    """

    def analyze(self, flight_id, affected_passengers):
        """
        Generate an optimized rebooking plan.
        """

        # Find alternative flights
        alternatives = find_alternative_flights(
            flight_id
        )

        if alternatives.empty:
            return {
                "status": "NO_ALTERNATIVES",
                "flight_id": flight_id,
                "results": [],
                "solver_status": "NO_SOLUTION",
            }

        # Run OR-Tools optimization
        (
            results,
            feasible_options,
            solver_status,
        ) = optimize_rebooking(
            affected_passengers,
            alternatives,
        )

        rebooked = sum(
            result["status"] == "REBOOKED"
            for result in results
        )

        unresolved = sum(
            result["status"] != "REBOOKED"
            for result in results
        )

        return {
            "status": "REBOOKING_COMPLETED",
            "flight_id": flight_id,
            "solver_status": solver_status,
            "total_passengers": len(
                affected_passengers
            ),
            "rebooked": rebooked,
            "unresolved": unresolved,
            "results": results,
            "feasible_options": feasible_options,
        }