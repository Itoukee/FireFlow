# FireFlow


Description of the project

## Environnement requirements
You need a .env file that is not provided. Use the .env.example to get the keys and set your values as you need

- Python 3.13.X
- Docker and Docker compose
- `chmod +x ./entrypoint.sh`

## Local use
 - Create the migrations
    - `alembic revision -m "revision message"`
 - Run the last migration 
    - `alembic upgrade head`

## Production use

Run `docker compose up --build`