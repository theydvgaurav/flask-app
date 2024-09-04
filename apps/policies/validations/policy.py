from apps.policies.validations.base import PolicyBase, RemarksBase, MedicalBase


class ICICIPolicy(PolicyBase, RemarksBase):
    """"""


class MaxPolicy(PolicyBase, MedicalBase):
    """"""


class HDFCPolicy(PolicyBase, MedicalBase, RemarksBase):
    """"""

