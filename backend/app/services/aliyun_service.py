from flask import request
from app.utils.response import success_response, error_response

class AliyunService:
    """阿里云相关服务业务逻辑"""
    @staticmethod
    def send_sms(phone, code):
        # 实际应调用阿里云短信服务，这里模拟
        print(f"发送短信到 {phone}: {code}")
        return True, "短信发送成功"

    @staticmethod
    def send_email(email, code):
        # 实际应调用阿里云邮件服务，这里模拟
        print(f"发送邮件到 {email}: {code}")
        return True, "邮件发送成功"

    @staticmethod
    def upload_oss(file):
        # 实际应调用阿里云OSS，这里模拟
        return {"url": "https://oss.aliyun.com/demo.jpg"}, "上传成功"