import pytest

from domain.policy.entity import DefaultAction, Policy
from domain.policy.repository import PolicyRepository
from domain.policy.use_cases import GetPolicyByIdUC


def test_id_found(mocker):
    """Testing a get by id where one is found"""
    repo = mocker.Mock(spec=PolicyRepository)

    repo.get_by_id.return_value = Policy(
        id=0,
        name="policy",
        firewall_id=0,
        default_action=DefaultAction.ALLOW,
        priority=0,
    )

    use_case = GetPolicyByIdUC(repo)

    policy = use_case.execute(0, 0)

    assert policy
    assert policy.id == 0
    assert policy.firewall_id == 0

    repo.get_by_id.assert_called_once()


def test_id_not_found(mocker):
    """Testing a get by id where none is found"""
    repo = mocker.Mock(spec=PolicyRepository)
    repo.get_by_id.return_value = None

    use_case = GetPolicyByIdUC(repo)
    policy = use_case.execute(0, 1)

    assert not policy

    repo.get_by_id.assert_called_once()


def test_policy_forbidden(mocker):
    """Test that you can't access to the policy of another firewall"""
    repo = mocker.Mock(spec=PolicyRepository)
    repo.get_by_id.return_value = Policy(
        id=0,
        name="policy",
        firewall_id=0,
        default_action=DefaultAction.ALLOW,
        priority=0,
    )

    use_case = GetPolicyByIdUC(repo)
    with pytest.raises(ValueError, match="Policy does not belong to this Firewall"):
        use_case.execute(firewall_id=15, policy_id=0)

    repo.get_by_id.assert_called_once()
