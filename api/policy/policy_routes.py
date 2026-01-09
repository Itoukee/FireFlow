from flask_restx import Resource
from pydantic import ValidationError

from api.policy.policy_models import api, policy_create_model
from domain.policy.ports import PolicyCreate
from domain.policy.use_cases.create import CreatePolicyUC
from infrastructure.policy.sql_repository import PolicySQLRepository

repo = PolicySQLRepository()


@api.route("/")
class Policies(Resource):
    @api.doc("Create")
    @api.expect(policy_create_model)
    def post(self, firewall_id: int):
        """Creates a policy given a firewall id"""

        if not api.payload or not isinstance(api.payload, dict):
            api.abort(400, "JSON body required")

        try:
            policy_create = PolicyCreate(**api.payload, firewall_id=firewall_id)
        except ValidationError as ve:
            return api.abort(400, ve.errors())

        try:
            policy = CreatePolicyUC(repo).execute(firewall_id, policy_create)

        except ValueError:
            return api.abort(
                404,
                f"The firewall id={firewall_id} related was not found. Couldn't create the policy.",
            )

        return {
            "success": True,
            "data": {"policy": policy.to_dict()},
        }, 201
