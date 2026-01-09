from domain.rule.entity import Rule
from domain.rule.ports import PatchRule
from domain.rule.repository import RuleRepository
from infrastructure.rule.sql_model import RuleModel
from infrastructure.databases.sql import get_database_session


class RuleSQLRepository(RuleRepository):
    def __init__(self) -> None:
        self.session = get_database_session()

    def __to_entity(self, item: RuleModel) -> Rule:
        """Maps the Sql model to the business entity"""
        return Rule(
            id=item.id,
            policy_id=item.policy_id,
            name=item.name,
            action=item.action,
            order=item.order,
            source_ip=item.source_ip,
            destination_ip=item.destination_ip,
            protocol=item.protocl,
            port=item.port,
            enabled=item.enabled,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

    def __patch_item(self, row: RuleModel, upd: PatchRule):
        for key, value in upd.model_dump(exclude_unset=True).items():
            setattr(row, key, value)
        return row

    def create(self, rule: Rule) -> Rule:
        """Creates a new rule associated to a policy

        Args:

            rule (Rule)

        Returns:
            rule
        """

        row = RuleModel(
            policy_id=rule.policy_id,
            name=rule.name,
            action=rule.action,
            order=rule.order,
            source_ip=rule.source_ip,
            destination_ip=rule.destination_ip,
            protocol=rule.protocol,
            port=rule.port,
            enabled=rule.enabled,
        )
        self.session.add(row)
        self.session.commit()

        rule.id = row.id
        rule.created_at = row.created_at.now()
        rule.updated_at = row.updated_at.now()

        return rule

    def paginate_by_policy(
        self, policy_id: int, page: int, limit: int
    ) -> tuple[list[Rule], int]:
        """
        Returns a list of rules with the total count of records
        Uses pagination for optimization

        Args:
            page (int)
            limit (int)

        Returns:
            tuple[list[Rule], int]
        """
        query = self.session.query(RuleModel).filter_by(policy_id=policy_id)
        total_records = query.count()

        # Starts at page 0
        items = query.offset(page * limit).limit(limit).all()

        policies = [self.__to_entity(item) for item in items]

        return policies, total_records

    def get_by_id(self, rule_id: int) -> Rule | None:
        """Gets a rule by id

        Args:
            rule_id: unique id

        Returns:
            Rule | None
        """
        row = self.session.query(RuleModel).filter_by(id=rule_id).first()

        if row:
            return self.__to_entity(row)
        return None

    def patch(self, rule_id: int, upd: PatchRule):
        """Patches a rule

        Args:
            rule_id (int): unique id
            upd (PolicyPatch): potential attributes to update

        Raises:
            ValueError: If not found

        Returns:
            Rule: the patched row
        """
        row = self.session.query(RuleModel).filter_by(id=rule_id).first()
        if not row:
            raise ValueError(f"The rule id={rule_id} to update was not found")

        row = self.__patch_item(row, upd)

        self.session.commit()
        self.session.refresh(row)

        return self.__to_entity(row)

    def delete(self, rule_id: int) -> bool:
        """Delete a rule

        Args:
            rule_id (int): unique id

        Raises:
            ValueError: If not found

        Returns:
            bool: True | error raised
        """
        row = self.session.query(RuleModel).filter_by(id=rule_id).first()
        if not row:
            raise ValueError(f"The rule id={rule_id} to delete was not found")

        self.session.delete(row)
        self.session.commit()

        return True
