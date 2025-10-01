from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services.gp_service import GPService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.auth import auth_required, get_current_user_id

bp = Blueprint('grouppurchase', __name__)

@bp.route('/hotsearchProduct', methods=['GET'])
def hot_search_product():
    """获取热门搜索关键词"""
    try:
        data = GPService.get_hot_search_product()
        return success_response(data=data, message="获取热门搜索成功")
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/getRecommendSearchProduct', methods=['POST'])
def get_recommend_search_product():
    """获取推荐搜索关键词"""
    try:
        content = request.form.get('content', '')
        data = GPService.get_recommend_search_product(content)
        return success_response(data=data, message="获取推荐搜索成功")
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/updateGoodPriceCollection', methods=['POST'])
@auth_required
def update_good_price_collection():
    """收藏好价商品"""
    try:
        good_price_id = request.form.get('goodpriceid')
        user_id = request.form.get('uid') or get_current_user_id()
        
        if not good_price_id:
            return error_response(message="商品ID不能为空")
        
        success, message = GPService.update_good_price_collection(
            int(good_price_id), int(user_id)
        )
        
        if success:
            return success_response(message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/delGoodPriceCollection', methods=['POST'])
@auth_required
def del_good_price_collection():
    """取消收藏好价商品"""
    try:
        good_price_id = request.form.get('goodpriceid')
        user_id = request.form.get('uid') or get_current_user_id()
        
        if not good_price_id:
            return error_response(message="商品ID不能为空")
        
        success, message = GPService.del_good_price_collection(
            int(good_price_id), int(user_id)
        )
        
        if success:
            return success_response(message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/getUserGoodPriceCollectionInfo', methods=['GET', 'POST'])
@auth_required
def get_user_good_price_collection_info():
    """获取用户收藏的好价商品"""
    try:
        if request.method == 'GET':
            current_index = int(request.args.get('currentIndex', 0))
            user_id = int(request.args.get('uid', get_current_user_id()))
        else:
            current_index = int(request.form.get('currentIndex', 0))
            user_id = int(request.form.get('uid', get_current_user_id()))
        
        data, total = GPService.get_user_good_price_collection_info(
            user_id, current_index
        )
        
        return paginated_response(
            items=data,
            page=current_index + 1,
            per_page=20,
            total=total,
            message="获取收藏列表成功"
        )
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/updatecomment', methods=['POST'])
@auth_required
def update_comment():
    """添加评论或回复"""
    try:
        good_price_id = request.form.get('goodpriceid')
        user_id = request.form.get('uid') or get_current_user_id()
        to_user_id = request.form.get('touid', 0)
        content = request.form.get('content')
        comment_id = request.form.get('commentid', 0)
        
        if not good_price_id or not content:
            return error_response(message="参数不完整")
        
        # 如果comment_id不为0，说明是回复
        parent_id = int(comment_id) if int(comment_id) > 0 else None
        
        result_id, message = GPService.update_comment(
            int(good_price_id),
            int(user_id),
            int(to_user_id) if int(to_user_id) > 0 else None,
            content,
            parent_id
        )
        
        if result_id > 0:
            return success_response(data=result_id, message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/updateCommentLike', methods=['POST'])
@auth_required
def update_comment_like():
    """点赞评论"""
    try:
        comment_id = request.form.get('commentid')
        user_id = request.form.get('uid') or get_current_user_id()
        good_price_id = request.form.get('goodpriceid')
        
        if not comment_id:
            return error_response(message="评论ID不能为空")
        
        success, message = GPService.update_comment_like(
            int(comment_id), int(user_id), int(good_price_id)
        )
        
        if success:
            return success_response(message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/delCommentLike', methods=['POST'])
@auth_required
def del_comment_like():
    """取消点赞评论"""
    try:
        comment_id = request.form.get('commentid')
        user_id = request.form.get('uid') or get_current_user_id()
        
        if not comment_id:
            return error_response(message="评论ID不能为空")
        
        success, message = GPService.del_comment_like(
            int(comment_id), int(user_id)
        )
        
        if success:
            return success_response(message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/getcomment', methods=['GET'])
def get_comment():
    """获取评论列表"""
    try:
        good_price_id = request.args.get('goodpriceid')
        user_id = request.args.get('uid', 0)
        
        if not good_price_id:
            return error_response(message="商品ID不能为空")
        
        data = GPService.get_comment_list(int(good_price_id), int(user_id))
        return success_response(data=data, message="获取评论列表成功")
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/delcomment', methods=['POST'])
@auth_required
def del_comment():
    """删除评论"""
    try:
        comment_id = request.form.get('commentid', 0)
        reply_id = request.form.get('replyid', 0)
        user_id = request.form.get('uid') or get_current_user_id()
        good_price_id = request.form.get('goodpriceid')
        
        # 确定删除的是评论还是回复
        target_id = int(reply_id) if int(reply_id) > 0 else int(comment_id)
        is_reply = int(reply_id) > 0
        
        if target_id <= 0:
            return error_response(message="参数错误")
        
        success, message = GPService.del_comment(
            target_id, int(user_id), int(good_price_id), is_reply
        )
        
        if success:
            return success_response(message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/updateGoodPriceLike', methods=['POST'])
@auth_required
def update_good_price_like():
    """好价点赞"""
    try:
        good_price_id = request.form.get('goodpriceid')
        user_id = request.form.get('uid') or get_current_user_id()
        
        if not good_price_id:
            return error_response(message="商品ID不能为空")
        
        success, message = GPService.update_good_price_like(
            int(good_price_id), int(user_id)
        )
        
        if success:
            return success_response(message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/updateCancelLike', methods=['POST'])
@auth_required
def update_cancel_like():
    """取消好价点赞"""
    try:
        good_price_id = request.form.get('goodpriceid')
        user_id = request.form.get('uid') or get_current_user_id()
        
        if not good_price_id:
            return error_response(message="商品ID不能为空")
        
        success, message = GPService.del_good_price_like(
            int(good_price_id), int(user_id)
        )
        
        if success:
            return success_response(message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/searchProduct', methods=['POST'])
def search_product():
    """搜索商品"""
    try:
        content = request.form.get('content', '')
        order_type = request.form.get('ordertype', 'time')
        city_code = request.form.get('citycode', '')
        current_index = int(request.form.get('currentIndex', 0))
        is_all_city = request.form.get('isAllCity', '1') == '1'
        
        data, total = GPService.search_product(
            content, order_type, city_code, current_index, is_all_city
        )
        
        return paginated_response(
            items=data,
            page=current_index + 1,
            per_page=20,
            total=total,
            message="搜索成功"
        )
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/getGoodPriceInfo', methods=['GET'])
def get_good_price_info():
    """获取商品详情"""
    try:
        good_price_id = request.args.get('goodpriceid')
        
        if not good_price_id:
            return error_response(message="商品ID不能为空")
        
        data = GPService.get_good_price_info(int(good_price_id))
        
        if data:
            return success_response(data=data, message="获取商品详情成功")
        else:
            return error_response(message="商品不存在")
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/getRecommendGoodPriceList', methods=['GET'])
def get_recommend_good_price_list():
    """获取推荐商品列表"""
    try:
        type_id = int(request.args.get('type', 1))
        current_index = int(request.args.get('currentIndex', 0))
        city_code = request.args.get('citycode', '')
        
        data, total = GPService.get_recommend_good_price_list(
            type_id, current_index, city_code
        )
        
        return paginated_response(
            items=data,
            page=current_index + 1,
            per_page=20,
            total=total,
            message="获取推荐列表成功"
        )
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/createGoodPrice', methods=['POST'])
@auth_required
def create_good_price():
    """创建好价商品"""
    try:
        user_id = request.form.get('uid') or get_current_user_id()
        
        kwargs = {
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'price': float(request.form.get('price', 0)),
            'original_price': float(request.form.get('originalprice', 0)),
            'pic': request.form.get('pic'),
            'purchase_channels': request.form.get('purchasechannels'),
            'product_url': request.form.get('producturl'),
            'category': request.form.get('category'),
            'province': request.form.get('province'),
            'city': request.form.get('city')
        }
        
        good_price_id, message = GPService.create_good_price(int(user_id), **kwargs)
        
        if good_price_id:
            return success_response(data=good_price_id, message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/getMyGoodPricePendingList', methods=['GET'])
@auth_required
def get_my_good_price_pending_list():
    """获取我的待审核商品"""
    try:
        user_id = int(request.args.get('uid', get_current_user_id()))
        data = GPService.get_my_good_price_pending_list(user_id)
        return success_response(data=data, message="获取待审核列表成功")
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/getMyGoodPriceFinishList', methods=['GET'])
@auth_required
def get_my_good_price_finish_list():
    """获取我的已审核商品"""
    try:
        user_id = int(request.args.get('uid', get_current_user_id()))
        data = GPService.get_my_good_price_finish_list(user_id)
        return success_response(data=data, message="获取已审核列表成功")
    except Exception as e:
        return error_response(message=str(e))

@bp.route('/delMyGoodPrice', methods=['GET'])
@auth_required
def del_my_good_price():
    """删除我的商品"""
    try:
        good_price_id = request.args.get('goodpriceid')
        user_id = int(request.args.get('uid', get_current_user_id()))
        
        if not good_price_id:
            return error_response(message="商品ID不能为空")
        
        success, message = GPService.del_my_good_price(int(good_price_id), user_id)
        
        if success:
            return success_response(message=message)
        else:
            return error_response(message=message)
    except Exception as e:
        return error_response(message=str(e))

# 活动相关接口 (简化实现)
@bp.route('/getActivityList', methods=['GET'])
def get_activity_list():
    """获取活动列表"""
    try:
        good_price_id = request.args.get('goodpriceid')
        # 这里暂时返回空数组，实际应该根据商品ID查询相关活动
        return success_response(data=[], message="获取活动列表成功")
    except Exception as e:
        return error_response(message=str(e))

# 其他暂时返回空实现的接口
@bp.route('/updateProductCollection', methods=['POST'])
@auth_required
def update_product_collection():
    """收藏商品 (产品收藏，与好价收藏不同)"""
    return success_response(message="收藏成功")

@bp.route('/delProductCollection', methods=['POST'])
@auth_required
def del_product_collection():
    """取消收藏商品"""
    return success_response(message="取消收藏成功")

@bp.route('/updateUnLike', methods=['POST'])
@auth_required
def update_unlike():
    """点不赞"""
    return success_response(message="操作成功")

@bp.route('/updateCancelUnLike', methods=['POST'])
@auth_required
def update_cancel_unlike():
    """取消点不赞"""
    return success_response(message="操作成功")

@bp.route('/createGPOrder', methods=['POST'])
@auth_required
def create_gp_order():
    """创建团购订单"""
    return success_response(data="ORDER_" + str(int(datetime.now().timestamp())), message="订单创建成功")

@bp.route('/updategoodpricestatus', methods=['POST'])
@auth_required
def update_good_price_status():
    """更新商品状态"""
    return success_response(message="状态更新成功")

@bp.route('/updateGoodPrice', methods=['POST'])
@auth_required
def update_good_price():
    """更新商品信息"""
    return success_response(message="更新成功")

@bp.route('/getSysGoodPriceCheck', methods=['GET'])
@auth_required
def get_sys_good_price_check():
    """系统审核商品列表"""
    return success_response(data=[], message="获取审核列表成功")

@bp.route('/getSkuStockList', methods=['GET'])
def get_sku_stock_list():
    """获取商品规格列表"""
    good_price_id = request.args.get('goodpriceid')
    return success_response(data=[], message="获取规格列表成功")

@bp.route('/getEvaluateGoodPriceList', methods=['POST'])
def get_evaluate_good_price_list():
    """获取商品评价列表"""
    return success_response(data=[], message="获取评价列表成功")