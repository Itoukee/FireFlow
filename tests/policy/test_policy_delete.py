from domain.enums import DefaultAction, Protocol
from domain.firewall.repository import FirewallRepository
from domain.policy.repository import PolicyRepository
from domain.policy.use_cases import DeletePolicyByIdUC
from infrastructure.policy.sql_model import PolicyModel
from infrastructure.rule.sql_model import RuleModel


def test_delete(mocker):
    """Testing a delete by id where one is found"""
    repo = mocker.Mock(spec=PolicyRepository)
    firewall_repo = mocker.Mock(spec=FirewallRepository)

    repo.delete.return_value = True

    use_case = DeletePolicyByIdUC(repo, firewall_repo)

    succeed = use_case.execute(0, 0)

    assert succeed

    repo.delete.assert_called_once()


def test_delete_cascade_rules(db_session):
    """Integration test

    Here we test that when the policy is deleted, its related rules are too
    """
    policy = PolicyModel(
        name="policy_test",
        default_action=DefaultAction.DENY,
        priority=0,
        firewall_id=0,
    )

    db_session.add(policy)
    db_session.commit()

    rules = [
        RuleModel(
            id=i,
            policy_id=policy.id,
            name=f"rule_{i}",
            order=0,
            source_ip="10.0.0.0",
            destination_ip="11.11.11.11",
            protocol=Protocol.ANY,
            enabled=False,
            port=None,
            action=DefaultAction.DENY,
        )
        for i in range(5)
    ]

    db_session.add_all(rules)
    db_session.commit()

    db_session.delete(policy)
    db_session.commit()

    assert db_session.query(PolicyModel).filter_by(id=policy.id).first() is None
    assert db_session.query(RuleModel).count() == 0
