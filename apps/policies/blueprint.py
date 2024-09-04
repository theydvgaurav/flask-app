from flask import Blueprint

from apps.policies.views import PolicyDetailAPIView, PolicyListAPIView, CommentsAPIView

policy_blueprint = Blueprint('policy', __name__)
policy_blueprint.add_url_rule('policy/', view_func=PolicyListAPIView.as_view('policy-detail'))
policy_blueprint.add_url_rule('policy/<uuid:policy_id>/', view_func=PolicyDetailAPIView.as_view('policy-list'))
policy_blueprint.add_url_rule('policy/<uuid:policy_id>/comments/', view_func=CommentsAPIView.as_view('comments'))
