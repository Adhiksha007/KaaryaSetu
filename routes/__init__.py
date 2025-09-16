from .auth_routes import auth_bp
from .job_routes import job_bp
from .dashboard_routes import dashboard_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(dashboard_bp)