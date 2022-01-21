from flask import request
from flask_apispec import doc, use_kwargs
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from scrimdor.models.auth import User, UserRiding
from scrimdor.models.common.redis_conn import RedisConn
from scrimdor.controllers.auth import (
    API_CATEGORY,
    auth_bp,
    authorization_header
)
from scrimdor.utils.common import (
    response_json_with_code,
)

@auth_bp.route("/current-user", methods=["GET"])
@jwt_required(locations="headers")
@doc(
    tags=[API_CATEGORY],
    summary="현재 로그인 한 유저의 정보",
    description="access token으로 로그인한 유저의 간단한 정보 반환",
    params=authorization_header,
    response={
        200: {"description" : "success response"},
        404: {"description" : "Not Found"}
    }
)
def get_current_user():
    user_idx = get_jwt_identity()
    user_row = User.get_user_by_idx(user_idx)
    if user_row:
        user_dict = user_row.to_dict()
        
        return response_json_with_code(
            user = user_dict
        )
    else:
        return response_json_with_code(
            404,
            result="not found"    
        )

@auth_bp.route("/profile/<id>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="유저의 프로필 확인",
    description="유저의 프로필을 확인합니다.",
    response={
        200: {"description" : "success response"},
        404: {"description" : "Not Found"}
    }
)
def get_user_profile(id):
    user_row = User.get_user_by_id(id)
    if user_row:
        user_riding_row = UserRiding.get_user_riding_by_idx(user_row.idx)
        return response_json_with_code(
            profile = {
                "id" : id,
                "nickname" : user_row.nickname,
                "distance" : user_riding_row.distance,
                "time" : user_riding_row.time
            }
        )
    else:
        return response_json_with_code(
            404,
            result="not found"    
        )
            
