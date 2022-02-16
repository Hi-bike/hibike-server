import os
import requests
from furl import furl
from io import BufferedReader
from werkzeug.datastructures import FileStorage
from hibike import app
from hibike.utils.common import check_mime_type


class CDN():
    def __init__(self):
        self.cdn_url = None
        self.docker = None

    def set_cdn_url(self, cdn_url=None, docker=False):
        self.docker = docker
        if self.docker:
            self.cdn_url = furl("http://scrimdor-cnd:4000")
        else:
            self.cdn_url = furl(cdn_url)
            
    def _send_file(self, filename, image, content_type):
        res = requests.post(
            self.cdn_url.copy().set(path="/image/upload").url,
            files={"file": (filename, image, content_type)}
        )
        return res.status_code

    def _delete_file(self, filename):
        res = requests.delete(
            self.cdn_url.copy().set(path="/image/delete").url,
            json={"filename":filename}
        )
        return res.status_code

    def get_image_path(self, filename):
        if self.docker:
                return furl(app.config['CDN_URL']).copy().set(path=f"/image/{filename}").url
        return self.cdn_url.copy().set(path=f"/image/{filename}").url

    def send_stream_file(self, file: FileStorage, id: int, kinds):
        # 유저가 업로드한 파일 등 파일스트림을 전달받아 전송하는 메소드
        if not check_mime_type(file.content_type):
            return None
        image = BufferedReader(file)
        # now_time = int(time.time())
        root, ext = os.path.splitext(file.filename)
        filename = f"{id}_{kinds}{ext}"
        status_code = self._send_file(filename=filename, image=image, content_type=file.content_type)        
        if status_code == 200:
            return filename
        else:
            return "default.png"

    def send_defualt_file(self, filename, file: FileStorage):
        image = BufferedReader(file)
        root, ext = os.path.splitext(file.filename)
        filename = filename.replace(" ","_")
        status_code = self._send_file(filename=filename, image=image, content_type=file.content_type)
        if status_code == 200:
            return filename
        else:
            return None
        
    def delete_file(self, filename):
        if filename and filename != 'default.png':
            filename = filename.replace(" ","_")
            filename = filename.replace(app.config['CDN_URL']+'/image/','')
            filename = filename.replace('/image/','')
            status_code = self._delete_file(filename)
            if status_code == 200:
                return filename
            else:
                return None