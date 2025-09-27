import 'package:flutter_app_badger/flutter_app_badger.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../model/usernotice.dart';
import '../../model/commentreply.dart';
import '../../service/activity.dart';
import '../../service/imservice.dart';
import '../../util/imhelper_util.dart';

import 'event/reply_notice_event.dart';
import 'state/reply_notice_state.dart';
export 'event/reply_notice_event.dart';
export 'state/reply_notice_state.dart';

class ReplyNoticeBloc extends Bloc<ReplyNoticeEvent, ReplyNoticeState> {
  final ImHelper imHelper = ImHelper();
  String error = "";
  String errorstatusCode = "";
  final ImService imService = ImService();
  final ActivityService activityService = ActivityService();

  ReplyNoticeBloc() : super(initState()) {
    on<initStateNoticeAndReply>(_onInitStateNoticeAndReply);
    on<getUserCommentReplyNotice>(_onGetUserCommentReplyNotice);
    on<readed>(_onReaded);
    on<OrderExpiration>(_onOrderExpiration);
    on<getlocalNotice>(_onGetlocalNotice);
    on<getlocalSysNotice>(_onGetlocalSysNotice);
  }

  Future<void> _onInitStateNoticeAndReply(
    initStateNoticeAndReply event,
    Emitter<ReplyNoticeState> emit,
  ) async {
    emit(PostInitial());
  }

  Future<void> _onGetUserCommentReplyNotice(
    getUserCommentReplyNotice event,
    Emitter<ReplyNoticeState> emit,
  ) async {
    //从服务器获取未读回复列表
    emit(ReplyPostLoading());
    UserNotice? userNotice;
    if (event.userNotice != null) {
      userNotice = event.userNotice;
    } else {
      userNotice = await activityService.syncUserNotice(
        event.user.uid,
        event.user.token!,
        errorCallBack,
      );
    }
    if (userNotice != null) {
      await activityService.saveLocalStore(
        userNotice,
        event.user.token!,
        event.user.uid,
        errorCallBack,
      );
    }

    int count = await imHelper.getCommentReplysCount(); //新的留言,评论与回复
    int getLikeCount = await imHelper.getNewFollowCount(); //新的关注
    int mynoticecount = 0;
    int activityEvaluteCount = await imHelper.getActivityEvaluateCount(
      0,
    ); //有新的待评价活动不加入提醒，在用户主动点击我的页面后显示
    int newsharedCount = await imHelper.getUserSharedCount(); //有新的分享
    int neworderPending = await imHelper.getUserOrder(0); //获取待支付订单
    int neworderFinish = await imHelper.getUserOrder(1); //获取待确认订单
    int newlithumbupCount = await imHelper.getLikeNoticeCount(); //未读的点赞

    //不要把待评价活动加入到桌面图标中
    int sumcount =
        count +
        getLikeCount +
        newsharedCount +
        neworderPending +
        neworderFinish +
        newlithumbupCount +
        activityEvaluteCount;
    if (sumcount >= 0) {
      setAppUnReadCount(sumcount);
    }
    if (count >= 0 || getLikeCount >= 0) {
      emit(
        newReplyCount(
          count: count + getLikeCount + newlithumbupCount,
          followcount: getLikeCount,
        ),
      );
    }

    mynoticecount =
        activityEvaluteCount +
        newsharedCount +
        neworderPending +
        neworderFinish;

    int myordercount = neworderPending + neworderFinish;

    if (mynoticecount >= 0) {
      emit(myNoticeCount(count: mynoticecount));
    }

    if (newsharedCount >= 0) {
      emit(newSharedCount(count: newsharedCount));
    }

    if (myordercount >= 0) {
      emit(newOrderCount(count: myordercount));
    }
    //      if(activityEvaluteCount >= 0){
    //        emit(newUnActivityEvaluteCount(count: activityEvaluteCount));
    //      }
    return;
  }

