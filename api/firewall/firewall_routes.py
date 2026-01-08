from flask_restx import Resource
from flask import request
from pydantic import ValidationError

from api.firewall.firewall_models import (
    api,
    firewall_create_model,
    firewall_update_model,
)
from domain.firewall.use_cases import CreateFirewallUC, PaginateFirewallsUC
from domain.firewall.ports import FirewallCreate, FirewallUpdate
from infrastructure.firewall.sql_repository import FirewallSQLRepository

firewall_repo = FirewallSQLRepository()


@api.route("/<int:firewall_id>")
class Firewall(Resource):

    @api.doc("Get one by id", params={"firewall_id": "Unique identifier"})
    def get(self, firewall_id: int):
        firewall = firewall_repo.get_by_id(firewall_id)

        if not firewall:
            api.abort(404, f"Firewall with id={firewall_id} has not been found")
        else:
            return {"success": True, "data": {"firewall": firewall.to_dict()}}

    @api.doc(
        "Patch one",
        params={
            "firewall_id": "Unique identifier",
            "name": "optional",
            "description": "optional",
        },
    )
    @api.expect(firewall_update_model)
    def patch(self, firewall_id: int):
        if not api.payload or not isinstance(api.payload, dict):
            api.abort(400, "JSON body required")

        try:
            firewall_update = FirewallUpdate(**api.payload)
        except ValidationError as ve:
            return api.abort(400, ve.errors())

        try:
            firewall = firewall_repo.update(firewall_id, firewall_update)
        except ValueError as e:
            print(e)
            return api.abort(404, f"Firewall id={firewall_id} not found")
        return {"success": True, "data": {"firewall": firewall.to_dict()}}


@api.route("/")
class Firewalls(Resource):
    @api.doc(
        "Get many firewalls with pagination",
        params={"page": "target page", "limit": "maximum elements per page"},
    )
    def get(self):
        page = int(request.args.get("page", 0))
        limit = int(request.args.get("limit", 10))

        firewalls, total = PaginateFirewallsUC(firewall_repo).execute(page, limit)

        return {
            "success": True,
            "data": {
                "total_records": total,
                "firewall": [firewall.to_dict() for firewall in firewalls],
            },
        }

    @api.doc("Create")
    @api.expect(firewall_create_model)
    def post(self):
        if not api.payload or not isinstance(api.payload, dict):
            api.abort(400, "JSON body required")

        try:
            firewall_create = FirewallCreate(**api.payload)
        except ValidationError as ve:
            return api.abort(400, ve.errors())

        firewall_dict = (
            CreateFirewallUC(firewall_repo).execute(firewall_create).to_dict()
        )

        return {"success": True, "data": {"firewall": firewall_dict}}, 201
