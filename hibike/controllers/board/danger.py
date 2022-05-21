from flask import request, session, send_from_directory
from flask_apispec import doc, use_kwargs
from hibike import app, db
from hibike.models.board import Board,Reply,Danger
from hibike.models.auth import User, UserRiding
from hibike.models.common.redis_conn import RedisConn
from hibike.controllers.board import (
    API_CATEGORY,
    board_bp
)
from hibike.models.riding import RidingEach
from hibike.utils.common import (
    response_json_with_code,
)
from hibike.schema.user import (
    RequestDangerRangeSchema,
    RequestDangerInformationSchema,
    RequestDeleteDanger,
    RequestMyDanger,
    RequestDeleteNearDanger,
    RequestDeleteMyDanger
)
import  os
from datetime import datetime
import time as t
from pytz import timezone
from haversine import haversine
import logging

path = os.path.abspath("./hibike/static/image/danger")

@board_bp.route("/danger", methods=["POST"])
@use_kwargs(RequestDangerRangeSchema)
@doc(
    tags=[API_CATEGORY],
    summary="범위내 등록된 위험정보 가져오기",
    description="범위내 등록된 위험정보 가져오기",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_danger(danger_range):
    danger_list = []
    range_list = danger_range
    db_latitude = []
    db_longitude = []
    count_list = []
    tmp_danger_list = []
    
    danger_row = db.session.query(Danger).filter(Danger.is_delete == 'N').all()
    if danger_row == []:
        return response_json_with_code(
            danger_list = danger_list
        )
    for row in danger_row:
        db_latitude.append(row.latitude)
        db_longitude.append(row.longitude)
    
    for i in range(len(range_list)):
        latitude_list = []
        longitude_list = []
        count = 0
        for j in range(8):
            if j%2 != 1:
                latitude_list.append(range_list[i][j])
            else:
                longitude_list.append(range_list[i][j])

        for j in range(len(db_latitude)):
            if min(latitude_list) <= db_latitude[j] and max(latitude_list) >= db_latitude[j] and min(longitude_list) <= db_longitude[j] and max(longitude_list) >= db_longitude[j]:
                if db_latitude[j] not in tmp_danger_list and db_longitude[j] not in tmp_danger_list:
                    tmp_danger_list.append(db_latitude[j])
                    tmp_danger_list.append(db_longitude[j])
                    count += 1
                    
        count_list.append(count)
        
    for i in range(int(len(tmp_danger_list)/2)):
        tmp_list = []
        for j in range(i*2,i*2+2):
            tmp_list.append(tmp_danger_list[j])
        danger_list.append(tmp_list)
        
    return response_json_with_code(
        danger_list = danger_list,
        danger_count = count_list
    )

@board_bp.route("/post-danger", methods=["POST"])
@doc(
    tags=[API_CATEGORY],
    summary="위험지역 등록",
    description="위험지역 등록",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def post_danger():
    id = request.form.get("id")
    title = request.form.get("title")
    contents = request.form.get("contents")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    region = request.form.get("region")
    region_detail = request.form.get("region_detail")
    period = request.form.get("period")
    image = request.files.get("file")
    
    latitude = float(latitude)
    longitude = float(longitude)
    period = int(period)
    
    image_name = ""
    
    user_row = db.session.query(User).filter(User.id == id).first()
    KST = timezone('Asia/Seoul')
    time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
    if image:
        image_name = image.filename
        full_path = os.path.join(path, image_name)
        image.save(full_path)
    
    db.session.add(Danger(
        title=title,
        contents=contents,
        nickname = user_row.nickname,
        latitude = latitude,
        longitude = longitude,
        time=time,
        image=image_name,
        region=region,
        region_detail=region_detail,
        period=period,
    ))
    db.session.commit()

    return response_json_with_code(
        result="Success"
    )

@board_bp.route("/danger-info", methods=["POST"])
@use_kwargs(RequestDangerInformationSchema)
@doc(
    tags=[API_CATEGORY],
    summary="위험지역 상세정보",
    description="위험지역 상세정보",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_danger_info(latitude, longitude):
    danger_row = db.session.query(Danger).filter((Danger.latitude == latitude) and (Danger.latitude == longitude)).first()
    if not danger_row:
        return response_json_with_code(
            401,
            result = "no data"
        )
    if danger_row.is_delete == "Y":
        return response_json_with_code(401)
    
    res = {
        "nickname" : danger_row.nickname,
        "title" : danger_row.title,
        "contents" : danger_row.contents,
        "latitude" : danger_row.latitude,
        "longitude" : danger_row.longitude,
        "time" : danger_row.time,
        "image" : danger_row.image,
        "region" : danger_row.region,
        "region_detail" : danger_row.region_detail,
        "period" : danger_row.period,
    }

    return response_json_with_code(
        result = res
    )

@board_bp.route("/delete-danger", methods=["POST"])
@use_kwargs(RequestDeleteDanger)
@doc(
    tags=[API_CATEGORY],
    summary="등록한 위험지역 삭제",
    description="등록한 위험지역 삭제",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def del_my_danger(user_id, latitude, longitude, my_latitude, my_longitude):
    user_row = db.session.query(User).filter(User.id == user_id).first()
    nickname = user_row.nickname

    danger_row = db.session.query(Danger).filter((Danger.nickname == nickname) & (Danger.latitude == latitude) & (Danger.longitude == longitude) & (Danger.is_delete == 'N')).first()
    if danger_row: #본인이 등록한 경우
        danger_row.is_delete = 'Y'
        db.session.commit()
        return response_json_with_code(result = "success")
    else:
        is_closer = False
        is_exist = False
        
        riding_row = db.session.query(RidingEach).filter(RidingEach.user_id == user_id).all()
        if not riding_row == []:
            for row in riding_row:
                tmp_latitude = []
                tmp_longitude = []
                tmp_latitude.append(row.northeast_lati)
                tmp_latitude.append(row.southwest_lati)
                tmp_longitude.append(row.northeast_long)
                tmp_longitude.append(row.southwest_long)
                if (min(tmp_latitude) <= latitude) and (latitude <= max(tmp_latitude)) and (min(tmp_longitude) <= longitude) and (longitude <= max(tmp_longitude)):
                    is_exist = True
        
        mark_location = (latitude, longitude)
        my_location = (my_latitude, my_longitude)
        
        if haversine(mark_location, my_location, unit = 'm') <= 600.0:
            is_closer = True
        
        if is_closer or is_exist:
            danger_row = db.session.query(Danger).filter((Danger.latitude == latitude) & (Danger.longitude == longitude) & (Danger.is_delete == 'N')).first()
            danger_row.is_delete = 'Y'
            db.session.commit()
            return response_json_with_code(200, result="success")
        else:
            return response_json_with_code(400, result="fail")
                
    
@board_bp.route("/dimage/<filename>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="riding image donwload",
    description="image download"
)
def ddonwload(filename):
    # row = RidingEach.get_one_by_unique_id(unique_id)
    # if row:
    abspath = os.path.abspath(path)
    return send_from_directory(abspath, filename)


@board_bp.route("/mydanger/<user_id>/<int:page>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="내가 등록한 위험요소",
    description="내가 등록한 위험요소 5개 반환",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_my_danger(user_id, page):
    user_row = db.session.query(User).filter(User.id == user_id).first()
    count = -1
    if page == 0:
        count = db.session.query(Danger).filter(Danger.nickname==user_row.nickname).count()
    
    nickname = user_row.nickname
    
    rows = db.session.query(Danger)\
            .filter(Danger.nickname==nickname)\
            .order_by(Danger.time.desc())\
            .slice(page, page+15)\
            .all()
    
    result = []
    if rows == []:
        return response_json_with_code(
            result=result,
        )
        
    for row in rows:
        result.append({
            "nickname" : row.nickname,
            "title" : row.title,
            "time" : row.time,
            "is_delete" : row.is_delete,
            "region" : row.region,
            "region_detail" : row.region_detail,
            "danger_id" : row.id,
            "count":count
        })
            
    return response_json_with_code(result=result)
    

@board_bp.route("/delete-near-danger", methods=["POST"])
@use_kwargs(RequestDeleteNearDanger)
@doc(
    tags=[API_CATEGORY],
    summary="현재 위치 근처의 위험지역 삭제",
    description="현재 위치 근처의 위험지역 삭제",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def del_near_danger(latitude,longitude):
    danger_row = db.session.query(Danger).filter((Danger.latitude == latitude) & (Danger.longitude == longitude)).first()
    if danger_row:
        danger_row.is_delete = 'Y'
        db.session.commit()
    return response_json_with_code(result = 'success')


@board_bp.route("/all-danger", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="모든 위험정보 반환",
    description="모든 위험정보 반환",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def all_danger():
    danger_list = []
    danger_row = db.session.query(Danger).all()
    if danger_row == []:
        return response_json_with_code(result = danger_list)
    for row in danger_row:
        if row.is_delete == 'N':
            tmp_list = []
            tmp_list.append(row.latitude)
            tmp_list.append(row.longitude)
            tmp_list.append(float(row.id))
            danger_list.append(tmp_list)
            
    return response_json_with_code(result = danger_list)

@board_bp.route("/shift-mydanger", methods=["POST"])
@use_kwargs(RequestDeleteMyDanger)
def shift_mydanger(danger_id):
    row = Danger.query.filter(Danger.id == danger_id).one_or_none()
    if row.is_delete == "N":
        row.is_delete = "Y"
    else:
        row.is_delete = "N"
        
    db.session.commit()
    
    return response_json_with_code(result="success")


@board_bp.route("/danger/<int:danger_id>", methods=["GET"])
def get_my_danger_one(danger_id):
    row = Danger.query.filter(Danger.id==danger_id).one_or_none()
    
    result = {
        "title":row.title,
        "contents":row.contents,
        "time":row.time,
        "is_delete":row.is_delete,
        "image":row.image,
        "region":row.region,
        "region_detail":row.region_detail,
        "period":row.period,
        "nickname":row.nickname
    }
    
    return response_json_with_code(result=result)
