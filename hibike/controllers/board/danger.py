from pstats import SortKey
from flask import request, session
from flask_apispec import doc, use_kwargs
from hibike import app, db
from hibike.models.board import Board,Reply,Danger
from hibike.models.auth import User, UserRiding
from hibike.models.common.redis_conn import RedisConn
from hibike.controllers.board import (
    API_CATEGORY,
    board_bp
)
from hibike.utils.common import (
    response_json_with_code,
)
from hibike.schema.user import (
    RequestPostDangerSchema
)
import requests
import json
from datetime import datetime
import time
from pytz import timezone

@board_bp.route("/danger", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="범위내 등록된 위험정보 가져오기",
    description="범위내 등록된 위험정보 가져오기",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_danger():
    danger_list = []
    range_list = []
    db_latitude = []
    db_longitude = []
    ranges = request.form.get('ranges')
    len_range = ranges.count(",") + 1
    
    danger_row = db.session.query(Danger).all()
    if danger_row == []:
        return response_json_with_code(
            danger_list = danger_list
        )
    for row in danger_row:
        db_latitude.append(row.latitude)
        db_longitude.append(row.longitude)

    for i in range(len_range):
        range_list.append(float(ranges.split(",")[i]))
    
    for i in range(int(len(range_list)/8)):
        latitude_list = []
        longitude_list = []
        for j in range(i*8,i*8+8):
            if j%2 != 1:
                latitude_list.append(range_list[j])
            else:
                longitude_list.append(range_list[j])

        for j in range(len(db_latitude)):
            if min(latitude_list) <= db_latitude[j] and max(latitude_list) >= db_latitude[j] and min(longitude_list) <= db_longitude[j] and max(longitude_list) >= db_longitude[j]:
                if db_latitude[j] not in danger_list and db_longitude[j] not in danger_list:
                    danger_list.append(db_latitude[j])
                    danger_list.append(db_longitude[j])

    return response_json_with_code(
        danger_list = danger_list
    )

@board_bp.route("/post-danger", methods=["POST"])
@use_kwargs(RequestPostDangerSchema)
@doc(
    tags=[API_CATEGORY],
    summary="위험지역 등록",
    description="위험지역 등록",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def post_danger(id, title, contents, latitude, longitude):
    user_row = db.session.query(User).filter(User.id == id).first()
    KST = timezone('Asia/Seoul')
    time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')

    db.session.add(Danger(
        title=title,
        contents=contents,
        nickname = user_row.nickname,
        latitude = latitude,
        longitude = longitude,
        time=time
    ))
    db.session.commit()

    return response_json_with_code(
        result="Success"
    )