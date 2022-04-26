from marshmallow import fields, Schema


# Requests
class RequestTestSchema(Schema):
      text = fields.Str(description="텍스트", required=True)

class RequestSetNicknameSchema(Schema):
      nickname = fields.Str(description="닉네임", required=True)
      id = fields.Str(description="유저 아이디", required=True)

class RequestSignupSchema(Schema):
      id = fields.Str(description="유저 아이디", required=True)
      password = fields.Str(description="비밀번호", required=True)
      nickname = fields.Str(description="닉네임", required=True)

class RequestSigninSchema(Schema):
      id = fields.Str(description="유저 아이디", required=True)
      password = fields.Str(description="비밀번호", required=True)
      fcm_token = fields.Str(description="fcm 토큰", required=True)

class RequestResetPasswordSchema(Schema):
      newpw = fields.Str(description="새비밀번호", required=True)

class RequestCheckPasswordSchema(Schema):
      password = fields.Str(description="비밀번호", required=True)


class RequestFileSchema(Schema):
      id = fields.Str(description="유저 아이디", required=True)
      file = fields.Raw(required=True, type="file")

class RequestByEmailSchema(Schema):
      email = fields.Str(description="이메일", required=True)

class RequestSendAuthCodeSchema(Schema):
      phone_number = fields.Str(description="휴대폰번호", required=True)

class RequestCheckAuthCodeSchema(Schema):
      key = fields.Str(description="사용자 이메일", required=True)
      authcode = fields.Str(description="인증코드", required=True)
      request_type = fields.Str(description="요청 타입", required=True)

class RequestCheckWithDrawalSchema(Schema):
      authcode = fields.Str(description="인증코드", required=True)

class RequestSendAuthCodeEmailSchema(Schema):
      email = fields.Str(description="이메일", required=True)
      request_type = fields.Str(description="signup or password or withdrawal", required=True)

class RequestGuestLoginSchema(Schema):
      nickname = fields.Str(description="게스트 유저 닉네임", required=False) 

class RequestCheckExistSchema(Schema):
      key = fields.Str(description="검사하고 싶은 유저 컬럼", required=False)
      value = fields.Str(description="검사하고 싶은 아이디", required=False)

class RequestSettingSchema(Schema):
      user_unique_id = fields.Str(description="고유아이디", required=True)
      birth = fields.Str(description="생년월일", required=True)
      gender = fields.Str(description="성별", required=True)
      
class RequestSnsSignupSchema(Schema):
      email = fields.Str(description="유저 이메일", required=True)
      birth = fields.Str(description="생년월일", required=True)
      gender = fields.Str(description="성별", required=True)
      nickname = fields.Str(description="닉네임", required=True)
      platform_type = fields.Str(description="플랫폼 종류(google, kakao, naver)", required=True)

class RequestPostSchema(Schema):
      id = fields.Str(description="유저 아이디", required=True)
      title = fields.Str(description="제목", required=True)
      contents = fields.Str(description="내용", required=True)

class RequestReplySchema(Schema):
      id = fields.Str(description="유저 아이디", required=True)
      contents = fields.Str(description="내용", required=True)
      post_id = fields.Int(description="포스트 id", requird=True)      

class RequestRidingEachSchema(Schema):
      user_id = fields.Str(description="유저 아이디", required=True)
      unique_id = fields.Str(description="유저 아이디", required=True)
      riding_time = fields.Str(description="주행 시간", required=True)
      ave_speed = fields.Str(description="평균 속도", required=True)
      distance = fields.Str(description="평균 거리", required=True)
      starting_point = fields.Str(description="출발지", required=True)
      end_point = fields.Str(description="도착지", required=True)