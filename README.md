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
python -m seeds.seed_users
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
- Sample users:
  - Worker: worker1 / workerpass
  - Manager: manager1 / managerpass
- Token-based authentication for API testing.

## API Endpoints

### 1. List All Resources

GET /resources/

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

GET /resources/{id}/availability/

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
    "pending_reservations": [],
    "reason": null
}
```

- MeetingRoom → shows hourly free slots and remaining capacity.
- Vehicle → only available if no reservation exists for the day.
- Equipment → shows hourly availability or full-day booking.

### 3. Create a Reservation

POST /api/resources/{id}/reservations/

Request body examples:

MeetingRoom (hourly, shared capacity):

```json
{
  "date": "2025-11-23",
  "start_time": "11:00",
  "end_time": "12:00",
  "used_capacity": 5
}
```

Vehicle (full day):

```json
{
  "date": "2025-11-23"
}
```

Equipment (hourly or full day):

```json
{
  "date": "2025-11-23",
  "start_time": "11:00",
  "end_time": "12:00"
}
```

Notes:

- Validation is based on availability and resource type.
- Pending reservations are created if the user role cannot auto-approve.
- Response includes the created reservation or ValidationError with reason and conflicting reservations.

Authentication: All requests require token-based authentication. Include in header

```text
Authorization: Token <USER_TOKEN>
```

### 4. User Testing & Roles

Sample users created via seeds:

| Role    | Username | Password    | Token (example)   |
| ------- | -------- | ----------- | ----------------- |
| Worker  | worker1  | workerpass  | `<WORKER_TOKEN>`  |
| Manager | manager1 | managerpass | `<MANAGER_TOKEN>` |

- In Postman, define environment variables for WORKER_TOKEN and MANAGER_TOKEN and use {{WORKER_TOKEN}} in the Authorization header. This way, you only need to change the value once for the collection.
- Ensures that scenarios like overlapping reservations or capacity limits can be tested consistently.

### 5. Postman Testing

- Import the included Postman collection to test all scenarios.
- Use environment variables for tokens to simplify role switching.
