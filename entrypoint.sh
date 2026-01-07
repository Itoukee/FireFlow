#!/bin/sh
set -e

: "${WORKERS:=2}"
: "${HOST:=0.0.0.0}"
: "${PORT:=8080}"

echo "Starting Gunicorn with $WORKERS workers on $HOST:$PORT"

exec gunicorn -w "$WORKERS" -b "$HOST:$PORT" wsgi:app
