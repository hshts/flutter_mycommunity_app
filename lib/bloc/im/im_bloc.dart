import 'package:flutter_app_badger/flutter_app_badger.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'dart:convert' as JSON;

import '../../service/activity.dart';
import '../../service/imservice.dart';
import '../../util/imhelper_util.dart';
import '../../model/im/grouprelation.dart';
import '../../model/im/timelinesync.dart';
import '../../model/im/sysmessage.dart';
import '../../model/usernotice.dart';

import '../../global.dart';
import 'event/im_event.dart';
import 'state/im_state.dart';
export 'event/im_event.dart';
export 'state/im_state.dart';

class ImBloc extends Bloc<ImEvent, ImState> {
  final ImHelper imHelper = ImHelper();
  String error = "";
  String errorstatusCode = "";
  List<TimeLineSync>? timeLineSyncs;

  final ImService imService = ImService();
  final ActivityService activityService = ActivityService();

  ImBloc() : super(initImState()) {
    on<UserRelationAndMessage>(_onUserRelationAndMessage);
    on<UserCommentReplyNotice>(_onUserCommentReplyNotice);
    on<NewMessage>(_onNewMessage);
    on<NewCommunityMessage>(_onNewCommunityMessage);
    on<NewUserMessage>(_onNewUserMessage);
    on<ReCallMessage>(_onReCallMessage);
    on<getlocalRelation>(_onGetlocalRelation);
    on<Already>(_onAlready);
    on<RelationTop>(_onRelationTop);
    on<RelationTopCancel>(_onRelationTopCancel);
    on<RelationDel>(_onRelationDel);
  }

  Future<void> _onUserRelationAndMessage(
    UserRelationAndMessage event,
    Emitter<ImState> emit,
  ) async {
    try {
      List<GroupRelation>? grouprelationlist = [];
      if (event.userNotice != null) {
        //聊天通知
        if (event.userNotice!.unread_gpmsg > 0) {
          //群聊关系同步本地储存，消息数据异步写入
          //用户登录成功后执行 活动群，自建群聊，私人聊天的同步
          grouprelationlist = await imService.syncActivityRelation(
            event.user.uid,
            event.user.token!,
            errorCallBack,
          );
          if (grouprelationlist != null && grouprelationlist.isNotEmpty) {
            await imService.saveLocalStore(
              grouprelationlist,
              event.user.token!,
              event.user.uid,
              errorCallBack,
            );
          }
        }
        if (event.userNotice!.unread_communitymsg > 0) {
          grouprelationlist = await imService.syncCommunityRelation(
            event.user.uid,
            event.user.token!,
            errorCallBack,
          );
          if (grouprelationlist != null && grouprelationlist.isNotEmpty) {
            await imService.saveLocalStore(
              grouprelationlist,
              event.user.token!,
              event.user.uid,
              errorCallBack,
            );
          }
        }
        if (event.userNotice!.unread_singlemsg > 0) {
          grouprelationlist = await imService.syncSingleRelation(
            event.user.uid,
            event.user.token!,
            errorCallBack,
          );
          if (grouprelationlist != null && grouprelationlist.isNotEmpty) {
            await imService.saveLocalStore(
              grouprelationlist,
              event.user.token!,
              event.user.uid,
              errorCallBack,
            );
          }
        }
        //活动通知
        await activityService.saveLocalStore(
          event.userNotice!,
          event.user.token!,
          event.user.uid,
          errorCallBack,
        );
      }
      //获取本地
      NewMessageState newMessageState = await setAppUnReadCount(event.user.uid);

      //消息通知接收的消息是最新的一条，导航到消息页面后旧的消息可能还没有下载完成。Global.profile.timeline_id是最新的聊天

      if (Global.timeline_id != "") {
        List<TimeLineSync> timeLineSyncs = [];
        timeLineSyncs = await imHelper.getTimeLineSync(
          Global.profile.user!.uid,
          0,
          30,
          Global.timeline_id,
        );
        Global.timeline_id = "";

        emit(
          NewMessageState(
            sysMessage: newMessageState.sysMessage,
            groupRelations: newMessageState.groupRelations,
            msgMessage: timeLineSyncs,
          ),
        );
      } else {
        emit(
          NewMessageState(
            sysMessage: newMessageState.sysMessage,
            groupRelations: newMessageState.groupRelations,
            msgMessage: [],
          ),
        );
      }
    } catch (_) {}
  }

  Future<void> _onUserCommentReplyNotice(
    UserCommentReplyNotice event,
    Emitter<ImState> emit,
  ) async {
    try {
      UserNotice? userNotice = await activityService.syncUserNotice(
        event.user.uid,
        event.user.token!,
        errorCallBack,
      );
      if (userNotice != null) {
        await activityService.saveLocalStore(
          userNotice,
          event.user.token!,
          event.user.uid,
          errorCallBack,
        );
      }
    } catch (_) {}
  }

