from db_models import db

class SavedJob(db.Model):
    __tablename__ = 'saved_job'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    profile = db.relationship('UserProfile', back_populates='saved_jobs')