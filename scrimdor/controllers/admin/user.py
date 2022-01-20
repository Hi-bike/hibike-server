from flask_apispec import doc, use_kwargs
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from scrimdor.controllers.admin import (
    API_CATEGORY,
    admin_bp,
    authorization_header
)
from scrimdor.utils.common import (
    response_json_with_code
) 
from scrimdor.models.auth import User
from scrimdor.models.report import (
    ReportLog,
    ReportRoomLog,
)
from scrimdor.schema.admin import (
    RequestReportSchema,
    RequestReportRoomSchema,
)


@admin_bp.route('/report', methods=["POST"])
@use_kwargs(RequestReportSchema)
@jwt_required(locations='headers')
@doc(
    tags=[API_CATEGORY],
    summary="유저 신고",
    description="유저 신고 접수",
    params=authorization_header,
)
def register_report(unique_id, report_list, etc_comment):
    from_user_id = get_jwt_identity()
    to_user_id = User.get_user_by_unique_id(unique_id)
    
    report_number = ''
    for report in report_list:
        report_number += str(report)+'/'
    
    ReportLog.register_report_log(str(from_user_id),str(to_user_id.id), report_number, etc_comment)
    return response_json_with_code()

@admin_bp.route('/report-room', methods=["POST"])
@use_kwargs(RequestReportRoomSchema)
@jwt_required(locations='headers')
@doc(
    tags=[API_CATEGORY],
    summary="매칭방 신고",
    description="매칭방 신고 접수",
    params=authorization_header,
)
def register_room_report(to_room_id, report_list, etc_comment):
    from_user_id = get_jwt_identity()    
    report_number = ''
    for report in report_list:
        report_number += str(report)+'/'
    
    ReportRoomLog.register_report_room_log(str(from_user_id),to_room_id, report_number, etc_comment)
    return response_json_with_code()