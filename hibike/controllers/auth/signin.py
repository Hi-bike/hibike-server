from flask import request, session
from flask_apispec import doc, use_kwargs
from hibike import app, db
from hibike.models.auth import User
from hibike.models.common.redis_conn import RedisConn
from hibike.controllers.auth import (
    API_CATEGORY,
    auth_bp
)
from hibike.schema.user import (
    RequestSigninSchema,
)
from hibike.utils.common import (
    response_json_with_code,
)
import bcrypt
import requests
import json

headers = {
    'Content-Type': 'application/json; chearset=utf-8',
    'Authorization':'key=AAAAgdsrYfY:APA91bFPnAbWgVS2NITYanribOeuBkTbB715mTGQzLNjo9W9waNmEjqMYOzzjbwbJilmla-6oA09qnddeIWAUpT_EUte9KJ5vHsBl4tM-jA-OLB29KjoS7vyeaFKL6c0MGfk7wRb7ksQ'
    }

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
        
        r = RedisConn()
        r.set(id,"login")
        
        dict = {
            'to' : fcm_token, 
            'priority' : 'high', 
            'data' : {
                'title' : '로그인 알림',
                'message' : user_row.nickname + '님 환영합니다.'
            }
        } 
        res = requests.post('https://fcm.googleapis.com/fcm/send', data=json.dumps(dict), headers=headers)
        return response_json_with_code(200)
    else:
        return response_json_with_code(
            401, 
            result="Failed"
        )   
        
        
@auth_bp.route('/signout')
@doc(
    tags=[API_CATEGORY],
    summary="로그아웃",
    description="로그아웃을 합니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def signout():
    id = request.args.get("id")
    r = RedisConn()
    if r.get(id):
        r.delete(id)

    return {"result":"success"}
        