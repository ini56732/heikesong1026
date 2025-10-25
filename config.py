import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置类"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # 数据库配置
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/fitness_db')
    
    # AI服务配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # 服务器配置
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv('TEST_DATABASE_URL', 'postgresql://username:password@localhost/fitness_test_db')

# 根据环境选择配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env=None):
    """获取配置类"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])