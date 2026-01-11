from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Index, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from domain.enums import DefaultAction
from infrastructure.databases.sql import Base


class PolicyModel(Base):
    __tablename__ = "policies"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, unique=True)
    firewall_id = mapped_column(
        Integer, ForeignKey("firewalls.id", ondelete="CASCADE"), nullable=False
    )
    default_action = mapped_column(SqlEnum(DefaultAction), nullable=False)
    priority = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    firewall = relationship("FirewallModel", back_populates="policies")
    rules = relationship(
        "RuleModel", cascade="all, delete-orphan", back_populates="policy"
    )
    __table_args__ = (
        Index("idx_policy_firewall", "firewall_id"),
        Index("idx_policy_name_per_firewall", "name"),
    )
