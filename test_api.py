#!/usr/bin/env python3
"""
API测试脚本
用于测试AI健身教练后端API的功能
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://localhost:5000"

class APITester:
    def __init__(self):
        self.token = None
        self.user_data = None
    
    def test_health_check(self):
        """测试健康检查接口"""
        print("\n=== 测试健康检查接口 ===")
        try:
            response = requests.get(f"{BASE_URL}/api/health")
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"健康检查失败: {e}")
            return False
    
    def test_register(self):
        """测试用户注册"""
        print("\n=== 测试用户注册 ===")
        
        # 测试数据
        user_data = {
            "username": f"test_user_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "password": "testpassword123",
            "profile": {
                "age": 28,
                "gender": "female",
                "height": 165,
                "weight": 58,
                "fitness_level": "beginner",
                "goals": ["weight_loss", "flexibility"]
            }
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/register",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                print("注册成功!")
                print(f"用户: {result['user']['username']}")
                print(f"令牌: {result['access_token'][:20]}...")
                
                self.token = result['access_token']
                self.user_data = user_data
                return True
            else:
                print(f"注册失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"注册请求失败: {e}")
            return False
    
    def test_login(self):
        """测试用户登录"""
        print("\n=== 测试用户登录 ===")
        
        # 使用预定义的测试用户
        login_data = {
            "username": "user1",
            "password": "password123"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("登录成功!")
                print(f"用户: {result['user']['username']}")
                print(f"令牌: {result['access_token'][:20]}...")
                
                self.token = result['access_token']
                return True
            else:
                print(f"登录失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"登录请求失败: {e}")
            return False
    
    def test_get_profile(self):
        """测试获取用户信息"""
        print("\n=== 测试获取用户信息 ===")
        
        if not self.token:
            print("未登录，跳过测试")
            return False
        
        try:
            response = requests.get(
                f"{BASE_URL}/api/auth/profile",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}"
                }
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("获取用户信息成功!")
                print(f"用户名: {result['username']}")
                print(f"邮箱: {result['email']}")
                print(f"档案: {json.dumps(result['profile'], indent=2, ensure_ascii=False)}")
                return True
            else:
                print(f"获取用户信息失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"获取用户信息请求失败: {e}")
            return False
    
    def test_ai_chat(self):
        """测试AI对话"""
        print("\n=== 测试AI对话 ===")
        
        if not self.token:
            print("未登录，跳过测试")
            return False
        
        test_messages = [
            "你好",
            "我想减肥",
            "推荐一些适合初学者的运动",
            "如何增肌"
        ]
        
        for message in test_messages:
            print(f"\n测试消息: {message}")
            
            try:
                response = requests.post(
                    f"{BASE_URL}/api/ai/chat",
                    json={"message": message},
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.token}"
                    }
                )
                
                print(f"状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"AI回复: {result['reply']}")
                else:
                    print(f"AI对话失败: {response.json()}")
                    return False
                    
            except Exception as e:
                print(f"AI对话请求失败: {e}")
                return False
        
        return True
    
    def test_workout_operations(self):
        """测试运动记录操作"""
        print("\n=== 测试运动记录操作 ===")
        
        if not self.token:
            print("未登录，跳过测试")
            return False
        
        # 添加运动记录
        workout_data = {
            "type": "running",
            "duration": 30,
            "calories": 300,
            "date": "2024-01-15",
            "notes": "晨跑训练"
        }
        
        try:
            # 添加运动记录
            response = requests.post(
                f"{BASE_URL}/api/workouts",
                json=workout_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}"
                }
            )
            
            print(f"添加运动记录状态码: {response.status_code}")
            
            if response.status_code == 201:
                print("添加运动记录成功!")
            else:
                print(f"添加运动记录失败: {response.json()}")
                return False
            
            # 获取运动记录
            response = requests.get(
                f"{BASE_URL}/api/workouts",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}"
                }
            )
            
            print(f"获取运动记录状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"运动记录数量: {len(result['workouts'])}")
                if result['workouts']:
                    print(f"最新运动: {result['workouts'][-1]}")
            else:
                print(f"获取运动记录失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"运动记录操作失败: {e}")
            return False
        
        return True
    
    def test_goal_operations(self):
        """测试健身目标操作"""
        print("\n=== 测试健身目标操作 ===")
        
        if not self.token:
            print("未登录，跳过测试")
            return False
        
        # 添加健身目标
        goal_data = {
            "type": "weight_loss",
            "target": 5.0,
            "deadline": "2024-02-15"
        }
        
        try:
            # 添加健身目标
            response = requests.post(
                f"{BASE_URL}/api/goals",
                json=goal_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}"
                }
            )
            
            print(f"添加健身目标状态码: {response.status_code}")
            
            if response.status_code == 201:
                print("添加健身目标成功!")
            else:
                print(f"添加健身目标失败: {response.json()}")
                return False
            
            # 获取健身目标
            response = requests.get(
                f"{BASE_URL}/api/goals",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}"
                }
            )
            
            print(f"获取健身目标状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"健身目标数量: {len(result['goals'])}")
                if result['goals']:
                    print(f"最新目标: {result['goals'][-1]}")
            else:
                print(f"获取健身目标失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"健身目标操作失败: {e}")
            return False
        
        return True
    
    def test_progress_tracking(self):
        """测试健身进度跟踪"""
        print("\n=== 测试健身进度跟踪 ===")
        
        if not self.token:
            print("未登录，跳过测试")
            return False
        
        try:
            response = requests.get(
                f"{BASE_URL}/api/progress",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}"
                }
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("获取健身进度成功!")
                print(f"进度统计: {json.dumps(result['progress'], indent=2, ensure_ascii=False)}")
                return True
            else:
                print(f"获取健身进度失败: {response.json()}")
                return False
                
        except Exception as e:
            print(f"健身进度请求失败: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始运行AI健身教练API测试...")
        
        tests = [
            ("健康检查", self.test_health_check),
            ("用户登录", self.test_login),
            ("获取用户信息", self.test_get_profile),
            ("AI对话", self.test_ai_chat),
            ("运动记录操作", self.test_workout_operations),
            ("健身目标操作", self.test_goal_operations),
            ("健身进度跟踪", self.test_progress_tracking)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                success = test_func()
                results.append((test_name, success))
                print(f"{test_name}: {'✓ 通过' if success else '✗ 失败'}")
            except Exception as e:
                print(f"{test_name}: ✗ 异常 - {e}")
                results.append((test_name, False))
        
        # 统计结果
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        print(f"\n=== 测试结果 ===")
        print(f"通过: {passed}/{total}")
        print(f"成功率: {passed/total*100:.1f}%")
        
        # 显示详细结果
        for test_name, success in results:
            status = "✓ 通过" if success else "✗ 失败"
            print(f"{test_name}: {status}")
        
        return all(success for _, success in results)

def main():
    """主函数"""
    tester = APITester()
    
    # 检查服务是否运行
    print("检查API服务状态...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print("API服务未运行，请先启动服务: python app.py")
            return
    except:
        print("API服务未运行，请先启动服务: python app.py")
        return
    
    # 运行测试
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 所有测试通过! API功能正常。")
    else:
        print("\n❌ 部分测试失败，请检查API服务。")

if __name__ == "__main__":
    main()