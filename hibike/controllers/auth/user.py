from flask import request, session, jsonify, send_from_directory
from flask_apispec import doc, use_kwargs
from hibike.models.auth import User, UserRiding
from hibike.models.common.redis_conn import RedisConn
from hibike.controllers.auth import (
    API_CATEGORY,
    auth_bp,
    authorization_header
)
from hibike.schema.user import (
    RequestTestSchema,
    RequestSetNicknameSchema,
    RequestFileSchema,
)
from hibike.utils.common import (
    response_json_with_code,
)
from hibike import db
import os

path = os.path.abspath("./hibike/static/image/profile")

@auth_bp.route('/test', methods=["POST"])
@use_kwargs(RequestTestSchema)
@doc(
    tags=[API_CATEGORY],
    summary="테스트용 api",
    description="테스트용 api",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def test_api(text):
    return response_json_with_code(
        result = text + ' from server'
    )

@auth_bp.route("/current-user", methods=["GET"])
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
    id = request.args.get("id")
   
    user_row = User.get_user_by_id(id)
    if user_row:
        user_dict = user_row.to_dict()
        
        return user_dict
    else:
        return response_json_with_code(
            404,
            result="not found"    
        )


@auth_bp.route("/setting", methods=["POST"])
@use_kwargs(RequestSetNicknameSchema)
@doc(
    tags=[API_CATEGORY],
    summary="닉네임 변경",
    description="닉네임 변경",
    params=authorization_header,
    response={
        200: {"description" : "success response"},
        404: {"description" : "Not Found"}
    }
)
def set_nickname(id, nickname):
    user_row = User.get_user_by_id(id)
    if user_row:
        user_row.nickname = nickname
        db.session.commit()
        return response_json_with_code()
    else:
        return response_json_with_code(404)
    

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
            

@auth_bp.route("/image", methods=["POST"])
@doc(
    tags=[API_CATEGORY],
    summary="유저의 프로필 이미지",
    description="유저의 프로필 이미지를 저장합니다.",
    response={
        200: {"description" : "success response"},
        404: {"description" : "Not Found"}
    }
)
def upload():
    id = request.form.get("id")
    file = request.files.get("file")

    if not file:
        return response_json_with_code()
    
    user_row = User.get_user_by_id(id)
    
    if not user_row:
        return response_json_with_code(404)
    
    filename = file.filename.split(".")
    new_filename = f"{id}.{filename[1]}"
    user_row.image = new_filename
    
    full_path = os.path.join(path, new_filename)
    file.save(full_path)
    db.session.commit()

    return response_json_with_code()


@auth_bp.route("/image/<id>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="donwload",
    description="image download"
)
def donwload(id):
    image = User.get_user_by_id(id).image
    if image:
        abspath = os.path.abspath(path)
        return send_from_directory(abspath, image)
    else:
        return response_json_with_code()