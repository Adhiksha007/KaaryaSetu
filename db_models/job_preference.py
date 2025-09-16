from db_models import db

class JobPreference(db.Model):
    __tablename__ = 'job_preference'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    titles = db.Column(db.Text)
    locations = db.Column(db.Text)
    salary_range = db.Column(db.String(50))
    employment_type = db.Column(db.String(50))
    relocate = db.Column(db.Text)

    profile = db.relationship('UserProfile', back_populates='job_preference')
