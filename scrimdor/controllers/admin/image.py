from flask import request
from flask_apispec import doc, use_kwargs
from scrimdor.controllers.admin import (
    API_CATEGORY,
    admin_bp,
)
from scrimdor import cdn, app
from scrimdor.utils.common import response_json_with_code

@admin_bp.route('/cdn',methods=['POST'])
@doc(
    tags=[API_CATEGORY],
    summary="cdn으로 이미지 보내기",
    description="클라이언트용\
    key, file(form)",
)
def send_image():
    key = request.form.get("key")
    if key == app.config['ADMIN_KEY']:
        file = request.files.get("file")
        profile_image_name = cdn.send_defualt_file(file=file, filename=file.filename)
        return{
            "profile_image_url": cdn.get_image_path(profile_image_name)
        }
    return response_json_with_code(403)