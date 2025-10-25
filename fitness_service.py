import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class FitnessService:
    """AI健身教练服务类"""
    
    def __init__(self):
        self.exercise_database = self._load_exercise_database()
        self.training_templates = self._load_training_templates()
    
    def _load_exercise_database(self) -> Dict:
        """加载运动数据库"""
        return {
            "strength": [
                {
                    "name": "深蹲",
                    "category": "strength",
                    "muscle_group": "腿部, 核心",
                    "difficulty": "beginner",
                    "description": "基础的下半身力量训练",
                    "instructions": "双脚与肩同宽，背部挺直，慢慢下蹲至大腿与地面平行"
                },
                {
                    "name": "卧推",
                    "category": "strength", 
                    "muscle_group": "胸部, 肩部, 三头肌",
                    "difficulty": "intermediate",
                    "description": "上半身力量训练",
                    "instructions": "平躺在卧推凳上，双手握杠铃，缓慢下放至胸部然后推起"
                }
            ],
            "cardio": [
                {
                    "name": "跑步",
                    "category": "cardio",
                    "muscle_group": "全身",
                    "difficulty": "beginner",
                    "description": "有氧运动，提高心肺功能",
                    "instructions": "保持均匀呼吸，控制速度和时间"
                }
            ],
            "flexibility": [
                {
                    "name": "瑜伽",
                    "category": "flexibility",
                    "muscle_group": "全身",
                    "difficulty": "beginner",
                    "description": "提高身体柔韧性和平衡性",
                    "instructions": "跟随指导进行各种瑜伽姿势"
                }
            ]
        }
    
    def _load_training_templates(self) -> Dict:
        """加载训练计划模板"""
        return {
            "beginner": {
                "name": "初学者训练计划",
                "description": "适合健身新手的全面训练计划",
                "weekly_schedule": [
                    {
                        "day": "周一",
                        "focus": "全身力量",
                        "exercises": ["深蹲", "俯卧撑", "仰卧起坐"],
                        "duration": 30
                    },
                    {
                        "day": "周三", 
                        "focus": "有氧运动",
                        "exercises": ["跑步", "跳绳"],
                        "duration": 20
                    },
                    {
                        "day": "周五",
                        "focus": "柔韧性",
                        "exercises": ["瑜伽", "拉伸"],
                        "duration": 15
                    }
                ]
            },
            "intermediate": {
                "name": "中级训练计划",
                "description": "适合有一定基础的健身者",
                "weekly_schedule": [
                    {
                        "day": "周一",
                        "focus": "胸部+三头肌",
                        "exercises": ["卧推", "哑铃飞鸟", "三头肌下压"],
                        "duration": 45
                    },
                    {
                        "day": "周二",
                        "focus": "背部+二头肌", 
                        "exercises": ["引体向上", "划船", "弯举"],
                        "duration": 45
                    },
                    {
                        "day": "周四",
                        "focus": "腿部",
                        "exercises": ["深蹲", "腿举", "腿弯举"],
                        "duration": 45
                    },
                    {
                        "day": "周五",
                        "focus": "有氧+核心",
                        "exercises": ["跑步", "平板支撑", "俄罗斯转体"],
                        "duration": 30
                    }
                ]
            }
        }
    
    def generate_personalized_plan(self, user_profile: Dict) -> Dict:
        """生成个性化训练计划"""
        fitness_level = user_profile.get('fitness_level', 'beginner')
        goals = user_profile.get('goals', [])
        
        # 根据用户水平选择模板
        template = self.training_templates.get(fitness_level, self.training_templates['beginner'])
        
        # 个性化调整
        personalized_plan = template.copy()
        
        # 根据目标调整计划
        if 'weight_loss' in goals:
            personalized_plan['description'] += " - 重点减脂"
            # 增加有氧运动比例
            for day in personalized_plan['weekly_schedule']:
                if '有氧' in day['focus']:
                    day['duration'] += 10
        
        if 'muscle_gain' in goals:
            personalized_plan['description'] += " - 重点增肌"
            # 增加力量训练强度
            for day in personalized_plan['weekly_schedule']:
                if any(keyword in day['focus'] for keyword in ['力量', '胸部', '背部', '腿部']):
                    day['duration'] += 15
        
        return personalized_plan
    
    def analyze_workout_data(self, workout_data: List[Dict]) -> Dict:
        """分析运动数据"""
        if not workout_data:
            return {
                "summary": "暂无运动数据",
                "recommendations": ["开始记录您的第一次运动吧！"]
            }
        
        # 计算统计数据
        total_workouts = len(workout_data)
        total_calories = sum(workout.get('calories_burned', 0) for workout in workout_data)
        avg_duration = sum(workout.get('duration', 0) for workout in workout_data) / total_workouts
        
        # 分析趋势
        recent_workouts = sorted(workout_data, key=lambda x: x.get('workout_date', ''), reverse=True)[:7]
        weekly_frequency = len(recent_workouts)
        
        analysis = {
            "summary": f"您已完成{total_workouts}次运动，共消耗{total_calories}卡路里",
            "stats": {
                "total_workouts": total_workouts,
                "total_calories": total_calories,
                "average_duration": round(avg_duration, 1),
                "weekly_frequency": weekly_frequency
            },
            "recommendations": []
        }
        
        # 生成建议
        if weekly_frequency < 3:
            analysis["recommendations"].append("建议增加运动频率，每周至少3次")
        
        if avg_duration < 30:
            analysis["recommendations"].append("每次运动时间可以适当延长至30分钟以上")
        
        return analysis
    
    def get_exercise_recommendations(self, muscle_group: str, difficulty: str = "beginner") -> List[Dict]:
        """获取运动推荐"""
        recommendations = []
        
        for category, exercises in self.exercise_database.items():
            for exercise in exercises:
                if (muscle_group in exercise.get('muscle_group', '') and 
                    exercise.get('difficulty') == difficulty):
                    recommendations.append(exercise)
        
        return recommendations[:5]  # 返回前5个推荐
    
    def calculate_calories_burned(self, exercise: str, duration: int, user_weight: float) -> float:
        """计算卡路里消耗"""
        # 基础代谢率估算（简化版）
        met_values = {
            "跑步": 8.0,
            "深蹲": 5.0,
            "卧推": 3.5,
            "瑜伽": 2.5,
            "拉伸": 2.0
        }
        
        met = met_values.get(exercise, 3.0)
        calories = met * user_weight * duration / 60
        
        return round(calories, 1)
    
    def generate_ai_response(self, user_message: str, user_context: Dict) -> str:
        """生成AI回复"""
        # 关键词匹配回复
        responses = {
            "体能概况": self._get_fitness_overview(user_context),
            "训练计划": self._get_training_plan_response(user_context),
            "运动记录": self._get_workout_history_response(user_context),
            "健身目标": self._get_goals_response(user_context),
            "开始健身": "太好了！让我们开始您的健身之旅。首先，我需要了解您的健身目标和当前水平。",
            "如何增肌": "增肌需要结合力量训练和适当的营养。建议每周进行3-4次力量训练，并确保摄入足够的蛋白质。",
            "如何减脂": "减脂需要创造热量赤字。建议结合有氧运动和力量训练，控制饮食热量摄入。"
        }
        
        # 匹配关键词
        for keyword, response in responses.items():
            if keyword in user_message:
                return response
        
        # 默认回复
        return "我理解您想了解健身相关信息。您可以问我关于体能概况、训练计划、运动记录或健身目标的问题。"
    
    def _get_fitness_overview(self, user_context: Dict) -> str:
        """获取体能概况回复"""
        profile = user_context.get('profile', {})
        fitness_level = profile.get('fitness_level', '未知')
        
        return f"根据您的数据，您的体能水平为{fitness_level}。建议加强核心训练和心肺功能。"
    
    def _get_training_plan_response(self, user_context: Dict) -> str:
        """获取训练计划回复"""
        return "当前训练计划：周一力量训练，周三有氧运动，周五柔韧性训练。需要调整计划吗？"
    
    def _get_workout_history_response(self, user_context: Dict) -> str:
        """获取运动记录回复"""
        workouts = user_context.get('workouts', [])
        if workouts:
            recent_workout = workouts[-1]
            return f"您最近一次运动是{recent_workout.get('type', '未知')}，持续{recent_workout.get('duration', 0)}分钟。"
        return "您还没有记录任何运动。开始记录您的第一次运动吧！"
    
    def _get_goals_response(self, user_context: Dict) -> str:
        """获取目标回复"""
        goals = user_context.get('goals', [])
        if goals:
            # 提取目标类型
            goal_types = [goal.get('type', '未知') for goal in goals]
            return f"您的健身目标：{', '.join(goal_types)}。需要我帮您制定具体计划吗？"
        return "您还没有设定健身目标。让我们一起设定明确的目标吧！"