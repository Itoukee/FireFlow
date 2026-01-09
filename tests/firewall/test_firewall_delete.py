from domain.firewall.repository import FirewallRepository
from domain.firewall.use_cases import DeleteFirewallUC


def test_delete(mocker):
    """Testing a delete by id where one is found"""
    repo = mocker.Mock(spec=FirewallRepository)

    repo.delete.return_value = True

    use_case = DeleteFirewallUC(repo)

    succeed = use_case.execute(0)

    assert succeed

    repo.delete.assert_called_once()
    # TODO test, the cascade
