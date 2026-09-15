MIN_CONNECTION_TIME = 60


def calculate_connection_minutes(
    alternative_arrival,
    next_departure,
):
    """
    Calculate available connection time in minutes.
    """

    difference = next_departure - alternative_arrival

    return int(
        difference.total_seconds() / 60
    )


def is_connection_feasible(
    alternative_arrival,
    next_departure,
):
    """
    Check whether minimum connection time
    is satisfied.
    """

    connection_minutes = calculate_connection_minutes(
        alternative_arrival,
        next_departure,
    )

    return connection_minutes >= MIN_CONNECTION_TIME


def get_connection_status(
    alternative_arrival,
    next_departure,
):
    """
    Return connection feasibility and
    available connection time.
    """

    connection_minutes = calculate_connection_minutes(
        alternative_arrival,
        next_departure,
    )

    if connection_minutes < 0:
        return {
            "valid": False,
            "reason": "Connecting flight already departed",
            "connection_minutes": connection_minutes,
        }

    if connection_minutes < MIN_CONNECTION_TIME:
        return {
            "valid": False,
            "reason": "Insufficient connection time",
            "connection_minutes": connection_minutes,
        }

    return {
        "valid": True,
        "reason": "Connection time is sufficient",
        "connection_minutes": connection_minutes,
    }