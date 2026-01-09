from domain.firewall.entity import Firewall
from domain.firewall.repository import FirewallRepository
from domain.firewall.use_cases import UpdateFirewallUC
from domain.firewall.ports import FirewallPatch


def test_upd_found(mocker):
    """Testing an update by id where one is found"""
    repo = mocker.Mock(spec=FirewallRepository)

    repo.update.return_value = Firewall(
        id=0,
        name="firetest",
        description="",
    )

    use_case = UpdateFirewallUC(repo)
    firewall_update = FirewallPatch(name="fire", description="")

    assert firewall_update.name == "fire"
    assert firewall_update.description == ""

    firewall = use_case.execute(0, firewall_update)

    assert firewall
    assert firewall.id == 0
    assert firewall.description == ""

    repo.update.assert_called_once()
