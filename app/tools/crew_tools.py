from app.database.connection import SessionLocal
from app.database.models import Crew


def get_db():
    return SessionLocal()


def load_crew():
    db = get_db()

    try:
        crew = db.query(Crew).all()

        return [
            {
                "crew_id": member.crew_id,
                "name": member.name,
                "role": member.role,
                "aircraft_type": member.aircraft_type,
                "base_airport": member.base_airport,
                "current_airport": member.current_airport,
                "duty_hours": member.duty_hours,
                "rest_hours": member.rest_hours,
                "status": member.status,
            }
            for member in crew
        ]

    finally:
        db.close()


def get_available_crew(origin):
    db = get_db()

    try:
        crew = (
            db.query(Crew)
            .filter(
                Crew.current_airport == origin,
                Crew.status == "AVAILABLE",
            )
            .all()
        )

        return [
            {
                "crew_id": member.crew_id,
                "name": member.name,
                "role": member.role,
                "aircraft_type": member.aircraft_type,
                "base_airport": member.base_airport,
                "current_airport": member.current_airport,
                "duty_hours": member.duty_hours,
                "rest_hours": member.rest_hours,
                "status": member.status,
            }
            for member in crew
        ]

    finally:
        db.close()


def get_matching_crew(origin, aircraft_type):
    crew = get_available_crew(origin)

    return [
        member
        for member in crew
        if member["aircraft_type"] == aircraft_type
    ]


def get_crew_member(crew_id):
    db = get_db()

    try:
        member = (
            db.query(Crew)
            .filter(Crew.crew_id == crew_id)
            .first()
        )

        if member is None:
            return None

        return {
            "crew_id": member.crew_id,
            "name": member.name,
            "role": member.role,
            "aircraft_type": member.aircraft_type,
            "base_airport": member.base_airport,
            "current_airport": member.current_airport,
            "duty_hours": member.duty_hours,
            "rest_hours": member.rest_hours,
            "status": member.status,
        }

    finally:
        db.close()