from flask_restx import Resource
from pydantic import ValidationError
from api.simulate.simulate_models import api, simulate_post
from domain.packet.entity import Packet
from domain.packet.use_cases.simulate import SimulateFirewallUC
from infrastructure.firewall.sql_repository import FirewallSQLRepository


firewall_repo = FirewallSQLRepository()


@api.route("/simulate/<int:firewall_id>")
class Simulate(Resource):
    @api.expect(simulate_post)
    def post(self, firewall_id: int):
        """Simulate a firewall with a packet"""
        if not isinstance(firewall_id, int):
            return api.abort(400, "The firewall id must be an integer", success=False)
        try:
            packet = Packet(**api.payload)
        except ValidationError as ve:
            return api.abort(400, ve.errors(), success=False)

        out = SimulateFirewallUC(firewall_repo).execute(packet, firewall_id)

        return {"success": True, "data": out.model_dump()}
