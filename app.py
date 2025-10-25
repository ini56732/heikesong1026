from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests

# 加载环境变量
load_dotenv()

# AI服务配置
DEEPSEEK_API_KEY = os.getenv('OPENAI_API_KEY')
DEEPSEEK_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.deepseek.com/v1')
DEEPSEEK_MODEL = os.getenv('OPENAI_MODEL', 'deepseek-chat')

# 外部AI服务调用函数
def call_external_ai_service(message, service_type="nutritionist"):
    """调用外部AI服务获取回复"""
    
    # 如果没有配置API密钥，使用模拟回复
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == 'your_openai_api_key_here':
        return get_simulated_reply(message, service_type)
    
    try:
        # 构建提示词
        system_prompt = get_system_prompt(service_type)
        
        # 调用DeepSeek API
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': DEEPSEEK_MODEL,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': message}
            ],
            'temperature': 0.7,
            'max_tokens': 500,
            'stream': False
        }
        
        response = requests.post(f'{DEEPSEEK_BASE_URL}/chat/completions', 
                                headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"AI服务调用失败: {response.status_code} - {response.text}")
            return get_simulated_reply(message, service_type)
            
    except Exception as e:
        print(f"AI服务调用异常: {e}")
        return get_simulated_reply(message, service_type)

def get_system_prompt(service_type):
    """根据服务类型获取系统提示词"""
    prompts = {
        "nutritionist": """你是一名专业的AI营养师，专注于提供个性化的营养建议和饮食指导。
        你的职责包括：
        1. 分析用户的营养需求和健康状况
        2. 提供科学的饮食建议和膳食计划
        3. 解答营养相关的专业问题
        4. 帮助用户制定合理的营养目标
        
        请用专业、友好的语气回复用户的问题，提供具体、实用的建议。""",
        
        "fitness_trainer": """你是一名专业的AI健身教练，专注于提供个性化的健身指导和训练计划。
        你的职责包括：
        1. 分析用户的健身需求和身体状况
        2. 提供科学的训练建议和运动指导
        3. 解答健身相关的专业问题
        4. 帮助用户制定合理的健身目标
        
        请用专业、友好的语气回复用户的问题，提供具体、实用的建议。"""
    }
    
    return prompts.get(service_type, "你是一名专业的AI助手，请用专业、友好的语气回复用户的问题。")

def get_simulated_reply(message, service_type):
    """模拟AI回复（当外部服务不可用时使用）"""
    
    if service_type == "nutritionist":
        # 营养师关键词匹配回复
        nutrition_responses = {
            "营养概况": "根据您的饮食记录，您今天的蛋白质摄入量已达到目标的75%，碳水化合物82%，脂肪80%。",
            "饮食记录": "您今天的饮食记录：早餐牛奶面包，午餐鸡胸肉沙拉，晚餐鱼肉糙米饭。",
            "营养目标": "您的营养目标：每日蛋白质60g，热量控制1800kcal，每周减重0.5kg。",
            "膳食计划": "本周膳食计划：周一高蛋白早餐+轻食午餐+低脂晚餐，周二水果早餐+均衡午餐+素食晚餐。",
            "减肥": "减肥期间建议：控制总热量摄入，增加蛋白质比例，减少精制碳水化合物。",
            "增肌": "增肌期间建议：增加蛋白质摄入至1.6-2.2g/kg体重，配合力量训练。",
            "糖尿病": "糖尿病患者饮食建议：控制碳水化合物总量，选择低GI食物，定时定量。",
            "高血压": "高血压患者饮食建议：低盐饮食，增加钾摄入，控制体重。"
        }
        
        for keyword, response in nutrition_responses.items():
            if keyword in message:
                return response
        
        return "我理解您想了解营养相关信息。请告诉我您具体想了解什么？比如营养概况、饮食记录、营养目标或膳食计划等。"
    
    else:  # fitness_trainer
        # 健身教练关键词匹配回复
        fitness_responses = {
            "体能概况": "根据您的运动记录，您本周已完成3次训练，总消耗1200卡路里。",
            "训练计划": "当前训练计划：周一力量训练，周三有氧运动，周五柔韧性训练。",
            "运动记录": "您最近一次运动是力量训练，消耗300卡路里。",
            "健身目标": "您的减重目标已完成50%，继续保持！"
        }
        
        for keyword, response in fitness_responses.items():
            if keyword in message:
                return response
        
        return "我理解您想了解健身相关信息。请告诉我您具体想了解什么？比如体能概况、训练计划、运动记录或健身目标等。"

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # 令牌永不过期（开发环境）

