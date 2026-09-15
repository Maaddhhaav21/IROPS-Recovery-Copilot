from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.graph.workflow import recovery_workflow


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
        result = recovery_workflow.invoke({
            "flight_id": request.flight_id
        })

        if result.get("briefing") is None:
            raise HTTPException(
                status_code=404,
                detail=f"No recovery plan generated for {request.flight_id}"
            )

        crew_analysis = result.get("crew_analysis", {})

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

        return {
            "flight_id": result.get("flight_id"),
            "disruption_type": result.get("disruption_type"),
            "severity": result.get("severity"),

            "affected_passengers": len(
                result.get("affected_passengers", [])
            ),

            "connecting_passengers": len(
                result.get("connecting_passengers", [])
            ),

            "solver_status": result.get(
                "solver_status"
            ),

            "rebooked": rebooked,
            "unresolved": unresolved,

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