from api import db
from datetime import datetime

class GoodPrice(db.Model):
    """好价商品模型"""
    __tablename__ = 'good_prices'
    
    # 基本字段
    goodpriceid = db.Column(db.String(50), primary_key=True)
    uid = db.Column(db.Integer, nullable=False)  # 发布者用户ID
    title = db.Column(db.String(255), nullable=False)  # 商品标题
    content = db.Column(db.Text)  # 商品详情内容
    
    # 商品信息
    productnum = db.Column(db.Integer, default=1)  # 商品数量
    category = db.Column(db.Integer)  # 分类
    brand = db.Column(db.String(100))  # 品牌
    
    # 价格信息
    totalprice = db.Column(db.Float)  # 总价
    price = db.Column(db.Float, nullable=False)  # 现价
    originalprice = db.Column(db.Float)  # 原价
    discount = db.Column(db.Float)  # 折扣
    
    # 时间信息
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    updatetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    endtime = db.Column(db.DateTime)  # 结束时间
    
    # 图片信息
    albumpics = db.Column(db.Text)  # 图片列表
    pic = db.Column(db.String(255))  # 主图
    
    # 位置信息
    province = db.Column(db.String(100))  # 省份
    city = db.Column(db.String(100))  # 城市
    citycode = db.Column(db.String(20))  # 城市代码
    lat = db.Column(db.Float)  # 纬度
    lng = db.Column(db.Float)  # 经度
    address = db.Column(db.String(255))  # 地址
    addresstitle = db.Column(db.String(255))  # 地址标题
    
    # 购买信息
    producturl = db.Column(db.String(500))  # 商品链接
    purchasechannels = db.Column(db.String(100))  # 购买渠道
    
    # 统计信息
    likenum = db.Column(db.Integer, default=0)  # 点赞数
    unlikenum = db.Column(db.Integer, default=0)  # 点不赞数
    collectionnum = db.Column(db.Integer, default=0)  # 收藏数
    commentnum = db.Column(db.Integer, default=0)  # 评论数
    viewnum = db.Column(db.Integer, default=0)  # 浏览数
    
    # 状态信息
    status = db.Column(db.Integer, default=0)  # 0:待审核 1:已通过 2:已拒绝
    statusmsg = db.Column(db.String(255))  # 状态消息
    tag = db.Column(db.String(50))  # 标签
    
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'goodpriceid': self.goodpriceid,
            'uid': self.uid,
            'title': self.title,
            'content': self.content,
            'productnum': self.productnum,
            'category': self.category,
            'brand': self.brand,
            'totalprice': self.totalprice,
            'price': self.price,
            'originalprice': self.originalprice,
            'discount': self.discount,
            'createtime': self.createtime.isoformat() if self.createtime else None,
            'updatetime': self.updatetime.isoformat() if self.updatetime else None,
            'endtime': self.endtime.isoformat() if self.endtime else None,
            'albumpics': self.albumpics,
            'pic': self.pic,
            'province': self.province,
            'city': self.city,
            'citycode': self.citycode,
            'lat': self.lat,
            'lng': self.lng,
            'address': self.address,
            'addresstitle': self.addresstitle,
            'producturl': self.producturl,
            'purchasechannels': self.purchasechannels,
            'likenum': self.likenum,
            'unlikenum': self.unlikenum,
            'collectionnum': self.collectionnum,
            'commentnum': self.commentnum,
            'viewnum': self.viewnum,
            'status': self.status,
            'statusmsg': self.statusmsg,
            'tag': self.tag
        }
    
    def __repr__(self):
        return f'<GoodPrice {self.goodpriceid}>'


class GoodPriceCollection(db.Model):
    """商品收藏模型"""
    __tablename__ = 'good_price_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)  # 用户ID
    goodpriceid = db.Column(db.String(50), nullable=False)  # 商品ID
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'goodpriceid': self.goodpriceid,
            'createtime': self.createtime.isoformat() if self.createtime else None
        }


class GoodPriceLike(db.Model):
    """商品点赞模型"""
    __tablename__ = 'good_price_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)  # 用户ID
    goodpriceid = db.Column(db.String(50), nullable=False)  # 商品ID
    liketype = db.Column(db.Integer, default=1)  # 1:点赞 2:点不赞
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'goodpriceid': self.goodpriceid,
            'liketype': self.liketype,
            'createtime': self.createtime.isoformat() if self.createtime else None
        }


class GoodPriceComment(db.Model):
    """商品评论模型"""
    __tablename__ = 'good_price_comments'
    
    commentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goodpriceid = db.Column(db.String(50), nullable=False)  # 商品ID
    uid = db.Column(db.Integer, nullable=False)  # 评论者用户ID
    touid = db.Column(db.Integer)  # 目标用户ID（回复时使用）
    content = db.Column(db.Text, nullable=False)  # 评论内容
    likenum = db.Column(db.Integer, default=0)  # 点赞数
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'commentid': self.commentid,
            'goodpriceid': self.goodpriceid,
            'uid': self.uid,
            'touid': self.touid,
            'content': self.content,
            'likenum': self.likenum,
            'createtime': self.createtime.isoformat() if self.createtime else None
        }


class GoodPriceCommentReply(db.Model):
    """商品评论回复模型"""
    __tablename__ = 'good_price_comment_replies'
    
    replyid = db.Column(db.String(50), primary_key=True)
    commentid = db.Column(db.Integer, nullable=False)  # 评论ID
    goodpriceid = db.Column(db.String(50), nullable=False)  # 商品ID
    uid = db.Column(db.Integer, nullable=False)  # 回复者用户ID
    touid = db.Column(db.Integer)  # 目标用户ID
    content = db.Column(db.Text, nullable=False)  # 回复内容
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'replyid': self.replyid,
            'commentid': self.commentid,
            'goodpriceid': self.goodpriceid,
            'uid': self.uid,
            'touid': self.touid,
            'content': self.content,
            'createtime': self.createtime.isoformat() if self.createtime else None
        }