# 启用CORS - 仅允许指定的域名
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:5000').split(',')
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS, "methods": ["GET", "POST", "PUT", "DELETE"]}}, supports_credentials=True)

# 初始化JWT
jwt = JWTManager(app)

# 导入并注册蓝图
from routes.auth_routes import auth_bp
from routes.fitness_routes import fitness_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(fitness_bp, url_prefix='/api')

# 模拟数据库数据（实际项目中应使用真实数据库）
users_db = {
    "user1": {
        "username": "user1",
        "password": "password123",
        "profile": {
            "age": 30,
            "gender": "male",
            "height": 175,
            "weight": 70,
            "fitness_level": "intermediate",
            "goals": ["weight_loss", "muscle_gain"]
        }
    }
}

# 模拟健身数据
fitness_data = {
    "user1": {
        "workouts": [
            {
                "id": 1,
                "type": "strength",
                "duration": 60,
                "calories": 300,
                "exercises": [
                    {"name": "Bench Press", "sets": 3, "reps": 10, "weight": 60},
                    {"name": "Squats", "sets": 3, "reps": 12, "weight": 80}
                ],
                "date": "2024-01-15"
            }
        ],
        "fitness_goals": [
            {
                "id": 1,
                "type": "weight_loss",
                "target": 5,
                "current": 2.5,
                "deadline": "2024-03-01"
            }
        ]
    }
}

# 模拟AI对话历史
ai_conversations = {
    "user1": {
        "fitness_trainer": [
            {
                "id": 1,
                "message": "我想开始健身，有什么建议吗？",
                "sender": "user",
                "timestamp": "2024-01-15T10:00:00"
            },
            {
                "id": 2,
                "message": "根据您的身体状况，我建议从基础力量训练开始，每周3次，每次45-60分钟。",
                "sender": "ai",
                "timestamp": "2024-01-15T10:01:00"
            }
        ],
        "nutritionist": [
            {
                "id": 1,
                "message": "您好！我是您的AI营养师，可以根据您的健康状况和饮食偏好为您提供个性化的营养建议。请问有什么我可以帮助您的吗？",
                "sender": "ai",
                "timestamp": "2024-01-15T10:00:00"
            }
        ]
    }
}

