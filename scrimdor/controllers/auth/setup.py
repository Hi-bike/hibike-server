from scrimdor import db
from flask_apispec import doc, use_kwargs
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from scrimdor.models.auth import User
from scrimdor.controllers.auth import (
    API_CATEGORY,
    auth_bp,
    authorization_header
)
from scrimdor.schema.user import (
    RequestResetPasswordSchema,
    RequestCheckPasswordSchema,
    RequestSettingSchema
)
from scrimdor.utils.common import (
    response_json_with_code
)
import bcrypt

@auth_bp.route('/resetpw',methods=['POST'])
@jwt_required(locations="headers")
@use_kwargs(RequestResetPasswordSchema)
@doc(
    tags=[API_CATEGORY],
    summary="비밀번호변경",
    description="유저의 비밀번호를 변경합니다.",
    params=authorization_header,
    responses={200: {"description" : "success response"}, 
               401: {"description" : "Unauthorized"}
    }
)
def reset_password(newpw):
    user_id= get_jwt_identity()
    user_row = User.get_user_by_id(user_id)
    
    if user_row.platform_type != 'scrimdor':
        return response_json_with_code(401)
    
    encrypted_newpw = bcrypt.hashpw(newpw.encode("utf-8"), bcrypt.gensalt())
    
    if user_row:
        user_row.password = encrypted_newpw
        db.session.commit()
        return response_json_with_code(
            result="reset password"
        )
    else:
        return response_json_with_code(
            401, 
            result="fail"
        )

@auth_bp.route('/check-pw', methods=["POST"])
@jwt_required(locations="headers")
@use_kwargs(RequestCheckPasswordSchema)
@doc(
    tags=[API_CATEGORY],
    summary="비밀번호 체크",
    description="비밀번호 체크",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def check_password(password):
    user_id = get_jwt_identity()
    user_row = User.get_user_by_id(user_id)
    if bcrypt.checkpw(password.encode('utf-8'), user_row.password.encode('utf-8')):
        return response_json_with_code(
            authenticated = True
        )
    else:
        return response_json_with_code(
            authenticated = False
        )
        

@auth_bp.route('/setting', methods=["POST"])
@jwt_required(locations="headers")
@use_kwargs(RequestSettingSchema)
@doc(
    tags=[API_CATEGORY],
    summary="고유아이디/생년월일/성별 수정",
    description="고유아이디/생년월일/성별 수정",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def profile_update(user_unique_id, birth, gender):
    if not 4 <=len(user_unique_id) <= 16:
        if 'guest-' in user_unique_id:
            return response_json_with_code(
                res_code= 422,
                result = "id not available"
            )
        return response_json_with_code(
            res_code = 422,
            result = "letter count error"
        )
        
    user_id = get_jwt_identity()
    user_row = User.get_user_by_id(user_id)
    user_row.unique_id = user_unique_id
    user_row.birth = birth
    user_row.gender = gender
    db.session.commit()
    return response_json_with_code()