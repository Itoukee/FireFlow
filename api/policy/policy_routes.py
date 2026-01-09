from flask import request
from flask_restx import Resource
from pydantic import ValidationError

from api.policy.policy_models import api, policy_create_model, policy_patch_model
from domain.policy.ports import PolicyCreate, PolicyPatch
from domain.policy.use_cases import (
    CreatePolicyUC,
    PaginatePoliciesByFirewallUC,
    GetPolicyByIdUC,
    PatchPolicyUC,
    DeletePolicyByIdUC,
)
from infrastructure.policy.sql_repository import PolicySQLRepository

policy_repo = PolicySQLRepository()


@api.route("/<int:policy_id>")
class Policy(Resource):
    @api.doc("Get one by id")
    def get(self, firewall_id: int, policy_id: int):
        """Get a specific policy

        Args:
            firewall_id (int): Params
            policy_id (int): Params
        """
        if not isinstance(firewall_id, int) or not isinstance(policy_id, int):
            api.abort(400, "The firewall_id and policy_id must be an integer")
        try:
            policy = GetPolicyByIdUC(policy_repo).execute(firewall_id, policy_id)
        except ValueError as err:
            return api.abort(
                404,
                str(err),
            )
        if not policy:
            return api.abort(404, f"Policy id={policy_id} not found")

        return {"success": True, "data": {"policy": policy.to_dict()}}

    @api.doc("Patch a policy")
    @api.expect(policy_patch_model)
    def patch(self, firewall_id: int, policy_id: int):
        """Patch a policy
        Args:
            firewall_id (int): Params
        """
        if not isinstance(firewall_id, int) or not isinstance(policy_id, int):
            api.abort(400, "The firewall_id and policy_id must be an integer")
        if not api.payload or not isinstance(api.payload, dict):
            api.abort(400, "JSON body required")

        try:
            policy_patch = PolicyPatch(**api.payload)
        except ValidationError as ve:
            return api.abort(400, ve.errors())

        try:
            policy = PatchPolicyUC(policy_repo).execute(
                policy_id, firewall_id, policy_patch
            )
        except ValueError:
            return api.abort(404, f"Policy id={policy_id} not found")
        return {"success": True, "data": {"policy": policy.to_dict()}}

    def delete(self, firewall_id: int, policy_id: int):
        """Delete one
        Args:
            firewall_id (int): Params
        """
        if not isinstance(firewall_id, int) or not isinstance(policy_id, int):
            api.abort(400, "The firewall_id and policy_id must be an integer")
        try:
            DeletePolicyByIdUC(policy_repo).execute(firewall_id, policy_id)
        except ValueError as value_err:
            api.abort(404, str(value_err))
        return "", 204


@api.route("/")
class Policies(Resource):

    @api.doc(
        "Paginate policies by firewall_id",
        params={"page": "target page", "limit": "maximum elements per page"},
    )
    def get(self, firewall_id: int):
        """Paginates the policies of a firewall"""
        page = int(request.args.get("page", 0))
        limit = int(request.args.get("limit", 10))

        policies, total_records = PaginatePoliciesByFirewallUC(policy_repo).execute(
            firewall_id, page, limit
        )

        return {
            "success": True,
            "data": {
                "total_records": total_records,
                "policies": [policy.to_dict() for policy in policies],
            },
        }

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
            policy = CreatePolicyUC(policy_repo).execute(firewall_id, policy_create)

        except ValueError:
            return api.abort(
                404,
                f"The firewall id={firewall_id} related was not found. Couldn't create the policy.",
            )

        return {
            "success": True,
            "data": {"policy": policy.to_dict()},
        }, 201
