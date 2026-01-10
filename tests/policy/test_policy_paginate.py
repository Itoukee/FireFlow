from domain.enums import DefaultAction
from domain.policy.entity import Policy
from domain.policy.repository import PolicyRepository
from domain.policy.use_cases import PaginatePoliciesByFirewallUC


def test_paginate_empty(mocker):
    """
    Testing the pagination
    With no policies
    """
    repo = mocker.Mock(spec=PolicyRepository)
    repo.paginate_by_firewall.return_value = ([], 0)

    use_case = PaginatePoliciesByFirewallUC(repo)

    policies, total_records = use_case.execute(0, 1, 15)

    assert policies == []
    assert total_records == 0

    repo.paginate_by_firewall.assert_called_once()


def test_paginate(mocker):
    """
    Testing the pagination
    With more policies than we should return
    """
    policies = [
        Policy(
            id=i,
            name=f"policy_{i}",
            firewall_id=0,
            default_action=DefaultAction.ALLOW,
            priority=0,
        )
        for i in range(50)
    ]
    repo = mocker.Mock(spec=PolicyRepository)

    def fake_paginate(firewall_id: int, page: int, limit: int):
        """
        We fake the pagination algorithm here, using the same method
        """
        start = page * limit
        end = start + limit

        return list(
            filter(lambda x: x.firewall_id == firewall_id, policies[start:end])
        ), len(policies)

    repo.paginate_by_firewall.side_effect = fake_paginate

    use_case = PaginatePoliciesByFirewallUC(repo)

    items, total_records = use_case.execute(firewall_id=0, page=0, limit=15)

    assert items[0].id == 0
    assert items[-1].id == 14
    assert len(items) == 15

    items, total_records = use_case.execute(firewall_id=0, page=1, limit=10)
    assert len(items) == 10
    assert items[0].id == 10
    assert items[-1].id == 19

    assert total_records == 50

    assert repo.paginate_by_firewall.call_count == 2
