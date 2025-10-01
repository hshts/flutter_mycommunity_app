from flask import jsonify

def success_response(data=None, message="操作成功", code=200):
    """成功响应格式"""
    response = {
        "code": code,
        "message": message,
        "success": True
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), code

def error_response(message="操作失败", code=400, data=None):
    """错误响应格式"""
    response = {
        "code": code,
        "message": message,
        "success": False
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), code

def paginated_response(items, page, per_page, total, message="查询成功"):
    """分页响应格式"""
    data = {
        "items": items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "has_prev": page > 1,
            "has_next": page * per_page < total
        }
    }
    return success_response(data=data, message=message)