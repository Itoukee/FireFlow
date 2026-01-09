from domain.firewall.repository import FirewallRepository
from domain.firewall.use_cases import DeleteFirewallUC
from domain.policy.entity import DefaultAction
from infrastructure.firewall.sql_model import FirewallModel
from infrastructure.policy.sql_model import PolicyModel


def test_delete(mocker):
    """Testing a delete by id where one is found"""
    repo = mocker.Mock(spec=FirewallRepository)

    repo.delete.return_value = True

    use_case = DeleteFirewallUC(repo)

    succeed = use_case.execute(0)

    assert succeed

    repo.delete.assert_called_once()


def test_delete_cascade_policies(db_session):
    """Integration test

    Here we test that when the firewall is deleted, its related policies are too
    """
    firewall = FirewallModel(name="firetest", description="")

    db_session.add(firewall)
    db_session.commit()

    policies = [
        PolicyModel(
            name=f"policy_{i}",
            default_action=DefaultAction.DENY,
            priority=0,
            firewall_id=firewall.id,
        )
        for i in range(5)
    ]

    db_session.add_all(policies)
    db_session.commit()

    db_session.delete(firewall)
    db_session.commit()

    assert db_session.query(FirewallModel).filter_by(id=firewall.id).first() is None
    assert db_session.query(PolicyModel).count() == 0
