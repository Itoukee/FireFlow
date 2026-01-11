from flask_restx import Namespace, fields

from domain.enums import Protocol


api = Namespace("simulate", description="Simulate a firewall response")


# Simulation test
simulate_post = api.model(
    "SimulatePost",
    {
        "source_ip": fields.String(
            required=False,
            description="Source ip of the request",
            example="0.0.0.0",
        ),
        "destination_ip": fields.String(
            required=False,
            description="Destination ip of the request",
            example="10.10.10.22",
        ),
        "port": fields.Integer(required=False, description="Target port", example=80),
        "protocol": fields.String(
            enum=[e.value for e in Protocol],
            required=False,
            description="Request protocol",
        ),
    },
)
