from scrimdor import db
from datetime import datetime
from pytz import timezone

class ReportLog(db.Model):
    __tablename__ = "report_log"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, nullable=False)
    to_user_id = db.Column(db.Integer, nullable=False)
    report_number = db.Column(db.String(50))
    etc_comment = db.Column(db.Text)
    create_date = db.Column(db.DateTime)
    is_processed = db.Column(db.String(2), default='N')
    
    @staticmethod
    def register_report_log(from_user_id, to_user_id, report_number, etc_comment):
        KST = timezone('Asia/Seoul')
        db.session.add(ReportLog(
            from_user_id = from_user_id,
            to_user_id = to_user_id,
            report_number = report_number,
            etc_comment = etc_comment,
            create_date = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
        ))
        db.session.commit()

class ReportRoomLog(db.Model):
    __tablename__ = "report_room_log"
    __table_args__ = {"mysql_collate": "utf8_bin"}
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, nullable=False)
    to_room_id = db.Column(db.String(30), nullable=False)
    report_number = db.Column(db.String(50))
    etc_comment = db.Column(db.Text)
    create_date = db.Column(db.DateTime)
    is_processed = db.Column(db.String(2), default='N')
    
    @staticmethod
    def register_report_room_log(from_user_id, to_room_id, report_number, etc_comment):
        KST = timezone('Asia/Seoul')
        db.session.add(ReportRoomLog(
            from_user_id = from_user_id,
            to_room_id = to_room_id,
            report_number = report_number,
            etc_comment = etc_comment,
            create_date = datetime.now().astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')
        ))
        db.session.commit()

#     @staticmethod
#     def get_ReportLog(page, filter, user_id=None):
#         '''최신순, 오래된순, 유저별, 전체, 해결된것만, 신고 많이 받은 순'''
#         '''latest, oldest, user, all, processed, worst'''
#         if filter == 'latest':
#             query = 1Log.query.filter(ReportLog.is_processed == 'N')\
#                 .order_by(ReportLog.create_date.desc())\
#                 .slice((page - 1) * 30, page * 30)
                
#         elif filter == 'oldest':
#             query = ReportLog.query.filter(ReportLog.is_processed == 'N')\
#                 .order_by(ReportLog.create_date.asc())\
#                 .slice((page - 1) * 30, page * 30)
                
#         elif filter == 'user':
#             if not user_id:
#                 return None
#             query = ReportLog.query.filter(ReportLog.to_user_id == user_id)\
#                 .order_by(ReportLog.create_date.desc())\
#                 .slice((page - 1) * 30, page * 30)
                
#         elif filter == 'all':
#             query = ReportLog.query.filter()\
#                 .order_by(ReportLog.create_date.desc())\
#                 .slice((page - 1) * 30, page * 30)
        
#         elif filter == 'processed':
#             query = ReportLog.query.filter(ReportLog.is_processed == 'Y')\
#                 .order_by(ReportLog.create_date.desc())\
#                 .slice((page - 1) * 30, page * 30)
                
#         # elif filter == 'worst':
#         #     query = ReportLog.query.filter(ReportLog.is_processed == 'N')\
#         #         .order_by(ReportLog.create_date.desc())\
#         #         .slice((page - 1) * 30, page * 30)
#         pass
    
# class PerUserReport:
#     pass