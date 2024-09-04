import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from base.model import ApplicationBaseModel


class Comments(ApplicationBaseModel):
    __tablename__ = 'comments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String(200), nullable=False)
    policy_id = Column(UUID(as_uuid=True), ForeignKey('policies.id'), nullable=True)
    comment_by = Column(UUID(as_uuid=True), ForeignKey('admin_user.id'), nullable=True)
