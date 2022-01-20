from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

API_CATEGORY = "Auth"

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

from scrimdor.controllers.auth.signin import *
from scrimdor.controllers.auth.signup import *
from scrimdor.controllers.auth.setup import *
from scrimdor.controllers.auth.guest import *
from scrimdor.controllers.auth.user import *
from scrimdor.controllers.auth.withdrawal import *