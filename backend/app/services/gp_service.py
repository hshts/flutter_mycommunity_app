from flask import request
from app import db
from app.models import GoodPrice, Comment, Activity, User, Collection, Like
from app.utils.response import success_response, error_response, paginated_response
from sqlalchemy import and_, or_, desc, asc
from datetime import datetime
import json

class GPService:
    """团购服务业务逻辑"""
    
    @staticmethod
    def get_hot_search_product():
        """获取热门搜索关键词"""
        # 这里应该根据实际搜索频率统计，暂时返回模拟数据
        hot_searches = [
            {"keyword": "手机", "count": 1000},
            {"keyword": "电脑", "count": 800},
            {"keyword": "家电", "count": 600},
            {"keyword": "服装", "count": 500},
            {"keyword": "食品", "count": 400}
        ]
        return hot_searches
    
    @staticmethod
    def get_recommend_search_product(content):
        """获取推荐搜索关键词"""
        # 模糊匹配商品标题
        good_prices = GoodPrice.query.filter(
            GoodPrice.title.like(f'%{content}%'),
            GoodPrice.status == 1
        ).limit(10).all()
        
        results = []
        for gp in good_prices:
            results.append({
                "keyword": gp.title,
                "count": gp.view_count
            })
        return results
    
    @staticmethod
    def update_good_price_collection(good_price_id, user_id):
        """收藏好价商品"""
        try:
            # 检查是否已经收藏
            existing = Collection.query.filter_by(
                user_id=user_id,
                good_price_id=good_price_id
            ).first()
            
            if existing:
                return False, "已经收藏过了"
            
            # 创建收藏记录
            collection = Collection(
                user_id=user_id,
                good_price_id=good_price_id
            )
            db.session.add(collection)
            
            # 更新商品收藏数
            good_price = GoodPrice.query.get(good_price_id)
            if good_price:
                good_price.collect_count += 1
            
            db.session.commit()
            return True, "收藏成功"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def del_good_price_collection(good_price_id, user_id):
        """取消收藏好价商品"""
        try:
            collection = Collection.query.filter_by(
                user_id=user_id,
                good_price_id=good_price_id
            ).first()
            
            if not collection:
                return False, "未找到收藏记录"
            
            db.session.delete(collection)
            
            # 更新商品收藏数
            good_price = GoodPrice.query.get(good_price_id)
            if good_price and good_price.collect_count > 0:
                good_price.collect_count -= 1
            
            db.session.commit()
            return True, "取消收藏成功"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_user_good_price_collection_info(user_id, current_index=0, per_page=20):
        """获取用户收藏的好价商品"""
        try:
            # 分页查询用户收藏
            query = db.session.query(GoodPrice, Collection).join(
                Collection, GoodPrice.id == Collection.good_price_id
            ).filter(
                Collection.user_id == user_id,
                GoodPrice.status == 1
            ).order_by(desc(Collection.created_at))
            
            # 分页
            offset = current_index * per_page
            total = query.count()
            items = query.offset(offset).limit(per_page).all()
            
            # 转换数据格式
            good_prices = []
            for good_price, collection in items:
                gp_dict = good_price.to_dict()
                gp_dict['collectTime'] = collection.created_at.isoformat()
                good_prices.append(gp_dict)
            
            return good_prices, total
        except Exception as e:
            return [], 0
    
    @staticmethod
    def update_comment(good_price_id, user_id, to_user_id, content, parent_id=None):
        """添加评论或回复"""
        try:
            # 获取用户信息
            user = User.query.get(user_id)
            if not user:
                return 0, "用户不存在"
            
            # 创建评论
            comment = Comment(
                content=content,
                good_price_id=good_price_id,
                user_id=user_id,
                user_name=user.nickname or user.username,
                user_avatar=user.avatar,
                parent_id=parent_id,
                reply_to_user_id=to_user_id if parent_id else None
            )
            
            # 如果是回复，获取被回复用户信息
            if to_user_id and parent_id:
                to_user = User.query.get(to_user_id)
                if to_user:
                    comment.reply_to_user_name = to_user.nickname or to_user.username
            
            db.session.add(comment)
            
            # 更新商品评论数
            good_price = GoodPrice.query.get(good_price_id)
            if good_price:
                good_price.comment_count += 1
            
            # 如果是回复，更新父评论的回复数
            if parent_id:
                parent_comment = Comment.query.get(parent_id)
                if parent_comment:
                    parent_comment.reply_count += 1
            
            db.session.commit()
            return comment.id, "评论成功"
        except Exception as e:
            db.session.rollback()
            return 0, str(e)
    
    @staticmethod
    def update_comment_like(comment_id, user_id, good_price_id):
        """点赞评论"""
        try:
            # 检查是否已经点赞
            existing = Like.query.filter_by(
                user_id=user_id,
                target_id=comment_id,
                target_type=2  # 2表示评论
            ).first()
            
            if existing:
                return False, "已经点赞过了"
            
            # 创建点赞记录
            like = Like(
                user_id=user_id,
                target_id=comment_id,
                target_type=2
            )
            db.session.add(like)
            
            # 更新评论点赞数
            comment = Comment.query.get(comment_id)
            if comment:
                comment.like_count += 1
            
            db.session.commit()
            return True, "点赞成功"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def del_comment_like(comment_id, user_id):
        """取消点赞评论"""
        try:
            like = Like.query.filter_by(
                user_id=user_id,
                target_id=comment_id,
                target_type=2
            ).first()
            
            if not like:
                return False, "未找到点赞记录"
            
            db.session.delete(like)
            
            # 更新评论点赞数
            comment = Comment.query.get(comment_id)
            if comment and comment.like_count > 0:
                comment.like_count -= 1
            
            db.session.commit()
            return True, "取消点赞成功"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_comment_list(good_price_id, user_id):
        """获取评论列表"""
        try:
            # 查询顶级评论
            comments = Comment.query.filter_by(
                good_price_id=good_price_id,
                parent_id=None,
                status=1
            ).order_by(desc(Comment.created_at)).all()
            
            result = []
            for comment in comments:
                comment_dict = comment.to_dict()
                
                # 检查当前用户是否点赞了这条评论
                user_like = Like.query.filter_by(
                    user_id=user_id,
                    target_id=comment.id,
                    target_type=2
                ).first()
                comment_dict['isLiked'] = bool(user_like)
                
                # 查询回复
                replies = Comment.query.filter_by(
                    parent_id=comment.id,
                    status=1
                ).order_by(asc(Comment.created_at)).all()
                
                comment_dict['replies'] = []
                for reply in replies:
                    reply_dict = reply.to_dict()
                    reply_user_like = Like.query.filter_by(
                        user_id=user_id,
                        target_id=reply.id,
                        target_type=2
                    ).first()
                    reply_dict['isLiked'] = bool(reply_user_like)
                    comment_dict['replies'].append(reply_dict)
                
                result.append(comment_dict)
            
            return result
        except Exception as e:
            return []
    
    @staticmethod
    def del_comment(comment_id, user_id, good_price_id, is_reply=False):
        """删除评论或回复"""
        try:
            comment = Comment.query.filter_by(
                id=comment_id,
                user_id=user_id
            ).first()
            
            if not comment:
                return False, "评论不存在或无权限删除"
            
            # 软删除
            comment.status = 0
            
            # 更新统计数据
            if not is_reply:
                # 删除主评论，减少商品评论数
                good_price = GoodPrice.query.get(good_price_id)
                if good_price and good_price.comment_count > 0:
                    good_price.comment_count -= 1
            else:
                # 删除回复，减少父评论回复数
                if comment.parent_id:
                    parent_comment = Comment.query.get(comment.parent_id)
                    if parent_comment and parent_comment.reply_count > 0:
                        parent_comment.reply_count -= 1
            
            db.session.commit()
            return True, "删除成功"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def update_good_price_like(good_price_id, user_id):
        """好价点赞"""
        try:
            # 检查是否已经点赞
            existing = Like.query.filter_by(
                user_id=user_id,
                target_id=good_price_id,
                target_type=1  # 1表示商品
            ).first()
            
            if existing:
                return False, "已经点赞过了"
            
            # 创建点赞记录
            like = Like(
                user_id=user_id,
                target_id=good_price_id,
                target_type=1
            )
            db.session.add(like)
            
            # 更新商品点赞数
            good_price = GoodPrice.query.get(good_price_id)
            if good_price:
                good_price.like_count += 1
            
            db.session.commit()
            return True, "点赞成功"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def del_good_price_like(good_price_id, user_id):
        """取消好价点赞"""
        try:
            like = Like.query.filter_by(
                user_id=user_id,
                target_id=good_price_id,
                target_type=1
            ).first()
            
            if not like:
                return False, "未找到点赞记录"
            
            db.session.delete(like)
            
            # 更新商品点赞数
            good_price = GoodPrice.query.get(good_price_id)
            if good_price and good_price.like_count > 0:
                good_price.like_count -= 1
            
            db.session.commit()
            return True, "取消点赞成功"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def search_product(content, order_type="time", city_code="", current_index=0, is_all_city=True, per_page=20):
        """搜索商品"""
        try:
            query = GoodPrice.query.filter(GoodPrice.status == 1)
            
            # 关键词搜索
            if content:
                query = query.filter(
                    or_(
                        GoodPrice.title.like(f'%{content}%'),
                        GoodPrice.desc.like(f'%{content}%'),
                        GoodPrice.category.like(f'%{content}%')
                    )
                )
            
            # 地区筛选
            if not is_all_city and city_code:
                query = query.filter(GoodPrice.location.like(f'%{city_code}%'))
            
            # 排序
            if order_type == "price_asc":
                query = query.order_by(asc(GoodPrice.price))
            elif order_type == "price_desc":
                query = query.order_by(desc(GoodPrice.price))
            elif order_type == "hot":
                query = query.order_by(desc(GoodPrice.like_count))
            else:  # time
                query = query.order_by(desc(GoodPrice.created_at))
            
            # 分页
            offset = current_index * per_page
            total = query.count()
            items = query.offset(offset).limit(per_page).all()
            
            return [item.to_dict() for item in items], total
        except Exception as e:
            return [], 0
    
    @staticmethod
    def get_good_price_info(good_price_id):
        """获取商品详情"""
        try:
            good_price = GoodPrice.query.filter_by(
                id=good_price_id,
                status=1
            ).first()
            
            if not good_price:
                return None
            
            # 增加浏览次数
            good_price.view_count += 1
            db.session.commit()
            
            return good_price.to_dict()
        except Exception as e:
            return None
    
    @staticmethod
    def get_recommend_good_price_list(type_id=1, current_index=0, city_code="", per_page=20):
        """获取推荐商品列表"""
        try:
            query = GoodPrice.query.filter(GoodPrice.status == 1)
            
            # 根据类型筛选
            if type_id == 1:  # 最新
                query = query.order_by(desc(GoodPrice.created_at))
            elif type_id == 2:  # 热门
                query = query.filter(GoodPrice.is_hot == True).order_by(desc(GoodPrice.like_count))
            elif type_id == 3:  # 推荐
                query = query.filter(GoodPrice.is_recommend == True).order_by(desc(GoodPrice.created_at))
            
            # 地区筛选
            if city_code:
                query = query.filter(GoodPrice.location.like(f'%{city_code}%'))
            
            # 分页
            offset = current_index * per_page
            total = query.count()
            items = query.offset(offset).limit(per_page).all()
            
            return [item.to_dict() for item in items], total
        except Exception as e:
            return [], 0
    
    @staticmethod
    def create_good_price(user_id, **kwargs):
        """创建好价商品"""
        try:
            # 获取用户信息
            user = User.query.get(user_id)
            if not user:
                return "", "用户不存在"
            
            # 创建商品
            good_price = GoodPrice(
                title=kwargs.get('title'),
                desc=kwargs.get('content'),
                price=kwargs.get('price'),
                original_price=kwargs.get('original_price'),
                image_url=kwargs.get('pic'),
                platform=kwargs.get('purchase_channels'),
                platform_url=kwargs.get('product_url'),
                category=kwargs.get('category'),
                user_id=user_id,
                user_name=user.nickname or user.username,
                user_avatar=user.avatar,
                location=f"{kwargs.get('province')},{kwargs.get('city')}"
            )
            
            db.session.add(good_price)
            db.session.commit()
            
            return str(good_price.id), "创建成功"
        except Exception as e:
            db.session.rollback()
            return "", str(e)
    
    @staticmethod
    def get_my_good_price_pending_list(user_id):
        """获取我的待审核商品"""
        try:
            good_prices = GoodPrice.query.filter_by(
                user_id=user_id,
                status=0  # 0表示待审核
            ).order_by(desc(GoodPrice.created_at)).all()
            
            return [gp.to_dict() for gp in good_prices]
        except Exception as e:
            return []
    
    @staticmethod
    def get_my_good_price_finish_list(user_id):
        """获取我的已审核商品"""
        try:
            good_prices = GoodPrice.query.filter_by(
                user_id=user_id,
                status=1  # 1表示已审核通过
            ).order_by(desc(GoodPrice.created_at)).all()
            
            return [gp.to_dict() for gp in good_prices]
        except Exception as e:
            return []
    
    @staticmethod
    def del_my_good_price(good_price_id, user_id):
        """删除我的商品"""
        try:
            good_price = GoodPrice.query.filter_by(
                id=good_price_id,
                user_id=user_id
            ).first()
            
            if not good_price:
                return False, "商品不存在或无权限删除"
            
            # 软删除
            good_price.status = -1
            db.session.commit()
            
            return True, "删除成功"
        except Exception as e:
            db.session.rollback()
            return False, str(e)