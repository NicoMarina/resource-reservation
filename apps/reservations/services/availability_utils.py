from datetime import datetime, time


def overlaps(a_start, a_end, b_start, b_end):
    """Check if two time intervals overlap."""
    return not (a_end <= b_start or a_start >= b_end)


def calculate_free_hours(reservations, opening_time, closing_time):
    """
    Calculate free hourly slots given booked slots and operating hours.
    Reservations must have start_time and end_time defined.
    """
    if not reservations:
        return [{"start": opening_time, "end": closing_time}]

    intervals = sorted(
        [(r.start_time, r.end_time) for r in reservations], key=lambda x: x[0]
    )
    free_hours = []
    cursor = opening_time

    for start, end in intervals:
        if start > cursor:
            free_hours.append({"start": cursor, "end": start})
        cursor = max(cursor, end)

    if cursor < closing_time:
        free_hours.append({"start": cursor, "end": closing_time})

    return free_hours


def normalize_reservation_inputs(date_str, start_time=None, end_time=None):
    """Convierte strings a objetos date y time, asignando valores por defecto si faltan."""
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    default_start = time(8, 0)
    default_end = time(20, 0)

    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%H:%M").time()
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%H:%M").time()

    start_time = start_time or default_start
    end_time = end_time or default_end

    return date, start_time, end_time
