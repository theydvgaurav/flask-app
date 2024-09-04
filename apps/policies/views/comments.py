from flask import request

from apps.policies.models.comment import Comments
from base.views.base import BaseView
from databases.extensions import db
from middlewares.auth_middleware import require_admin_authentication


class CommentsAPIView(BaseView):

    @require_admin_authentication
    def get(self, admin_user, policy_id, *args, **kwargs):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        query = Comments.query.filter_by(policy_id=policy_id)
        comments = query.paginate(page=page, per_page=per_page, max_per_page=20, count=True, error_out=False)
        return self.get_response(data={
            'total': comments.total,
            'pages': comments.pages,
            'current_page': comments.page,
            'results': [comment.to_dict() for comment in comments.items]
        })

    @require_admin_authentication
    def post(self, admin_user, *args, **kwargs):
        data = self.request_data
        new_comment = Comments(content=data.get("content"), comment_by=admin_user.id, policy_id=data.get("policyId"))
        db.session.add(new_comment)
        db.session.commit()
        return self.get_response({})
