from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from dreimire import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    budgets: so.WriteOnlyMapped["Budget"] = so.relationship(back_populates="owner")

    def __repr__(self):
        return "<User {}>".format(self.username)


class Budget(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(500))
    amount: so.Mapped[int]
    period: so.Mapped[str] = so.mapped_column(sa.String(64), default="P1M")
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    owner: so.Mapped[User] = so.relationship(back_populates="budgets")

    def __repr__(self):
        return "<Budget {}, owner={}>".format(self.name, self.owner.username)
