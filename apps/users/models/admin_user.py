import uuid

from sqlalchemy import Column, Boolean, String
from sqlalchemy.dialects.postgresql import UUID

from base.model import ApplicationBaseModel


class AdminUser(ApplicationBaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=True)
