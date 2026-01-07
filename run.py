from infrastructure.flask_app import create_app
from settings import settings


app_base_configs = {
    "host": settings.host,
    "port": settings.ports,
    "workers": settings.workers,
    "access_log": True,
    "reload": True,
}


app = create_app()

if __name__ == "__main__":
    app.run()
