#!/bin/bash

# Apply migrations
python manage.py migrate

# Optional: Create a superuser non-interactively
# (only if you set env vars for DJANGO_SUPERUSER_USERNAME etc.)
python manage.py createsuperuser --noinput || true

# Start the ASGI server
daphne EnviroVista_dep.asgi:application --bind 0.0.0.0 --port 8000
