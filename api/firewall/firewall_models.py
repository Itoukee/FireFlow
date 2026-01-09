from flask_restx import Namespace, fields


api = Namespace("firewalls", description="Firewalls operations")


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

# Firewall udpate model
firewall_update_model = api.model(
    "FirewallUpdate",
    {
        "name": fields.String(
            required=False, description="The firewall name", min_length=3
        ),
        "description": fields.String(
            required=False, description="The firewall description"
        ),
    },
)

# Firewall pagination model
firewall_paginate = api.model(
    "FirewallPaginate",
    {
        "page": fields.Integer(required=True, description="The current page"),
        "limit": fields.Integer(required=True, description="The current page"),
    },
)
