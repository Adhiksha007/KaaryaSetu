from db_models import db

class WorkExperience(db.Model):
    __tablename__ = 'work_experience'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    company = db.Column(db.String(100))
    title = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    technologies = db.Column(db.Text)

    profile = db.relationship('UserProfile', back_populates='experiences')



    def __repr__(self):
        return f"<WorkExperience {self.title} at {self.company}>"
