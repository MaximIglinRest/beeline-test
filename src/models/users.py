import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Base


class User(Base):
    """Модель пользователя"""

    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(300), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    event_registrations = relationship(
        "UserEventRegistration",
        uselist=True,
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    def __repr__(self):
        return f"<User {self.id}: Name {self.name}>"
