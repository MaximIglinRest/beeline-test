from sqlalchemy.orm import configure_mappers

from .base import Base
from .events import Event
from .users import User
from .users_events import UserEventRegistration

configure_mappers()
