from api import db
from api.models.group_purchase import (
    GoodPrice, GoodPriceCollection, GoodPriceLike, 
    GoodPriceComment, GoodPriceCommentReply, GoodPriceCommentLike,
    SkuStock, GroupPurchaseOrder,
    GoodPriceEvaluate, GoodPriceEvaluateReply, GoodPriceEvaluateLike
)
from sqlalchemy import desc, asc, or_, and_
import uuid
from datetime import datetime


class GroupPurchaseService:
    """团购服务类"""
    
    @staticmethod
    def create_good_price(data):
        """创建商品"""
        goodpriceid = str(uuid.uuid4())
        
        good_price = GoodPrice(
            goodpriceid=goodpriceid,
            uid=data.get('uid'),
            title=data.get('title'),
            content=data.get('content'),
            productnum=data.get('productnum', 1),
            category=data.get('category'),
            brand=data.get('brand'),
            totalprice=data.get('totalprice'),
            price=data.get('price'),
            originalprice=data.get('originalprice'),
            discount=data.get('discount'),
            endtime=datetime.fromisoformat(data['endtime']) if data.get('endtime') else None,
            albumpics=data.get('albumpics'),
            pic=data.get('pic'),
            province=data.get('province'),
            city=data.get('city'),
            citycode=data.get('citycode'),
            lat=data.get('lat'),
            lng=data.get('lng'),
            address=data.get('address'),
            addresstitle=data.get('addresstitle'),
            producturl=data.get('producturl'),
            purchasechannels=data.get('purchasechannels'),
            status=0  # 待审核
        )
        
        db.session.add(good_price)
        db.session.commit()
        
        return goodpriceid
    
    @staticmethod
    def update_good_price(goodpriceid, data):
        """更新商品信息"""
        good_price = GoodPrice.query.get(goodpriceid)
        if not good_price:
            return False
        
        # 更新字段
        if 'title' in data:
            good_price.title = data['title']
        if 'content' in data:
            good_price.content = data['content']
        if 'productnum' in data:
            good_price.productnum = data['productnum']
        if 'category' in data:
            good_price.category = data['category']
        if 'brand' in data:
            good_price.brand = data['brand']
        if 'totalprice' in data:
            good_price.totalprice = data['totalprice']
        if 'price' in data:
            good_price.price = data['price']
        if 'originalprice' in data:
            good_price.originalprice = data['originalprice']
        if 'discount' in data:
            good_price.discount = data['discount']
        if 'endtime' in data:
            good_price.endtime = datetime.fromisoformat(data['endtime']) if data['endtime'] else None
        if 'albumpics' in data:
            good_price.albumpics = data['albumpics']
        if 'pic' in data:
            good_price.pic = data['pic']
        if 'province' in data:
            good_price.province = data['province']
        if 'city' in data:
            good_price.city = data['city']
        if 'lat' in data:
            good_price.lat = data['lat']
        if 'lng' in data:
            good_price.lng = data['lng']
        if 'address' in data:
            good_price.address = data['address']
        if 'addresstitle' in data:
            good_price.addresstitle = data['addresstitle']
        if 'producturl' in data:
            good_price.producturl = data['producturl']
        if 'purchasechannels' in data:
            good_price.purchasechannels = data['purchasechannels']
        
        good_price.updatetime = datetime.utcnow()
        
        db.session.commit()
        return True
    
    @staticmethod
    def get_good_price(goodpriceid):
        """获取商品详情"""
        good_price = GoodPrice.query.get(goodpriceid)
        if good_price:
            # 增加浏览数
            good_price.viewnum = (good_price.viewnum or 0) + 1
            db.session.commit()
        return good_price
    
    @staticmethod
    def update_good_price_status(goodpriceid, uid, status, msg=None, tag=None):
        """更新商品状态"""
        good_price = GoodPrice.query.get(goodpriceid)
        if not good_price or good_price.uid != uid:
            return False
        
        good_price.status = status
        if msg:
            good_price.statusmsg = msg
        if tag:
            good_price.tag = tag
        good_price.updatetime = datetime.utcnow()
        
        db.session.commit()
        return True
    
    @staticmethod
    def delete_good_price(goodpriceid, uid):
        """删除商品"""
        good_price = GoodPrice.query.get(goodpriceid)
        if not good_price or good_price.uid != uid:
            return False
        
        db.session.delete(good_price)
        db.session.commit()
        return True
    
    @staticmethod
    def get_recommend_good_price_list(type_filter=None, citycode=None, current_index=0, page_size=20):
        """获取推荐商品列表"""
        query = GoodPrice.query.filter_by(status=1)  # 只显示已审核通过的

        if citycode and citycode != 'allCode':
            query = query.filter_by(citycode=citycode)
        
        # 按更新时间倒序
        query = query.order_by(desc(GoodPrice.updatetime))
        
        # 分页
        offset = current_index * page_size
        good_prices = query.offset(offset).limit(page_size).all()
        
        return good_prices
    
    @staticmethod
    def search_product(content, ordertype='updatetime', citycode=None, current_index=0, is_all_city=False, page_size=20):
        """搜索商品"""
        query = GoodPrice.query.filter_by(status=1)
        
        # 搜索条件
        if content:
            query = query.filter(
                or_(
                    GoodPrice.title.like(f'%{content}%'),
                    GoodPrice.content.like(f'%{content}%'),
                    GoodPrice.brand.like(f'%{content}%')
                )
            )
        
        # 城市筛选
        if not is_all_city and citycode and citycode != 'allCode':
            query = query.filter_by(citycode=citycode)
        
        # 排序
        if ordertype == 'likenum':
            query = query.order_by(desc(GoodPrice.likenum))
        elif ordertype == 'viewnum':
            query = query.order_by(desc(GoodPrice.viewnum))
        elif ordertype == 'price':
            query = query.order_by(asc(GoodPrice.price))
        else:  # 默认按更新时间
            query = query.order_by(desc(GoodPrice.updatetime))
        
        # 分页
        offset = current_index * page_size
        good_prices = query.offset(offset).limit(page_size).all()
        
        return good_prices
    
    @staticmethod
    def get_my_good_price_pending_list(uid):
        """获取我的待审核商品列表"""
        good_prices = GoodPrice.query.filter_by(uid=uid, status=0).order_by(desc(GoodPrice.createtime)).all()
        return good_prices
    
    @staticmethod
    def get_my_good_price_finish_list(uid):
        """获取我的已审核商品列表"""
        good_prices = GoodPrice.query.filter(
            GoodPrice.uid == uid,
            GoodPrice.status.in_([1, 2])
        ).order_by(desc(GoodPrice.createtime)).all()
        return good_prices
    
    # 收藏相关
    @staticmethod
    def add_collection(uid, goodpriceid):
        """添加收藏"""
        # 检查是否已收藏
        existing = GoodPriceCollection.query.filter_by(uid=uid, goodpriceid=goodpriceid).first()
        if existing:
            return True
        
        collection = GoodPriceCollection(uid=uid, goodpriceid=goodpriceid)
        db.session.add(collection)
        
        # 更新商品收藏数
        good_price = GoodPrice.query.get(goodpriceid)
        if good_price:
            good_price.collectionnum = (good_price.collectionnum or 0) + 1
        
        db.session.commit()
        return True
    
    @staticmethod
    def remove_collection(uid, goodpriceid):
        """取消收藏"""
        collection = GoodPriceCollection.query.filter_by(uid=uid, goodpriceid=goodpriceid).first()
        if not collection:
            return True
        
        db.session.delete(collection)
        
        # 更新商品收藏数
        good_price = GoodPrice.query.get(goodpriceid)
        if good_price and good_price.collectionnum > 0:
            good_price.collectionnum -= 1
        
        db.session.commit()
        return True
    
    @staticmethod
    def get_user_collections(uid, current_index=0, page_size=20):
        """获取用户收藏的商品"""
        collections = GoodPriceCollection.query.filter_by(uid=uid).order_by(desc(GoodPriceCollection.createtime)).all()
        goodprice_ids = [c.goodpriceid for c in collections]
        
        if not goodprice_ids:
            return []
        
        # 分页查询商品
        offset = current_index * page_size
        good_prices = GoodPrice.query.filter(GoodPrice.goodpriceid.in_(goodprice_ids)).offset(offset).limit(page_size).all()
        
        return good_prices
    
    @staticmethod
    def check_user_collection(uid, goodpriceid):
        """检查用户是否收藏了商品"""
        collection = GoodPriceCollection.query.filter_by(uid=uid, goodpriceid=goodpriceid).first()
        return collection is not None
    
    # 点赞相关
    @staticmethod
    def add_like(uid, goodpriceid):
        """点赞商品"""
        # 检查是否已点赞
        existing = GoodPriceLike.query.filter_by(uid=uid, goodpriceid=goodpriceid, liketype=1).first()
        if existing:
            return True
        
        # 如果之前点了不赞，则删除
        unlike = GoodPriceLike.query.filter_by(uid=uid, goodpriceid=goodpriceid, liketype=2).first()
        if unlike:
            db.session.delete(unlike)
            good_price = GoodPrice.query.get(goodpriceid)
            if good_price and good_price.unlikenum > 0:
                good_price.unlikenum -= 1
        
        like = GoodPriceLike(uid=uid, goodpriceid=goodpriceid, liketype=1)
        db.session.add(like)
        
        # 更新商品点赞数
        good_price = GoodPrice.query.get(goodpriceid)
        if good_price:
            good_price.likenum = (good_price.likenum or 0) + 1
        
        db.session.commit()
        return True
    
    @staticmethod
    def remove_like(uid, goodpriceid):
        """取消点赞"""
        like = GoodPriceLike.query.filter_by(uid=uid, goodpriceid=goodpriceid, liketype=1).first()
        if not like:
            return True
        
        db.session.delete(like)
        
        # 更新商品点赞数
        good_price = GoodPrice.query.get(goodpriceid)
        if good_price and good_price.likenum > 0:
            good_price.likenum -= 1
        
        db.session.commit()
        return True
    
    @staticmethod
    def add_unlike(uid, goodpriceid):
        """点不赞商品"""
        # 检查是否已点不赞
        existing = GoodPriceLike.query.filter_by(uid=uid, goodpriceid=goodpriceid, liketype=2).first()
        if existing:
            return True
        
        # 如果之前点了赞，则删除
        like = GoodPriceLike.query.filter_by(uid=uid, goodpriceid=goodpriceid, liketype=1).first()
        if like:
            db.session.delete(like)
            good_price = GoodPrice.query.get(goodpriceid)
            if good_price and good_price.likenum > 0:
                good_price.likenum -= 1
        
        unlike = GoodPriceLike(uid=uid, goodpriceid=goodpriceid, liketype=2)
        db.session.add(unlike)
        
        # 更新商品点不赞数
        good_price = GoodPrice.query.get(goodpriceid)
        if good_price:
            good_price.unlikenum = (good_price.unlikenum or 0) + 1
        
        db.session.commit()
        return True
    
    @staticmethod
    def remove_unlike(uid, goodpriceid):
        """取消点不赞"""
        unlike = GoodPriceLike.query.filter_by(uid=uid, goodpriceid=goodpriceid, liketype=2).first()
        if not unlike:
            return True
        
        db.session.delete(unlike)
        
        # 更新商品点不赞数
        good_price = GoodPrice.query.get(goodpriceid)
        if good_price and good_price.unlikenum > 0:
            good_price.unlikenum -= 1
        
        db.session.commit()
        return True
    
    # 评论相关
    @staticmethod
    def add_comment(data):
        """添加评论或回复"""
        commentid = data.get('commentid')
        
        if commentid:
            # 这是回复
            replyid = str(uuid.uuid4())
            reply = GoodPriceCommentReply(
                replyid=replyid,
                commentid=commentid,
                goodpriceid=data['goodpriceid'],
                uid=data['uid'],
                touid=data.get('touid'),
                content=data['content']
            )
            db.session.add(reply)
            result_id = replyid
        else:
            # 这是评论
            comment = GoodPriceComment(
                goodpriceid=data['goodpriceid'],
                uid=data['uid'],
                touid=data.get('touid'),
                content=data['content']
            )
            db.session.add(comment)
            db.session.flush()  # 获取自动生成的 commentid
            result_id = comment.commentid
            
            # 更新商品评论数
            good_price = GoodPrice.query.get(data['goodpriceid'])
            if good_price:
                good_price.commentnum = (good_price.commentnum or 0) + 1
        
        db.session.commit()
        return result_id
    
    @staticmethod
    def delete_comment(commentid, uid, replyid=None, goodpriceid=None):
        """删除评论或回复"""
        if replyid:
            # 删除回复
            reply = GoodPriceCommentReply.query.get(replyid)
            if not reply or reply.uid != uid:
                return False
            db.session.delete(reply)
        else:
            # 删除评论
            comment = GoodPriceComment.query.get(commentid)
            if not comment or comment.uid != uid:
                return False
            
            # 删除该评论的所有回复
            replies = GoodPriceCommentReply.query.filter_by(commentid=commentid).all()
            for reply in replies:
                db.session.delete(reply)
            
            db.session.delete(comment)
            
            # 更新商品评论数
            if goodpriceid:
                good_price = GoodPrice.query.get(goodpriceid)
                if good_price and good_price.commentnum > 0:
                    good_price.commentnum -= 1
        
        db.session.commit()
        return True
    
    @staticmethod
    def get_comments(goodpriceid, uid=None):
        """获取商品评论列表"""
        comments = GoodPriceComment.query.filter_by(goodpriceid=goodpriceid).order_by(desc(GoodPriceComment.createtime)).all()
        return comments
    
    @staticmethod
    def add_comment_like(commentid, uid, likeuid, goodpriceid):
        """评论点赞"""
        # 检查是否已点赞
        existing = GoodPriceCommentLike.query.filter_by(commentid=commentid, uid=uid).first()
        if existing:
            return True
        
        like = GoodPriceCommentLike(
            commentid=commentid,
            uid=uid,
            likeuid=likeuid,
            goodpriceid=goodpriceid
        )
        db.session.add(like)
        
        # 更新评论点赞数
        comment = GoodPriceComment.query.get(commentid)
        if comment:
            comment.likenum = (comment.likenum or 0) + 1
        
        db.session.commit()
        return True
    
    @staticmethod
    def remove_comment_like(commentid, uid, likeuid):
        """取消评论点赞"""
        like = GoodPriceCommentLike.query.filter_by(commentid=commentid, uid=uid, likeuid=likeuid).first()
        if not like:
            return True
        
        db.session.delete(like)
        
        # 更新评论点赞数
        comment = GoodPriceComment.query.get(commentid)
        if comment and comment.likenum > 0:
            comment.likenum -= 1
        
        db.session.commit()
        return True
    
    # SKU相关
    @staticmethod
    def get_sku_stock_list(goodpriceid):
        """获取商品SKU列表"""
        skus = SkuStock.query.filter_by(goodpriceid=goodpriceid).all()
        return skus
    
    # 订单相关
    @staticmethod
    def create_order(actid, uid, touid=None):
        """创建团购订单"""
        orderid = str(uuid.uuid4())
        
        order = GroupPurchaseOrder(
            orderid=orderid,
            actid=actid,
            uid=uid,
            touid=touid,
            amount=0,  # 金额需要后续计算
            status=0  # 待支付
        )
        
        db.session.add(order)
        db.session.commit()
        
        return orderid
    
    # 评价相关
    @staticmethod
    def add_evaluate(data):
        """添加商品评价"""
        evaluate = GoodPriceEvaluate(
            goodpriceid=data['goodpriceid'],
            uid=data['uid'],
            orderid=data.get('orderid'),
            content=data['content'],
            images=data.get('images'),
            liketype=data.get('liketype', 5)
        )
        
        db.session.add(evaluate)
        db.session.flush()  # 获取自动生成的 evaluateid
        evaluateid = evaluate.evaluateid
        db.session.commit()
        
        return evaluateid
    
    @staticmethod
    def get_evaluate_list(goodpriceid, current_index=0, page_size=20):
        """获取商品评价列表"""
        query = GoodPriceEvaluate.query.filter_by(goodpriceid=goodpriceid)
        query = query.order_by(desc(GoodPriceEvaluate.createtime))
        
        # 分页
        offset = current_index * page_size
        evaluates = query.offset(offset).limit(page_size).all()
        
        return evaluates
    
    @staticmethod
    def get_evaluate(evaluateid):
        """获取单个评价详情"""
        return GoodPriceEvaluate.query.get(evaluateid)
    
    @staticmethod
    def add_evaluate_reply(data):
        """添加评价回复"""
        replyid = str(uuid.uuid4())
        
        reply = GoodPriceEvaluateReply(
            replyid=replyid,
            evaluateid=data['evaluateid'],
            goodpriceid=data['goodpriceid'],
            uid=data['uid'],
            touid=data.get('touid'),
            content=data['content']
        )
        
        db.session.add(reply)
        
        # 更新评价的回复数
        evaluate = GoodPriceEvaluate.query.get(data['evaluateid'])
        if evaluate:
            evaluate.replynum = (evaluate.replynum or 0) + 1
        
        db.session.commit()
        
        return replyid
    
    @staticmethod
    def get_evaluate_replies(evaluateid):
        """获取评价回复列表"""
        replies = GoodPriceEvaluateReply.query.filter_by(evaluateid=evaluateid).order_by(
            GoodPriceEvaluateReply.createtime
        ).all()
        return replies
    
    @staticmethod
    def add_evaluate_like(evaluateid, uid, likeuid, goodpriceid):
        """评价点赞"""
        # 检查是否已点赞
        existing = GoodPriceEvaluateLike.query.filter_by(evaluateid=evaluateid, uid=uid).first()
        if existing:
            return True
        
        like = GoodPriceEvaluateLike(
            evaluateid=evaluateid,
            uid=uid,
            likeuid=likeuid,
            goodpriceid=goodpriceid
        )
        db.session.add(like)
        
        # 更新评价点赞数
        evaluate = GoodPriceEvaluate.query.get(evaluateid)
        if evaluate:
            evaluate.likenum = (evaluate.likenum or 0) + 1
        
        db.session.commit()
        return True
    
    @staticmethod
    def remove_evaluate_like(evaluateid, uid, likeuid):
        """取消评价点赞"""
        like = GoodPriceEvaluateLike.query.filter_by(evaluateid=evaluateid, uid=uid, likeuid=likeuid).first()
        if not like:
            return True
        
        db.session.delete(like)
        
        # 更新评价点赞数
        evaluate = GoodPriceEvaluate.query.get(evaluateid)
        if evaluate and evaluate.likenum > 0:
            evaluate.likenum -= 1
        
        db.session.commit()
        return True
    
    @staticmethod
    def get_activities_by_goodprice(goodpriceid):
        """获取商品关联的活动列表"""
        from api.models.activity import Activity
        if not goodpriceid:
            return []
        activities = Activity.query.filter_by(goodpriceid=goodpriceid).all()
        return activities