  Future<void> _onNewMessage(NewMessage event, Emitter<ImState> emit) async {
    try {
      //活动群聊同步
      List<GroupRelation> grouprelationlist = [];
      List<TimeLineSync> timeLineSyncs = [];
      // grouprelationlist = await imService.syncActivityRelation(event.user.uid, event.user.token, errorCallBack);
      //群聊关系同步本地储存，消息数据异步写入
      String message = event.content;
      if (message.isNotEmpty) {
        if (Global.isInDebugMode) print(message);
        Map<String, dynamic> data =
            (JSON.jsonDecode(message)) as Map<String, dynamic>;

        GroupRelation groupRelation = GroupRelation.fromJson(
          data["groupRelation"] as Map<String, dynamic>,
        );
        grouprelationlist.add(groupRelation);
        if (await imHelper.saveGroupRelation(grouprelationlist) > 0) {
          TimeLineSync timeLineSync = TimeLineSync.fromMapByServer(data);
          await imService.saveTimeLineSync(
            timeLineSync,
            event.user.token,
            event.user.uid,
            errorCallBack,
          );
        }
        timeLineSyncs = await imHelper.getTimeLineSync(
          Global.profile.user!.uid,
          0,
          timeLineSyncs.length + 30,
          groupRelation.timeline_id,
        );
      }
      //用户本地替换服务器数据
      NewMessageState newMessageState = await setAppUnReadCount(event.user.uid);
      emit(
        NewMessageState(
          sysMessage: newMessageState.sysMessage,
          groupRelations: newMessageState.groupRelations,
          msgMessage: timeLineSyncs,
        ),
      );
    } catch (_) {}
  }

  Future<void> _onNewCommunityMessage(
    NewCommunityMessage event,
    Emitter<ImState> emit,
  ) async {
    try {
      List<GroupRelation> grouprelationlist = [];
      List<TimeLineSync> timeLineSyncs = [];

      String message = event.content;
      if (message.isNotEmpty) {
        Map<String, dynamic> data =
            (JSON.jsonDecode(message)) as Map<String, dynamic>;
        GroupRelation groupRelation = GroupRelation.fromJson(
          data["groupRelation"] as Map<String, dynamic>,
        );
        grouprelationlist.add(groupRelation);
        if (await imHelper.saveGroupRelation(grouprelationlist) > 0) {
          TimeLineSync timeLineSync = TimeLineSync.fromMapByServer(data);
          await imService.saveCommunityTimeLineSync(
            timeLineSync,
            event.user.token,
            event.user.uid,
            errorCallBack,
          );
        }
        timeLineSyncs = await imHelper.getTimeLineSync(
          Global.profile.user!.uid,
          0,
          timeLineSyncs.length + 30,
          groupRelation.timeline_id,
        );
      }
      //用户本地替换服务器数据
      NewMessageState newMessageState = await setAppUnReadCount(event.user.uid);
      emit(
        NewMessageState(
          sysMessage: newMessageState.sysMessage,
          groupRelations: newMessageState.groupRelations,
          msgMessage: timeLineSyncs,
        ),
      );
    } catch (_) {}
  }

  Future<void> _onNewUserMessage(
    NewUserMessage event,
    Emitter<ImState> emit,
  ) async {
    try {
      //有新的私聊
      List<TimeLineSync> timeLineSyncs = [];
      List<GroupRelation> grouprelationlist = [];
      String message = event.content;
      if (message.isNotEmpty) {
        Map<String, dynamic> data =
            (JSON.jsonDecode(message)) as Map<String, dynamic>;
        if (Global.isInDebugMode) print(data);
        GroupRelation groupRelation = GroupRelation.fromJson(
          data["groupRelation"] as Map<String, dynamic>,
        );
        grouprelationlist.add(groupRelation);
        if (await imHelper.saveGroupRelation(grouprelationlist) > 0) {
          TimeLineSync timeLineSync = TimeLineSync.fromMapByServer(data);
          await imService.saveSingleTimeLineSync(
            timeLineSync,
            event.user.token,
            event.user.uid,
            errorCallBack,
          );
        }
        timeLineSyncs = await imHelper.getTimeLineSync(
          Global.profile.user!.uid,
          0,
          timeLineSyncs.length + 30,
          groupRelation.timeline_id,
        );
      }
      //群聊关系同步本地储存，消息数据异步写入
      //私人群聊同步
      //用户本地替换服务器数据
      NewMessageState newMessageState = await setAppUnReadCount(event.user.uid);
      emit(
        NewMessageState(
          sysMessage: newMessageState.sysMessage,
          groupRelations: newMessageState.groupRelations,
          msgMessage: timeLineSyncs,
        ),
      );
    } catch (_) {}
  }

  Future<void> _onReCallMessage(
    ReCallMessage event,
    Emitter<ImState> emit,
  ) async {
    try {
      //撤回消息,接收方
      List<TimeLineSync> timeLineSyncs = [];
      //撤回消息根据source_id, 需要改两个地方，一个是relation_table 一个是synctable
      String timelineId = event.content.split("^※^")[0];
      String sourceId = event.content.split("^※^")[1];
      String reCallContent = event.content.split("^※^")[2];

      ///撤回数据
      await imHelper.recallMessageToUid(sourceId, reCallContent);
      await imHelper.recallGroupRelation(sourceId, reCallContent);
      //用户本地替换服务器数据
      NewMessageState newMessageState = await setAppUnReadCount(event.user.uid);
      timeLineSyncs = await imHelper.getTimeLineSync(
        Global.profile.user!.uid,
        0,
        timeLineSyncs.length + 30,
        timelineId,
      );
      emit(
        NewMessageState(
          sysMessage: newMessageState.sysMessage,
          groupRelations: newMessageState.groupRelations,
          msgMessage: timeLineSyncs,
        ),
      );
    } catch (_) {}
  }

