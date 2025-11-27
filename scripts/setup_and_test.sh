#!/bin/bash
set -e

echo "=== Starting setup and test script ==="

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate authtoken
python manage.py migrate

# Run tests
python manage.py test

# Seeds, sample data
echo "Loading sample data..."
python -m seeds.seed_users
python -m seeds.seed_resources
python -m seeds.seed_reservations

echo "=== Setup and tests completed successfully ==="

# Run server
python manage.py runserver