from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime, timezone

from infrastructure.databases import Base


class FirewallModel(Base):
    __tablename__ = "firewalls"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
