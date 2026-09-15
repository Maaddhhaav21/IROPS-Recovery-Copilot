import pandas as pd

from app.tools.flight_tools import get_alternative_flights
from app.optimization.model import optimize_rebooking


class RebookingAgent:

    def analyze(self, flight_id, affected_passengers):

        alternatives = get_alternative_flights(flight_id)

        if not alternatives:
            return {
                "status": "NO_ALTERNATIVES",
                "flight_id": flight_id,
                "results": [],
                "solver_status": "NO_SOLUTION",
                "feasible_options": {},
            }

        # The optimizer currently expects pandas DataFrames.
        affected_df = pd.DataFrame(affected_passengers)
        alternatives_df = pd.DataFrame(alternatives)

        # Make sure the flight time columns are datetime values.
        alternatives_df["departure"] = pd.to_datetime(
            alternatives_df["departure"]
        )
        alternatives_df["arrival"] = pd.to_datetime(
            alternatives_df["arrival"]
        )

        results, feasible_options, solver_status = optimize_rebooking(
            affected_df,
            alternatives_df,
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
            "total_passengers": len(affected_passengers),
            "rebooked": rebooked,
            "unresolved": unresolved,
            "results": results,
            "feasible_options": feasible_options,
        }