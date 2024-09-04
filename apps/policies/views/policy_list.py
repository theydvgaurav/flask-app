from datetime import datetime

from flask import request
from sqlalchemy import extract

from apps.policies.enums import PolicyStatus
from apps.policies.models.policy import Policy
from apps.policies.validations.policy import HDFCPolicy, ICICIPolicy, MaxPolicy
from base.exception_handler.base_exception import APIException
from base.views.base import BaseView
from databases.extensions import db
from middlewares.auth_middleware import require_admin_authentication


class PolicyListAPIView(BaseView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.policy_type_map = {
            'max_life': MaxPolicy,
            'hdfc_life': HDFCPolicy,
            'icici_life': ICICIPolicy
        }

    @require_admin_authentication
    def get(self, admin_user, *args, **kwargs):
        """"""
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        status_filter = request.args.get('policy_status')
        customer_name_filter = request.args.get('customer_name')
        created_date_filter = request.args.get('created_date')

        query = Policy.query.filter_by(is_active=True)

        if status_filter:
            try:
                status_filter = PolicyStatus(status_filter)
            except ValueError:
                raise APIException(message=f"{status_filter} is not a valid choice", status_code=400)
            query = query.filter_by(policy_status=status_filter)
        if customer_name_filter:
            query = query.filter(Policy.customer_name.ilike(f'%{customer_name_filter}%'))
        if created_date_filter:
            try:
                created_date = datetime.fromisoformat(created_date_filter)
                query = query.filter(extract('year', Policy.created_at) == created_date.year,
                                     extract('month', Policy.created_at) == created_date.month,
                                     extract('day', Policy.created_at) == created_date.day)
            except ValueError:
                raise APIException(message="Invalid date format. Use YYYY-MM-DD.", status_code=400)

        policies = query.paginate(page=page, per_page=per_page, max_per_page=20, count=True, error_out=False)

        return self.get_response(data={
            'total': policies.total,
            'pages': policies.pages,
            'current_page': policies.page,
            'results': [policy.to_dict() for policy in policies.items]
        })

    @require_admin_authentication
    def post(self, admin_user, *args, **kwargs):
        """"""
        data = self.request_data
        policy_type = data.get('policyType')
        if not policy_type:
            raise APIException("Policy Type is required field", 400)
        validation_class = self.policy_type_map.get(policy_type.lower())
        validated_data = self.get_validated_data(validation_class=validation_class, data=data)
        new_policy = Policy(**validated_data, updated_by=admin_user.id)
        db.session.add(new_policy)
        try:
            db.session.commit()
        except Exception as e:
            raise APIException(message=str(e), status_code=400)
        return self.get_response(data={"message": "User Policy Created", "status": "success"}, status_code=201)
