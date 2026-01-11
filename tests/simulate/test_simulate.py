from domain.enums import DefaultAction, Protocol
from domain.firewall.repository import FirewallRepository
from domain.packet.entity import Packet
from domain.packet.use_cases.simulate import SimulateFirewallUC
from tests.conftest import sample_charged_firewall


def test_rule_deny(mocker):
    """Test if the packet is denied by matching a rule from the sample firewall"""
    repo = mocker.Mock(FirewallRepository)
    repo.get_policies_and_rules.return_value = sample_charged_firewall()

    packet = Packet(
        source_ip="10.0.0.1", destination_ip="8.8.8.8", port=22, protocol=Protocol.TCP
    )

    result = SimulateFirewallUC(repo).execute(firewall_id=1, packet=packet)

    assert result.access == DefaultAction.DENY
    assert result.rule_id == 100
    assert result.policy_id == 10


def test_rule_policy_fallback(mocker):
    """Test if the packet falls into the default_action of the last policy
    from the sample firewall"""
    repo = mocker.Mock(FirewallRepository)
    repo.get_policies_and_rules.return_value = sample_charged_firewall()

    packet = Packet(
        source_ip="10.0.0.1", destination_ip="8.8.8.8", port=80, protocol=Protocol.TCP
    )

    result = SimulateFirewallUC(repo).execute(firewall_id=1, packet=packet)

    assert result.access == DefaultAction.DENY
    assert result.rule_id is None
    assert result.policy_id == 11


def test_rule_allow(mocker):
    """Test if an allowed packet is allowed by the sample firewall"""
    repo = mocker.Mock(FirewallRepository)
    repo.get_policies_and_rules.return_value = sample_charged_firewall()

    packet = Packet(
        source_ip="10.0.0.2", destination_ip="8.8.8.8", protocol=Protocol.TCP
    )

    result = SimulateFirewallUC(repo).execute(firewall_id=1, packet=packet)

    assert result.access == DefaultAction.ALLOW
    assert result.rule_id == 101
    assert result.policy_id == 10
