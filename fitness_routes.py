from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json
import sys
import os

# 添加services目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.fitness_service import FitnessService

fitness_bp = Blueprint('fitness', __name__)
fitness_service = FitnessService()

# 模拟用户数据（实际项目中应从数据库获取）
user_profiles = {
    "user1": {
        "profile": {
            "age": 30,
            "gender": "male", 
            "height": 175,
            "weight": 70,
            "fitness_level": "intermediate",
            "goals": ["weight_loss", "muscle_gain"]
        },
        "workouts": [
            {
                "id": 1,
                "type": "strength",
                "duration": 60,
                "calories_burned": 300,
                "exercises": ["深蹲", "卧推"],
                "workout_date": "2024-01-15T10:00:00"
            }
        ],
        "goals": [
            {
                "id": 1,
                "type": "weight_loss",
                "target": 5,
                "current": 2.5,
                "unit": "kg",
                "deadline": "2024-03-01"
            }
        ]
    }
}

@fitness_bp.route('/ai/chat', methods=['POST'])
@jwt_required()
def ai_fitness_chat():
    """AI健身教练对话接口"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    user_message = data['message']
    
    # 获取用户上下文
    user_context = user_profiles.get(current_user, {})
    
    # 生成AI回复
    ai_response = fitness_service.generate_ai_response(user_message, user_context)
    
    # 保存对话记录（实际项目中应保存到数据库）
    conversation_entry = {
        "user_message": user_message,
        "ai_response": ai_response,
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify({
        'reply': ai_response,
        'timestamp': conversation_entry['timestamp']
    }), 200

@fitness_bp.route('/workouts', methods=['GET'])
@jwt_required()
def get_workouts():
    """获取用户运动记录"""
    current_user = get_jwt_identity()
    
    # 获取查询参数
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    user_data = user_profiles.get(current_user, {})
    workouts = user_data.get('workouts', [])
    
    # 分页处理
    paginated_workouts = workouts[offset:offset + limit]
    
    return jsonify({
        'workouts': paginated_workouts,
        'total': len(workouts),
        'limit': limit,
        'offset': offset
    }), 200

@fitness_bp.route('/workouts', methods=['POST'])
@jwt_required()
def add_workout():
    """添加新的运动记录"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Workout data is required'}), 400
    
    # 验证必要字段
    required_fields = ['type', 'duration']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # 创建新的运动记录
    new_workout = {
        'id': len(user_profiles.get(current_user, {}).get('workouts', [])) + 1,
        'type': data['type'],
        'duration': data['duration'],
        'calories_burned': data.get('calories_burned', 0),
        'exercises': data.get('exercises', []),
        'notes': data.get('notes', ''),
        'workout_date': data.get('workout_date', datetime.now().isoformat())
    }
    
    # 计算卡路里消耗（如果未提供）
    if not new_workout['calories_burned']:
        user_weight = user_profiles.get(current_user, {}).get('profile', {}).get('weight', 70)
        # 简化计算：使用第一个运动类型
        if new_workout['exercises']:
            exercise = new_workout['exercises'][0]
        else:
            exercise = new_workout['type']
        
        new_workout['calories_burned'] = fitness_service.calculate_calories_burned(
            exercise, new_workout['duration'], user_weight
        )
    
    # 保存到用户数据（实际项目中应保存到数据库）
    if current_user not in user_profiles:
        user_profiles[current_user] = {'workouts': [], 'goals': []}
    
    user_profiles[current_user]['workouts'].append(new_workout)
    
    return jsonify({
        'message': 'Workout added successfully',
        'workout': new_workout
    }), 201

@fitness_bp.route('/goals', methods=['GET'])
@jwt_required()
def get_goals():
    """获取用户健身目标"""
    current_user = get_jwt_identity()
    
    user_data = user_profiles.get(current_user, {})
    goals = user_data.get('goals', [])
    
    return jsonify({'goals': goals}), 200

