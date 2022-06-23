#!/usr/bin/env bash
(cd website; python manage.py makemigrations; python manage.py migrate;
  python manage.py loaddata fixtures.json; python manage.py collectstatic --no-input)

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
  (cd website; python manage.py createsuperuser --no-input)
fi
(cd website; gunicorn website.wsgi:application --bind 0.0.0.0:$PORT --workers 3)