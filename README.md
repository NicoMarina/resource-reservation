# Resource Reservation System

## Description

This project is a backend application to manage reservations of business resources:

- Meeting rooms
- Vehicles
- Equipment

It implements a REST API using Django and Django REST Framework.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/NicoMarina/resource-reservation.git
cd resource-reservation
```

2. Set Up Virtual Environment

```bash
sudo apt update
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Testing

Run tests with:

``` bash
python manage.py test
```

### Load seeds

Load sample data with:

```bash
python -m seeds.seed_resources
python -m seeds.seed_reservations
```

This will create:

- Meeting Rooms: Room A, Room B
- Vehicles: Vehicle A, Vehicle B
- Equipment: Projector, Whiteboard
- Sample reservations covering:
  - Partial day bookings
  - Full day bookings
  - Overlapping reservations

## API Endpoints

### 1. List All Resources

Endpoint: GET /resources/

Response Example:

```json
[
    {
        "id": 1,
        "name": "Room A",
        "description": "Main meeting room",
        "type": "meeting_room",
        "attributes": {"capacity": 20},
        "image_url": "http://example.com/room_a.png"
    },
    {
        "id": 2,
        "name": "Vehicle A",
        "description": "Company car",
        "type": "vehicle",
        "attributes": {},
        "image_url": "http://example.com/vehicle_a.png"
    }
]
```

### 2. Check Resource Availability

Endpoint: GET /resources/{id}/availability/

Query Parameters (optional start_time and end_time):

- date: required, format YYYY-MM-DD
- start_time: optional, format HH:MM
- end_time: optional, format HH:MM

Example Call (cURL):

```bash
curl "http://localhost:8000/resources/1/availability/?date=2025-11-23&start_time=10:00&end_time=12:00"
```

Response Example:

```json
{
    "resource_id": 1,
    "available": true,
    "capacity_total": 20,
    "capacity_used": 10,
    "capacity_remaining": 10,
    "free_hours": [
        {"start": "08:00", "end": "10:00"},
        {"start": "12:00", "end": "14:00"},
        {"start": "16:00", "end": "20:00"}
    ],
    "blocking_reservations": [
        {
            "id": 3,
            "start_time": "10:00",
            "end_time": "12:00",
            "used_capacity": 10
        }
    ],
    "reason": null
}
```

- MeetingRoom: calculates capacity and free hourly slots.
- Vehicle: available only if no full-day reservation exists.
- Equipment: calculates free hours; can be booked by hour or full day.

### 3. Notes

- API supports query parameters (date, start_time, end_time) for testing and integration.
- The sample seeds allow immediate testing of overlapping and partial reservations.
- The system uses polymorphic models to simplify resource handling and avoid type-specific conditionals.