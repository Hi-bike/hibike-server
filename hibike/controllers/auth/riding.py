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
    RequestRidingRegionSchema
)
from hibike.utils.common import (
    response_json_with_code,
)
from datetime import datetime
from pytz import timezone
import os, json

path = os.path.abspath("./hibike/static/image/riding")


@auth_bp.route("/rone/<unique_id>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 정보 하나 반환",
    description="라이딩 정보 하나 반환합니다.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_riding_info_one(unique_id):
    row = RidingEach.get_one_by_unique_id(unique_id)
    
    return response_json_with_code(
        result={
            "create_time":row.create_time,
            "user_id":row.user_id,
            "riding_time":row.riding_time,
            "ave_speed":row.ave_speed,
            "distance":row.distance,
            "starting_region":row.starting_region,
            "end_region":row.end_region
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
def create_riding(user_id, unique_id, riding_time, ave_speed, distance): #, starting_point, end_point):
    KST = timezone('Asia/Seoul')
    time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
    
    if riding_time == "nan" and distance == "nan":
        return response_json_with_code()
    
    RidingEach.create(
        user_id, unique_id, riding_time, ave_speed, distance, time
    )
    
    RidingTotal.update(
        user_id, riding_time, distance
    )
    
    return response_json_with_code()

@auth_bp.route("/rmulti", methods=["POST"])
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 저장",
    description="라이딩 정보 저장.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def create_multi_riding():
    user_id = request.form.get("user_id")
    unique_id = request.form.get("unique_id")
    riding_time = request.form.get("riding_time")
    ave_speed = request.form.get("ave_speed")
    distance = request.form.get("distance")
    starting_region = request.form.get("starting_region")
    end_region = request.form.get("end_region")
    northeast_lati = request.form.get("northeast_lati")
    northeast_long = request.form.get("northeast_long")
    southwest_lati = request.form.get("southwest_lati")
    southwest_long = request.form.get("southwest_long")
    file = request.files.get("file")
    
    new_filename = ""
    northeast_lati = float(northeast_lati)
    northeast_long = float(northeast_long)
    southwest_lati = float(southwest_lati)
    southwest_long = float(southwest_long)
    
    KST = timezone('Asia/Seoul')
    create_time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
    
    if file:
        filename = file.filename.split(".")
        new_filename = f"{unique_id}.{filename[1]}"
        
        full_path = os.path.join(path, new_filename)
        file.save(full_path)
    
    
    RidingEach.multi_create(user_id=user_id, unique_id=unique_id, riding_time=riding_time, ave_speed=ave_speed, distance=distance,
        starting_region=starting_region, end_region=end_region, northeast_lati=northeast_lati, northeast_long=northeast_long, 
        southwest_lati=southwest_lati, southwest_long=southwest_long,
        image=new_filename, create_time=create_time
    )
    
    
    RidingTotal.update(
        user_id, riding_time, distance
    )
    
    return response_json_with_code(
        result="success"
    )

    
@auth_bp.route("/sregion", methods=["POST"])
@use_kwargs(RequestRidingRegionSchema)
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 지역 정보 저장",
    description="라이딩 정보 저장.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def update_riding_sregion(region, unique_id):
    row = RidingEach.get_one_by_unique_id(unique_id)
    if row:
        row.starting_region = region
        db.session.commit()
        return response_json_with_code()
        
    return response_json_with_code(401)
        

@auth_bp.route("/eregion", methods=["POST"])
@use_kwargs(RequestRidingRegionSchema)
@doc(
    tags=[API_CATEGORY],
    summary="라이딩 지역 정보 저장",
    description="라이딩 정보 저장.",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def update_riding_eregion(region, unique_id):
    row = RidingEach.get_one_by_unique_id(unique_id)
    if row:
        row.end_region = region
        db.session.commit()
        return response_json_with_code()

    return response_json_with_code(401)
        
    


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
    if row:
        return response_json_with_code(
            total_time=row.total_time,
            total_distance=row.total_distance,
        )
    else:
        return response_json_with_code(
            total_time="0",
            total_distance="0",
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
        )
    
    for row in riding_rows:
        result.append({
            "create_time": str(row.create_time),
            "distance": row.distance,
            "ave_speed": row.ave_speed,
            "riding_time": row.riding_time,
            "starting_region": row.starting_region,
            "end_region": row.end_region,
            "unique_id": row.unique_id,
            "count":row.count
        })
            
    return response_json_with_code(result=result)


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
    row = RidingEach.get_one_by_unique_id(unique_id)
    abspath = os.path.abspath(path)
    return send_from_directory(abspath, row.image)
    
    # return response_json_with_code()
