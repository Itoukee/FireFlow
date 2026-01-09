from datetime import datetime

from domain.policy.entity import DefaultAction, Policy
from domain.policy.repository import PolicyRepository
from domain.policy.use_cases import CreatePolicyUC
from domain.policy.ports import PolicyCreate


def test_create_policy(mocker):
    """Testing the creation of a policy"""
    repo = mocker.Mock(spec=PolicyRepository)

    repo.create.return_value = Policy(
        id=0,
        firewall_id=0,
        name="test_policy",
        priority=0,
        default_action=DefaultAction.DENY,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    use_case = CreatePolicyUC(repo)
    create_policy = PolicyCreate(
        firewall_id=0, name="test_policy", priority=0, default_action=DefaultAction.DENY
    )

    policy = use_case.execute(0, create_policy)

    assert policy.id == 0
    assert policy.name == "test_policy"
    assert policy.firewall_id == 0
    assert policy.default_action == DefaultAction.DENY
