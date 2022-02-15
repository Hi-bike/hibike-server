from hibike import jwt
from hibike.models.common.redis_conn import RedisConn
from flask_jwt_extended import (
    create_access_token, create_refresh_token
)
import datetime

jwt_redis_blocklist = RedisConn()

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token_in_redis = jwt_redis_blocklist.get(jti)

    return token_in_redis is not None


class JwtToken:
    def __init__(self, identity):
        self.refresh_token = create_refresh_token(identity=identity)
        self.access_token = create_access_token(identity=identity, fresh=True)
    
    def set_refresh_token_expire(self, resp, days=1):
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=days) 
        resp.set_cookie('refresh_token_cookie', value=self.refresh_token, expires=expire_date, httponly=True)
        
        return resp
        