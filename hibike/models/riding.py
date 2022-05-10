from hibike import db, app

OFFSET = 15

class RidingEach(db.Model):
    __tablename__ = "riding_each"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    user_id = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime)
    riding_time = db.Column(db.String(30), nullable=True)
    ave_speed = db.Column(db.String(30), nullable=True)
    distance = db.Column(db.String(30), nullable=True)
    starting_region = db.Column(db.String(30), default="") #출발지
    end_region = db.Column(db.String(30), default="") #도착지
    image = db.Column(db.String(30), nullable=True)
    unique_id = db.Column(db.String(30), nullable=True)
    count = db.Column(db.Integer, default=0)
    northeast_lati = db.Column(db.Float(50), nullable=True)
    northeast_long = db.Column(db.Float(50), nullable=True)
    southwest_lati = db.Column(db.Float(50), nullable=True)
    southwest_long = db.Column(db.Float(50), nullable=True)
    id = db.Column(db.Integer, primary_key = True)
    
    @staticmethod
    def create(user_id, unique_id, riding_time, ave_speed, distance, create_time):
        count = RidingEach.query.filter(RidingEach.user_id==user_id).count()
        
        db.session.add(RidingEach(
            user_id=user_id,
            unique_id=unique_id,
            riding_time=riding_time,
            ave_speed=ave_speed,
            distance=distance,
            create_time=create_time,
            count=count+1
        ))
        db.session.commit()
        
    @staticmethod
    def multi_create(user_id, unique_id, riding_time, ave_speed, distance
                    ,starting_region, end_region, northeast_lati, northeast_long, southwest_lati, southwest_long, image, create_time):
        count = RidingEach.query.filter(RidingEach.user_id==user_id).count()
        
        db.session.add(RidingEach(
            user_id=user_id,
            unique_id=unique_id,
            riding_time=riding_time,
            ave_speed=ave_speed,
            distance=distance,
            starting_region=starting_region,
            end_region=end_region,
            northeast_lati=northeast_lati,
            northeast_long=northeast_long,
            southwest_lati=southwest_lati,
            southwest_long=southwest_long,
            image=image,
            create_time=create_time,
            count=count+1
        ))
        db.session.commit()
                
    @staticmethod
    def get_one_by_id(id):
        return RidingEach.query.filter(
            RidingEach.id == id
        ).one_or_none()
        
    @staticmethod
    def get_one_by_unique_id(unique_id):
        return RidingEach.query.filter(
            RidingEach.unique_id == unique_id
        ).one_or_none()
    
    @staticmethod
    def get_one_by_user_id(user_id):
        return RidingEach.query.filter(
            RidingEach.user_id == user_id
        ).one_or_none()
    
    @staticmethod
    def get_all_by_user_id(user_id):
        return RidingEach.query.filter(
            RidingEach.user_id == user_id
        ).one_or_none()
    
    @staticmethod
    def get_all_by_page(user_id, page):
        return db.session.query(RidingEach)\
            .filter(RidingEach.user_id==user_id)\
            .order_by(RidingEach.create_time.desc())\
            .slice(page, page+OFFSET)\
            .all()
                    
    
class RidingTotal(db.Model):
    __tablename__ = "riding_total"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    user_id = db.Column(db.String(30), nullable=False)
    total_time = db.Column(db.String(30), nullable=True)
    total_distance = db.Column(db.String(30), nullable=True)
    id = db.Column(db.Integer, primary_key = True)
    

    @staticmethod
    def update(user_id, riding_time, distance):
        row = RidingTotal.get_by_user_id(user_id)
        if row:
            splited_time = row.total_time.split(" : ")
            total_minute = int(splited_time[0])
            total_second = int(splited_time[1])
            
            splited_time = riding_time.split(" : ")
            riding_minute = int(splited_time[0])
            riding_second = int(splited_time[1])
            
            secend = total_second + riding_second
            minute = total_minute + riding_minute
            if secend > 60:
                secend -= 60
                minute += 1
                
            row.total_time = str(minute) + " : " + str(secend)
            row.total_distance = float(row.total_distance) + float(distance)
        else:
            db.session.add(RidingTotal(
                user_id=user_id,
                total_time=riding_time,
                total_distance=distance,
            ))
            
        db.session.commit()
            
    @staticmethod
    def get_by_user_id(user_id):
        return RidingTotal.query.filter(
            RidingTotal.user_id == user_id
        ).one_or_none()