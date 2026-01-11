from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from domain.enums import DefaultAction, Protocol
from domain.firewall.ports import ChargedFirewall, ChargedPolicy
from domain.rule.entity import Rule
from infrastructure.databases.sql import Base


@fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    session = Session(engine)

    yield session

    session.close()


def sample_charged_firewall():
    return ChargedFirewall(
        id=1,
        name="Firewall test",
        description="",
        policies=[
            ChargedPolicy(
                id=10,
                name="Policy1",
                default_action=DefaultAction.ALLOW,
                priority=0,
                rules=[
                    Rule(
                        id=100,
                        policy_id=10,
                        name="Rule100",
                        order=0,
                        action=DefaultAction.DENY,
                        protocol=Protocol.TCP,
                        source_ip="10.0.0.1",
                        destination_ip=None,
                        port=22,
                        enabled=True,
                    ),
                    Rule(
                        id=101,
                        policy_id=10,
                        name="Rule101",
                        order=1,
                        action=DefaultAction.ALLOW,
                        protocol=Protocol.ANY,
                        source_ip="10.0.0.2",
                        destination_ip=None,
                        port=None,
                        enabled=True,
                    ),
                ],
            ),
            ChargedPolicy(
                id=11,
                name="Policy2",
                default_action="DENY",
                priority=1,
                rules=[
                    Rule(
                        id=102,
                        policy_id=11,
                        name="Rule102",
                        order=0,
                        action=DefaultAction.ALLOW,
                        protocol=Protocol.UDP,
                        source_ip=None,
                        destination_ip=None,
                        port=53,
                        enabled=True,
                    )
                ],
            ),
        ],
    )
