#!/bin/bash
#
#if [ "$DATABASE" = "postgres" ]
#then
#    echo "Waiting for postgres..."
#
#    while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
#      sleep 0.1
#    done
#
#    echo "PostgreSQL started"
#fi
echo "================================ Server is starting now  =================================="

#migrations
python3 manage.py makemigrations &&
python3 manage.py migrate &&
#runners
python3 manage.py grpcrunserver --dev 0.0.0.0:50051 &
python3 manage.py runserver 0.0.0.0:8000