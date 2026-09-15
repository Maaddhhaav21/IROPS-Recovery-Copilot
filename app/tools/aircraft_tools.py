from app.database.connection import SessionLocal
from app.database.models import Aircraft


def get_db():
    return SessionLocal()


def load_aircraft():
    db = get_db()

    try:
        aircraft = db.query(Aircraft).all()

        return [
            {
                "aircraft_id": item.aircraft_id,
                "aircraft_type": item.aircraft_type,
                "capacity": item.capacity,
                "current_airport": item.current_airport,
                "status": item.status,
            }
            for item in aircraft
        ]

    finally:
        db.close()


def get_aircraft(aircraft_id):
    db = get_db()

    try:
        aircraft = (
            db.query(Aircraft)
            .filter(Aircraft.aircraft_id == aircraft_id)
            .first()
        )

        if aircraft is None:
            return None

        return {
            "aircraft_id": aircraft.aircraft_id,
            "aircraft_type": aircraft.aircraft_type,
            "capacity": aircraft.capacity,
            "current_airport": aircraft.current_airport,
            "status": aircraft.status,
        }

    finally:
        db.close()


def get_aircraft_type(aircraft_id):
    aircraft = get_aircraft(aircraft_id)

    if aircraft is None:
        return None

    return aircraft["aircraft_type"]


def get_aircraft_capacity(aircraft_id):
    aircraft = get_aircraft(aircraft_id)

    if aircraft is None:
        return None

    return int(aircraft["capacity"])