import uuid

from sqlalchemy import Column, Date, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Base


class Event(Base):
    """Модель мероприятия"""

    __tablename__ = "event"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(
        String(300),
        nullable=False,
    )
    description = Column(
        Text,
        nullable=False,
    )
    date = Column(Date, nullable=False)
    event_registrations = relationship(
        "UserEventRegistration",
        uselist=True,
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    def __repr__(self):
        return f"<Event {self.id}: Name {self.name}>"
