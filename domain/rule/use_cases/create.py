from domain.enums import DefaultAction, Protocol
from domain.exceptions import NotFoundError
from domain.policy.repository import PolicyRepository
from domain.rule.entity import Rule
from domain.rule.ports import CreateRule
from domain.rule.repository import RuleRepository


class CreateRuleUC:
    def __init__(self, repo: RuleRepository, policy_repo: PolicyRepository) -> None:
        self.repo = repo
        self.policy_repo = policy_repo

    def execute(self, policy_id: int, create_rule: CreateRule):
        """Use case of creating the policy

        Args:
            policy_id (int)
            create_rule (CreateRule)

        Returns:
            Rule
        """

        policy = self.policy_repo.get_by_id(policy_id)
        if not policy:
            raise NotFoundError(f"The policy id={policy_id} doesn't exist")

        exists = self.repo.name_exists_within_parent(create_rule.name, policy_id)
        if exists:
            raise ValueError("Firewall with this name already exists")

        rule = Rule(
            policy_id=policy_id,
            name=create_rule.name,
            action=create_rule.action or DefaultAction.DENY,
            order=create_rule.order or 0,
            source_ip=create_rule.source_ip,
            destination_ip=create_rule.destination_ip,
            protocol=create_rule.protocol or Protocol.ANY,
            port=create_rule.port,
            enabled=create_rule.enabled,
        )

        return self.repo.create(rule)
