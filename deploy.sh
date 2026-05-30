#!/bin/bash
# Serverga o'rnatish skripti
set -e

echo "=== Izhor Platform — O'rnatish ==="

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py seed_categories
python manage.py collectstatic --noinput

echo ""
echo "Superuser yaratish:"
python manage.py createsuperuser

echo ""
echo "=== Tayyor! Ishga tushirish: ==="
echo "source venv/bin/activate"
echo "python manage.py runserver 0.0.0.0:8000"
