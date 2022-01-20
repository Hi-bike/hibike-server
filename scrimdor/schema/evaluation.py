from marshmallow import fields, Schema


# Requests
class RequestEvaluationCreateSchema(Schema):
    evaluated_user = fields.Str(description="평가할 유저의 unique_id", required=True)
    evaluation = fields.List(fields.Str, description="평가 번호 최대 4개", required=False)
    etc_comment = fields.Str(description="기타 평가 내용", required=False)
    is_positive = fields.Bool(description="긍정 or 부정", required=True)

class RequestEvaluationUpdateSchema(Schema):
    evaluated_user = fields.Str(description="평가할 유저의 unique_id", required=True)
    previous_evaluation = fields.List(fields.Str, description="이전 평가", required=False)
    is_previous_positive = fields.Bool(description="이전 긍정 or 부정", required=True)
    evaluation = fields.List(fields.Str, description="평가 번호 최대 4개", required=False)
    etc_comment = fields.Str(description="기타 평가 내용", required=False)
    is_positive = fields.Bool(description="긍정 or 부정", required=True)
    
class RequestEvaluationDeleteSchema(Schema):
    evaluated_user = fields.Str(description="평가된 유저의 unique_id", required=True)
    evaluation = fields.List(fields.Int, description="평가 내용 최대 4개", required=False)
    is_positive = fields.Bool(description="긍정 or 부정", required=True)