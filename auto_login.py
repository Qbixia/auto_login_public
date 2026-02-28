import requests
import pickle
import os
import uuid

base_url = "https://chat-go.jwzhd.com"
token_file = "token.pkl"

class ChatClient:
    def __init__(self):
        self.token = None
        self.load_token()
    
    def save_token(self):
        """保存token到文件"""
        with open(token_file, 'wb') as f:
            pickle.dump(self.token, f)
    
    def load_token(self):
        """从文件加载token"""
        if os.path.exists(token_file):
            with open(token_file, 'rb') as f:
                self.token = pickle.load(f)
    
    def get_captcha(self):
        url = f"{base_url}/v1/user/captcha"
        response = requests.post(url)
        result = response.json()
        if result["code"] == 1:
            return result["data"]
        else:
            print(f"获取验证码失败: {result['msg']}")
            return None
    
    def get_sms_code(self, mobile, platform="windows"):
        """获取短信验证码"""
        url = f"{base_url}/v1/verification/get-verification-code"
        data = {
            "mobile": mobile,
            "code": "123456",  # 用户输入的人机验证码
            "id": "123",       # 人机验证ID
            "platform": platform
        }
        response = requests.post(url, json=data)
        result = response.json()
        if result["code"] == 1:
            print("短信验证码发送成功")
            return True
        else:
            print(f"短信验证码发送失败: {result['msg']}")
            return False
    
    def verification_login(self, mobile, captcha, device_id=None, platform="windows"):
        """手机号验证码登录"""
        if not device_id:
            device_id = str(uuid.uuid4())
        
        url = f"{base_url}/v1/user/verification-login"
        data = {
            "mobile": mobile,
            "captcha": captcha,
            "deviceId": device_id,
            "platform": platform
        }
        
        response = requests.post(url, json=data)
        result = response.json()
        if result["code"] == 1:
            self.token = result["data"]["token"]
            self.save_token()
            print("登录成功")
            return True
        else:
            print(f"登录失败: {result['msg']}")
            return False
    
    def email_login(self, email, password, device_id=None, platform="windows"):
        """邮箱密码登录"""
        if not device_id:
            device_id = str(uuid.uuid4())
        
        url = f"{base_url}/v1/user/email-login"
        data = {
            "email": email,
            "password": password,
            "deviceId": device_id,
            "platform": platform
        }
        
        response = requests.post(url, json=data)
        result = response.json()
        if result["code"] == 1:
            self.token = result["data"]["token"]
            self.save_token()
            print("登录成功")
            return True
        else:
            print(f"登录失败: {result['msg']}")
            return False

def main():
    client = ChatClient()
    print("请选择登录方式：")
    print("1. 手机号验证码登录")
    print("2. 邮箱密码登录")
    choice = "2"
    
    if choice == "1":
        mobile = input("请输入手机号: ")
        if client.get_sms_code(mobile):
            captcha = input("请输入验证码: ")
            client.verification_login(mobile, captcha)
    elif choice == "2":
        email = "" #你的邮箱
        password = "" #你的密码
        client.email_login(email, password)
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
#注:Token为预留 部分，可以根据个人需求加上