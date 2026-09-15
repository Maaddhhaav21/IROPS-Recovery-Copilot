MIN_REST_HOURS = 10
MAX_DUTY_HOURS = 14


def is_crew_available(crew_member):
    return crew_member.get("status") == "AVAILABLE"


def is_aircraft_qualified(crew_member, aircraft_type):
    return (
        crew_member.get("aircraft_type")
        == aircraft_type
    )


def has_sufficient_rest(crew_member):
    return (
        float(crew_member.get("rest_hours", 0))
        >= MIN_REST_HOURS
    )


def is_within_duty_limit(crew_member):
    return (
        float(crew_member.get("duty_hours", 0))
        <= MAX_DUTY_HOURS
    )


def is_crew_eligible(
    crew_member,
    aircraft_type,
):
    if not is_crew_available(crew_member):
        return False

    if not is_aircraft_qualified(
        crew_member,
        aircraft_type,
    ):
        return False

    if not has_sufficient_rest(crew_member):
        return False

    if not is_within_duty_limit(
        crew_member
    ):
        return False

    return True