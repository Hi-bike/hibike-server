from flask import request, send_from_directory
from flask_apispec import doc, use_kwargs
from hibike import app, db
from hibike.models.riding import RidingEach, RidingTotal
from hibike.controllers.auth import (
    API_CATEGORY,
    auth_bp
)
from hibike.schema.user import (
    RequestRidingEachSchema,
)
from hibike.utils.common import (
    response_json_with_code,
)
from datetime import datetime
from pytz import timezone
import os

path = os.path.abspath("./hibike/static/image/riding")

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
    row = RidingEach.get_one_by_id(id)
    
    return response_json_with_code(
        result={
            "id":row.id,
            "user_id":row.user_id,
            "riding_time":row.riding_time,
            "ave_speed":row.ave_speed,
            "distance":row.distance,
            "starting_point":row.starting_point,
            "end_point":row.end_point
        }
    )
    
    
@auth_bp.route("/rone", methods=["POST"])
@use_kwargs(RequestRidingEachSchema)
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 저장",
    description="라이딩 정보 저장.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def create_riding(user_id, unique_id, riding_time, ave_speed, distance, starting_point, end_point):
    KST = timezone('Asia/Seoul')
    time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
    
    RidingEach.create(
        user_id, unique_id, riding_time, ave_speed, distance, time, 
        starting_point=starting_point,
        end_point=end_point
    )
    
    RidingTotal.update(
        user_id, riding_time, distance
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
        total_time=row.total_time,
        total_distance=row.total_distance,
        count=row.count
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
    riding_rows = RidingEach.get_all_by_page(user_id, page)
        
    result = []
    if riding_rows == []:
        return response_json_with_code(
            result=result,
            is_last = "True"
        )
    
    for row in riding_rows:
        result.append({
            "creating_time": row.create_time,
            "distance": row.distance,
            "ave_speed": row.ave_speed,
            "riding_time": row.riding_time,
            "starting_point": row.starting_point,
            "end_point": row.end_point,
            "unique_id": row.unique_id,
        })
            
    return response_json_with_code(
        result=result,
        is_last = "False"
    )


@auth_bp.route("/rimage", methods=["POST"])
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 결과 이미지",
    description="라이딩 결과 이미지를 저장합니다.",
    response={
        200: {"description" : "success response"},
        404: {"description" : "Not Found"}
    }
)
def rupload():
    unique_id = request.form.get("unique_id")
    file = request.files.get("file")
    
    if not file:
        return response_json_with_code()
    
    filename = file.filename.split(".")
    new_filename = f"{unique_id}.{filename[1]}"
    
    # row = RidingEach.get_one_by_unique_id(unique_id)
    # if row:
       
    full_path = os.path.join(path, new_filename)
    file.save(full_path)
        # row.image = new_filename
        
    db.session.commit()
    return response_json_with_code()


@auth_bp.route("/rimage/<unique_id>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="riding image donwload",
    description="image download"
)
def rdonwload(unique_id):
    # row = RidingEach.get_one_by_unique_id(unique_id)
    # if row:
    abspath = os.path.abspath(path)
    return send_from_directory(abspath, f"{unique_id}.png")
    
    # return response_json_with_code()
