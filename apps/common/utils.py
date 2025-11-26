from datetime import datetime, time

def normalize_reservation_inputs(date_str, start_time=None, end_time=None):
    """Convert strings to date and time objects, assigning default values if missing."""
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
