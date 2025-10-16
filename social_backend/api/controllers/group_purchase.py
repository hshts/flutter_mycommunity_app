from flask import request
from flask_restx import Namespace, Resource, fields
from api.services.group_purchase_service import GroupPurchaseService
from api.utils.auth import token_required

# 创建命名空间
ns = Namespace('grouppurchase', description='团购相关操作')

# 定义请求和响应模型
create_good_price_model = ns.model('CreateGoodPrice', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'title': fields.String(required=True, description='商品标题'),
    'content': fields.String(description='商品详情'),
    'productnum': fields.Integer(description='商品数量'),
    'category': fields.String(description='分类'),
    'brand': fields.String(description='品牌'),
    'totalprice': fields.Float(description='总价'),
    'price': fields.Float(required=True, description='现价'),
    'originalprice': fields.Float(description='原价'),
    'endtime': fields.String(description='结束时间(ISO格式)'),
    'albumpics': fields.String(description='图片列表'),
    'pic': fields.String(description='主图'),
    'province': fields.String(description='省份'),
    'city': fields.String(description='城市'),
    'citycode': fields.String(description='城市代码'),
    'producturl': fields.String(description='商品链接'),
    'purchasechannels': fields.String(description='购买渠道'),
    'discount': fields.Float(description='折扣'),
    'lat': fields.Float(description='纬度'),
    'lng': fields.Float(description='经度'),
    'address': fields.String(description='地址'),
    'addresstitle': fields.String(description='地址标题'),
})

collection_model = ns.model('Collection', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'productid': fields.String(required=True, description='商品ID'),
    'uid': fields.Integer(required=True, description='用户ID')
})

goodprice_collection_model = ns.model('GoodPriceCollection', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'goodpriceid': fields.String(required=True, description='商品ID'),
    'uid': fields.Integer(required=True, description='用户ID')
})

comment_model = ns.model('Comment', {
    'commentid': fields.String(description='评论ID(回复时使用)'),
    'token': fields.String(required=True, description='用户认证令牌'),
    'goodpriceid': fields.String(required=True, description='商品ID'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'touid': fields.Integer(description='目标用户ID'),
    'content': fields.String(required=True, description='评论内容'),
})

delete_comment_model = ns.model('DeleteComment', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'commentid': fields.String(required=True, description='评论ID'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'replyid': fields.String(description='回复ID'),
    'goodpriceid': fields.String(description='商品ID'),
})

comment_like_model = ns.model('CommentLike', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'commentid': fields.String(required=True, description='评论ID'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'likeuid': fields.Integer(required=True, description='被点赞用户ID'),
    'goodpriceid': fields.String(required=True, description='商品ID'),
})

like_model = ns.model('Like', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'goodpriceid': fields.String(required=True, description='商品ID'),
    'uid': fields.Integer(required=True, description='用户ID')
})

search_model = ns.model('SearchProduct', {
    'content': fields.String(description='搜索内容'),
    'ordertype': fields.String(description='排序类型'),
    'citycode': fields.String(description='城市代码'),
    'currentIndex': fields.Integer(description='当前索引'),
    'isAllCity': fields.Boolean(description='是否所有城市'),
})