class GoodPriceCommentLike(db.Model):
    """商品评论点赞模型"""
    __tablename__ = 'good_price_comment_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    commentid = db.Column(db.Integer, nullable=False)  # 评论ID
    uid = db.Column(db.Integer, nullable=False)  # 点赞者用户ID
    likeuid = db.Column(db.Integer, nullable=False)  # 被点赞用户ID
    goodpriceid = db.Column(db.String(50), nullable=False)  # 商品ID
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'commentid': self.commentid,
            'uid': self.uid,
            'likeuid': self.likeuid,
            'goodpriceid': self.goodpriceid,
            'createtime': self.createtime.isoformat() if self.createtime else None
        }


class SkuStock(db.Model):
    """商品规格库存模型"""
    __tablename__ = 'sku_stocks'
    
    skuid = db.Column(db.String(50), primary_key=True)
    goodpriceid = db.Column(db.String(50), nullable=False)  # 商品ID
    skucode = db.Column(db.String(100))  # SKU编码
    price = db.Column(db.Float, nullable=False)  # 价格
    stock = db.Column(db.Integer, default=0)  # 库存
    lockstock = db.Column(db.Integer, default=0)  # 锁定库存
    specs = db.Column(db.Text)  # 规格JSON字符串
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'skuid': self.skuid,
            'goodpriceid': self.goodpriceid,
            'skucode': self.skucode,
            'price': self.price,
            'stock': self.stock,
            'lockstock': self.lockstock,
            'specs': self.specs,
            'createtime': self.createtime.isoformat() if self.createtime else None
        }


class GroupPurchaseOrder(db.Model):
    """团购订单模型"""
    __tablename__ = 'group_purchase_orders'
    
    orderid = db.Column(db.String(50), primary_key=True)
    actid = db.Column(db.String(50), nullable=False)  # 活动ID
    uid = db.Column(db.Integer, nullable=False)  # 购买用户ID
    touid = db.Column(db.Integer)  # 目标用户ID
    goodpriceid = db.Column(db.String(50))  # 商品ID
    amount = db.Column(db.Float, nullable=False)  # 订单金额
    status = db.Column(db.Integer, default=0)  # 0:待支付 1:已支付 2:已退款 3:已确认
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    paytime = db.Column(db.DateTime)  # 支付时间
    
    def to_dict(self):
        return {
            'orderid': self.orderid,
            'actid': self.actid,
            'uid': self.uid,
            'touid': self.touid,
            'goodpriceid': self.goodpriceid,
            'amount': self.amount,
            'status': self.status,
            'createtime': self.createtime.isoformat() if self.createtime else None,
            'paytime': self.paytime.isoformat() if self.paytime else None
        }


class GoodPriceEvaluate(db.Model):
    """商品评价模型"""
    __tablename__ = 'good_price_evaluates'
    
    evaluateid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goodpriceid = db.Column(db.String(50), nullable=False)  # 商品ID
    uid = db.Column(db.Integer, nullable=False)  # 评价者用户ID
    orderid = db.Column(db.String(50))  # 关联订单ID
    content = db.Column(db.Text, nullable=False)  # 评价内容
    images = db.Column(db.Text)  # 评价图片列表
    liketype = db.Column(db.Integer, default=5)  # 评分 1-5星
    likenum = db.Column(db.Integer, default=0)  # 点赞数
    replynum = db.Column(db.Integer, default=0)  # 回复数
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'evaluateid': self.evaluateid,
            'goodpriceid': self.goodpriceid,
            'uid': self.uid,
            'orderid': self.orderid,
            'content': self.content,
            'images': self.images,
            'liketype': self.liketype,
            'likenum': self.likenum,
            'replynum': self.replynum,
            'createtime': self.createtime.isoformat() if self.createtime else None
        }


class GoodPriceEvaluateReply(db.Model):
    """商品评价回复模型"""
    __tablename__ = 'good_price_evaluate_replies'
    
    replyid = db.Column(db.String(50), primary_key=True)
    evaluateid = db.Column(db.Integer, nullable=False)  # 评价ID
    goodpriceid = db.Column(db.String(50), nullable=False)  # 商品ID
    uid = db.Column(db.Integer, nullable=False)  # 回复者用户ID
    touid = db.Column(db.Integer)  # 目标用户ID
    content = db.Column(db.Text, nullable=False)  # 回复内容
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'replyid': self.replyid,
            'evaluateid': self.evaluateid,
            'goodpriceid': self.goodpriceid,
            'uid': self.uid,
            'touid': self.touid,
            'content': self.content,
            'createtime': self.createtime.isoformat() if self.createtime else None
        }


class GoodPriceEvaluateLike(db.Model):
    """商品评价点赞模型"""
    __tablename__ = 'good_price_evaluate_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    evaluateid = db.Column(db.Integer, nullable=False)  # 评价ID
    uid = db.Column(db.Integer, nullable=False)  # 点赞者用户ID
    likeuid = db.Column(db.Integer, nullable=False)  # 被点赞用户ID
    goodpriceid = db.Column(db.String(50), nullable=False)  # 商品ID
    createtime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'evaluateid': self.evaluateid,
            'uid': self.uid,
            'likeuid': self.likeuid,
            'goodpriceid': self.goodpriceid,
            'createtime': self.createtime.isoformat() if self.createtime else None
        }
