from marshmallow import fields, Schema


# Requests
class RequestByPubgNicknameSchema(Schema):
    nickname = fields.Str(description="배그 닉네임", required=True)
    server = fields.Str(description="배그 서버(steam or kakao)", required=True)

class RequestByPubgMatchSchema(Schema):
    nickname = fields.Str(description="배그 닉네임", required=True)
    count = fields.Int(description="매치 갯수", required=False)

class RequestProfileByPubgNicknameSchema(Schema):
    nickname = fields.Str(description="배그 닉네임", required=True)