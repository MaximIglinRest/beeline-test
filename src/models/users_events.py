import uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from models import Base


class UserEventRegistration(Base):
    """Модель ригистрации пользователя на мероприятие"""

    __tablename__ = "user_event_registration"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    event_id = Column(
        UUID(as_uuid=True),
        ForeignKey("event.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    UniqueConstraint("user_id", "event_id", name="unique_user_event")

    def __repr__(self):
        return f"<Registration {self.id}: User {self.user_id} Event: {self.event_id}>"
