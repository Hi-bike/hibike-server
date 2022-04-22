from hibike import db, app

NUMBER_OF_INFO_PER_PAGE = 8

class RidingAve(db.Model):
    __tablename__ = "riding_ave"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    user_id = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime)
    riding_time = db.Column(db.String(30), nullable=True)
    ave_speed = db.Column(db.String(30), nullable=True)
    ave_distance = db.Column(db.String(30), nullable=True)
    id = db.Column(db.Integer, primary_key = True)
    
    @staticmethod
    def create(user_id, riding_time, ave_speed, ave_distance, time):
        db.session.add(RidingAve(
            user_id=user_id,
            riding_time=riding_time,
            ave_speed=ave_speed,
            ave_distance=ave_distance,
            create_time=time
        ))
        db.session.commit()
        
    @staticmethod
    def get_one_by_id(id):
        return RidingAve.query.filter(
            id==id
        ).first()
    
    @staticmethod
    def get_one_by_user_id(user_id):
        return RidingAve.query.filter(
            user_id==user_id
        ).one_or_none()
    
    @staticmethod
    def get_all_by_user_id(user_id):
        return RidingAve.query.filter(
            user_id==user_id
        ).all()
    
    @staticmethod
    def get_all_by_page(user_id, page):
        return db.session.query(RidingAve)\
            .filter(RidingAve.user_id==user_id)\
            .order_by(RidingAve.riding_time.desc())\
            .slice(page, page+NUMBER_OF_INFO_PER_PAGE)\
            .all()
        
    
class RidingTotal(db.Model):
    __tablename__ = "riding_total"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    user_id = db.Column(db.String(30), nullable=False)
    total_time = db.Column(db.String(30), nullable=True)
    total_distance = db.Column(db.String(30), nullable=True)
    id = db.Column(db.Integer, primary_key = True)
    
        
    @staticmethod
    def update(user_id, riding_time, ave_speed, ave_distance):
        row = RidingTotal.get_by_user_id(user_id)
        if row:
            splited_time = row.total_time.split(" : ")
            total_minute = splited_time[0]
            total_second = splited_time[1]
            
            splited_time = riding_time.split(" : ")
            riding_minute = splited_time[0]
            riding_second = splited_time[1]
            
            row.riding_time = (int(total_minute) + int(riding_minute)) + " : " + (int(total_second) + int(riding_second))
            row.total_distance = float(row.total_distance) + float(ave_distance)
            
            db.session.commit()
        else:
            db.session.add(RidingTotal(
                user_id=user_id,
                total_time=riding_time,
                total_distance=ave_distance
            ))
            db.session.commit()
            
    @staticmethod
    def get_by_user_id(user_id):
        return RidingTotal.query.filter(
            user_id==user_id
        ).first()
    
    