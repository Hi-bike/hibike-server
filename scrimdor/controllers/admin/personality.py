from flask_apispec import doc, use_kwargs
from scrimdor.controllers.admin import (
    API_CATEGORY,
    admin_bp,
)
from scrimdor import mongo, app
from scrimdor.schema.admin import(
    RequestPersonalitySchema,
    RequestAdminKeySchema
)
from scrimdor.utils.common import (
    response_json_with_code
) 
 
@admin_bp.route('/add-personality', methods=['POST'])
@use_kwargs(RequestPersonalitySchema)
@doc(
    tags=[API_CATEGORY],
    summary="DB에 성향 태그 등록",
    description="클라이언트용"
)
def register_personality(key, personality):
    if key == app.config['ADMIN_KEY']:
        mongo.db.personality_list.update_one(
            {},
            {'$push':{
                'personality_list':personality
            }},
            upsert = True
        )
        return mongo.db.personality_list.find_one()['personality_list']
     
    return response_json_with_code(403)


@admin_bp.route('/delete-personality', methods=['POST'])
@use_kwargs(RequestPersonalitySchema)
@doc(
    tags=[API_CATEGORY],
    summary="DB에 성향 태그 삭제",
    description="클라이언트용"
)
def delete_personality(key, personality):
    if key == app.config['ADMIN_KEY']:
        mongo.db.personality_list.update_one(
            {},
            {'$pull':{
                'personality_list':personality
            }}
        )
        return mongo.db.personality_list.find_one()['personality_list']
     
    return response_json_with_code(403)
