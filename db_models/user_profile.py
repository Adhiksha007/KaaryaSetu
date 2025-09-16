from db_models import db


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_auth.id'), nullable=False)
    notification_frequency = db.Column(db.Text)

    job_preference = db.relationship('JobPreference', back_populates='profile', uselist=False)
    resume = db.relationship('Resume', backref='profile', uselist=False)
    skills = db.relationship('Skill', back_populates='profile', cascade='all, delete-orphan')
    qualifications = db.relationship('Qualification', backref='profile', cascade="all, delete-orphan")
    experiences = db.relationship('WorkExperience', back_populates='profile', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='profile', cascade="all, delete-orphan")
    saved_jobs = db.relationship('SavedJob', back_populates='profile', cascade='all, delete-orphan')
