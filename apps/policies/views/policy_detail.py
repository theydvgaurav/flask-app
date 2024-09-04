from apps.policies.enums import PolicyStatus
from apps.policies.models import Policy
from apps.policies.utils import send_policy_creation_email
from apps.policies.validations.base import UpdateExistingPolicy
from base.exception_handler.base_exception import APIException
from base.views.base import BaseView
from databases.extensions import db
from middlewares.auth_middleware import require_admin_authentication


class PolicyDetailAPIView(BaseView):

    @staticmethod
    def get_policy_or_404(policy_id):
        policy = Policy.query.filter_by(id=policy_id, is_active=True).first()
        if not policy:
            raise APIException("Resource not found!", 404)
        return policy

    @require_admin_authentication
    def get(self, admin_user, policy_id, *args, **kwargs):
        policy = self.get_policy_or_404(policy_id)
        return self.get_response(policy.to_dict())

    @require_admin_authentication
    def delete(self, admin_user, policy_id, *args, **kwargs):
        policy = self.get_policy_or_404(policy_id)
        policy.is_active = False
        policy.updated_by = admin_user.id
        db.session.commit()
        return self.get_response({})

    @require_admin_authentication
    def patch(self, admin_user, policy_id, *args, **kwargs):
        data = self.request_data
        validated_data = self.get_validated_data(validation_class=UpdateExistingPolicy, data=data, exclude_none=True)
        Policy.query.filter_by(id=policy_id, is_active=True).update(validated_data)
        db.session.commit()
        if validated_data.get("policy_status") == PolicyStatus.POLICY_ISSUED:
            policy = Policy.query.filter_by(id=policy_id, is_active=True).first()
            send_policy_creation_email.delay(policy=policy.to_dict())
        return self.get_response({})
