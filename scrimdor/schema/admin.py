from marshmallow import fields, Schema

class RequestReportSchema(Schema):
    unique_id = fields.Str(description="신고할 유저 고유 아이디", required=True)
    report_list = fields.List(fields.Str, description="신고 번호 배열", required=False)
    etc_comment = fields.Str(description="기타 신고 내용", required=False)
    
class RequestReportRoomSchema(Schema):
    to_room_id = fields.Str(description="신고할 방 고유 아이디", required=True)
    report_list = fields.List(fields.Str, description="신고 번호 배열", required=False)
    etc_comment = fields.Str(description="기타 신고 내용", required=False)
    
class RequestAdminKeySchema(Schema):
    key = fields.Str(description="key", required=False)
    
class RequestGameSchema(Schema):
    key = fields.Str(description="key", required=False)
    game = fields.Str(description="game", required=False)
    
class RequestGameImageFileSchema(Schema):
    key = fields.Str(description="key", required=False)
    game = fields.Str(description="game", required=False)
    file = fields.Raw(required=False, type="file")
    
class RequestFileSchema(Schema):
    key = fields.Str(description="key", required=False)
    file = fields.Raw(required=False, type="file")
    
class RequestPersonalitySchema(Schema):
    key = fields.Str(description="key", required=False)
    personality = fields.Str(description="personality", required=False)