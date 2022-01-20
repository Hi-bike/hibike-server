from scrimdor import db, app

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    nickname = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(15))
    birth = db.Column(db.String(15))
    email_auth = db.Column(db.Integer, default=0)
    introduction = db.Column(db.Text)
    profile_image_name = db.Column(db.String(150))
    platform_type = db.Column(db.String(20), default="scrimdor")
    is_ban = db.Column(db.Integer, default=0)

    @staticmethod
    def get_user_by_id(id):
        return User.query.filter(
            User.id == id
        ).one_or_none()

    @staticmethod
    def get_user_by_unique_id(unique_id):
        return User.query.filter(
            User.unique_id == unique_id
        ).one_or_none()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter(
            User.email == email
        ).one_or_none()

    @staticmethod
    def get_user_by_nickname(nickname):
        return User.query.filter(
            User.nickname == nickname
        ).one_or_none()
    
    @staticmethod
    def get_user_by_email_and_platform(email, platform_type):
        return User.query.filter(
            (User.email==email)&
            (User.platform_type == platform_type)
        ).one_or_none()
        
    def to_dict_profile(self):
        return {
            "unique_id":self.unique_id,
            "nickname": self.nickname,
            "introduction":self.introduction,
            "profile_image_name": str(self.profile_image_name),
            "is_guest":False
        }
    
    def to_dict_current_profile(self):
        return {
            "unique_id":self.unique_id,
            "nickname": self.nickname,
            "profile_image_name": str(self.profile_image_name),
            "platform_type":self.platform_type,
            "is_guest":False
        }

    def to_dict(self):
        return {
            "id": self.id,
            "unique_id":self.unique_id,
            "email":self.email,
            "nickname": self.nickname,
            "gender":self.gender,
            "birth":self.birth,
            "introduction":self.introduction,
            "email_auth": self.email_auth,
            "profile_image_name": str(self.profile_image_name),
            "is_ban":self.is_ban
        }