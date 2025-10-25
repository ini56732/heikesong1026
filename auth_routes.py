from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import hashlib

auth_bp = Blueprint('auth', __name__)

# 模拟用户数据库（实际项目中应使用真实数据库）
users_db = {
    "user1": {
        "username": "user1",
        "email": "user1@example.com",
        "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
        "profile": {
            "age": 30,
            "gender": "male",
            "height": 175,
            "weight": 70,
            "fitness_level": "intermediate",
            "goals": ["weight_loss", "muscle_gain"]
        },
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-15T00:00:00"
    },
    "user2": {
        "username": "user2", 
        "email": "user2@example.com",
        "password_hash": hashlib.sha256("password456".encode()).hexdigest(),
        "profile": {
            "age": 25,
            "gender": "female", 
            "height": 165,
            "weight": 55,
            "fitness_level": "beginner",
            "goals": ["weight_loss", "flexibility"]
        },
        "created_at": "2024-01-10T00:00:00",
        "updated_at": "2024-01-15T00:00:00"
    }
}

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证必要字段
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    username = data['username']
    email = data['email']
    password = data['password']
    
    # 检查用户是否已存在
    if username in users_db:
        return jsonify({'error': 'Username already exists'}), 400
    
    # 检查邮箱是否已存在
    for user in users_db.values():
        if user['email'] == email:
            return jsonify({'error': 'Email already exists'}), 400
    
    # 创建新用户
    users_db[username] = {
        "username": username,
        "email": email,
        "password_hash": hashlib.sha256(password.encode()).hexdigest(),
        "profile": data.get('profile', {}),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # 生成访问令牌
    access_token = create_access_token(identity=username)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': {
            'username': username,
            'email': email,
            'profile': users_db[username]['profile']
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # 验证必要字段
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    username = data['username']
    password = data['password']
    
    # 验证用户凭据
    if username not in users_db:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    user = users_db[username]
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if user['password_hash'] != password_hash:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # 生成访问令牌
    access_token = create_access_token(identity=username)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'username': username,
            'email': user['email'],
            'profile': user['profile']
        }
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户个人信息"""
    current_user = get_jwt_identity()
    
    if current_user not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    user = users_db[current_user]
    
    return jsonify({
        'username': user['username'],
        'email': user['email'],
        'profile': user['profile'],
        'created_at': user['created_at'],
        'updated_at': user['updated_at']
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新用户个人信息"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    if current_user not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    user = users_db[current_user]
    
    # 更新用户信息
    if 'email' in data:
        # 检查邮箱是否已被其他用户使用
        for username, user_data in users_db.items():
            if username != current_user and user_data['email'] == data['email']:
                return jsonify({'error': 'Email already in use'}), 400
        user['email'] = data['email']
    
    if 'profile' in data:
        # 合并profile数据
        user['profile'] = {**user['profile'], **data['profile']}
    
    user['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'username': user['username'],
            'email': user['email'],
            'profile': user['profile']
        }
    }), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """修改密码"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['current_password', 'new_password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    if current_user not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    user = users_db[current_user]
    
    # 验证当前密码
    current_password_hash = hashlib.sha256(data['current_password'].encode()).hexdigest()
    if user['password_hash'] != current_password_hash:
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    # 更新密码
    new_password_hash = hashlib.sha256(data['new_password'].encode()).hexdigest()
    user['password_hash'] = new_password_hash
    user['updated_at'] = datetime.now().isoformat()
    
    return jsonify({'message': 'Password changed successfully'}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户登出"""
    # 在实际项目中，这里可以处理令牌黑名单等
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """验证令牌有效性"""
    current_user = get_jwt_identity()
    
    if current_user not in users_db:
        return jsonify({'valid': False, 'error': 'User not found'}), 404
    
    return jsonify({
        'valid': True,
        'user': {
            'username': current_user,
            'email': users_db[current_user]['email']
        }
    }), 200