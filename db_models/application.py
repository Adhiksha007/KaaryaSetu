from db_models import db
from datetime import datetime

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    job_id = db.Column(db.Integer)
    status = db.Column(db.String(50))
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

