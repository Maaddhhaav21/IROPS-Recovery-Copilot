from sqlalchemy import Column, Integer, String, Float
from app.database.connection import Base


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True)

    airport_code = Column(
        String,
        unique=True,
        nullable=False,
    )

    name = Column(String)
    city = Column(String)
    country = Column(String)


class AirportCapacity(Base):
    __tablename__ = "airport_capacity"

    id = Column(Integer, primary_key=True)

    airport_code = Column(String, nullable=False)
    airport_type = Column(String)

    max_daily_movements = Column(Integer)
    available_slots = Column(Integer)


class Aircraft(Base):
    __tablename__ = "aircraft"

    id = Column(Integer, primary_key=True)

    aircraft_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    aircraft_type = Column(String)
    capacity = Column(Integer)
    current_airport = Column(String)
    status = Column(String)


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True)

    flight_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    origin = Column(String)
    destination = Column(String)

    departure = Column(String)
    arrival = Column(String)

    aircraft_id = Column(String)

    capacity = Column(Integer)
    occupied_seats = Column(Integer)
    available_seats = Column(Integer)

    status = Column(String)


class FlightRotation(Base):
    __tablename__ = "flight_rotations"

    id = Column(Integer, primary_key=True)

    rotation_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    aircraft_id = Column(String)
    flight_id = Column(String)

    leg_number = Column(Integer)


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True)

    passenger_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    name = Column(String)

    flight_id = Column(String)

    origin = Column(String)
    destination = Column(String)

    passenger_type = Column(String)

    cabin = Column(String)
    fare_class = Column(String)

    special_assistance = Column(String)

    priority_level = Column(String)

    status = Column(String)


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True)

    connection_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    passenger_id = Column(String)

    first_flight_id = Column(String)
    second_flight_id = Column(String)

    connection_airport = Column(String)

    arrival_time = Column(String)
    next_departure_time = Column(String)

    connection_minutes = Column(Integer)


class Crew(Base):
    __tablename__ = "crew"

    id = Column(Integer, primary_key=True)

    crew_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    name = Column(String)

    role = Column(String)

    aircraft_type = Column(String)

    base_airport = Column(String)
    current_airport = Column(String)

    duty_hours = Column(Float)
    rest_hours = Column(Float)

    status = Column(String)


class CrewQualification(Base):
    __tablename__ = "crew_qualifications"

    id = Column(Integer, primary_key=True)

    crew_id = Column(String)

    aircraft_type = Column(String)

    qualification_level = Column(String)

    valid_until = Column(String)


class CrewAssignment(Base):
    __tablename__ = "crew_assignments"

    id = Column(Integer, primary_key=True)

    assignment_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    crew_id = Column(String)

    flight_id = Column(String)

    role = Column(String)

    status = Column(String)


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True)

    maintenance_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    aircraft_id = Column(String)

    maintenance_type = Column(String)

    status = Column(String)

    start_time = Column(String)
    end_time = Column(String)


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)

    weather_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    airport_code = Column(String)

    date = Column(String)

    condition = Column(String)

    severity = Column(String)

    visibility_km = Column(Float)

    wind_speed_kmh = Column(Float)


class Disruption(Base):
    __tablename__ = "disruptions"

    id = Column(Integer, primary_key=True)

    disruption_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    flight_id = Column(String)

    type = Column(String)

    severity = Column(String)

    status = Column(String)

    description = Column(String)