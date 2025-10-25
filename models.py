from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 用户档案信息
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    height = db.Column(db.Float)  # 厘米
    weight = db.Column(db.Float)  # 公斤
    fitness_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    fitness_goals = db.Column(db.Text)  # JSON格式存储目标
    
    # 关系
    health_data = db.relationship('HealthData', backref='user', lazy=True)
    fitness_workouts = db.relationship('FitnessWorkout', backref='user', lazy=True)
    fitness_goals = db.relationship('FitnessGoal', backref='user', lazy=True)
    ai_conversations = db.relationship('AIConversation', backref='user', lazy=True)

class HealthData(db.Model):
    __tablename__ = 'health_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_type = db.Column(db.String(50), nullable=False)  # sleep, exercise, nutrition, etc.
    value = db.Column(db.Text)  # JSON格式存储数据值
    recorded_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FitnessWorkout(db.Model):
    __tablename__ = 'fitness_workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_type = db.Column(db.String(50), nullable=False)  # strength, cardio, flexibility
    duration = db.Column(db.Integer)  # 分钟
    calories_burned = db.Column(db.Integer)
    exercises = db.Column(db.Text)  # JSON格式存储练习列表
    notes = db.Column(db.Text)
    workout_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FitnessGoal(db.Model):
    __tablename__ = 'fitness_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal_type = db.Column(db.String(50), nullable=False)  # weight_loss, muscle_gain, endurance
    target_value = db.Column(db.Float)
    current_value = db.Column(db.Float)
    unit = db.Column(db.String(20))  # kg, %, etc.
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AIConversation(db.Model):
    __tablename__ = 'ai_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ai_type = db.Column(db.String(50), nullable=False)  # fitness_trainer, nutritionist, etc.
    message = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(20), nullable=False)  # user, ai
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 消息元数据
    message_type = db.Column(db.String(20), default='text')  # text, image, workout_data
    metadata = db.Column(db.Text)  # JSON格式存储额外信息

class TrainingPlan(db.Model):
    __tablename__ = 'training_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    plan_data = db.Column(db.Text)  # JSON格式存储训练计划
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # strength, cardio, flexibility
    muscle_group = db.Column(db.String(100))  # 主要锻炼的肌肉群
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 辅助函数
def serialize_model(model):
    """将SQLAlchemy模型转换为字典"""
    if model is None:
        return None
    
    result = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        
        # 处理JSON字段
        if column.name in ['fitness_goals', 'exercises', 'value', 'plan_data', 'metadata'] and value:
            try:
                value = json.loads(value)
            except:
                pass
        
        # 处理日期时间
        if isinstance(value, datetime):
            value = value.isoformat()
        
        result[column.name] = value
    
    return result