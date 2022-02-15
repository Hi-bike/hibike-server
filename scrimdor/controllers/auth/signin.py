from flask import request, jsonify
from flask_apispec import doc, use_kwargs
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    decode_token
)
from scrimdor import app, db
from scrimdor.models.auth import User
from scrimdor.models.common.redis_conn import RedisConn
from scrimdor.controllers.auth import (
    API_CATEGORY,
    auth_bp,
    authorization_header
)
from scrimdor.schema.user import (
    RequestSigninSchema,
)
from scrimdor.utils.common import (
    response_json_with_code,
)
from scrimdor.utils.jwt import (
    jwt_redis_blocklist,
    JwtToken
)
import bcrypt
import datetime
import requests
import json

headers = {'Content-Type': 'application/json; chearset=utf-8','Authorization':'key=AAAAgdsrYfY:APA91bFPnAbWgVS2NITYanribOeuBkTbB715mTGQzLNjo9W9waNmEjqMYOzzjbwbJilmla-6oA09qnddeIWAUpT_EUte9KJ5vHsBl4tM-jA-OLB29KjoS7vyeaFKL6c0MGfk7wRb7ksQ'}

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
def login(id, password, fcm_token):
    user_row = User.get_user_by_id(id)
    if user_row is None:
        return response_json_with_code(
            401, 
            result="There is no ID on db."
        )
    if bcrypt.checkpw(password.encode('utf-8'), user_row.password.encode('utf-8')):
        user_row.fcm_token = fcm_token
        db.session.commit()

        token = JwtToken(user_row.idx)
        resp = response_json_with_code(access_token=token.access_token)
         
        dict = {
            'to' : fcm_token, 
            'priority' : 'high', 
            'data' : {
                'title' : '로그인 알림',
                'message' : user_row.nickname + '님 환영합니다.'
            }
        } 
        res = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(dict), headers=headers)
        return resp
    else:
        dict = {
            'to' : fcm_token, 
            'priority' : 'high', 
            'data' : {
                'title' : '로그인 실패알림',
                'message' : '로그인 정보가 일치하지 않습니다.'
            }
        } 
        res = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(dict), headers=headers)
        return response_json_with_code(
            401, 
            result="Failed"
        )