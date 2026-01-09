from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import mapped_column, Mapped

from domain.policy.entity import DefaultAction
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
    name = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
