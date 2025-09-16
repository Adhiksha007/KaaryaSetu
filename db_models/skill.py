from db_models import db

class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    skills = db.Column(db.Text)
    languages = db.Column(db.Text)

    profile = db.relationship('UserProfile', back_populates='skills')
