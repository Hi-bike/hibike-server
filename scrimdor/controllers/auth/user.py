from flask import request
from flask_apispec import doc, use_kwargs
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from scrimdor.models.auth import User
from scrimdor.models.common.redis_conn import RedisConn
from scrimdor.controllers.auth import (
    API_CATEGORY,
    auth_bp,
    authorization_header
)
from scrimdor.schema.user import (
    RequestCheckExistSchema
)
from scrimdor.utils.common import (
    response_json_with_code,
)


@auth_bp.route("/current-user", methods=["GET"])
@jwt_required(locations="headers")
@doc(
    tags=[API_CATEGORY],
    summary="현재 로그인 한 유저의 간단한 정보",
    description="유저의 프로필을 확인합니다.",
    params=authorization_header,
    response={
        200: {"description" : "success response"},
        404: {"description" : "Not Found"}
    }
)
def get_current_user():
    user_id = get_jwt_identity()
    user = User.get_user_by_id(user_id)
    if user:
        user_dict = user.to_dict_current_profile()
        
        return response_json_with_code(
            user = user_dict
        )
    else:
        return response_json_with_code(404)
            

@auth_bp.route('/info', methods=["GET"])
@jwt_required(locations="headers")
@doc(
    tags=[API_CATEGORY],
    summary="개인정보 반환",
    description="고유아이디/생년월일/성별 반환",
    responses={200: {"description" : "success response"},
               404: {"description" : "Not Found"},
    },
    params=authorization_header
)
def get_auth_info():
    user_id = get_jwt_identity()
    user_row = User.get_user_by_id(user_id)
    if not user_row:
        return response_json_with_code(404)
    
    user_info = user_row.to_dict()
    del(user_info['id'], user_info['email_auth']) 
    
    return response_json_with_code(
        user = user_info
    )


@auth_bp.route('/basic-info', methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="유저 email로 개인정보 반환",
    description="email = email\n\
        withdrawal = true, false\n\
        image, unique_id, nickname",
    responses={200: {"description" : "success response"},
               404: {"description" : "Unauthorized"},
    }
)
def get_auth_info_by_email():
    email = request.args.get('email')
    withdrawal = request.args.get('withdrawal')
    
    if withdrawal == 'true':
        r = RedisConn()
        user = r.hgetall('delete:'+email)
        if not user:
            return response_json_with_code(404)
        result = {
            "unique_id" : user['unique_id'],
            "nickname" : user['nickname'],
            "profile_image_name":user['profile_image_name']
        }
    else:
        user_row = User.get_user_by_email_and_platform(email, 'scrimdor')
        result = {
            "unique_id" : user_row.unique_id,
            "nickname" : user_row.nickname,
            "profile_image_name":user_row.profile_image_name
        }
    return response_json_with_code(
        result = result
    )

    
@auth_bp.route("/check-exists", methods=["POST"])
@use_kwargs(RequestCheckExistSchema)
@doc(
    tags=[API_CATEGORY],
    summary="중복 확인",
    description="unique_id, email \nex) key: unique_id, value: 의찬군",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }    
)
def check_exists(key, value):
    if key not in dir(User):
        return response_json_with_code(
            400, 
            message=key + " is not a vaild key."
        )
    
    if key == 'email':
        r = RedisConn()
        row = r.hgetall('delete:'+ value)
        if row != {}:
            return response_json_with_code(
                result='already exists email'
            )
    user_row = User.query.filter(
        getattr(User, key) == value
    ).one_or_none()

    if user_row and user_row.email_auth != 0:
        return response_json_with_code(
            result=True, 
            message=key + " " + value + " exists in database."
        )

    return response_json_with_code(
        result=False, 
        message=key + " " + value + " does not exists in database."
    )