@fitness_bp.route('/goals', methods=['POST'])
@jwt_required()
def add_goal():
    """添加新的健身目标"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Goal data is required'}), 400
    
    # 验证必要字段
    required_fields = ['type', 'target']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # 创建新的目标
    new_goal = {
        'id': len(user_profiles.get(current_user, {}).get('goals', [])) + 1,
        'type': data['type'],
        'target': data['target'],
        'current': data.get('current', 0),
        'unit': data.get('unit', ''),
        'deadline': data.get('deadline'),
        'status': 'active',
        'created_at': datetime.now().isoformat()
    }
    
    # 保存到用户数据（实际项目中应保存到数据库）
    if current_user not in user_profiles:
        user_profiles[current_user] = {'workouts': [], 'goals': []}
    
    user_profiles[current_user]['goals'].append(new_goal)
    
    return jsonify({
        'message': 'Goal added successfully',
        'goal': new_goal
    }), 201

@fitness_bp.route('/training-plan', methods=['GET'])
@jwt_required()
def get_training_plan():
    """获取个性化训练计划"""
    current_user = get_jwt_identity()
    
    user_profile = user_profiles.get(current_user, {}).get('profile', {})
    
    # 生成个性化训练计划
    training_plan = fitness_service.generate_personalized_plan(user_profile)
    
    return jsonify(training_plan), 200

@fitness_bp.route('/analysis', methods=['GET'])
@jwt_required()
def get_fitness_analysis():
    """获取健身数据分析"""
    current_user = get_jwt_identity()
    
    user_data = user_profiles.get(current_user, {})
    workouts = user_data.get('workouts', [])
    
    # 分析运动数据
    analysis = fitness_service.analyze_workout_data(workouts)
    
    return jsonify(analysis), 200

@fitness_bp.route('/exercises/recommendations', methods=['GET'])
@jwt_required()
def get_exercise_recommendations():
    """获取运动推荐"""
    muscle_group = request.args.get('muscle_group', '')
    difficulty = request.args.get('difficulty', 'beginner')
    
    if not muscle_group:
        return jsonify({'error': 'Muscle group is required'}), 400
    
    recommendations = fitness_service.get_exercise_recommendations(muscle_group, difficulty)
    
    return jsonify({
        'muscle_group': muscle_group,
        'difficulty': difficulty,
        'recommendations': recommendations
    }), 200

@fitness_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_fitness_profile():
    """获取用户健身概况"""
    current_user = get_jwt_identity()
    
    user_data = user_profiles.get(current_user, {})
    profile = user_data.get('profile', {})
    workouts = user_data.get('workouts', [])
    goals = user_data.get('goals', [])
    
    # 计算健身概况
    total_workouts = len(workouts)
    total_calories = sum(w.get('calories_burned', 0) for w in workouts)
    active_goals = [g for g in goals if g.get('status') == 'active']
    
    fitness_profile = {
        'basic_info': profile,
        'stats': {
            'total_workouts': total_workouts,
            'total_calories': total_calories,
            'active_goals': len(active_goals)
        },
        'recent_workouts': workouts[-3:] if workouts else [],
        'active_goals': active_goals
    }
    
    return jsonify(fitness_profile), 200

@fitness_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress_tracking():
    """获取健身进度跟踪"""
    current_user = get_jwt_identity()
    
    user_data = user_profiles.get(current_user, {})
    workouts = user_data.get('workouts', [])
    goals = user_data.get('goals', [])
    
    # 计算进度统计
    total_workouts = len(workouts)
    total_calories = sum(w.get('calories_burned', 0) for w in workouts)
    
    # 计算每周运动频率
    recent_workouts = sorted(workouts, key=lambda x: x.get('workout_date', ''), reverse=True)[:7]
    weekly_frequency = len(recent_workouts)
    
    # 计算目标完成度
    goal_progress = []
    for goal in goals:
        if goal.get('status') == 'active':
            target = goal.get('target', 0)
            current = goal.get('current', 0)
            progress_percentage = (current / target * 100) if target > 0 else 0
            
            goal_progress.append({
                'type': goal.get('type'),
                'target': target,
                'current': current,
                'progress_percentage': round(progress_percentage, 1),
                'deadline': goal.get('deadline')
            })
    
    progress_data = {
        'stats': {
            'total_workouts': total_workouts,
            'total_calories': total_calories,
            'weekly_frequency': weekly_frequency,
            'active_goals': len(goals)
        },
        'goal_progress': goal_progress,
        'recent_activity': recent_workouts[:3]
    }
    
    return jsonify({'progress': progress_data}), 200