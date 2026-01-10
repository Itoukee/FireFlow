from domain.enums import DefaultAction, Protocol
from domain.policy.repository import PolicyRepository
from domain.rule.entity import Rule
from domain.rule.repository import RuleRepository
from domain.rule.use_cases import GetRuleByIdUC


def test_id_found(mocker):
    """Testing a get by id where one is found"""
    repo = mocker.Mock(spec=RuleRepository)
    policy_repo = mocker.Mock(spec=PolicyRepository)

    repo.get_by_id.return_value = Rule(
        id=0,
        policy_id=0,
        name="test_rule",
        order=0,
        source_ip="10.0.0.0",
        destination_ip="11.11.11.11",
        enabled=False,
        port=None,
        protocol=Protocol.ANY,
        action=DefaultAction.DENY,
    )

    use_case = GetRuleByIdUC(repo, policy_repo)

    rule = use_case.execute(0, 0)

    assert rule
    assert rule.id == 0
    assert rule.policy_id == 0

    repo.get_by_id.assert_called_once()


def test_id_not_found(mocker):
    """Testing a get by id where none is found"""
    repo = mocker.Mock(spec=RuleRepository)
    repo.get_by_id.return_value = None

    policy_repo = mocker.Mock(spec=RuleRepository)

    use_case = GetRuleByIdUC(repo, policy_repo)
    rule = use_case.execute(0, 1)

    assert not rule

    repo.get_by_id.assert_called_once()
