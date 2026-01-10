from domain.enums import DefaultAction, Protocol
from domain.rule.entity import Rule
from domain.rule.repository import RuleRepository
from domain.rule.use_cases import PaginateRulesByPolicyUC


def test_paginate_empty(mocker):
    """
    Testing the pagination
    With no rules
    """
    repo = mocker.Mock(spec=RuleRepository)

    repo.paginate_by_policy.return_value = ([], 0)

    use_case = PaginateRulesByPolicyUC(repo)

    rules, total_records = use_case.execute(0, 1, 15)

    assert rules == []
    assert total_records == 0

    repo.paginate_by_policy.assert_called_once()


def test_paginate(mocker):
    """
    Testing the pagination
    With more rules than we should return
    """
    rules = [
        Rule(
            id=i,
            policy_id=0,
            name=f"{i}_rule",
            order=i,
            source_ip="10.0.0.0",
            destination_ip="11.11.11.11",
            enabled=False,
            port=None,
            protocol=Protocol.ANY,
            action=DefaultAction.DENY,
        )
        for i in range(50)
    ]
    repo = mocker.Mock(spec=RuleRepository)

    def fake_paginate(policy_id: int, page: int, limit: int):
        """
        We fake the pagination algorithm here, using the same method
        """
        start = page * limit
        end = start + limit

        return list(filter(lambda x: x.policy_id == policy_id, rules[start:end])), len(
            rules
        )

    repo.paginate_by_policy.side_effect = fake_paginate

    use_case = PaginateRulesByPolicyUC(repo)

    items, total_records = use_case.execute(policy_id=0, page=0, limit=15)

    assert items[0].id == 0
    assert items[-1].id == 14
    assert len(items) == 15

    items, total_records = use_case.execute(policy_id=0, page=1, limit=10)
    assert len(items) == 10
    assert items[0].id == 10
    assert items[-1].id == 19

    assert total_records == 50

    assert repo.paginate_by_policy.call_count == 2
