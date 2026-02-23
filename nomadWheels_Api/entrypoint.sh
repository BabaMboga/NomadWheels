#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for running database as postgres"

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Database is up and running 😏"
fi

python manage.py migrate

exec "$@"