from marshmallow import fields, Schema


# Requests
class RequestByMapleNicknameSchema(Schema):
    nickname = fields.Str(description="메이플 닉네임", required=True)

