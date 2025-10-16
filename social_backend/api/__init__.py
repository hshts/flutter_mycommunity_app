from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_cors import CORS

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api(
    version='1.0',
    title='Social E-commerce API',
    description='A social e-commerce backend API',
    doc='/doc'
)

def create_app():
    app = Flask(__name__)
    app.config.from_object('api.config.Config')
    
    # 启用 CORS（允许所有来源访问）
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)
    
    # 注册命名空间
    from api.controllers.activity import ns as activity_ns
    from api.controllers.group_purchase import ns as grouppurchase_ns
    from api.controllers.im_moment import ns as im_moment_ns
    
    api.add_namespace(activity_ns, path='/Activity')
    api.add_namespace(grouppurchase_ns, path='/grouppurchase')
    api.add_namespace(im_moment_ns, path='/IM')
    
    @app.route('/')
    def index():
        return {'message': 'Social E-commerce Backend API'}
    
    return app