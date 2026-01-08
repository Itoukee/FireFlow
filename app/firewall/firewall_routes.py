from flask_restx import Resource
from pydantic import ValidationError

from app.firewall.firewall_models import (
    api,
    firewall_create_model,
)
from domain.firewall.use_cases.create import CreateFirewallUC
from domain.firewall.ports import FirewallCreate
from infrastructure.firewall.sql_repository import FirewallSQLRepository

firewall_repo = FirewallSQLRepository()


@api.route("/")
class Firewall(Resource):
    @api.doc("Get all")
    def get(self):
        return

    @api.doc("Create")
    @api.expect(firewall_create_model)
    def post(self):
        if not api.payload or not isinstance(api.payload, dict):
            api.abort(400, "JSON body required")

        try:
            firewall_create = FirewallCreate(**api.payload)
        except ValidationError as ve:
            api.abort(400, ve.errors())

        firewall_dict = (
            CreateFirewallUC(firewall_repo).execute(firewall_create).to_dict()
        )

        print(firewall_dict)
        return {"success": True, "data": {"firewall": firewall_dict}}, 201
