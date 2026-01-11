import ipaddress
from typing import Optional

from domain.enums import DefaultAction, Protocol
from domain.firewall.ports import ChargedPolicy
from domain.firewall.repository import FirewallRepository
from domain.exceptions import NotFoundError
from domain.packet.entity import Packet
from domain.packet.ports import PacketAnswer


class SimulateFirewallUC:
    """
    Simulates granting access or not from a packet to a destination
    """

    def __init__(self, firewall_repo: FirewallRepository) -> None:
        self.firewall_repo = firewall_repo

    def __ip_matches(self, packet_ip: str, rule_ip: Optional[str] = None):
        """Check if the packet ip (source / destination ) matches the rule
        if the rule is set to None then we pass

        Args:
            packet_ip (str)
            rule_ip (str)
        """
        if not rule_ip:
            return True
        return ipaddress.ip_address(packet_ip) == ipaddress.ip_address(rule_ip)

    def __protocol_mactches(
        self, rule_protocol: Protocol, packet_protocol: Protocol
    ) -> bool:
        """If the rule protocol is any we don't check more
        Args:
            rule_protocol (Protocol)
            packet_protocol (Protocol)

        Returns:
            bool
        """
        return rule_protocol == Protocol.ANY or rule_protocol == packet_protocol

    def __field_matches(self, rule_value, packet_value) -> bool:
        """If the rule value is None then we pass. Else check the equality

        Args:
            rule_value (_type_)
            packet_value (_type_)

        Returns:
            bool
        """
        return not rule_value or rule_value == packet_value

    def __check_policy_rules(
        self, policy: ChargedPolicy, packet: Packet
    ) -> PacketAnswer | None:
        """Parse the policy rules and look for a match

        Args:
            policy (ChargedPolicy)
            packet (Packet)

        Returns:
            PacketAnswer | None
        """
        for rule in filter(lambda x: x.enabled, policy.rules):
            out = PacketAnswer(
                access=rule.action, rule_id=rule.id, policy_id=rule.policy_id
            )

            if (
                self.__protocol_mactches(rule.protocol, packet.protocol)
                and self.__field_matches(rule.port, packet.port)
                and self.__ip_matches(packet.source_ip, rule.source_ip)
                and self.__ip_matches(packet.destination_ip, rule.destination_ip)
            ):
                return out

    def execute(self, packet: Packet, firewall_id: int):
        """Executes the simulation with a specific firewall, policies and rules
        Args:
            packet (Packet)
            firewall_id (int)

        Raises:
            NotFoundError
        """

        out = PacketAnswer(
            access=DefaultAction.DENY,
            reason="No rule matched, therefore deny is applied",
        )

        charged_firewall = self.firewall_repo.get_policies_and_rules(firewall_id)
        if not charged_firewall:
            raise NotFoundError(
                f"The firewall id={firewall_id} to simulate does not exist"
            )

        for policy in charged_firewall.policies:
            rule_match = self.__check_policy_rules(policy, packet)
            if rule_match:
                return rule_match

            if policy.default_action == DefaultAction.DENY:
                out.reason = (
                    f"Default action of the policy {policy.name}"
                    + "applied since no rules matched."
                )
                out.policy_id = policy.id
                return out

        return out
