from app.database.connection import SessionLocal
from app.database.models import Passenger, Connection


def get_db():
    return SessionLocal()


def load_passengers():
    db = get_db()

    try:
        passengers = db.query(Passenger).all()

        return [
            {
                "passenger_id": passenger.passenger_id,
                "name": passenger.name,
                "flight_id": passenger.flight_id,
                "origin": passenger.origin,
                "destination": passenger.destination,
                "passenger_type": passenger.passenger_type,
                "cabin": passenger.cabin,
                "fare_class": passenger.fare_class,
                "special_assistance": passenger.special_assistance,
                "priority_level": passenger.priority_level,
                "status": passenger.status,
            }
            for passenger in passengers
        ]

    finally:
        db.close()


def load_connections():
    db = get_db()

    try:
        connections = db.query(Connection).all()

        return [
            {
                "connection_id": connection.connection_id,
                "passenger_id": connection.passenger_id,
                "first_flight_id": connection.first_flight_id,
                "second_flight_id": connection.second_flight_id,
                "connection_airport": connection.connection_airport,
                "arrival_time": connection.arrival_time,
                "next_departure_time": connection.next_departure_time,
                "connection_minutes": connection.connection_minutes,
            }
            for connection in connections
        ]

    finally:
        db.close()


def get_affected_passengers(flight_id):
    db = get_db()

    try:
        passengers = (
            db.query(Passenger)
            .filter(Passenger.flight_id == flight_id)
            .all()
        )

        return [
            {
                "passenger_id": passenger.passenger_id,
                "name": passenger.name,
                "flight_id": passenger.flight_id,
                "origin": passenger.origin,
                "destination": passenger.destination,
                "passenger_type": passenger.passenger_type,
                "cabin": passenger.cabin,
                "fare_class": passenger.fare_class,
                "special_assistance": passenger.special_assistance,
                "priority_level": passenger.priority_level,
                "status": passenger.status,
            }
            for passenger in passengers
        ]

    finally:
        db.close()


def get_connecting_passengers(flight_id):
    db = get_db()

    try:
        connections = (
            db.query(Connection)
            .filter(Connection.first_flight_id == flight_id)
            .all()
        )

        passenger_ids = {
            connection.passenger_id
            for connection in connections
        }

        if not passenger_ids:
            return []

        passengers = (
            db.query(Passenger)
            .filter(Passenger.passenger_id.in_(passenger_ids))
            .all()
        )

        return [
            {
                "passenger_id": passenger.passenger_id,
                "name": passenger.name,
                "flight_id": passenger.flight_id,
                "origin": passenger.origin,
                "destination": passenger.destination,
                "passenger_type": passenger.passenger_type,
                "cabin": passenger.cabin,
                "fare_class": passenger.fare_class,
                "special_assistance": passenger.special_assistance,
                "priority_level": passenger.priority_level,
                "status": passenger.status,
            }
            for passenger in passengers
        ]

    finally:
        db.close()


def get_passenger_connections(passenger_id):
    db = get_db()

    try:
        connections = (
            db.query(Connection)
            .filter(Connection.passenger_id == passenger_id)
            .all()
        )

        return [
            {
                "connection_id": connection.connection_id,
                "passenger_id": connection.passenger_id,
                "first_flight_id": connection.first_flight_id,
                "second_flight_id": connection.second_flight_id,
                "connection_airport": connection.connection_airport,
                "arrival_time": connection.arrival_time,
                "next_departure_time": connection.next_departure_time,
                "connection_minutes": connection.connection_minutes,
            }
            for connection in connections
        ]

    finally:
        db.close()