  Future<void> _onGetlocalRelation(
    getlocalRelation event,
    Emitter<ImState> emit,
  ) async {
    try {
      NewMessageState newMessageState = await setAppUnReadCount(event.user.uid);
      emit(
        NewMessageState(
          sysMessage: newMessageState.sysMessage,
          groupRelations: newMessageState.groupRelations,
          msgMessage: [],
        ),
      );
    } catch (_) {}
  }

  Future<void> _onAlready(Already event, Emitter<ImState> emit) async {
    try {
      //将未读消息状态改成已读
      await imHelper.updateAlready(event.timeline_id);
    } catch (_) {}
  }

  Future<void> _onRelationTop(RelationTop event, Emitter<ImState> emit) async {
    try {
      //将群聊置顶
      if (await imHelper.updateTop(event.timeline_id, event.user.uid) > 0) {
        NewMessageState newMessageState = await setAppUnReadCount(
          event.user.uid,
        );
        emit(
          NewMessageState(
            sysMessage: newMessageState.sysMessage,
            groupRelations: newMessageState.groupRelations,
            msgMessage: [],
          ),
        );
      }
    } catch (_) {}
  }

  Future<void> _onRelationTopCancel(
    RelationTopCancel event,
    Emitter<ImState> emit,
  ) async {
    try {
      //取消置顶
      if (await imHelper.updateTopCancel(event.timeline_id, event.user.uid) >
          0) {
        NewMessageState newMessageState = await setAppUnReadCount(
          event.user.uid,
        );
        emit(
          NewMessageState(
            sysMessage: newMessageState.sysMessage,
            groupRelations: newMessageState.groupRelations,
            msgMessage: [],
          ),
        );
      }
    } catch (_) {}
  }

  Future<void> _onRelationDel(RelationDel event, Emitter<ImState> emit) async {
    try {
      //删除群聊关系
      if (await imHelper.delGroupRelation(event.timeline_id, event.user.uid) >
          0) {
        imHelper.delTimeLineSync(event.user.uid, event.timeline_id);
        NewMessageState newMessageState = await setAppUnReadCount(
          event.user.uid,
        );
        emit(
          NewMessageState(
            sysMessage: newMessageState.sysMessage,
            groupRelations: newMessageState.groupRelations,
            msgMessage: [],
          ),
        );
      }
    } catch (_) {}
  }

  Future<NewMessageState> setAppUnReadCount(int uid) async {
    int unAllReadCount = 0; //所有未读消息 待付款 待评价
    NewMessageState newMessageState = await getAllMessage(uid);

    unAllReadCount =
        newMessageState.sysMessage.newImMode +
        newMessageState.sysMessage.neworderpending_count +
        newMessageState.sysMessage.neworderfinish_count +
        newMessageState.sysMessage.activityevalute_count;

    if (unAllReadCount > 0) {
      FlutterAppBadger.updateBadgeCount(
        unAllReadCount > 99 ? 99 : unAllReadCount,
      );
    } else {
      FlutterAppBadger.removeBadge();
    }

    return newMessageState;
  }

  Future<NewMessageState> getAllMessage(int uid) async {
    int unImReadCount = 0;
    List<GroupRelation> grouprelationlist = await imHelper.getGroupRelation(
      uid.toString(),
    );
    //IM为读
    if (grouprelationlist.isNotEmpty) {
      for (GroupRelation groupRelation in grouprelationlist) {
        unImReadCount += groupRelation.unreadcount;
      }
    }
    int commentreplyCount = await imHelper.getCommentReplysCount(); //新的留言,评论与回复
    int followCount = await imHelper.getNewFollowCount(); //新的关注
    int activityevaluteCount = await imHelper
        .getUserUnEvaluateOrder(); //有新的待评价活动不加入提醒，在用户主动点击我的页面后显示
    int neworderpendingCount = await imHelper.getUserOrder(0); //获取待支付订单
    int neworderfinishCount = await imHelper.getUserOrder(1); //获取待确认订单
    int newlithumbupCount = await imHelper.getLikeNoticeCount(); //未读的点赞

    SysMessage sysMessage = SysMessage(
      commentreplyCount,
      followCount,
      activityevaluteCount,
      neworderpendingCount,
      neworderfinishCount,
      newlithumbupCount,
      unImReadCount + commentreplyCount + followCount + newlithumbupCount,
      activityevaluteCount + neworderpendingCount + neworderfinishCount,
    );

    return NewMessageState(
      groupRelations: grouprelationlist,
      sysMessage: sysMessage,
      msgMessage: [],
    );
  }

  void errorCallBack(String statusCode, String msg) {
    error = msg;
    errorstatusCode = statusCode;
  }
}
