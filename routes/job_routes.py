from flask import Blueprint, request, render_template, redirect, url_for, jsonify, session
from utils.recommender import get_recommendations
from db_models import db, SavedJob
from db_models.user_profile import UserProfile 
import joblib
from .utils import parse_experience, save_results, load_results

model = joblib.load("models/job_recommendation_model.pkl")
tfidf_matrix = joblib.load("models/tfidf_matrix.pkl")
data = joblib.load("models/jobs_data.pkl")

job_bp = Blueprint('job', __name__)

@job_bp.route('/')
def home():
    open_modal = request.args.get('open_modal')
    return render_template("main.html", open_modal=open_modal)

@job_bp.route('/jobs')
def jobs_home():
    return render_template(
        "index.html",
        results=[],
        jobs=[],
        current_page=1,
        total_pages=0,
        filters={  
            "experience": "",
            "work_type": "",
            "country": "",
            "sector": "",
            "qualification": ""
        },
        result_id=None  
    )
@job_bp.route('/recommend', methods=['POST'])
def recommend():
    skills = request.form.get("skills", "")
    qualifications = request.form.get("qualification", "")
    experience = request.form.get("experience", "")
    user_input = qualifications + skills + experience

    if not user_input:
        return render_template(
            "index.html",
            results=[],
            jobs=[],
            current_page=1,
            total_pages=0,
            filters={  
                "experience": "",
                "work_type": "",
                "country": "",
                "sector": "",
                "qualification": ""
            },
            result_id=None
        )


    recommended_jobs = get_recommendations(user_input, model, tfidf_matrix, data)
    results = recommended_jobs.to_dict(orient="records")[:50]
    for idx, job in enumerate(results):
        job['job_id'] = idx

    result_id = save_results(results)

    return redirect(url_for('job.filter_jobs', id=result_id, filter_qualification=qualifications))

@job_bp.route('/filter')
def filter_jobs():
    result_id = request.args.get("id")
    if not result_id:
        return render_template(
            "index.html",
            results=[],
            jobs=[],
            current_page=1,
            total_pages=0,
            result_id=None,
            filters={} 
        )


    results = load_results(result_id)
    for idx, job in enumerate(results):
        job['job_id'] = idx

    # Get filter inputs
    filter_experience = request.args.get("filter_experience", "")
    filter_work_type = request.args.get("filter_work_type", "").lower()
    filter_country = request.args.get("filter_country", "").lower()
    filter_sector = request.args.get("filter_sector", "").lower()
    qualification = request.args.get("filter_qualification")


    # Apply filters
    filtered_results = []
    for job in results:
        job_exp = parse_experience(job.get("Experience", ""))
        job_work_type = job.get("Work Type", "").lower()
        job_country = job.get("Country", "").lower()
        job_sector = job.get("Sector", "").lower()

        if filter_experience:
            if filter_experience == "10+" and job_exp < 10:
                continue
            elif filter_experience != "10+":
                try:
                    min_exp, max_exp = map(int, filter_experience.split("-"))
                    if job_exp < min_exp or job_exp > max_exp:
                        continue
                except:
                    continue

        if filter_work_type and filter_work_type not in job_work_type:
            continue
        if filter_country and filter_country not in job_country:
            continue
        if filter_sector and filter_sector not in job_sector:
            continue
        if qualification and qualification.lower() not in job.get("Qualifications", "").lower():
            continue


        filtered_results.append(job)

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_pages = (len(filtered_results) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    jobs_paginated = filtered_results[start:end]

    return render_template(
        'index.html',
        results=filtered_results,
        jobs=jobs_paginated,
        current_page=page,
        total_pages=total_pages,
        result_id=result_id,
        filters={
            "experience": filter_experience,
            "work_type": filter_work_type,
            "country": filter_country,
            "sector": filter_sector,
            "qualification": qualification
        }
    )


@job_bp.route('/save_job', methods=['POST'])
def save_job():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401

    data = request.get_json()
    job_id = data.get('job_id')
    profile_id = session['profile_id']  # assuming profile_id is saved in session

    if not job_id:
        return jsonify({'success': False, 'message': 'No job ID provided'}), 400

    # Check if already saved
    existing = SavedJob.query.filter_by(profile_id=profile_id, job_id=job_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'Job already saved'}), 200

    saved_job = SavedJob(profile_id=profile_id, job_id=job_id)
    db.session.add(saved_job)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Job saved successfully'}), 200
    