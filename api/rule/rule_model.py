from flask_restx import Namespace, fields

from domain.enums import DefaultAction, Protocol


api = Namespace(
    "rules",
    path="/firewalls/<int:firewall_id>/policies/<int:policy_id>/rules",
    description="Rules management",
)


# Rule creation input
rule_create_model = api.model(
    "RuleCreate",
    {
        "name": fields.String(required=True, description="Rule name", min_length=3),
        "action": fields.String(
            required=False,
            enum=[e.value for e in DefaultAction],
            description="Rule action if it matches",
        ),
        "order": fields.Integer(
            required=False, description="Execution order (Ascending)", example=0
        ),
        "source_ip": fields.String(
            required=False, description="Source ip of the request", example="0.0.0.0"
        ),
        "dest_ip": fields.String(
            required=False,
            description="Destination ip of the request",
            example="0.0.0.0",
        ),
        "port": fields.Integer(required=False, description="Target port", example=80),
        "protocol": fields.String(
            enum=[e.value for e in Protocol],
            required=False,
            description="Request protocol",
        ),
        "enabled": fields.Boolean(
            required=False, description="Enable the rule", example=True
        ),
    },
)

# Rule patch model
rule_patch_model = api.model(
    "RulePatch",
    {
        "name": fields.String(required=False, description="Rule name", min_length=3),
        "action": fields.String(
            required=False,
            enum=[e.value for e in DefaultAction],
            description="Rule action if it matches",
        ),
        "order": fields.Integer(
            required=False, description="Execution order (Ascending)", example=0
        ),
        "source_ip": fields.String(
            required=False, description="Source ip of the request", example="0.0.0.0"
        ),
        "destination_ip": fields.String(
            required=False,
            description="Destination ip of the request",
            example="0.0.0.0",
        ),
        "port": fields.Integer(required=False, description="Target port", example=80),
        "protocol": fields.String(
            enum=[e.value for e in Protocol],
            required=False,
            description="Request protocol",
        ),
        "enabled": fields.Boolean(
            required=False, description="Enable the rule", example=True
        ),
    },
)
