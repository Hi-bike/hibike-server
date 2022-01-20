from flask import render_template
from flask_apispec import doc, use_kwargs
from flask_mail import Message
from scrimdor.models.auth import User
from scrimdor.models.common.redis_conn import RedisConn
from scrimdor import db, mail
from scrimdor.controllers.auth import (
    API_CATEGORY,
    auth_bp
)
from scrimdor.schema.user import (
    RequestSendAuthCodeEmailSchema,
    RequestCheckAuthCodeSchema,
    RequestSignupSchema,
    RequestSnsSignupSchema
)
from scrimdor.utils.common import (
    response_json_with_code,
    gen_unique_id
)   
from scrimdor.utils.jwt import JwtToken
import base64
import hashlib
import hmac
import random
import bcrypt

def is_empty(email, password, birth, gender, nickname):
    if email == "" or password == "" or birth == "" or gender == "" or nickname == ""\
    or email == None or password == None or birth == None or gender == None or nickname == None:
        return True
    else:
        return False

@auth_bp.route('/signup', methods=["POST"])
@use_kwargs(RequestSignupSchema)
@doc(
    tags=[API_CATEGORY],
    summary="회원가입",
    description="회원가입을 합니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def signup(email, password, birth, gender, nickname):
    if not 1 <= len(nickname) <= 30:
        return response_json_with_code(
            res_code = 422,
            result = "letter count error"
        )
        
    user_row = User.get_user_by_email_and_platform(email, 'scrimdor')
    
    if user_row is not None:
        #email_auth = 0 인 유저라면 삭제
        if user_row.email_auth == 0:
            User.query.filter(User.email == user_row.email).delete()
            db.session.commit()
        else:
            return response_json_with_code(
                401, 
                result="There is ID on db."
            )
        
    #unique_id 생성
    while True:
        unique_id = gen_unique_id()
        other_user = User.get_user_by_unique_id(unique_id)
        if not other_user:
            break
        
    encrypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())                
    
    db.session.add(User(
        unique_id = unique_id,
        email = email,
        password = encrypted_password,
        birth = birth,
        gender = gender,
        nickname = nickname,
        profile_image_name = 'default.png',
        platform_type = 'scrimdor'
    ))

    db.session.commit()

    return response_json_with_code(
        200
    )
    
    
@auth_bp.route('/sns-signup', methods=['POST'])
@use_kwargs(RequestSnsSignupSchema)
@doc(
    tags=[API_CATEGORY],
    summary="sns 회원가입 개인정보 입력",
    description="sns 최초 로그인시, 개인정보를 db에 저장합니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def sns_signup(email, gender, birth, nickname, platform_type):
    password = gen_unique_id() + gen_unique_id()
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    while True:
        unique_id = gen_unique_id()
        other_user = User.get_user_by_unique_id(unique_id)
        if not other_user:
            break
    
    db.session.add(User(
        unique_id = unique_id,
        email = email,
        password = password,
        birth = birth,
        gender = gender,
        nickname = nickname,
        profile_image_name = 'default.png',
        email_auth = 1,
        platform_type = platform_type
    ))
    db.session.commit()        

    user_row = User.get_user_by_unique_id(unique_id)
    
    token = JwtToken(user_row.id)
    resp = response_json_with_code(access_token=token.access_token)
    resp = token.set_refresh_token_expire(resp, days=30)
    
    return resp


@auth_bp.route('/email-authcode', methods=["POST"])
@use_kwargs(RequestSendAuthCodeEmailSchema)
@doc(
    tags=[API_CATEGORY],
    summary="인증 메일 전송",
    description="본인인증을 위한 인증번호를 메일로 전송합니다.\n\
                 request_type : signup - 회원가입, password - 비밀번호 찾기\n\
                 email : email",
    responses={200: {"description" : "success response"}, 
               401: {"description" : "Unauthorized"}
    }
)
def send_email(email, request_type):    
    user_row = User.get_user_by_email_and_platform(email, 'scrimdor')
    if not user_row:
        return response_json_with_code(404)
    
    msg = Message("[scrimdor]", sender="scrimdor2@gmail.com", recipients=[email])
    authcode = str(random.randrange(100000, 999999))
    if request_type == "signup":
        msg.html = render_template(
            'code_email.html',
            title = 'SCRIMDOR',
            Account = email,
            Verification_Code = authcode
        )

    elif request_type == "password":
        msg.html = render_template(
            'code_email.html',
            title = 'SCRIMDOR',
            Account = email,
            Verification_Code = authcode
        )

    else:
        return response_json_with_code(
            401,
            result="wrong keyword"
        )
    mail.send(msg)
    r = RedisConn()
    r.set(email, authcode)
    r.expire(email, 600)

    return response_json_with_code(
        200,
        result="succeed"
    )


def make_signature(string):
    secret_key = bytes("XJfrUIgD9FaZ3ttH4jVfEPNco0jXGoTX50Qa4K6S", 'UTF-8')
    string = bytes(string, 'UTF-8')
    string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
    return string_base64  


@auth_bp.route('/check-auth', methods=["POST"])
@use_kwargs(RequestCheckAuthCodeSchema)
@doc(
    tags=[API_CATEGORY],
    summary="인증코드 확인",
    description="전송한 인증코드와 입력받은 인증코드가 동일한지 확인합니다.\n\
                 authcode : 인증번호\n\
                 key : email or 폰번호\n\
                 request_type : signup - 회원가입&아이디 찾기, password - 비밀번호\n",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def check_authcode(key, authcode, request_type):
    r = RedisConn()
    user_row = User.get_user_by_email_and_platform(key, 'scrimdor')
    
    if not user_row:
        return response_json_with_code(
            404,
            result="user not found"
        )
        
    token = JwtToken(user_row.id)
    
    if authcode == r.get(key):
        r.delete(key)
        if request_type == "signup":
            user_row.email_auth = 1
            
            resp = response_json_with_code(
                access_token=token.access_token,
                is_auth = True,
                is_first = True
                )
            resp = token.set_refresh_token_expire(resp, days=30)
            db.session.commit()
            return resp
            
        elif request_type == "password":
            return response_json_with_code(
                access_token = token.access_token,
                is_auth = True
            )
        else:
            return response_json_with_code(
                401,
                is_auth = False
            )        
    else:
        return response_json_with_code(
            401,
            is_auth = False
        )