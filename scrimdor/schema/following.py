from marshmallow import fields, Schema


class RequestFollowingShema(Schema):
    user_unique_id = fields.Str(description="유저 유니크 아이디", required=True)
    is_following = fields.Bool(description="팔로우 여부", required=True)

class RequestBlacklistShema(Schema):
    user_unique_id = fields.Str(description="유저 유니크 아이디", required=True)
    is_block = fields.Bool(description="차단 여부", required=False)