from flask import request
from flask_apispec import doc, use_kwargs
from scrimdor.controllers.admin import (
    API_CATEGORY,
    admin_bp,
)
from scrimdor.utils.common import (
    response_json_with_code
)
from scrimdor.schema.admin import (
    RequestAdminKeySchema,
    RequestGameSchema,
)
from scrimdor import mongo, cdn, app


@admin_bp.route('/add-game', methods=['POST'])
@doc(
    tags=[API_CATEGORY],
    summary="지원하는 게임 등록",
    description="클라이언트용(form)\
        game: 게임이름\
        file: 이미지파일(게임이름과 같은 이름으로 보내야됨)"
)
def register_game():
    key = request.form.get("key")
    if key == app.config['ADMIN_KEY']:
        game = request.form.get("game")
        file = request.files.get("file")
        mongo.db.game_list.insert_one({
            game:{
                'game':game,
                'image':cdn.send_defualt_file(file=file, filename=file.filename)
            }
        })
        return str(mongo.db.game_list.find())
    
    return response_json_with_code(403)


@admin_bp.route('/delete-game', methods=['POST'])
@use_kwargs(RequestGameSchema)
@doc(
    tags=[API_CATEGORY],
    summary="지원하는 게임 삭제",
    description="클라이언트용"
)
def delete_game(key, game):
    if key == app.config['ADMIN_KEY']:
        filename = mongo.db.game_list.find_one({f"{game}.game":game})[game]["image"]
        mongo.db.game_list.delete_one({f"{game}.game":game})
        cdn.delete_file(filename)
        
        return response_json_with_code()
    
    return response_json_with_code(403)


@admin_bp.route('/gamelist', methods=['POST'])
@use_kwargs(RequestAdminKeySchema)
@doc(
    tags=[API_CATEGORY],
    summary="지원하는 전체 게임 반환",
    description="클라이언트용"
)
def get_games(key):
    if key == app.config['ADMIN_KEY']:
        games = mongo.db.game_list.find({})
        result = []
        
        for game in games:
            del(game['_id'])
            result.append(game[list(game.keys())[0]])
            
        return result
    
    return response_json_with_code(403)


@admin_bp.route('/game', methods=['POST'])
@use_kwargs(RequestGameSchema)
@doc(
    tags=[API_CATEGORY],
    summary="지원하는 게임 하나 반환",
    description="클라이언트용"
)
def get_game(key, game):
    if key == app.config['ADMIN_KEY']:
        game = mongo.db.game_list.find_one({f"{game}.game":game})
        del(game['_id'])
            
        return game
    
    return response_json_with_code(403)