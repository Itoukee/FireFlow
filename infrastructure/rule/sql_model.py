from datetime import datetime, timezone
from sqlalchemy import Boolean, ForeignKey, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from domain.enums import DefaultAction, Protocol
from infrastructure.databases.sql import Base
from infrastructure.policy.sql_model import PolicyModel


class RuleModel(Base):
    __tablename__ = "rules"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, unique=True)
    policy_id = mapped_column(
        Integer, ForeignKey("policies.id", ondelete="CASCADE"), nullable=False
    )
    action = mapped_column(SqlEnum(DefaultAction), nullable=False)
    order = mapped_column(Integer, nullable=False)
    source_ip = mapped_column(String, nullable=True)
    destination_ip = mapped_column(String, nullable=True)
    port = mapped_column(Integer, nullable=True)
    protocol = mapped_column(SqlEnum(Protocol), nullable=True)
    enabled = mapped_column(Boolean, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    policy: Mapped[PolicyModel] = relationship("PolicyModel", back_populates="rules")
