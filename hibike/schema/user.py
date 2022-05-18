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
      
class RequestRidingRegionSchema(Schema):
      region = fields.Str(description="지역", required=True)
      unique_id = fields.Str(description="라이딩 유니크 아이디", required=True)

class RequestPostDangerSchema(Schema):
      id = fields.Str(description="유저 아이디", required=True)
      title = fields.Str(description="제목", required=True)
      contents = fields.Str(description="내용", required=True)
      latitude = fields.Float(description="위도", required=True)
      longitude = fields.Float(description="경도", required=True)
      image = fields.Str(description="이미지 이름", required=True)
      region = fields.Str(description="지역 이름", required=True)
      region_detail = fields.Str(description="지역 상세 정보", required=True)
      period = fields.Int(description="기간 설정", requird=True)  

class RequestDangerRangeSchema(Schema):
      danger_range = fields.List(fields.List(fields.Float,description="위험지역 탐색 범위 리스트", required=True))

class RequestDangerInformationSchema(Schema):
      latitude = fields.Float(description="위도", required=True)
      longitude = fields.Float(description="경도", required=True)

class RequestDeleteDanger(Schema):
      user_id = fields.Str(description="유저 id", required=True)
      latitude = fields.Float(description="위도", required=True)
      longitude = fields.Float(description="경도", required=True)
      my_latitude = fields.Float(description="위도", required=True)
      my_longitude = fields.Float(description="경도", required=True)

class RequestMyPosts(Schema):
      user_id = fields.Str(description="유저 id", required=True)
      page = fields.Int(description="page number", required=True)

class RequestMyDanger(Schema):
      user_id = fields.Str(description="유저 id", required=True)
      page = fields.Int(description="page number", required=True)

class RequestDeleteNearDanger(Schema):
      latitude = fields.Float(description="위도", required=True)
      longitude = fields.Float(description="경도", required=True)
      
class RequestDeleteMyPost(Schema):
      post_id = fields.Int(description="포스트 id", requird=True)
      
class RequestDeleteMyDanger(Schema):
      danger_id = fields.Int(description="위험요소 id", requird=True)