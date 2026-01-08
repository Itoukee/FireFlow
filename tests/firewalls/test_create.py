from datetime import datetime

from domain.firewall.entity import Firewall
from domain.firewall.repository import FirewallRepository
from domain.firewall.use_cases import CreateFirewallUC
from domain.firewall.ports import FirewallCreate


def test_create_firewall(mocker):
    """Testing the creation of a firewall"""
    repo = mocker.Mock(spec=FirewallRepository)

    repo.create.return_value = Firewall(
        id=0,
        name="firetest",
        description="fire description",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    use_case = CreateFirewallUC(repo)
    create_firewall = FirewallCreate(name="firetest", description="fire description")

    firewall = use_case.execute(create_firewall)

    assert firewall.id == 0
    assert firewall.name == "firetest"
    assert firewall.description == "fire description"
