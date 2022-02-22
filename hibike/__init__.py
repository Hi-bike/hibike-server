import os
import sys
import inspect

# swagger, OpenAPI 명세 작성
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask  # Falsk 2.0.0부터는 FlaskApiSpec이 동작하지 않는다. v1.1.4를 사용했다.
from flask_apispec.extension import FlaskApiSpec
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
base_dir = os.getcwd()
sys.path.append(base_dir)
try:
    app.config.from_pyfile(f"{base_dir}/hibike/default.cfg")
except FileNotFoundError:
    f = open(f"{base_dir}/hibike/default.cfg", "w")
    f.write(inspect.cleandoc("""
        SECRET_KEY="default_secret_key"
        SQLALCHEMY_DATABASE_URI="mariadb+pymysql://root:backstart@db:3306/hibike?charset=utf8"
        JWT_SECRET_KEY="default_jwt_secret_key"
        JWT_ACCESS_TOKEN_EXPIRES=180
        """))
    f.close()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
app.config.update({
    "APISPEC_SPEC": APISpec(
        title="hibike api",
        version="v1",
        openapi_version="2.0.0",
        plugins=[MarshmallowPlugin()],
    ),
    "APISPEC_SWAGGER_URL": "/docs.json",
    "APISPEC_SWAGGER_UI_URL": "/docs/"
})
CORS(app, supports_credentials=True)
docs = FlaskApiSpec(app)

from hibike.models import *
db.init_app(app)
migrate.init_app(app, db)

from hibike.models.common.cdn import CDN
cdn = CDN()
# 도커환경에서 작업할 경우: docker=True
cdn.set_cdn_url(app.config['CDN_URL'], docker=True)

mail = Mail(app)

from hibike.controllers.auth import auth_bp
from hibike.controllers.board import board_bp
app.register_blueprint(auth_bp)
app.register_blueprint(board_bp)

docs.register_existing_resources()
# 스웨거에서 options 제거
for key, value in docs.spec._paths.items():
    docs.spec._paths[key] = {
        inner_key: inner_value for inner_key, inner_value in value.items() if inner_key != "options"
    }
