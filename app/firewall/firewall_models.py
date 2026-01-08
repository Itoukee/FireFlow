from flask_restx import Namespace, fields


api = Namespace("firewalls", description="Firewalls operations")

# Flask API Models here, for ensuring the input


# Firewall creation input
firewall_create_model = api.model(
    "FirewallCreate",
    {
        "name": fields.String(
            required=True, description="The firewall name", min_length=3
        ),
        "description": fields.String(
            required=False, description="The firewall description"
        ),
    },
)
