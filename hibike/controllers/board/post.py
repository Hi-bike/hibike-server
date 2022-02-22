from flask import request, session
from flask_apispec import doc, use_kwargs
from hibike import app, db
from hibike.models.board import Board
from hibike.models.auth import User, UserRiding
from hibike.models.common.redis_conn import RedisConn
from hibike.controllers.board import (
    API_CATEGORY,
    board_bp
)
from hibike.schema.user import (
    RequestPostSchema,
)
from hibike.utils.common import (
    response_json_with_code,
)
import requests
import json
from datetime import datetime
import time
from pytz import timezone

@board_bp.route("/posts/<int:page>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="자유게시판 글 반환",
    description="현재 페이지의 글 5개 반환",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_posts(page): 
    query = db.session.query(Board).order_by(Board.time.desc()).slice((page - 1) * 5, page * 5)
    rows = query.all()
    result = []
    if rows == []:
        return response_json_with_code(
            result=result,
            is_last = True
        )
    # for row in rows:
    #     result.append(row.to_dict())

    return response_json_with_code(
        result=result,
        is_last = False
    )

@board_bp.route("/post", methods=["POST"])
@use_kwargs(RequestPostSchema)
@doc(
    tags=[API_CATEGORY],
    summary="post 쓰기",
    description="포스트 쓰기",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def write_post(title, contents, id):
    user_row = db.session.query(User).filter(User.id == id).first()
    KST = timezone('Asia/Seoul')
    time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')

    db.session.add(Board(
        title=title,
        contents=contents,
        nickname = user_row.nickname,
        create_date=time
    ))
    db.session.commit()

    return response_json_with_code(
        result="Success"
    )