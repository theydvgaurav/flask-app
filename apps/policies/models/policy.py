import uuid

from sqlalchemy import Column, String, Integer, Enum, Date, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from apps.policies.enums import PolicyStatus, MedicalType, MedicalStatus
from base.model import ApplicationBaseModel


class Policy(ApplicationBaseModel):
    __tablename__ = 'policies'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_number = Column(String(100), nullable=False, unique=True)
    customer_name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    phone_number = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    policy_cover = Column(Integer, nullable=False)
    policy_status = Column(Enum(PolicyStatus), nullable=False)
    policy_number = Column(String(100), unique=True, nullable=True)
    medical_type = Column(Enum(MedicalType), nullable=True)
    medical_status = Column(Enum(MedicalStatus), nullable=True)
    remarks = Column(String(200), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('admin_user.id'), nullable=True)
    is_active = Column(Boolean, default=True)
