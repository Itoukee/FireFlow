from datetime import datetime, timezone
from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from infrastructure.databases.sql import Base


class FirewallModel(Base):
    __tablename__ = "firewalls"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, unique=True)
    description = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    policies = relationship(
        "PolicyModel", cascade="all, delete-orphan", back_populates="firewall"
    )

    __table_args__ = (Index("idx_firewall_name", "name"),)
