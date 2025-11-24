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
python -m seed.seed_resources
```