  Future<void> _onReaded(readed event, Emitter<ReplyNoticeState> emit) async {
    //评论和评论回复是在同一个页面展示，进入后一起被标记为已读
    if (event.replyMsgType.toString() == ReplyMsgType.commentmsg.toString()) {
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.commentmsg);
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.replymsg);
    }

    if (event.replyMsgType.toString() ==
        ReplyMsgType.bugcommentmsg.toString()) {
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.bugcommentmsg);
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.bugreplymsg);
    }

    if (event.replyMsgType.toString() ==
        ReplyMsgType.suggestcommentmsg.toString()) {
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.suggestcommentmsg);
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.suggestreplymsg);
    }

    if (event.replyMsgType.toString() == ReplyMsgType.evaluatemsg.toString()) {
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.evaluatemsg);
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.evaluatereplymsg);
    }

    if (event.replyMsgType.toString() ==
        ReplyMsgType.goodpricecommentmsg.toString()) {
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.goodpricecommentmsg);
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.goodpricereplymsg);
    }

    if (event.replyMsgType.toString() == ReplyMsgType.replymsg.toString()) {
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.replymsg);
    }

    if (event.replyMsgType.toString() == ReplyMsgType.sysnotice.toString()) {
      imHelper.updateReplyCommentNoticeRead(ReplyMsgType.sysnotice);
    }

    if (event.replyMsgType.toString() == ReplyMsgType.newmember.toString()) {
      imHelper.updateNewMemberNoticeRead();
    }

    if (event.replyMsgType.toString() == ReplyMsgType.newfollowed.toString()) {
      imHelper.updateFollowedNoticeRead();
    }

    if (event.replyMsgType.toString() == ReplyMsgType.newfriend.toString()) {
      imHelper.updateNewFriendNoticeRead();
    }

    if (event.replyMsgType.toString() == ReplyMsgType.sharedReaded.toString()) {
      imHelper.updateUserSharedRead();
    }

    if (event.replyMsgType.toString() == ReplyMsgType.newliked.toString()) {
      imHelper.updateUserLikeRead();
    }

    int count = await imHelper.getCommentReplysCount();
    // int newmembercount = await imHelper.getCommunityMemberCount();
    int getLikeCount = await imHelper.getNewFollowCount();
    // int newfriendCount = await imHelper.getFriendCount();//有新的朋友
    int activityEvaluteCount = await imHelper
        .getUserUnEvaluateOrder(); //有新的待评价活动不加入提醒，在用户主动点击我的页面后显示
    int newsharedCount = await imHelper.getUserSharedCount(); //有新的分享
    int newlithumbupCount = await imHelper.getLikeNoticeCount(); //未读的点赞

    int sumcount = count + getLikeCount + newsharedCount;
    if (sumcount >= 0) {
      setAppUnReadCount(count + getLikeCount + newsharedCount);
    }
    int mynoticecount = 0;

    mynoticecount = activityEvaluteCount + newsharedCount;

    if (mynoticecount >= 0) {
      emit(myNoticeCount(count: mynoticecount));
    }

    if (count >= 0 || getLikeCount >= 0) {
      emit(
        newReplyCount(
          count: count + getLikeCount + newlithumbupCount,
          followcount: getLikeCount,
          newlithumbupCount: newlithumbupCount,
        ),
      );
      return;
    }

    if (sumcount >= 0) {
      emit(newSharedCount(count: newsharedCount));
    }
  }

  Future<void> _onOrderExpiration(
    OrderExpiration event,
    Emitter<ReplyNoticeState> emit,
  ) async {
    activityService.syncOrderExpirationFun(
      event.user.uid,
      event.user.token!,
      errorCallBack,
    );
  }

  Future<void> _onGetlocalNotice(
    getlocalNotice event,
    Emitter<ReplyNoticeState> emit,
  ) async {
    // Implement if needed
  }

  Future<void> _onGetlocalSysNotice(
    getlocalSysNotice event,
    Emitter<ReplyNoticeState> emit,
  ) async {
    // Implement if needed
  }

  void setAppUnReadCount(int count) {
    int unReadCount = 0;
    // Global.replyCount = count;
    // unReadCount = Global.immsgCount + Global.replyCount;
    if (unReadCount > 0) {
      FlutterAppBadger.updateBadgeCount(unReadCount > 99 ? 99 : unReadCount);
    } else {
      FlutterAppBadger.removeBadge();
    }
  }

  void errorCallBack(String statusCode, String msg) {
    error = msg;
    errorstatusCode = statusCode;
  }
}
