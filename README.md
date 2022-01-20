# 개발 환경
* Python 3.9
* Docker
* Docker-compose
* Flask
* Nginx
* Gunicorn
* MariaDB

# 프로젝트 구조
```
scrimdor-server/
    __init__.py
    app.py              # App Config 및 API Endpoint 라우팅
    scrimdor/
         controllers/     # API Endpoint 라우팅
            __init__.py
            board/
               __init__.py
               post.py
               reply.py 
            auth/
               __init__.py
               user.py
         models/           # API별 로직 구현
            __init__.py
            auth.py 
            board.py
         schema/           # API별 입출력 스키마 정의
```

# Code Style Check
```
flake8 --max-line-length 105
```

# DB 초기 설정
Docker 컨테이너 속에서
```
docker exec -it mysql /bin/bash
mysql -u root -p
create database scrimdor;
```
로컬 터미널에서
```
./db-migrate-oneshot.sh
```

# API 문서
```
http://127.0.0.1/docs/
```
# 개발 가이드
## For Windows (Native)
### Windows 로컬 환경에서 개발하기 위한 방법

* 프로젝트 Clone
```
git clone https://github.com/ScrimdorTest/scrimdor-server.git
```

* MariaDB (10.6 stable) 다운로드 및 설치

   * https://downloads.mariadb.org/interstitial/mariadb-10.6.3/winx64-packages/mariadb-10.6.3-winx64.msi/from/https%3A//mirror.yongbok.net/mariadb/
 
* 설치 후 MySQL Client (MariaDB 10.6) 실행
* 설치 시 입력한 비밀번호를 이용하여 접속 후 아래 커맨드 실행
```
source ${PROJECT_PATH}/init/init.sql
```

* 설치 시 입력한 계정 정보를 기반으로 /scrimdor/default.cfg 설정
  * 기본적으로 user는 root로 설정이 되어 있을 것입니다.

* */scrimdor/default.cfg* for Windows (example)
```
SECRET_KEY="{flask_secret_key}"
SQLALCHEMY_DATABASE_URI="mariadb+pymysql://{user_id}:{user_password}@{host}:{port}/{database name}?charset=utf8"
JWT_SECRET_KEY="{jwt_secret_key}"
JWT_ACCESS_TOKEN_EXPIRES=1800
MAIL_SERVER = "smtp.gmail.com"
CDN_URL = {cdn_url ex)http://127.0.0.1}
MAIL_PORT = 465
MAIL_USERNAME = "lmwljw96@gmail.com"
MAIL_PASSWORD = ""
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_AUTH_LINK = "http://127.0.0.1/api/auth/check-emailauth?jwt="
```
* 실행 방법
```
cd scrimdor-server 
pip install -r requirements.txt
(virtualenv를 사용하는 것을 매우 강력히 추천합니다.)
python run.py {port(ex:5000)}
```
***

## For Docker
* 최초 실행 시
```
docker-compose up -d --build
# 최초 빌드 후 DB service 시작하는데 좀 걸릴 수 있음.
```

* 시작
```
docker-compose start
```

* 종료
```
docker-compose stop
```

* 코드 변경 후 재시작
```
docker-compose restart
```

* 종료 및 삭제
```
docker-compose down
```

# 오류 해결법
* Windows WSL 환경에서 db 폴더 삭제 후 빌드 시 오류 발생하는 경우
  * Docker Desktop 재시작하기

* Windows WSL 환경에서 ./ 오류 발생하는 경우
   * sed -i 's/\r$//' {file_name}.sh

* Windows WSL 환경에서 Docker Mysql container 오류
   * docker mysql cli 실행
   * use mysql;
   * select user, host from user;
   * create user 'root'@'%' identified by '{mysql_password}';
   * grant all privileges on *.* to 'root'@'%' identified by '{mysql_password}';
   * mariadb.sys,'root'@'%' 유저를 제외한 모든 유저 삭제
