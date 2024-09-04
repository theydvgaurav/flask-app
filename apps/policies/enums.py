from enum import Enum


class PolicyStatus(str, Enum):
    REQUIREMENTS_AWAITED = "requirements_awaited"
    REQUIREMENTS_CLOSED = "requirements_closed"
    UNDERWRITING = "underwriting"
    POLICY_ISSUED = "policy_issued"
    POLICY_REJECTED = "policy_rejected"


class MedicalType(str, Enum):
    TELE_MEDICALS = "tele_medicals"
    PHYSICAL_MEDICALS = "physical_medicals"


class MedicalStatus(str, Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    WAITING_FOR_REPORT = "waiting_for_report"
    DONE = "done"


class PolicyType(str, Enum):
    HDFC_LIFE = 'hdfc_life'
    ICICI_LIFE = 'icici_life'
    MAX_LIFE = 'max_life'
