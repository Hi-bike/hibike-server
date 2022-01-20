from scrimdor import app
import requests


class KakaoAuth:
    def __init__(self):
        self.auth_server = "https://kauth.kakao.com%s"
        self.api_server = "https://kapi.kakao.com%s"
        self.default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }

    def get_auth(self, request_type, code):
        if request_type == 'login':
            redirect_uri = app.config['KAKAO_LOGIN_REDIRECT_URI']
        elif request_type == 'authentication':
            redirect_uri = app.config['KAKAO_AUTH_REDIRECT_URI']
        
        return requests.post(
            url=self.auth_server % "/oauth/token", 
            headers=self.default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": app.config['KAKAO_CLIENT_ID'],
                "client_secret": app.config['KAKAO_CLIENT_SECRET'],
                "redirect_uri": redirect_uri,
                "code": code,
            }, 
        ).json()
        

    def get_userinfo(self, bearer_token):
        return requests.post(
            url=self.api_server % "/v2/user/me", 
            headers={
                **self.default_header,
                **{"Authorization": bearer_token}
            },
            data={}
        ).json()