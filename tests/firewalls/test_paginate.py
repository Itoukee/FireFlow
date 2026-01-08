from domain.firewall.entity import Firewall
from domain.firewall.repository import FirewallRepository
from domain.firewall.use_cases import PaginateFirewallsUC


def test_paginate_empty(mocker):
    """
    Testing the pagination
    With no firewalls
    """
    repo = mocker.Mock(spec=FirewallRepository)
    repo.paginate.return_value = ([], 0)

    use_case = PaginateFirewallsUC(repo)

    firewalls, total_records = use_case.execute(1, 15)

    assert firewalls == []
    assert total_records == 0

    repo.paginate.assert_called_once()


def test_paginate(mocker):
    """
    Testing the pagination
    With more firewalls than we should return
    """
    firewalls = [Firewall(id=i, name=f"fw_{i}", description="") for i in range(50)]
    repo = mocker.Mock(spec=FirewallRepository)

    def fake_paginate(page, limit):
        """
        We fake the pagination algorithm here, using the same method
        """
        start = page * limit
        end = start + limit
        return firewalls[start:end], len(firewalls)

    repo.paginate.side_effect = fake_paginate

    use_case = PaginateFirewallsUC(repo)

    items, total_records = use_case.execute(page=0, limit=15)

    assert items[0].id == 0
    assert items[-1].id == 14
    assert len(items) == 15

    items, total_records = use_case.execute(page=1, limit=10)
    assert len(items) == 10
    assert items[0].id == 10
    assert items[-1].id == 19

    assert total_records == 50

    assert repo.paginate.call_count == 2
