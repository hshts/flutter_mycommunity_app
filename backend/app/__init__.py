from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    CORS(
        app,
        origins=app.config['CORS_ORIGINS'],
        supports_credentials=True,
        methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"]
    )

    # 全局 OPTIONS 响应，解决 CORS 预检 403
    @app.before_request
    def handle_options():
        from flask import request, make_response
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers', 'Authorization,Content-Type')
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.status_code = 200
            return response

    # 注册主路由
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.push import bp as push_bp
    app.register_blueprint(push_bp, url_prefix='/push')
    from app.routes.upload import bp as upload_bp
    app.register_blueprint(upload_bp, url_prefix='/upload')
    from app.routes.order import bp as order_bp
    app.register_blueprint(order_bp, url_prefix='/order')
    from app.routes.im import bp as im_bp
    app.register_blueprint(im_bp, url_prefix='/im')
    from app.routes.aliyun import bp as aliyun_bp
    app.register_blueprint(aliyun_bp, url_prefix='/aliyun')
    from app.routes.activity import bp as activity_bp
    app.register_blueprint(activity_bp, url_prefix='/activity')
    from app.routes.grouppurchase import bp as gp_bp
    app.register_blueprint(gp_bp, url_prefix='/grouppurchase')
    from app.routes.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app