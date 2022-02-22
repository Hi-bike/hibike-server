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
    user_row = User.get_user_by_id(id)
    if user_row:
        return response_json_with_code(
            401,
            result='이미 존재하는 아이디'
        )
        
    encrypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())                
    db.session.add(User(
        id = id,
        password = encrypted_password,
        nickname = nickname,
    ))
    db.session.add(UserRiding(
        user_id = id
    ))
    
    db.session.commit()
    
    return response_json_with_code()
    
    
