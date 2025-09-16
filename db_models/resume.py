from db_models import db

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    resume_path = db.Column(db.String(200))
    other_docs = db.Column(db.Text)

