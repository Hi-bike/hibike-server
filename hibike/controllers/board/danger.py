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
    danger_list = [37.504766,126.751009]
    range_list = []
    ranges = request.form.get('ranges')
    len_range = ranges.count(",") + 1
    is_included = False
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

        latitude_list = sorted(latitude_list, reverse=False)
        longitude_list = sorted(longitude_list, reverse=False)

        if latitude_list[0] < danger_list[0] and latitude_list[3] > danger_list[0] and longitude_list[0] < danger_list[1] and longitude_list[3] > danger_list[1]:
            is_included = True

    return response_json_with_code(
        danger_list = danger_list,
        latitude_list = latitude_list,
        longitude_list = longitude_list,
        is_included = is_included
    )
