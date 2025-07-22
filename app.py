from utils.recommender import get_recommendations
from flask import Flask, render_template, request, redirect, url_for
import joblib
import uuid
import pickle
import os

app = Flask(__name__)

model = joblib.load("models/job_recommendation_model.pkl")
tfidf_matrix = joblib.load("models/tfidf_matrix.pkl")
data = joblib.load("models/jobs_data.pkl")

RESULTS_DIR = "temp_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def save_results(results):
    result_id = str(uuid.uuid4())
    with open(f"{RESULTS_DIR}/{result_id}.pkl", "wb") as f:
        pickle.dump(results, f)
    return result_id

def load_results(result_id):
    try:
        with open(f"{RESULTS_DIR}/{result_id}.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    return render_template("main.html")

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        skills = request.form.get("skills", "")
        qualifications = request.form.get("qualification", "")
        experience = request.form.get("experience", "")
        user_input = qualifications + skills + experience
        if not user_input:
            return render_template("index.html", results=[], jobs=[], current_page=1, total_pages=0)

        recommended_jobs = get_recommendations(user_input, model, tfidf_matrix, data)
        results = recommended_jobs.to_dict(orient="records")[:50]
        for idx, job in enumerate(results):
            job['job_id'] = idx
        result_id = save_results(results)
        return redirect(url_for('recommend', page=1, id=result_id))

    # GET request
    result_id = request.args.get("id")
    if not result_id:
        return render_template("index.html", results=[], jobs=[], current_page=1, total_pages=0)

    results = load_results(result_id)
    for idx, job in enumerate(results):
        job['job_id'] = idx
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_pages = (len(results) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    jobs_paginated = results[start:end]

    return render_template(
        'index.html',
        results=results,
        jobs=jobs_paginated,
        current_page=page,
        total_pages=total_pages,
        result_id=result_id  # pass to pagination links
    )

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    result_id = request.args.get('id')
    current_page = request.args.get('page', 1, type=int)

    if not result_id:
        return "Job data not found", 404

    jobs = load_results(result_id)
    for idx, job in enumerate(jobs):
        job['job_id'] = idx  # Ensure job_id is added

    selected_job = next((job for job in jobs if job['job_id'] == job_id), None)
    if not selected_job:
        return "Job not found", 404

    return render_template(
        'job_details.html',
        job=selected_job,
        result_id=result_id,
        current_page=current_page
    )


if __name__ == "__main__":
    app.run(debug=True)