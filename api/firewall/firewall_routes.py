from flask_restx import Resource
from flask import request
from pydantic import ValidationError

from api.firewall.firewall_models import (
    api,
    firewall_create_model,
    firewall_patch_model,
)
from domain.exceptions import NotFoundError
from domain.firewall.use_cases import (
    CreateFirewallUC,
    PaginateFirewallsUC,
    PatchFirewallUC,
    GetFirewallByIdUC,
    DeleteFirewallUC,
)
from domain.firewall.ports import FirewallCreate, FirewallPatch
from infrastructure.firewall.sql_repository import FirewallSQLRepository

firewall_repo = FirewallSQLRepository()


@api.route("/<int:firewall_id>")
class FirewallResource(Resource):

    @api.doc("Get one by id", params={"firewall_id": "Unique identifier"})
    def get(self, firewall_id: int):
        """Get one
        Args:
            firewall_id (int): Params
        """
        firewall = GetFirewallByIdUC(firewall_repo).execute(firewall_id)

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
    @api.doc("Patch a given firewall by id")
    @api.expect(firewall_patch_model)
    def patch(self, firewall_id: int):
        """Patch one
        Args:
            firewall_id (int): Params
        """
        if not isinstance(firewall_id, int):
            api.abort(400, "The id must be an integer")
        if not api.payload or not isinstance(api.payload, dict):
            api.abort(400, "JSON body required")

        try:
            firewall_update = FirewallPatch(**api.payload)
        except ValidationError as ve:
            return api.abort(400, ve.errors())

        try:
            firewall = PatchFirewallUC(firewall_repo).execute(
                firewall_id, firewall_update
            )
        except NotFoundError as ne:
            return api.abort(404, ne)
        return {"success": True, "data": {"firewall": firewall.to_dict()}}

    @api.doc("Delete a firewall by id")
    def delete(self, firewall_id: int):
        """Delete one
        Args:
            firewall_id (int): Params
        """
        if not isinstance(firewall_id, int):
            api.abort(400, "The id must be an integer")
        try:
            DeleteFirewallUC(firewall_repo).execute(firewall_id)
        except NotFoundError as ne:
            api.abort(404, ne)
        return "", 204


@api.route("/")
class FirewallsResource(Resource):
    @api.doc(
        "Get many firewalls with pagination",
        params={"page": "target page", "limit": "maximum elements per page"},
    )
    def get(self):
        """Paginate the firewalls"""
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
        """Creates a firewall
        Args : Body {name:str,description:Optional[str]}
        """
        if not api.payload or not isinstance(api.payload, dict):
            api.abort(400, "JSON body required")

        try:
            firewall_create = FirewallCreate(**api.payload)
        except ValidationError as ve:
            return api.abort(400, ve.errors())

        try:
            firewall = CreateFirewallUC(firewall_repo).execute(firewall_create)
        except ValueError as ve:
            return api.abort(400, str(ve))

        return {"success": True, "data": {"firewall": firewall.to_dict()}}, 201
