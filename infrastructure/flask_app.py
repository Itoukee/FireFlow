from flask import Flask
from flask_restx import Api
from api.firewall.firewall_routes import api as firewall_ns
from api.policy.policy_routes import api as policy_ns
from api.rule.rule_routes import api as rule_ns


def create_app():
    app = Flask(__name__)
    api = Api(
        app,
        version="1.0",
        title="Sample API",
        description="Fireflow API, made to handle firewalls, policies and rules",
    )
    api.add_namespace(firewall_ns)
    api.add_namespace(policy_ns)
    api.add_namespace(rule_ns)

    return app
