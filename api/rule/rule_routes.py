from flask import request
from flask_restx import Resource
from pydantic import ValidationError

from api.rule.rule_model import api, rule_create_model, rule_patch_model
from domain.exceptions import NotFoundError
from domain.rule.ports import CreateRule, PatchRule
from domain.rule.use_cases import (
    PaginateRulesByPolicyUC,
    CreateRuleUC,
    GetRuleByIdUC,
    PatchRuleUC,
    DeleteRuleByIdUC,
)

from infrastructure.policy.sql_repository import PolicySQLRepository
from infrastructure.rule.sql_repository import RuleSQLRepository

rule_repo = RuleSQLRepository()
policy_repo = PolicySQLRepository()


@api.route("/<int:rule_id>")
class RuleResource(Resource):
    @api.doc("Get one by id")
    def get(self, firewall_id: int, policy_id: int, rule_id: int):
        """Get a specific rule

        Args:
            firewall_id (int): Params
            policy_id (int): Params
        """
        if (
            not isinstance(firewall_id, int)
            or not isinstance(policy_id, int)
            or not isinstance(rule_id, int)
        ):
            api.abort(400, "The ids must be an integer")
        try:
            rule = GetRuleByIdUC(rule_repo, policy_repo).execute(
                rule_id=rule_id, policy_id=policy_id
            )
        except NotFoundError as err:
            return api.abort(404, err)

        if not rule:
            return api.abort(404, f"Rule id={rule_id} not found")

        return {"success": True, "data": {"rule": rule.to_dict()}}

    @api.doc("Patch a rule")
    @api.expect(rule_patch_model)
    def patch(self, firewall_id: int, policy_id: int, rule_id: int):
        """Patch a rule
        Args:
            firewall_id (int): Params
            policy_id (int): Params
            rule_id (int): Params
        """
        if (
            not isinstance(firewall_id, int)
            or not isinstance(policy_id, int)
            or not isinstance(rule_id, int)
        ):
            api.abort(400, "The ids must be an integer")
        if not api.payload or not isinstance(api.payload, dict):
            api.abort(400, "JSON body required")

        try:
            rule_patch = PatchRule(**api.payload)
        except ValidationError as ve:
            return api.abort(400, ve.errors())

        try:
            rule = PatchRuleUC(rule_repo, policy_repo).execute(
                rule_id, policy_id, rule_patch
            )
        except NotFoundError as ne:
            return api.abort(404, ne)
        return {"success": True, "data": {"rule": rule.to_dict()}}

    def delete(self, firewall_id: int, policy_id: int, rule_id: int):
        """Delete one
        Args:
            firewall_id (int): Params
            policy_id (int): Params
            rule_id (int): Params
        """
        if (
            not isinstance(firewall_id, int)
            or not isinstance(policy_id, int)
            or not isinstance(rule_id, int)
        ):
            api.abort(400, "The ids must be an integer")
        try:
            DeleteRuleByIdUC(rule_repo, policy_repo).execute(rule_id, policy_id)
        except NotFoundError as ne:
            api.abort(404, ne)
        return "", 204


@api.route("/")
class RulesResource(Resource):

    @api.doc(
        "Paginate rules of a policy from a firewall",
        params={"page": "target page", "limit": "maximum elements per page"},
    )
    def get(self, firewall_id: int, policy_id: int):
        """Paginate the rules given a specific policy_id"""
        if not isinstance(policy_id, int) or not isinstance(firewall_id, int):
            api.abort(400, "The firewall_id and policy_id must be an integer")

        page = int(request.args.get("page", 0))
        limit = int(request.args.get("limit", 10))

        rules, total_records = PaginateRulesByPolicyUC(rule_repo).execute(
            policy_id, page, limit
        )

        return {
            "success": True,
            "data": {
                "total_records": total_records,
                "rules": [rule.to_dict() for rule in rules],
            },
        }

    @api.expect(rule_create_model)
    def post(self, firewall_id: int, policy_id: int):
        """Create a new policy rule"""

        if not isinstance(policy_id, int) or not isinstance(firewall_id, int):
            api.abort(400, "The firewall_id and policy_id must be an integer")

        try:
            create_rule = CreateRule(**api.payload, policy_id=policy_id)
        except ValidationError as ve:
            return api.abort(400, ve.errors())

        try:
            rule = CreateRuleUC(rule_repo, policy_repo).execute(policy_id, create_rule)
        except NotFoundError as ne:
            return api.abort(404, ne)

        return {"success": True, "data": {"rule": rule.to_dict()}}, 201
