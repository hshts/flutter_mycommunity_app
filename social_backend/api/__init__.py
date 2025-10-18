from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api

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
    
    # 初始化数据库扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # 初始化API
    api.init_app(app)
    
    # 注册命名空间
    from api.controllers.activity import ns as activity_ns
    from api.controllers.group_purchase import ns as grouppurchase_ns
    from api.controllers.im_moment import ns as im_moment_ns
    from api.controllers.user import ns as user_ns
    
    api.add_namespace(activity_ns, path='/Activity')
    api.add_namespace(grouppurchase_ns, path='/grouppurchase')
    api.add_namespace(im_moment_ns, path='/IM')
    api.add_namespace(user_ns, path='/user')
    
    # 添加CORS响应头
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    @app.route('/')
    def index():
        return {'message': 'Social E-commerce Backend API'}
    
    return app