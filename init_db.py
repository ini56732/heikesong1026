#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建数据库表和插入初始数据
"""

import os
import sys
from sqlalchemy import create_engine, text
from config import get_config

def init_database():
    """初始化数据库"""
    
    # 获取配置
    config = get_config()
    
    # 创建数据库引擎
    engine = create_engine(config.DATABASE_URL)
    
    # 创建表的SQL语句
    create_tables_sql = """
    -- 用户表
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        profile JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- 健康数据表
    CREATE TABLE IF NOT EXISTS health_data (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        weight DECIMAL(5,2),
        height DECIMAL(5,2),
        bmi DECIMAL(4,2),
        heart_rate INTEGER,
        blood_pressure VARCHAR(20),
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notes TEXT
    );

    -- 健身训练表
    CREATE TABLE IF NOT EXISTS fitness_workouts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        workout_type VARCHAR(50) NOT NULL,
        duration_minutes INTEGER NOT NULL,
        calories_burned INTEGER,
        intensity VARCHAR(20),
        date DATE NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- 健身目标表
    CREATE TABLE IF NOT EXISTS fitness_goals (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        goal_type VARCHAR(50) NOT NULL,
        target_value DECIMAL(8,2),
        current_value DECIMAL(8,2),
        deadline DATE,
        status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- AI对话记录表
    CREATE TABLE IF NOT EXISTS ai_conversations (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        user_message TEXT NOT NULL,
        ai_response TEXT NOT NULL,
        message_type VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- 运动推荐表
    CREATE TABLE IF NOT EXISTS exercise_recommendations (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        exercise_name VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        difficulty VARCHAR(20),
        recommended_sets INTEGER,
        recommended_reps INTEGER,
        recommended_duration INTEGER,
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- 训练计划表
    CREATE TABLE IF NOT EXISTS training_plans (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        plan_name VARCHAR(100) NOT NULL,
        plan_type VARCHAR(50),
        duration_weeks INTEGER,
        description TEXT,
        exercises JSONB,
        status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # 插入初始数据的SQL语句
    insert_initial_data_sql = """
    -- 插入示例用户（如果不存在）
    INSERT INTO users (username, email, password_hash, profile) 
    VALUES 
    ('demo_user', 'demo@example.com', 'hashed_password_here', '{"age": 30, "gender": "male", "height": 175, "weight": 70, "fitness_level": "intermediate"}'),
    ('test_user', 'test@example.com', 'hashed_password_here', '{"age": 25, "gender": "female", "height": 165, "weight": 55, "fitness_level": "beginner"}')
    ON CONFLICT (username) DO NOTHING;

    -- 插入示例健身数据
    INSERT INTO fitness_workouts (user_id, workout_type, duration_minutes, calories_burned, intensity, date, notes)
    SELECT 
        u.id, 
        'running', 
        30, 
        300, 
        'moderate', 
        CURRENT_DATE - INTERVAL '1 day', 
        '晨跑训练'
    FROM users u WHERE u.username = 'demo_user'
    ON CONFLICT DO NOTHING;

    INSERT INTO fitness_workouts (user_id, workout_type, duration_minutes, calories_burned, intensity, date, notes)
    SELECT 
        u.id, 
        'yoga', 
        45, 
        200, 
        'light', 
        CURRENT_DATE, 
        '瑜伽放松'
    FROM users u WHERE u.username = 'test_user'
    ON CONFLICT DO NOTHING;

    -- 插入示例健身目标
    INSERT INTO fitness_goals (user_id, goal_type, target_value, current_value, deadline, status)
    SELECT 
        u.id, 
        'weight_loss', 
        5.0, 
        0.0, 
        CURRENT_DATE + INTERVAL '30 days', 
        'active'
    FROM users u WHERE u.username = 'demo_user'
    ON CONFLICT DO NOTHING;

    INSERT INTO fitness_goals (user_id, goal_type, target_value, current_value, deadline, status)
    SELECT 
        u.id, 
        'muscle_gain', 
        2.0, 
        0.0, 
        CURRENT_DATE + INTERVAL '60 days', 
        'active'
    FROM users u WHERE u.username = 'test_user'
    ON CONFLICT DO NOTHING;
    """
    
    try:
        # 连接数据库并执行SQL
        with engine.connect() as connection:
            # 创建表
            print("正在创建数据库表...")
            for statement in create_tables_sql.split(';'):
                if statement.strip():
                    connection.execute(text(statement.strip()))
            
            # 插入初始数据
            print("正在插入初始数据...")
            for statement in insert_initial_data_sql.split(';'):
                if statement.strip():
                    connection.execute(text(statement.strip()))
            
            connection.commit()
            print("数据库初始化完成！")
            
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        sys.exit(1)

def check_database_connection():
    """检查数据库连接"""
    config = get_config()
    
    try:
        engine = create_engine(config.DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("数据库连接正常！")
            return True
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return False

if __name__ == '__main__':
    print("开始初始化AI健身教练数据库...")
    
    # 检查数据库连接
    if not check_database_connection():
        print("请确保数据库服务正在运行，并检查DATABASE_URL配置")
        sys.exit(1)
    
    # 初始化数据库
    init_database()