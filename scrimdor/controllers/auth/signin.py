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
from scrimdor.models.common.kakao_oauth import KakaoAuth
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
def login(email, password, remember_check):
    user_row = User.get_user_by_email_and_platform(email, 'scrimdor')
    if user_row is None:
        r = RedisConn()
        row = r.hgetall('delete:'+email)
        if row != {}:
            pw = row['password']
            if bcrypt.checkpw(password.encode('utf-8'), pw.encode('utf-8')):
                time = r.ttl('delete:'+email)
                time = int(time/86400)
                return response_json_with_code(
                    result = str(time)+'일 후 삭제예정입니다.'
                )
        return response_json_with_code(
            401, 
            result="There is no ID on db."
        )
    if user_row.email_auth == 0:
        return response_json_with_code(
            result="not authorized email"
        )
    if user_row.is_ban == 1:
        return response_json_with_code(
            result="banned"
        )
    if bcrypt.checkpw(password.encode('utf-8'), user_row.password.encode('utf-8')):
        token = JwtToken(user_row.id)
        resp = response_json_with_code(access_token=token.access_token)
    
        if remember_check == 1:
            resp = token.set_refresh_token_expire(resp, days=30)
        else :
            resp = token.set_refresh_token_expire(resp)
            
        return resp
    else:
        return response_json_with_code(
            401, 
            result="Failed"
        )

@auth_bp.route('/refresh',methods=['GET'])
@jwt_required(locations='cookies', refresh=True)
@doc(
    tags=[API_CATEGORY],
    summary="새로운 access token",
    description="access token을 새로 발급합니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    },
    params=authorization_header
)
def refresh():
    user_id = get_jwt_identity()
    user_row = User.get_user_by_id(user_id)
    if user_row.is_ban == 0: #벤 체크
        return response_json_with_code(
            access_token=create_access_token(identity=user_id)
        )
    return response_json_with_code()


@auth_bp.route('/signout',methods=['GET'])
@doc(
    tags=[API_CATEGORY],
    summary="로그아웃",
    description="access token을 blocklist에 넣고 refresh token을 만료시킵니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def logout():
    access_token = request.headers.get('Authorization')
    resp = response_json_with_code(result = 'success')

    if access_token is None:
        resp.set_cookie('refresh_token_cookie', value='', expires=0, httponly=True)
   
    else:
        decoded_token = decode_token(access_token.replace('Bearer ',''))
        jti = decoded_token['jti']
        jwt_redis_blocklist.set(jti,"",ex=datetime.timedelta(minutes=30))
        resp.set_cookie('refresh_token_cookie', value='', expires=0, httponly=True)
    
    return resp


@auth_bp.route('/kauth/url')
@doc(
    tags=[API_CATEGORY],
    summary="Kakao OAuth URL 가져오기",
    description="",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_oauth_url_api():
    request_type = request.args.get('request_type')
    if request_type == 'login':
        return jsonify(
            kakao_oauth_url="https://kauth.kakao.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code" \
            % (app.config['KAKAO_CLIENT_ID'], app.config['KAKAO_LOGIN_REDIRECT_URI'])
        )
        
    elif  request_type == 'authentication':
        return jsonify(
            kakao_oauth_url="https://kauth.kakao.com/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code" \
            % (app.config['KAKAO_CLIENT_ID'], app.config['KAKAO_AUTH_REDIRECT_URI'])
        )

        
@auth_bp.route('/kauth', methods=['GET'])
@doc(
    tags=[API_CATEGORY],
    summary="카카오 회원가입 및 로그인",
    description="",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def kakao_auth():
    code = str(request.args.get('code'))
    request_type = request.args.get('request_type')
    
    kauth = KakaoAuth()
    auth_info = kauth.get_auth(request_type, code)
    
    kakao_user = kauth.get_userinfo('Bearer ' + auth_info['access_token'])
    if not kakao_user:
        return response_json_with_code(401)
    
    email = kakao_user['kakao_account']['email']
    
    user_row = User.get_user_by_email_and_platform(email, 'kakao')
    
    if request_type == 'login':
        if not user_row:# 회원가입
            try:
                gender = kakao_user['kakao_account']['gender']
            except:            
                gender = 'non-binary'
            birth = str(kakao_user['kakao_account']['birthyear']) + str(kakao_user['kakao_account']['birthday'])           
            return response_json_with_code(
                200,
                userinfo = {
                    "email":email,
                    "gender":gender,
                    "birth":birth
                },
                platform_type = 'kakao'
            )
        
        token = JwtToken(user_row.id)
        resp = response_json_with_code(access_token=token.access_token)
        resp = token.set_refresh_token_expire(resp, days=30)
        
        return resp

    elif request_type == 'authentication':
        return response_json_with_code(
            200,
            unique_id = user_row.unique_id
        )
    
    else:
        return response_json_with_code(401)