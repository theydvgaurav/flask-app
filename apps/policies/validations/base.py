import re
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr

from apps.policies.enums import PolicyStatus, MedicalStatus, MedicalType


class PolicyBase(BaseModel):
    application_number: str = Field(alias="applicationNumber")
    customer_name: str = Field(alias="customerName", max_length=100)
    email: EmailStr = Field(alias="email")
    phone_number: str = Field(alias="phoneNumber")
    date_of_birth: str = Field(alias="dateOfBirth")
    policy_cover: int = Field(alias="policyCover", ge=2500000, le=10000000)
    policy_status: PolicyStatus = Field(alias="policyStatus")
    policy_number: Optional[str] = Field(alias="policyNumber")

    @field_validator('application_number')
    def alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9]*$', v):
            raise ValueError('Application Number must be alphanumeric')
        return v

    @field_validator('phone_number')
    def valid_indian_phone_number(cls, v):
        if not re.match(r'^[6789]\d{9}$', v):
            raise ValueError(
                'phone_number must be a valid Indian phone number starting with 6, 7, 8, or 9 and 10 digits long')
        return v

    @model_validator(mode='before')
    def check_policy_number(cls, values):
        policy_status = values.get('policyStatus')
        policy_number = values.get('policyNumber')

        if policy_status == PolicyStatus.POLICY_ISSUED:
            if not policy_number:
                raise ValueError('policy_number is required when status is "Policy Issued"')
            if not re.match(r'^[a-zA-Z0-9]*$', policy_number):
                raise ValueError('policy_number must be alphanumeric')
        return values

    @field_validator('date_of_birth')
    def valid_dob(cls, v):
        try:
            dob = datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('date_of_birth must be in yyyy-mm-dd format')

        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age <= 18 or age >= 99:
            raise ValueError('Age must be between 18 and 99 years')
        return v


class MedicalBase(BaseModel):
    medical_type: MedicalType = Field(alias="medicalType")
    medical_status: MedicalStatus = Field(alias="medicalStatus")


class RemarksBase(BaseModel):
    remarks: str = Field(alias="remarks", min_length=1, max_length=200)


class UpdateExistingPolicy(BaseModel):
    customer_name: Optional[str] = Field(default=None, alias="customerName", max_length=100)
    email: Optional[EmailStr] = Field(default=None, alias="email")
    phone_number: Optional[str] = Field(default=None, alias="phoneNumber")
    date_of_birth: Optional[str] = Field(default=None, alias="dateOfBirth")
    policy_cover: Optional[int] = Field(default=None, alias="policyCover", ge=2500000, le=10000000)
    policy_status: Optional[PolicyStatus] = Field(default=None, alias="policyStatus")
    policy_number: Optional[str] = Field(default=None, alias="policyNumber")
    medical_type: Optional[MedicalType] = Field(default=None, alias="medicalType")
    medical_status: Optional[MedicalStatus] = Field(default=None, alias="medicalStatus")
    remarks: Optional[str] = Field(default=None, alias="remarks", min_length=1, max_length=200)

    @model_validator(mode='before')
    def check_policy_number(cls, values):
        policy_status = values.get('policyStatus')
        policy_number = values.get('policyNumber')

        if policy_status == PolicyStatus.POLICY_ISSUED:
            if not policy_number:
                raise ValueError('policy_number is required when status is "Policy Issued"')
            if not re.match(r'^[a-zA-Z0-9]*$', policy_number):
                raise ValueError('policy_number must be alphanumeric')
        return values
