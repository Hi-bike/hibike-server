from hibike import db, app

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    nickname = db.Column(db.String(30), nullable=False)
    fcm_token = db.Column(db.String(300), nullable=True)

    @staticmethod
    def get_user_by_id(id):
        return User.query.filter(
            User.id == id
        ).one_or_none()

    @staticmethod
    def get_user_by_idx(idx):
        return User.query.filter(
            User.idx == idx
        ).one_or_none()

    @staticmethod
    def get_user_by_nickname(nickname):
        return User.query.filter(
            User.nickname == nickname
        ).one_or_none()
        
    def to_dict(self):
        return {
            "id" : self.id,
            "nickname" : self.nickname,
        }

class UserRiding(db.Model):
    __tablename__ = "user_riding"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    user_idx = db.Column(db.String(30), nullable=False)
    distance = db.Column(db.Float(10), default=0)
    time = db.Column(db.String(30), default=0)
    id = db.Column(db.Integer, primary_key = True)

    @staticmethod
    def get_user_riding_by_idx(idx):
        return UserRiding.query.filter(
            UserRiding.user_idx == idx
        ).one_or_none()

    def to_dict(self):
        return {
            "distance" : self.distance,
            "time" : self.time,
        }