# 认证路由
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users_db and users_db[username]['password'] == password:
        access_token = create_access_token(identity=username)
        return jsonify({
            'access_token': access_token,
            'user': {
                'username': username,
                'profile': users_db[username]['profile']
            }
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# AI健身教练对话接口
@app.route('/api/ai/fitness/chat', methods=['POST'])
@jwt_required()
def ai_fitness_chat():
    current_user = get_jwt_identity()
    data = request.get_json()
    message = data.get('message', '')
    
    # 调用外部AI服务
    ai_reply = call_external_ai_service(message, "fitness_trainer")
    
    # 保存对话记录
    if current_user not in ai_conversations:
        ai_conversations[current_user] = {"fitness_trainer": []}
    
    conversation = ai_conversations[current_user]["fitness_trainer"]
    user_message = {
        "id": len(conversation) + 1,
        "message": message,
        "sender": "user",
        "timestamp": datetime.now().isoformat()
    }
    ai_message = {
        "id": len(conversation) + 2,
        "message": ai_reply,
        "sender": "ai",
        "timestamp": datetime.now().isoformat()
    }
    
    conversation.extend([user_message, ai_message])
    
    return jsonify({
        'reply': ai_reply,
        'conversation_id': len(conversation)
    }), 200

# 获取对话历史
@app.route('/api/ai/fitness/history', methods=['GET'])
@jwt_required()
def get_fitness_conversation_history():
    current_user = get_jwt_identity()
    
    if current_user in ai_conversations and "fitness_trainer" in ai_conversations[current_user]:
        return jsonify({
            'conversations': ai_conversations[current_user]["fitness_trainer"]
        }), 200
    
    return jsonify({'conversations': []}), 200

# AI营养师对话接口
@app.route('/api/nutritionist/chat', methods=['POST'])
@jwt_required()
def ai_nutritionist_chat():
    current_user = get_jwt_identity()
    data = request.get_json()
    message = data.get('message', '')
    
    # 调用外部AI服务
    ai_reply = call_external_ai_service(message, "nutritionist")
    
    # 保存对话记录
    if current_user not in ai_conversations:
        ai_conversations[current_user] = {"nutritionist": []}
    
    conversation = ai_conversations[current_user]["nutritionist"]
    user_message = {
        "id": len(conversation) + 1,
        "message": message,
        "sender": "user",
        "timestamp": datetime.now().isoformat()
    }
    ai_message = {
        "id": len(conversation) + 2,
        "message": ai_reply,
        "sender": "ai",
        "timestamp": datetime.now().isoformat()
    }
    
    conversation.extend([user_message, ai_message])
    
    return jsonify({
        'reply': ai_reply,
        'conversation_id': len(conversation)
    }), 200

# 获取营养师对话历史
@app.route('/api/ai/chat/history', methods=['GET'])
@jwt_required()
def get_nutritionist_conversation_history():
    current_user = get_jwt_identity()
    
    if current_user in ai_conversations and "nutritionist" in ai_conversations[current_user]:
        return jsonify({
            'conversations': ai_conversations[current_user]["nutritionist"]
        }), 200
    
    return jsonify({'conversations': []}), 200

# 获取用户健身数据
@app.route('/api/fitness/data', methods=['GET'])
@jwt_required()
def get_fitness_data():
    current_user = get_jwt_identity()
    
    if current_user in fitness_data:
        return jsonify(fitness_data[current_user]), 200
    
    return jsonify({
        'workouts': [],
        'fitness_goals': []
    }), 200

# 提交健身数据
@app.route('/api/fitness/data', methods=['POST'])
@jwt_required()
def submit_fitness_data():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    if current_user not in fitness_data:
        fitness_data[current_user] = {'workouts': [], 'fitness_goals': []}
    
    # 处理不同类型的健身数据
    if 'workout' in data:
        workout = data['workout']
        workout['id'] = len(fitness_data[current_user]['workouts']) + 1
        workout['date'] = datetime.now().isoformat()
        fitness_data[current_user]['workouts'].append(workout)
    
    if 'goal' in data:
        goal = data['goal']
        goal['id'] = len(fitness_data[current_user]['fitness_goals']) + 1
        fitness_data[current_user]['fitness_goals'].append(goal)
    
    return jsonify({'message': 'Data submitted successfully'}), 201

# 获取个性化训练计划
@app.route('/api/fitness/training-plan', methods=['GET'])
@jwt_required()
def get_training_plan():
    current_user = get_jwt_identity()
    
    # 基于用户档案生成个性化训练计划
    user_profile = users_db.get(current_user, {}).get('profile', {})
    
    training_plan = {
        'weekly_schedule': [
            {
                'day': 'Monday',
                'type': 'Strength Training',
                'exercises': ['Bench Press', 'Squats', 'Deadlifts'],
                'duration': 60
            },
            {
                'day': 'Wednesday', 
                'type': 'Cardio',
                'exercises': ['Running', 'Cycling'],
                'duration': 45
            },
            {
                'day': 'Friday',
                'type': 'Flexibility',
                'exercises': ['Yoga', 'Stretching'],
                'duration': 30
            }
        ],
        'recommendations': [
            'Focus on proper form to prevent injuries',
            'Gradually increase weight and intensity',
            'Ensure adequate rest between sessions'
        ]
    }
    
    return jsonify(training_plan), 200

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')