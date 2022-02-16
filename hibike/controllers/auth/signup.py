from flask_apispec import doc, use_kwargs
from flask_mail import Message
from hibike.models.auth import User,UserRiding
from hibike.models.common.redis_conn import RedisConn
from hibike import db
from hibike.controllers.auth import (
    API_CATEGORY,
    auth_bp
)
from hibike.schema.user import (
    RequestSignupSchema,
)
from hibike.utils.common import (
    response_json_with_code,
)   
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
def signup(id, password, nickname):
    if not 1 <= len(nickname) <= 30:
        return response_json_with_code(
            res_code = 422,
            result = "letter count error"
        )
        
    user_row = User.get_user_by_id(id)
    
    if user_row is None:
        encrypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())                
        db.session.add(User(
            id = id,
            password = encrypted_password,
            nickname = nickname,
        ))
        db.session.commit()

        user_row = User.get_user_by_id(id)
        db.session.add(UserRiding(
            user_idx = user_row.idx
        ))
        db.session.commit()
        
    else:
        return response_json_with_code(
            401,
            result='이미 존재하는 아이디'
        )
    return response_json_with_code(
        200,
        result = 'success'
    )
    
    
