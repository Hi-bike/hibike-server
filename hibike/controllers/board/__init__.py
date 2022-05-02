from flask import Blueprint

board_bp = Blueprint("board", __name__, url_prefix="/api/board")

API_CATEGORY = "Board"

authorization_header = {
    "Authorization": {
        "description":
        "Autorization HTTP header with JWT access token,\
        like: Autorization: Bearer header.payload.signature",
        "in":
        "header",
        "type":
        "string",
        "required":
        True
    }
}

from hibike.controllers.board.post import *
from hibike.controllers.board.danger import *

