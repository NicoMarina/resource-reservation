from datetime import datetime, time


def overlaps(a_start, a_end, b_start, b_end):
    """Check if two time intervals overlap."""
    if not a_start or not a_end or not b_start or not b_end:
        return False
    return a_start < b_end and b_start < a_end


def calculate_free_hours(reservations, opening_time, closing_time):
    """
    Calculate free hourly slots given booked slots and operating hours.
    Only approved reservations are considered as blocking.
    """
    # Keep only approved reservations
    approved = [r for r in reservations if r.status == "approved"]

    if not approved:
        return [
            {
                "start": opening_time.strftime("%H:%M"),
                "end": closing_time.strftime("%H:%M"),
            }
        ]

    # Sort intervals by start time
    intervals = sorted(
        [(r.start_time, r.end_time) for r in approved], key=lambda x: x[0]
    )
    free_hours = []
    cursor = opening_time

    for start, end in intervals:
        if start > cursor:
            free_hours.append({"start": cursor, "end": start})
        cursor = max(cursor, end)

    if cursor < closing_time:
        free_hours.append({"start": cursor, "end": closing_time})

    # Format times as strings
    for slot in free_hours:
        slot["start"] = slot["start"].strftime("%H:%M")
        slot["end"] = slot["end"].strftime("%H:%M")

    return free_hours


def sum_used_capacity(reservations, start_time, end_time):
    """Sum used capacity of reservations overlapping with given time interval."""
    total = 0
    for r in reservations:
        if r.status == "approved" and overlaps(
            r.start_time, r.end_time, start_time, end_time
        ):
            total += getattr(r, "used_capacity", 1)
    return total


def serialize_blocking_reservations(reservations, include_capacity=False):
    serialized = []

    for r in reservations:
        base = {
            "id": r.id,
            "date": r.date.isoformat() if r.date else None,
            "start_time": (
                r.start_time.strftime("%H:%M")
                if getattr(r, "start_time", None)
                else None
            ),
            "end_time": (
                r.end_time.strftime("%H:%M") if getattr(r, "end_time", None) else None
            ),
            "status": getattr(r, "status", None),
            "created_by": getattr(r.created_by, "username", None),
            "approved_by": getattr(r.approved_by, "username", None),
        }
        if include_capacity:
            base["used_capacity"] = getattr(r, "used_capacity", 1)
        serialized.append(base)

    return serialized


def get_reservations_info(reservations, resource, start_time=None, end_time=None):
    include_capacity = getattr(resource, "allow_shared_capacity", lambda: False)()

    approved = [r for r in reservations if r.status == "approved"]
    pending = [r for r in reservations if r.status == "pending"]

    if start_time and end_time:
        approved = [
            r
            for r in approved
            if overlaps(r.start_time, r.end_time, start_time, end_time)
        ]
        pending = [
            r
            for r in pending
            if overlaps(r.start_time, r.end_time, start_time, end_time)
        ]

    return {
        "blocking_reservations": serialize_blocking_reservations(
            approved, include_capacity
        ),
        "pending_reservations": serialize_blocking_reservations(
            pending, include_capacity
        ),
    }
