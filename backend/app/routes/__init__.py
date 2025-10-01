from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return {
        "message": "社交电商团购后端服务",
        "version": "1.0.0",
        "status": "running"
    }

@bp.route('/health')
def health():
    return {"status": "healthy"}