from flask_apispec import doc
from flask_apispec.annotations import use_kwargs
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
    create_refresh_token
)
from scrimdor.models.common.redis_conn import RedisConn
from scrimdor.controllers.auth import (
    API_CATEGORY,
    auth_bp,
    authorization_header
)
from scrimdor.schema.user import(
    RequestGuestLoginSchema
)
from scrimdor.utils.common import (
    response_json_with_code,
)
from scrimdor.utils.jwt import jwt_redis_blocklist
import datetime
import random
import string


@auth_bp.route('/guest', methods=['POST'])
@use_kwargs(RequestGuestLoginSchema)
@doc(
    tags=[API_CATEGORY],
    summary="게스트 로그인",
    description="게스트로 로그인합니다.",
    responses={200: {"description" : "success response"}}
)
def guest_signin(nickname):
    '''게스트 만료시간'''
    string_pool = string.ascii_uppercase + string.digits
    r = RedisConn()

    while True:
        guest_id = "guest-"
        for i in range(6):
            guest_id += random.choice(string_pool)

        if not r.get(guest_id):
            break
        break
    
    
    r.set(guest_id, nickname)
    r.expire(guest_id,datetime.timedelta(days=60))

    access_token = create_access_token(identity=guest_id, fresh=True) #,expires_delta=datetime.timedelta(days=1)) 
    refresh_token = create_refresh_token(identity=guest_id)
    resp = response_json_with_code(
        access_token=access_token,
        guest_id = guest_id,
    )

    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=60)
    resp.set_cookie('refresh_token_cookie', value=refresh_token, expires=expire_date, httponly=True)
    
    return resp


@auth_bp.route('/guest',methods=['DELETE'])
@jwt_required(locations="headers")
@doc(
    tags=[API_CATEGORY],
    summary="게스트 로그아웃",
    description="게스트를 로그아웃시킵니다.",
    params=authorization_header,
    responses={200: {"description" : "success response"}}
)
def guest_signout():
    r = RedisConn()
    jwt = get_jwt()
    r.delete(jwt['sub'])
    jwt_redis_blocklist.set(jwt['jti'],"",ex=datetime.timedelta(days=1))

    resp = response_json_with_code(res_code=200)
    resp.set_cookie('refresh_token_cookie', value='', expires=0, httponly=True)
    
    return resp
   