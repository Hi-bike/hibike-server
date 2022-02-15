from marshmallow import fields, Schema


# Requests
class RequestTestSchema(Schema):
      text = fields.Str(description="텍스트", required=True)

class RequestSignupSchema(Schema):
      id = fields.Str(description="유저 아이디", required=True)
      password = fields.Str(description="비밀번호", required=True)
      nickname = fields.Str(description="닉네임", required=True)

class RequestSigninSchema(Schema):
      id = fields.Str(description="유저 아이디", required=True)
      password = fields.Str(description="비밀번호", required=True)

class RequestResetPasswordSchema(Schema):
      newpw = fields.Str(description="새비밀번호", required=True)

class RequestCheckPasswordSchema(Schema):
      password = fields.Str(description="비밀번호", required=True)


class RequestFileSchema(Schema):
      file = fields.Raw(required=True, type="file")

class RequestByEmailSchema(Schema):
      email = fields.Str(description="이메일", required=True)
# class RequestAccuontSettingSchema(Schema):
#   nickname = fields.Str(description="프로플 설정할 닉네임", required=False)
#   # profile_image_url = fields.Str(required=False)
#   #file = fields.Raw(required=False, type="file")
#   introduction = fields.Str(description="자기소개", required=False)

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