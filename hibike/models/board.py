from email.policy import default
from hibike import db, app

class Danger(db.Model):
    __tablename__ = "danger"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    nickname = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    contents = db.Column(db.Text)
    latitude = db.Column(db.Float(50), nullable=False)
    longitude = db.Column(db.Float(50), nullable=False)
    time = db.Column(db.DateTime)
    is_delete = db.Column(db.String(1), default="N")
    image = db.Column(db.String(50), nullable=True)
    region = db.Column(db.String(50), nullable=False)
    region_detail = db.Column(db.String(50), nullable=False)
    period = db.Column(db.Integer, default=15)
    id = db.Column(db.Integer, primary_key = True)

    def to_dict(self):
        return {
        "id" : self.id,
        "nickname" : self.nickname,
        "region" : self.region,
        "region_detail" : self.region_detail,
        "image" : self.image,
        "period" : self.period,
        "time" : self.time,
        "title" : self.title,
        "contents" : self.contents,
    }

class Board(db.Model):
    __tablename__ = "board"
    __table_args__ = {"mysql_collate" : "utf8_bin"}
    nickname = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    contents = db.Column(db.Text)
    time = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key = True)

    def to_dict(self):
        return {
        "id" : self.id,
        "nickname" : self.nickname,
        "title" : self.title,
        "contents" : self.contents,
    }

class Reply(db.Model):
    __tablename__ = "reply"
    __table_args__ = {"mysql_collate" : "utf8_bin"}
    nickname = db.Column(db.String(30), nullable=False)
    contents = db.Column(db.Text)
    time = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key = True)

    def to_dict(self):
        return {
        "id" : self.id,
        "nickname" : self.nickname,
        "contents" : self.contents,
        "post_id" : self.post_id
    }