update_status_model = ns.model('UpdateStatus', {
    'goodpriceid': fields.String(required=True, description='商品ID'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'token': fields.String(required=True, description='用户认证令牌'),
    'status': fields.Integer(required=True, description='状态'),
    'msg': fields.String(description='消息'),
    'tag': fields.String(description='标签'),
})

create_order_model = ns.model('CreateOrder', {
    'token': fields.String(required=True, description='用户认证令牌'),
    'actid': fields.String(required=True, description='活动ID'),
    'uid': fields.Integer(required=True, description='用户ID'),
    'touid': fields.Integer(description='目标用户ID'),
})


@ns.route('/createGPOrder')
class CreateGPOrder(Resource):
    """3.1 创建团购订单"""
    @ns.expect(create_order_model)
    @token_required
    def post(self):
        """创建团购订单"""
        data = request.json
        orderid = GroupPurchaseService.create_order(
            actid=data['actid'],
            uid=data['uid'],
            touid=data.get('touid')
        )
        return {'success': True, 'orderid': orderid}, 200


@ns.route('/updateProductCollection')
class UpdateProductCollection(Resource):
    """3.2 商品收藏"""
    @ns.expect(collection_model)
    @token_required
    def post(self):
        """收藏商品"""
        data = request.json
        success = GroupPurchaseService.add_collection(
            uid=data['uid'],
            goodpriceid=data['productid']
        )
        return {'success': success}, 200


@ns.route('/getUserGoodPriceCollectionInfo')
class GetUserGoodPriceCollectionInfo(Resource):
    """3.3 获取用户收藏的商品"""
    @token_required
    def get(self):
        """获取用户收藏的商品"""
        current_index = int(request.args.get('currentIndex', 0))
        uid = int(request.args.get('uid'))
        
        good_prices = GroupPurchaseService.get_user_collections(uid, current_index)
        
        return {
            'success': True,
            'data': [gp.to_dict() for gp in good_prices]
        }, 200


@ns.route('/delProductCollection')
class DelProductCollection(Resource):
    """3.4 取消商品收藏"""
    @ns.expect(collection_model)
    @token_required
    def post(self):
        """取消商品收藏"""
        data = request.json
        success = GroupPurchaseService.remove_collection(
            uid=data['uid'],
            goodpriceid=data['productid']
        )
        return {'success': success}, 200


@ns.route('/updatecomment')
class UpdateComment(Resource):
    """3.5 发布商品评论"""
    @ns.expect(comment_model)
    @token_required
    def post(self):
        """发布商品评论"""
        data = request.json
        commentid = GroupPurchaseService.add_comment(data)
        return {'success': True, 'commentid': commentid}, 200


@ns.route('/delcomment')
class DelComment(Resource):
    """3.6 删除商品评论"""
    @ns.expect(delete_comment_model)
    @token_required
    def post(self):
        """删除商品评论"""
        data = request.json
        success = GroupPurchaseService.delete_comment(
            commentid=data['commentid'],
            uid=data['uid'],
            replyid=data.get('replyid'),
            goodpriceid=data.get('goodpriceid')
        )
        return {'success': success}, 200


@ns.route('/updateCommentLike')
class UpdateCommentLike(Resource):
    """3.7 商品评论点赞"""
    @ns.expect(comment_like_model)
    @token_required
    def post(self):
        """商品评论点赞"""
        data = request.json
        success = GroupPurchaseService.add_comment_like(
            commentid=data['commentid'],
            uid=data['uid'],
            likeuid=data['likeuid'],
            goodpriceid=data['goodpriceid']
        )
        return {'success': success}, 200


@ns.route('/getcomment')
class GetComment(Resource):
    """3.8 获取商品评论列表"""
    def get(self):
        """获取商品评论列表"""
        goodpriceid = request.args.get('goodpriceid')
        uid = request.args.get('uid')
        
        comments = GroupPurchaseService.get_comments(goodpriceid, uid)
        
        return {
            'success': True,
            'data': [c.to_dict() for c in comments]
        }, 200


@ns.route('/updateGoodPriceLike')
class UpdateGoodPriceLike(Resource):
    """3.9 商品点赞"""
    @ns.expect(like_model)
    @token_required
    def post(self):
        """商品点赞"""
        data = request.json
        success = GroupPurchaseService.add_like(
            uid=data['uid'],
            goodpriceid=data['goodpriceid']
        )
        return {'success': success}, 200


@ns.route('/updateCancelLike')
class UpdateCancelLike(Resource):
    """3.10 商品取消点赞"""
    @ns.expect(like_model)
    @token_required
    def post(self):
        """商品取消点赞"""
        data = request.json
        success = GroupPurchaseService.remove_like(
            uid=data['uid'],
            goodpriceid=data['goodpriceid']
        )
        return {'success': success}, 200


@ns.route('/searchProduct')
class SearchProduct(Resource):
    """3.11 搜索商品"""
    @ns.expect(search_model)
    def post(self):
        """搜索商品"""
        data = request.json
        good_prices = GroupPurchaseService.search_product(
            content=data.get('content'),
            ordertype=data.get('ordertype', 'updatetime'),
            citycode=data.get('citycode'),
            current_index=data.get('currentIndex', 0),
            is_all_city=data.get('isAllCity', False)
        )
        
        return {
            'success': True,
            'data': [gp.to_dict() for gp in good_prices]
        }, 200


@ns.route('/getGoodPriceInfo')
class GetGoodPriceInfo(Resource):
    """3.12 获取商品详情"""
    def get(self):
        """获取商品详情"""
        goodpriceid = request.args.get('goodpriceid')
        good_price = GroupPurchaseService.get_good_price(goodpriceid)
        
        if not good_price:
            return {'success': False, 'message': 'Good price not found'}, 404
        
        return {
            'success': True,
            'data': good_price.to_dict()
        }, 200


@ns.route('/createGoodPrice')
class CreateGoodPrice(Resource):
    """3.13 提交推荐商品"""
    @ns.expect(create_good_price_model)
    @token_required
    def post(self):
        """提交推荐商品"""
        data = request.json
        goodpriceid = GroupPurchaseService.create_good_price(data)
        return {'success': True, 'goodpriceid': goodpriceid}, 200


@ns.route('/hotsearchProduct')
class HotSearchProduct(Resource):
    """3.14 获取热门搜索商品"""
    def get(self):
        """获取热门搜索商品"""
        # TODO: 实现热门搜索逻辑
        return {'success': True, 'data': []}, 200


@ns.route('/getRecommendSearchProduct')
class GetRecommendSearchProduct(Resource):
    """3.15 获取推荐搜索商品关键词"""
    def post(self):
        """获取推荐搜索商品关键词"""
        # TODO: 实现推荐搜索逻辑
        return {'success': True, 'data': []}, 200


@ns.route('/updateGoodPriceCollection')
class UpdateGoodPriceCollection(Resource):
    """3.16 收藏好价优惠"""
    @ns.expect(goodprice_collection_model)
    @token_required
    def post(self):
        """收藏好价优惠"""
        data = request.json
        success = GroupPurchaseService.add_collection(
            uid=data['uid'],
            goodpriceid=data['goodpriceid']
        )
        return {'success': success}, 200


@ns.route('/delGoodPriceCollection')
class DelGoodPriceCollection(Resource):
    """3.18 取消好价收藏"""
    @ns.expect(goodprice_collection_model)
    @token_required
    def post(self):
        """取消好价收藏"""
        data = request.json
        success = GroupPurchaseService.remove_collection(
            uid=data['uid'],
            goodpriceid=data['goodpriceid']
        )
        return {'success': success}, 200


@ns.route('/updateUnLike')
class UpdateUnLike(Resource):
    """3.19 商品点不赞"""
    @ns.expect(like_model)
    @token_required
    def post(self):
        """商品点不赞"""
        data = request.json
        success = GroupPurchaseService.add_unlike(
            uid=data['uid'],
            goodpriceid=data['goodpriceid']
        )
        return {'success': success}, 200


@ns.route('/updateCancelUnLike')
class UpdateCancelUnLike(Resource):
    """3.20 取消商品点不赞"""
    @ns.expect(like_model)
    @token_required
    def post(self):
        """取消商品点不赞"""
        data = request.json
        success = GroupPurchaseService.remove_unlike(
            uid=data['uid'],
            goodpriceid=data['goodpriceid']
        )
        return {'success': success}, 200


@ns.route('/getActivityList')
class GetActivityList(Resource):
    """3.23 获取相关活动列表"""
    def get(self):
        """获取相关活动列表"""
        goodpriceid = request.args.get('goodpriceid')
        # TODO: 实现获取关联活动逻辑
        return {'success': True, 'data': []}, 200


@ns.route('/updategoodpricestatus')
class UpdateGoodPriceStatus(Resource):
    """3.24 更新商品状态"""
    @ns.expect(update_status_model)
    @token_required
    def post(self):
        """更新商品状态"""
        data = request.json
        success = GroupPurchaseService.update_good_price_status(
            goodpriceid=data['goodpriceid'],
            uid=data['uid'],
            status=data['status'],
            msg=data.get('msg'),
            tag=data.get('tag')
        )
        return {'success': success}, 200


@ns.route('/updateGoodPrice')
class UpdateGoodPrice(Resource):
    """3.25 修改推荐商品"""
    @ns.expect(create_good_price_model)
    @token_required
    def post(self):
        """修改推荐商品"""
        data = request.json
        goodpriceid = data.get('goodpriceid')
        success = GroupPurchaseService.update_good_price(goodpriceid, data)
        return {'success': success, 'goodpriceid': goodpriceid}, 200


@ns.route('/getSysGoodPriceCheck')
class GetSysGoodPriceCheck(Resource):
    """3.26 获取系统待审核商品列表"""
    @token_required
    def get(self):
        """获取系统待审核商品列表"""
        # TODO: 实现系统管理员审核列表逻辑
        return {'success': True, 'data': []}, 200


@ns.route('/getMyGoodPricePendingList')
class GetMyGoodPricePendingList(Resource):
    """3.27 获取我的待审核商品列表"""
    @token_required
    def get(self):
        """获取我的待审核商品列表"""
        uid = int(request.args.get('uid'))
        good_prices = GroupPurchaseService.get_my_good_price_pending_list(uid)
        
        return {
            'success': True,
            'data': [gp.to_dict() for gp in good_prices]
        }, 200


@ns.route('/getMyGoodPriceFinishList')
class GetMyGoodPriceFinishList(Resource):
    """3.28 获取我的已审核商品列表"""
    @token_required
    def get(self):
        """获取我的已审核商品列表"""
        uid = int(request.args.get('uid'))
        good_prices = GroupPurchaseService.get_my_good_price_finish_list(uid)
        
        return {
            'success': True,
            'data': [gp.to_dict() for gp in good_prices]
        }, 200


@ns.route('/delMyGoodPrice')
class DelMyGoodPrice(Resource):
    """3.29 删除我的推荐商品"""
    @token_required
    def get(self):
        """删除我的推荐商品"""
        uid = int(request.args.get('uid'))
        goodpriceid = request.args.get('goodpriceid')
        
        success = GroupPurchaseService.delete_good_price(goodpriceid, uid)
        return {'success': success}, 200


@ns.route('/getRecommendGoodPriceList')
class GetRecommendGoodPriceList(Resource):
    """3.30 获取推荐商品列表"""
    def get(self):
        """获取推荐商品列表"""
        type_filter = request.args.get('type')
        current_index = int(request.args.get('currentIndex', 0))
        citycode = request.args.get('citycode')
        
        good_prices = GroupPurchaseService.get_recommend_good_price_list(
            type_filter=type_filter,
            citycode=citycode,
            current_index=current_index
        )
        
        return {
            'success': True,
            'data': [gp.to_dict() for gp in good_prices]
        }, 200


@ns.route('/getSkuStockList')
class GetSkuStockList(Resource):
    """3.31 获取商品规格列表"""
    def get(self):
        """获取商品规格列表"""
        goodpriceid = request.args.get('goodpriceid')
        skus = GroupPurchaseService.get_sku_stock_list(goodpriceid)
        
        return {
            'success': True,
            'data': [sku.to_dict() for sku in skus]
        }, 200


@ns.route('/getEvaluateGoodPriceList')
class GetEvaluateGoodPriceList(Resource):
    """3.32 获取商品评价列表"""
    def post(self):
        """获取商品评价列表"""
        data = request.json
        # TODO: 实现评价列表逻辑（需要评价表）
        return {'success': True, 'data': []}, 200


@ns.route('/getEvaluateGoodPriceList')
class GetEvaluateGoodPriceList(Resource):
    """3.32 获取商品评价列表"""
    def post(self):
        """获取商品评价列表"""
        data = request.json
        goodpriceid = data.get('goodpriceid')
        current_index = data.get('currentIndex', 0)
        
        if not goodpriceid:
            return {'success': False, 'message': 'Missing goodpriceid'}, 400
        
        evaluates = GroupPurchaseService.get_evaluate_list(goodpriceid, current_index)
        
        return {
            'success': True,
            'data': [e.to_dict() for e in evaluates],
            'total': len(evaluates)
        }, 200


@ns.route('/delCommentLike')
class DelCommentLike(Resource):
    """3.33 取消商品评论点赞"""
    @token_required
    def post(self):
        """取消商品评论点赞"""
        data = request.json
        success = GroupPurchaseService.remove_comment_like(
            commentid=data['commentid'],
            uid=data['uid'],
            likeuid=data['likeuid']
        )
        return {'success': success}, 200


@ns.route('/getUserGoodPriceCollection')
class GetUserGoodPriceCollection(Resource):
    """3.34 获取用户好价收藏状态"""
    @token_required
    def post(self):
        """获取用户好价收藏状态"""
        data = request.json
        uid = data['uid']
        goodpriceid = data.get('goodpriceid')
        
        if goodpriceid:
            is_collected = GroupPurchaseService.check_user_collection(uid, goodpriceid)
            return {'success': True, 'collected': is_collected}, 200
        
        return {'success': False, 'message': 'Missing goodpriceid'}, 400
