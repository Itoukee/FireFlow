from domain.enums import DefaultAction, Protocol
from domain.policy.repository import PolicyRepository
from domain.rule.entity import Rule
from domain.rule.ports import CreateRule
from domain.rule.repository import RuleRepository
from domain.rule.use_cases import CreateRuleUC


def test_create_rule(mocker):
    """Testing the creation of a rule"""
    repo = mocker.Mock(spec=RuleRepository)
    policy_repo = mocker.Mock(spec=PolicyRepository)

    repo.create.return_value = Rule(
        id=0,
        policy_id=0,
        name="test_rule",
        order=0,
        source_ip="10.0.0.0",
        destination_ip="11.11.11.11",
        protocol=Protocol.ANY,
        enabled=False,
        port=None,
        action=DefaultAction.DENY,
    )

    repo.name_exists_within_parent.return_value = False

    use_case = CreateRuleUC(repo, policy_repo)
    create_policy = CreateRule(
        policy_id=0, name="test_rule", order=0, action=DefaultAction.DENY, enabled=False
    )

    rule = use_case.execute(0, 0, create_policy)

    assert rule.id == 0
    assert rule.name == "test_rule"
    assert rule.policy_id == 0
    assert rule.action == DefaultAction.DENY
