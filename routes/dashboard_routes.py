from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_models import db
from db_models.user_auth import UserAuth
from db_models.user_profile import UserProfile
from db_models.job_preference import JobPreference
from db_models.skill import Skill
from db_models.qualification import Qualification
from db_models.work_experience import WorkExperience
from .utils import login_required
from datetime import datetime
import os

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    user_auth = UserAuth.query.get(user_id)

    # Fetch or auto-create profile
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.session.add(profile)
        db.session.commit()

    preferences = JobPreference.query.filter_by(profile_id=profile.id).first()

    # Skills
    skill_record = Skill.query.filter_by(profile_id=profile.id).first()
    skills_string = skill_record.skills if skill_record and skill_record.skills else ""
    languages = skill_record.languages if skill_record and skill_record.languages else ""

    # Qualifications
    qualifications = Qualification.query.filter_by(profile_id=profile.id).all()
    experience = WorkExperience.query.filter_by(profile_id=profile.id).all()

    # Resume & Documents
    user_folder = os.path.join('uploads', str(user_id))
    resume_file = None
    other_files = []
    certifications = []

    if os.path.exists(user_folder):
        for filename in os.listdir(user_folder):
            if filename.startswith('resume_'):
                resume_file = os.path.join(user_folder, filename).replace("\\", "/")
            elif filename.startswith('doc_'):
                other_files.append(os.path.join(user_folder, filename).replace("\\", "/"))
            elif filename.startswith('certification_'):
                certifications.append(os.path.join(user_folder, filename).replace("\\", "/"))

    return render_template(
        'dashboard.html',
        user=user_auth,
        profile=profile,
        preferences=preferences,
        skills=skills_string,
        languages=languages,
        qualifications=qualifications,
        experience=experience,
        resume_file=resume_file,
        other_files=other_files,
        certifications=certifications
    )

@dashboard_bp.route('/update-password', methods=['POST'])
def update_password():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401

    current_password = request.form.get('currentPassword')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')

    if new_password != confirm_password:
        return jsonify({'message': 'New passwords do not match'}), 400

    user = UserAuth.query.get(user_id)
    if not user or not check_password_hash(user.password, current_password):
        return jsonify({'message': 'Current password is incorrect'}), 400

    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'})


@dashboard_bp.route('/delete-account', methods=['POST'])
def delete_account():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401

    user = UserAuth.query.get(user_id)
    if user:
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        if profile:
            db.session.delete(profile)  

        db.session.delete(user)
        db.session.commit()
        session.clear()
        return jsonify({'message': 'Account deleted successfully'}), 200

    return jsonify({'message': 'User not found'}), 404



