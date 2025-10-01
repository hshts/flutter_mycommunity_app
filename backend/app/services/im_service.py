from flask import request
from app import db
from app.utils.response import success_response, error_response
from datetime import datetime

class IMService:
    """即时通讯服务业务逻辑"""
    @staticmethod
    def send_message(sender_id, receiver_id, content, msg_type="text"):
        # 这里应有消息模型 Message，可参考前端 model/message.dart
        # 暂时返回模拟结果
        return {
            "msg_id": int(datetime.now().timestamp()),
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": content,
            "msg_type": msg_type,
            "created_at": datetime.utcnow().isoformat()
        }, "消息发送成功"

    @staticmethod
    def get_conversation_list(user_id):
        # 返回模拟会话列表
        return [{
            "conversation_id": 1,
            "user_id": user_id,
            "last_message": "你好",
            "unread_count": 2
        }], "获取成功"

    @staticmethod
    def get_unread_count(user_id):
        # 返回模拟未读数
        return 2, "获取成功"