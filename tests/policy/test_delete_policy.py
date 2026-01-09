from domain.policy.repository import PolicyRepository
from domain.policy.use_cases import DeletePolicyByIdUC


def test_delete(mocker):
    """Testing a delete by id where one is found"""
    repo = mocker.Mock(spec=PolicyRepository)

    repo.delete.return_value = True

    use_case = DeletePolicyByIdUC(repo)

    succeed = use_case.execute(0, 0)

    assert succeed

    repo.delete.assert_called_once()