@dashboard_bp.route('/dashboard/save/<section>', methods=['POST'])
def save_dashboard_section(section):
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    if section == 'profile':
        phone = request.form.get('phone')
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.session.add(profile)
        profile.phone = phone
        db.session.commit()
        return jsonify({'message': 'Profile updated'})

    elif section == 'preferences':
        titles = request.form.get('titles')
        locations = request.form.get('locations')
        salary = request.form.get('salary')
        employment_type = request.form.get('employment_type')
        relocate = request.form.get('relocate')

        profile = UserProfile.query.filter_by(user_id=user_id).first()

        pref = JobPreference.query.filter_by(profile_id=profile.id).first()
        if not pref:
            pref = JobPreference(profile_id=profile.id)
            db.session.add(pref)
            db.session.commit()

        pref.titles = titles
        pref.locations = locations
        pref.salary_range = salary
        pref.employment_type = employment_type
        pref.relocate = relocate
        db.session.commit()
        return jsonify({'message': 'Preferences updated'})

    elif section == 'skills':
        skills_text = request.form.get('skills')
        languages = request.form.get('languages')
        educations = request.form.get('educations')

        # Fetch the user's profile
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return jsonify({'message': 'User profile not found.'}), 404

        # Fetch or create skill entry
        skill = Skill.query.filter_by(profile_id=profile.id).first()
        if not skill:
            skill = Skill(profile_id=profile.id)
            db.session.add(skill)
            db.session.commit()

        skill.skills = skills_text
        skill.languages = languages

        # Upload new certifications and remove old ones
        other_docs = request.files.getlist('certification[]')
        upload_dir = os.path.join('uploads', str(user_id))
        os.makedirs(upload_dir, exist_ok=True)
        if other_docs and any(doc.filename for doc in other_docs):
            # Delete previous certification files
            for file in os.listdir(upload_dir):
                if file.startswith('certification_'):
                    os.remove(os.path.join(upload_dir, file))

            # Save new ones
            for doc in other_docs:
                if doc.filename:
                    doc_path = os.path.join(upload_dir, 'certification_' + doc.filename)
                    doc.save(doc_path)

        # Clear old qualifications
        Qualification.query.filter_by(profile_id=profile.id).delete()

        # Add updated qualifications
        if educations:
            import json
            try:
                edu_list = json.loads(educations)
                for edu in edu_list:
                    q = Qualification(
                        profile_id  =profile.id,  # Update to profile_id=profile.id if needed
                        institution=edu.get('school'),
                        start_date=edu.get('start_date'),
                        end_date=edu.get('end_date'),
                        qualification=edu.get('qualification'),
                        cgpa=edu.get('cgpa'),
                        city=edu.get('city'),
                        state=edu.get('state'),
                        country=edu.get('country')
                    )
                    db.session.add(q)
                    db.session.commit()
            except Exception as e:
                return jsonify({'message': f'Invalid education data: {e}'}), 400

        db.session.commit()
        return jsonify({'message': 'Skills and education updated'})

    elif section == 'experience':
        experience_data = request.form.get('experiences')
        import json

        try:
            exp_list = json.loads(experience_data)
            if not isinstance(exp_list, list):
                exp_list = [exp_list]  # Wrap single entry in a list

            profile = UserProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                return jsonify({'message': 'User profile not found'}), 400

            profile_id = profile.id

            # Delete existing experience entries
            WorkExperience.query.filter_by(profile_id=profile_id).delete()

            for exp in exp_list:
                new_exp = WorkExperience(
                    profile_id=profile_id,
                    company=exp.get('company'),
                    title=exp.get('role'),  # Match frontend key "role"
                    start_date=datetime.strptime(exp.get('start_date'), '%Y-%m-%d') if exp.get('start_date') else None,
                    end_date=datetime.strptime(exp.get('end_date'), '%Y-%m-%d') if exp.get('end_date') else None,
                    description=exp.get('description'),
                    technologies=exp.get('technologies')
                )
                db.session.add(new_exp)

            db.session.commit()
            return jsonify({'message': 'Experience updated'})

        except Exception as e:
            return jsonify({'message': f'Invalid experience data: {e}'}), 400

    elif section == 'documents':
        resume_file = request.files.get('resume')
        other_docs = request.files.getlist('documents[]')

        upload_dir = os.path.join('uploads', str(user_id))
        os.makedirs(upload_dir, exist_ok=True)

        if resume_file:
            for file in os.listdir(upload_dir):
                if file.startswith('resume_'):
                    os.remove(os.path.join(upload_dir, file))
            resume_path = os.path.join(upload_dir, 'resume_' + resume_file.filename)
            resume_file.save(resume_path)

        if other_docs and any(doc.filename for doc in other_docs):
            for file in os.listdir(upload_dir):
                if file.startswith('doc_'):
                    os.remove(os.path.join(upload_dir, file))

            for doc in other_docs:
                if doc.filename:
                    doc_path = os.path.join(upload_dir, 'doc_' + doc.filename)
                    doc.save(doc_path)

        return jsonify({'message': 'Documents updated successfully'})

    elif section == 'notifications':
        frequency = request.form.get('notification_frequency')
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.session.add(profile)
        profile.notification_frequency = frequency
        db.session.commit()
        return jsonify({'message': 'Notification settings updated'})

    return jsonify({'message': f'Unknown section: {section}'}), 400
