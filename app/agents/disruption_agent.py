from app.database.connection import SessionLocal
from app.database.models import Disruption


class DisruptionAgent:

    def analyze(self, flight_id):
        db = SessionLocal()

        try:
            disruption = (
                db.query(Disruption)
                .filter(Disruption.flight_id == flight_id)
                .first()
            )

            if disruption is None:
                return {
                    "status": "NO_DISRUPTION",
                    "flight_id": flight_id,
                }

            return {
                "status": "DISRUPTION_FOUND",
                "flight_id": flight_id,
                "disruption_type": disruption.type,
                "severity": disruption.severity,
                "disruption_status": disruption.status,
                "description": disruption.description,
            }

        finally:
            db.close()