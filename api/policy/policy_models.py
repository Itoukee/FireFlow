from flask_restx import Namespace, fields

from domain.enums import DefaultAction


api = Namespace(
    "policies",
    path="/firewalls/<int:firewall_id>/policies",
    description="Policies operations",
)


# Policy creation input
policy_create_model = api.model(
    "PolicyCreate",
    {
        "name": fields.String(
            required=True, description="The policy name", min_length=3
        ),
        "default_action": fields.String(
            required=False,
            enum=[e.value for e in DefaultAction],
            description="Policy default action when no rule matches",
        ),
        "priority": fields.Integer(
            required=False, description="Priority (Ascending order)", example=0
        ),
    },
)

# Policy patch model
policy_patch_model = api.model(
    "PolicyPatch",
    {
        "name": fields.String(
            required=False, description="The policy name", min_length=3
        ),
        "default_action": fields.String(
            required=False,
            enum=[e.value for e in DefaultAction],
            description="Policy default action when no rule matches",
        ),
        "priority": fields.Integer(
            required=False, description="Priority (Ascending order)", example=0
        ),
    },
)
