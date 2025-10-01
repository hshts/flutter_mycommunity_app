from app.utils.response import success_response, error_response
from datetime import datetime

class PushService:
    """消息推送服务"""
    @staticmethod
    def push_message(user_id, title, content, msg_type="system"):
        # 实际应集成推送服务，这里模拟
        return {
            "userId": user_id,
            "title": title,
            "content": content,
            "msgType": msg_type,
            "pushTime": datetime.utcnow().isoformat()
        }, "推送成功"