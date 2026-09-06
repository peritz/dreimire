from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from dreimire import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    budgets: so.WriteOnlyMapped["Budget"] = so.relationship(back_populates="owner")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
