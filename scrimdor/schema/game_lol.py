from marshmallow import fields, Schema


# Requests
class RequestByLolNicknameSchema(Schema):
    nickname = fields.Str(description="롤 닉네임", required=True)

class RequestMatchHistorySchema(Schema):
    nickname = fields.Str(description="롤 닉네임", required=True)
    count = fields.Int(description="매치 갯수", required=False)

