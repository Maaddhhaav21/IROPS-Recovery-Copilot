def get_passenger_priority(passenger):
    """
    Determine passenger priority for recovery.

    Priority:
    1 = Highest
    2 = Medium
    3 = Normal
    """

    if passenger.get("special_assistance", False):
        return 1

    if passenger.get("has_connection", False):
        return 1

    if passenger.get("priority", False):
        return 2

    return 3


def is_passenger_eligible(passenger):
    """
    Check whether a passenger can be considered
    for rebooking.
    """

    if passenger is None:
        return False

    if passenger.get("status", "ACTIVE") != "ACTIVE":
        return False

    return True