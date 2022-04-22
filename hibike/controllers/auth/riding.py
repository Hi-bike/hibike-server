from flask_apispec import doc, use_kwargs
from hibike import app, db
from hibike.models.riding import RidingAve, RidingTotal
from hibike.controllers.auth import (
    API_CATEGORY,
    auth_bp
)
from hibike.schema.user import (
    RequestRidingAveSchema,
)
from hibike.utils.common import (
    response_json_with_code,
)
from datetime import datetime
from pytz import timezone

@auth_bp.route("/rone/<int:id>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 정보 하나 반환",
    description="라이딩 정보 하나 반환합니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_riding_info_one(id):
    row = RidingAve.get_one_by_id(id)
    
    return response_json_with_code(
        result={
            "id":row.id,
            "user_id":row.user_id,
            "riding_time":row.riding_time,
            "ave_speed":row.ave_speed,
            "ave_distance":row.ave_distance
        }
    )
    
    
@auth_bp.route("/rone", methods=["POST"])
@use_kwargs(RequestRidingAveSchema)
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 저장",
    description="라이딩 정보 저장.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def create_riding(user_id, riding_time, ave_speed, ave_distance):
    KST = timezone('Asia/Seoul')
    time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
    
    RidingAve.create(
        user_id, riding_time, ave_speed, ave_distance, time
    )
    
    RidingTotal.update(
        user_id, riding_time, ave_speed, ave_distance
    )
    
    return response_json_with_code()


@auth_bp.route("/rtotal/<user_id>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 전체 정보 반환",
    description="라이딩 전체 정보를 반환합니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_riding_total(user_id):
    row = RidingTotal.get_by_user_id(user_id)
    
    return response_json_with_code(
        result={
            "total_time":row.total_time,
            "total_speed":row.total_speed,
            "total_distance":row.total_distance
        }
    )


@auth_bp.route("/rall/<user_id>/<int:page>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 페이지 반환",
    description="라이딩 전체 정보를 반환합니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_riding_all(user_id, page):
    riding_rows = RidingAve.get_all_by_page(user_id, page)
        
    result = []
    if riding_rows == []:
        return response_json_with_code(
            result=result,
            is_last = "True"
        )
    
    for row in riding_rows:
        result.append({
            "id":row.id,
            "riding_time": row.riding_time,
            "ave_speed": row.ave_speed,
            "ave_distance": row.ave_distance,
        })
            
    return response_json_with_code(
        result=result,
        is_last = "False"
    )
