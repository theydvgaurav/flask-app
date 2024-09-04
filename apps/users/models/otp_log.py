import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from base.model import ApplicationBaseModel


class OTPLog(ApplicationBaseModel):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(120), nullable=False)
    otp = Column(String(6), nullable=False)
    expires_at = Column(DateTime, default=datetime.utcnow)
