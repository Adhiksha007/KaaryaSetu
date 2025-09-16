from functools import wraps
from flask import session, redirect, url_for
import pickle, uuid
import os

RESULTS_DIR = "temp_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated 

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

def parse_experience(exp_str):
    if not exp_str:
        return 0
    try:
        exp_str = exp_str.lower().replace("years", "").replace("+", "").strip()
        if "-" in exp_str:
            start, _ = exp_str.split("-", 1)
            return int(start.strip())
        return int(exp_str.strip())
    except Exception:
        return 0
