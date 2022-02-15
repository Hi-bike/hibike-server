from flask import request, jsonify
from flask_apispec import doc, use_kwargs
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    decode_token
)
from hibike import app, db
from hibike.models.auth import User
from hibike.models.common.redis_conn import RedisConn
from hibike.controllers.auth import (
    API_CATEGORY,
    auth_bp,
    authorization_header
)
from hibike.schema.user import (
    RequestSigninSchema,
)
from hibike.utils.common import (
    response_json_with_code,
)
from hibike.utils.jwt import (
    jwt_redis_blocklist,
    JwtToken
)
import bcrypt
import datetime

@auth_bp.route('/signin', methods=["POST"])
@use_kwargs(RequestSigninSchema)
@doc(
    tags=[API_CATEGORY],
    summary="로그인",
    description="로그인을 합니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def login(id, password):
    user_row = User.get_user_by_id(id)
    if user_row is None:
        return response_json_with_code(
            401, 
            result="There is no ID on db."
        )
    if bcrypt.checkpw(password.encode('utf-8'), user_row.password.encode('utf-8')):
        token = JwtToken(user_row.idx)
        resp = response_json_with_code(access_token=token.access_token)
        return resp
    else:
        return response_json_with_code(
            401, 
            result="Failed"
        )