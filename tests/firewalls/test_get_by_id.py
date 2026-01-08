import pytest
from datetime import datetime

from domain.firewall.entity import Firewall
from domain.firewall.repository import FirewallRepository
from domain.firewall.use_cases import GetFirewallByIdUC


def test_id_found(mocker):
    """Testing a get by id where one is found"""
    repo = mocker.Mock(spec=FirewallRepository)

    repo.get_by_id.return_value = Firewall(
        id=0,
        name="firetest",
        description="fire description",
    )

    use_case = GetFirewallByIdUC(repo)

    firewall = use_case.execute(0)

    assert firewall
    assert firewall.id == 0


def test_id_not_found(mocker):
    """Testing a get by id where none is found"""
    repo = mocker.Mock(spec=FirewallRepository)
    repo.get_by_id.return_value = None

    use_case = GetFirewallByIdUC(repo)
    firewall = use_case.execute(0)

    assert not firewall
