from hibike import db, app

class Danger(db.Model):
    __tablename__ = "danger"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    nickname = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    contents = db.Column(db.Text)
    location = db.Column(db.String(30), nullable=False)
    time = db.Column(db.DateTime)
    update_nickname = db.Column(db.Integer, nullable=True)
    update_time = db.Column(db.DateTime, nullable=True)
    danger_type = db.Column(db.String(30), nullable=True)
    is_delete = db.Column(db.String(1), default="N")
    id = db.Column(db.Integer, primary_key = True)

class Board(db.Model):
    __tablename__ = "board"
    __table_args__ = {"mysql_collate" : "utf8_bin"}
    nickname = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    contents = db.Column(db.Text)
    time = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key = True)