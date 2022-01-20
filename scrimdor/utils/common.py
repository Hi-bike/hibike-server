from flask import jsonify, make_response
import string
import random

def response_json_with_code(res_code=200, **kwargs):
    return make_response(jsonify(kwargs), res_code)


def check_mime_type(content_type):
    image_mime_type = ['image/gif', 'image/png', 'image/jpeg', 'image/bmp', 'image/webp']
    if content_type in image_mime_type:
        return True
    else: return False
    

def gen_unique_id():
    unique_id = ""
    string_pool = string.ascii_uppercase + string.digits #영어 대문자 + 숫자
    for i in range(6):
        unique_id += random.choice(string_pool)
        
    return unique_id