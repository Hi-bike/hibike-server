from flask import render_template
from flask_apispec import doc, use_kwargs
from flask_mail import Message
from flask_jwt_extended import (
    get_jwt_identity, 
    jwt_required,
)
from scrimdor.models.auth import User
from scrimdor.models.common.redis_conn import RedisConn
from scrimdor import db, mail
from scrimdor.controllers.auth import (
    API_CATEGORY,
    auth_bp,
)
from scrimdor.schema.user import (
    RequestByEmailSchema,
    RequestCheckWithDrawalSchema
)
from scrimdor.utils.common import (
    response_json_with_code
)   

import datetime
import random


@auth_bp.route('/withdrawal', methods=["GET"])
@jwt_required(locations="headers")
@doc(
    tags=[API_CATEGORY],
    summary="회원탈퇴",
    description="회원탈퇴하기",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def unregister():
    user_id = get_jwt_identity()
    user_row = User.get_user_by_id(user_id)
   
    if user_row.platform_type != 'scrimdor':
        db.session.query(User).filter(User.id == user_id).delete()    
        db.session.commit()
        return response_json_with_code(
            result = 'success'
        )
         
    r = RedisConn()
    row = {
        'id' : user_row.id,
        'unique_id' : user_row.unique_id,
        'email' : user_row.email,
        'password' : user_row.password,
        'nickname' : user_row.nickname,
        'gender' : user_row.gender,
        'birth' : user_row.birth,
        'email_auth' : user_row.email_auth,
        'profile_image_name': user_row.profile_image_name
    }
    r.hmset('delete:'+user_row.email, row)
    r.expire('delete:'+user_row.email,datetime.timedelta(days=30))
    db.session.query(User).filter(User.id == user_id).delete()
    db.session.commit()
    return response_json_with_code(
        result = 'success'
    )
    

@auth_bp.route('/restore', methods=["POST"])
@use_kwargs(RequestByEmailSchema)
@doc(
    tags=[API_CATEGORY],
    summary="회원탈퇴 복구",
    description="회원탈퇴 복구하기",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def restore(email):
    r = RedisConn()
    row = r.hgetall('delete:'+email)
    
    if row == {}:
        return response_json_with_code(
            result = '삭제 대기중인 계정이 아닙니다.'
        )
    db.session.add(User(
        id = row['id'],
        unique_id = row['unique_id'],
        email = row['email'],
        password = row['password'],
        nickname = row['nickname'],
        gender = row['gender'],
        birth = row['birth'],
        email_auth = row['email_auth'],
        profile_image_name = row['profile_image_name']
    ))
    db.session.commit()
    r.delete('delete:'+email)
    return response_json_with_code(
        result = 'success'
    )
    

@auth_bp.route('/withdrawal-authcode', methods=["GET"])
@jwt_required(locations="headers")
@doc(
    tags=[API_CATEGORY],
    summary="탈퇴 인증 메일 전송",
    description="탈퇴 시 본인인증을 위한 인증번호를 메일로 전송합니다.",
    responses={200: {"description" : "success response"}, 
               401: {"description" : "Unauthorized"}
    }
)
def send_email_withdrawal():
    user_id = get_jwt_identity()
    row = User.get_user_by_id(user_id)
    email = row.email
    msg = Message("[scrimdor]", sender="scrimdor2@gmail.com", recipients=[email])
    authcode = str(random.randrange(100000, 999999))
    msg.html = render_template(
        'code_email.html',
        title = 'SCRIMDOR',
        Account = email,
        Verification_Code = authcode
    )
    mail.send(msg)
    r = RedisConn()
    r.set(email, authcode)
    r.expire(email, 600)
    return response_json_with_code(
        result = "success"
    )


@auth_bp.route('/check-withdrawal', methods=["POST"])
@jwt_required(locations="headers")
@use_kwargs(RequestCheckWithDrawalSchema)
@doc(
    tags=[API_CATEGORY],
    summary="탈퇴시 인증코드 확인",
    description="전송한 인증코드와 입력받은 인증코드가 동일한지 확인합니다.\n\
                 authcode : 인증번호",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def check_authcode_withdrawal(authcode):
    user_id = get_jwt_identity()
    row = User.get_user_by_id(user_id)
    email = row.email
    r = RedisConn()
    if authcode == r.get(email):
        r.delete(email)
        return response_json_with_code(
            is_auth = True
        )        
    else:
        return response_json_with_code(
            is_auth = False
        )


