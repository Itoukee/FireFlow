from domain.enums import DefaultAction
from domain.firewall.repository import FirewallRepository
from domain.policy.entity import Policy
from domain.policy.repository import PolicyRepository
from domain.policy.use_cases import GetPolicyByIdUC


def test_id_found(mocker):
    """Testing a get by id where one is found"""
    repo = mocker.Mock(spec=PolicyRepository)
    firewall_repo = mocker.Mock(spec=FirewallRepository)

    repo.get_by_id.return_value = Policy(
        id=0,
        name="policy",
        firewall_id=0,
        default_action=DefaultAction.ALLOW,
        priority=0,
    )

    use_case = GetPolicyByIdUC(repo, firewall_repo)

    policy = use_case.execute(0, 0)

    assert policy
    assert policy.id == 0
    assert policy.firewall_id == 0

    repo.get_by_id.assert_called_once()


def test_id_not_found(mocker):
    """Testing a get by id where none is found"""
    repo = mocker.Mock(spec=PolicyRepository)
    repo.get_by_id.return_value = None

    firewall_repo = mocker.Mock(spec=FirewallRepository)

    use_case = GetPolicyByIdUC(repo, firewall_repo)
    policy = use_case.execute(0, 1)

    assert not policy

    repo.get_by_id.assert_called_once()
