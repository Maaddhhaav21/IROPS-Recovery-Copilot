from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Flight


def get_db():
    db = SessionLocal()

    try:
        return db
    except Exception:
        db.close()
        raise


def get_flight(flight_id):
    db = get_db()

    try:
        flight = (
            db.query(Flight)
            .filter(Flight.flight_id == flight_id)
            .first()
        )

        if flight is None:
            return None

        return {
            "flight_id": flight.flight_id,
            "origin": flight.origin,
            "destination": flight.destination,
            "departure": flight.departure,
            "arrival": flight.arrival,
            "aircraft_id": flight.aircraft_id,
            "capacity": flight.capacity,
            "occupied_seats": flight.occupied_seats,
            "available_seats": flight.available_seats,
            "status": flight.status,
        }

    finally:
        db.close()


def get_alternative_flights(flight_id):
    db = get_db()

    try:
        flight = (
            db.query(Flight)
            .filter(Flight.flight_id == flight_id)
            .first()
        )

        if flight is None:
            return []

        flights = (
            db.query(Flight)
            .filter(
                Flight.origin == flight.origin,
                Flight.destination == flight.destination,
                Flight.flight_id != flight_id,
                Flight.status == "SCHEDULED",
            )
            .all()
        )

        alternatives = []

        for alternative in flights:

            if alternative.departure > flight.departure:

                alternatives.append(
                    {
                        "flight_id": alternative.flight_id,
                        "origin": alternative.origin,
                        "destination": alternative.destination,
                        "departure": alternative.departure,
                        "arrival": alternative.arrival,
                        "aircraft_id": alternative.aircraft_id,
                        "capacity": alternative.capacity,
                        "occupied_seats": alternative.occupied_seats,
                        "available_seats": alternative.available_seats,
                        "status": alternative.status,
                    }
                )

        alternatives.sort(
            key=lambda x: x["departure"]
        )

        return alternatives

    finally:
        db.close()


def get_flight_status(flight_id):
    flight = get_flight(flight_id)

    if flight is None:
        return None

    return flight["status"]