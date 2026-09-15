from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.graph.workflow import recovery_workflow
from app.tools.flight_tools import get_alternative_flights


router = APIRouter()


class RecoveryRequest(BaseModel):
    flight_id: str


@router.get("/")
def home():
    return {
        "status": "IROPS Recovery Copilot API is running"
    }


@router.post("/recover")
def recover_flight(request: RecoveryRequest):

    try:
        flight_id = request.flight_id.strip().upper()

        if not flight_id:
            raise HTTPException(
                status_code=422,
                detail="Flight ID cannot be empty"
            )

        # Run the complete recovery workflow
        result = recovery_workflow.invoke(
            {
                "flight_id": flight_id
            }
        )

        # Check whether a disruption was found
        if result.get("disruption_type") is None:
            raise HTTPException(
                status_code=404,
                detail=f"No disruption found for {flight_id}"
            )

        # --------------------------------------------------
        # PASSENGER RECOVERY RESULTS
        # --------------------------------------------------

        rebooking_results = result.get(
            "rebooking_results",
            []
        )

        rebooked = sum(
            item.get("status") == "REBOOKED"
            for item in rebooking_results
        )

        unresolved = sum(
            item.get("status") != "REBOOKED"
            for item in rebooking_results
        )

        # --------------------------------------------------
        # ALTERNATIVE FLIGHTS
        # --------------------------------------------------

        alternatives = get_alternative_flights(
            flight_id
        )

        alternative_flights = []

        for flight in alternatives:

            alternative_flights.append(
                {
                    "flight_id": str(
                        flight["flight_id"]
                    ),
                    "origin": str(
                        flight["origin"]
                    ),
                    "destination": str(
                        flight["destination"]
                    ),
                    "departure": str(
                        flight["departure"]
                    ),
                    "arrival": str(
                        flight["arrival"]
                    ),
                    "available_seats": int(
                        flight["available_seats"]
                    ),
                    "capacity": int(
                        flight["capacity"]
                    ),
                    "status": str(
                        flight["status"]
                    ),
                }
            )

        # --------------------------------------------------
        # CREW
        # --------------------------------------------------

        crew_analysis = result.get(
            "crew_analysis",
            {}
        )

        # --------------------------------------------------
        # FINAL API RESPONSE
        # --------------------------------------------------

        return {

            "flight_id": result.get(
                "flight_id"
            ),

            "disruption_type": result.get(
                "disruption_type"
            ),

            "severity": result.get(
                "severity"
            ),

            "disruption_status": result.get(
                "disruption_status"
            ),

            # Passenger summary
            "affected_passengers": len(
                result.get(
                    "affected_passengers",
                    []
                )
            ),

            "connecting_passengers": len(
                result.get(
                    "connecting_passengers",
                    []
                )
            ),

            "solver_status": result.get(
                "solver_status"
            ),

            "rebooked": rebooked,

            "unresolved": unresolved,

            # --------------------------------------------------
            # INDIVIDUAL PASSENGER RECOVERY
            # --------------------------------------------------

            "passenger_recovery": rebooking_results,

            # --------------------------------------------------
            # ALTERNATIVE FLIGHTS
            # --------------------------------------------------

            "alternative_flights": alternative_flights,

            # --------------------------------------------------
            # CREW
            # --------------------------------------------------

            "crew": {
                "aircraft_type": crew_analysis.get(
                    "aircraft_type"
                ),
                "available_crew": len(
                    crew_analysis.get(
                        "available_crew",
                        []
                    )
                ),
                "matching_crew": len(
                    crew_analysis.get(
                        "matching_crew",
                        []
                    )
                ),
            },

            # --------------------------------------------------
            # AI BRIEFING
            # --------------------------------------------------

            "briefing": result.get(
                "briefing"
            ),
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )