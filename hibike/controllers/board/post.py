from flask import request, session
from flask_apispec import doc, use_kwargs
from hibike import app, db
from hibike.models.board import Board,Reply
from hibike.models.auth import User, UserRiding
from hibike.models.common.redis_conn import RedisConn
from hibike.controllers.board import (
    API_CATEGORY,
    board_bp
)
from hibike.schema.user import (
    RequestPostSchema,
    RequestReplySchema,
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
    result = {}
    if rows == []:
        return response_json_with_code(
            is_last = "True"
        )
    i = 1
    for row in rows:
        # if i == 1:
        #     index = "first"
        # elif i == 2:
        #     index = "second"
        result[i]= row.to_dict()
        i+=1
    return response_json_with_code(
        result=result,
        is_last = "False"
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
        time=time
    ))
    db.session.commit()

    return response_json_with_code(
        result="Success"
    )

@board_bp.route("/reply", methods=["POST"])
@use_kwargs(RequestReplySchema)
@doc(
    tags=[API_CATEGORY],
    summary="reply 쓰기",
    description="댓글 쓰기",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def write_reply(contents, id, post_id):
    user_row = db.session.query(User).filter(User.id == id).first()
    KST = timezone('Asia/Seoul')
    time = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')

    db.session.add(Reply(
        post_id = post_id,
        contents=contents,
        nickname = user_row.nickname,
        time=time
    ))
    db.session.commit()

    return response_json_with_code(
        result="Success"
    )    

@board_bp.route("/reply/<int:page>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="댓글 반환",
    description="현재 게시글의 댓글 5개 반환",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_reply(page): 
    query = db.session.query(Reply).order_by(Reply.time.asc()).slice((page - 1) * 5, page * 5)
    rows = query.all()
    result = {}
    if rows == []:
        return response_json_with_code(
            is_last = "True"
        )
    i = 1
    for row in rows:
        # if i == 1:
        #     index = "first"
        # elif i == 2:
        #     index = "second"
        result[i]= row.to_dict()
        i+=1
    return response_json_with_code(
        result=result,
        is_last = "False"
    )