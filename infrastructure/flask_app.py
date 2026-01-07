from flask import Flask
from flask_restx import Api


def create_app():
    app = Flask(__name__)
    api = Api(
        app,
        version="1.0",
        title="Sample API",
        description="Fireflow API, made to handle firewalls, policies and rules",
    )

    """ from .controllers.hello_controller import ns as hello_namespace

    api.add_namespace(hello_namespace)
    """
    return app
