from domain.policy.repository import PolicyRepository
from domain.rule.use_cases import DeleteRuleByIdUC
from domain.rule.repository import RuleRepository


def test_delete(mocker):
    """Testing a delete by id where one is found"""
    repo = mocker.Mock(spec=RuleRepository)
    policy_repo = mocker.Mock(spec=PolicyRepository)

    repo.delete.return_value = True

    use_case = DeleteRuleByIdUC(repo, policy_repo)

    succeed = use_case.execute(0, 0, 0)

    assert succeed

    repo.delete.assert_called_once()
