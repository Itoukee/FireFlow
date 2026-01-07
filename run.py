from infrastructure.flask_app import create_app
from settings import settings


app = create_app()

app_base_configs = {
    "host": settings.host,
    "port": settings.port,
    "debug": settings.log_level == "DEBUG",
}

if __name__ == "__main__":
    app.run(**app_base_configs)
