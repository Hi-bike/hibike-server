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
    RequestDeleteMyPost,
    RequestPostSchema,
    RequestReplySchema,
    RequestMyPosts,
)
from hibike.utils.common import (
    response_json_with_code,
)
import requests
import json
from datetime import datetime
import time
from pytz import timezone


# TODO: 경로상 위험요소 탐색

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

@board_bp.route("/reply/<int:page>/<int:post_id>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="댓글 반환",
    description="현재 게시글의 댓글 5개 반환",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_reply(page,post_id): 
    query = db.session.query(Reply).filter(Reply.post_id == post_id).order_by(Reply.time.asc()).slice((page - 1) * 5, page * 5)
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

@board_bp.route("/post_content/<int:post_id>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="게시글 내용 반환",
    description="게시글 내용 반환",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_posts_contents(post_id): 
    row = db.session.query(Board).filter(Board.id == post_id).first()
    
    return response_json_with_code(
        title = row.title,
        contents = row.contents,
        nickname = row.nickname
    )

@board_bp.route("/reply_content/<int:reply_id>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="게시글 내용 반환",
    description="게시글 내용 반환",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_reply_contents(reply_id): 
    row = db.session.query(Reply).filter(Reply.id == reply_id).first()
    
    return response_json_with_code(
        contents = row.contents,
        nickname = row.nickname
    )

@board_bp.route("/myposts/<user_id>/<int:page>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="내가 작성한 게시글",
    description="내가 작성한 게시글 5개 반환",
    responses={200: {"description" : "success response"},
               401: {"description" : "Unauthorized"},
    }
)
def get_my_posts(user_id, page):
    user_row = db.session.query(User).filter(User.id == user_id).first()
    count = -1
    if page == 0:
        count = db.session.query(Board).filter(Board.nickname==user_row.nickname).count()
        
    nickname = user_row.nickname
    
    rows = db.session.query(Board)\
            .filter(Board.nickname==nickname)\
            .order_by(Board.time.desc())\
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
            "contents":row.contents,
            "time" : row.time,
            "board_id" : row.id,
            "count":count
        })
            
    return response_json_with_code(result=result)


@board_bp.route("delete-mypost", methods=["POST"])
@use_kwargs(RequestDeleteMyPost)
def delete_mypost(post_id):
    Board.query.filter(Board.id==post_id).delete()
    db.session.commit()
    
    return response_json_with_code(result="success")
