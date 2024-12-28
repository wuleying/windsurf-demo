from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# 初始化数据库
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """
    应用工厂函数
    
    Args:
        config_name: 配置名称，默认为 'default'
        
    Returns:
        Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 注册蓝图
    from app.routes import word_bp
    app.register_blueprint(word_bp)
    
    return app
