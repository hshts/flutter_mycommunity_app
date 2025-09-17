import '../../../model/user.dart';
import '../../../model/usernotice.dart';

abstract class ImEvent {
  final User user;
  const ImEvent(this.user);

  List<Object> get props => [user];
}

//用户关系每次获取都要更新，客户端先删除再保存，消息只插入不删除
class UserRelationAndMessage extends ImEvent {
  final UserNotice? userNotice;
  UserRelationAndMessage(super.user, {this.userNotice});
}

class UserCommentReplyNotice extends ImEvent {
  UserCommentReplyNotice(super.user);
}

//如果是收到新消息需要等待返回
class NewMessage extends ImEvent {
  final String content;
  NewMessage(super.user, this.content);
}

//撤销
class ReCallMessage extends ImEvent {
  final String content;
  ReCallMessage(super.user, this.content);
}

class NewCommunityMessage extends ImEvent {
  final String content;
  NewCommunityMessage(super.user, this.content);
}

class NEWFRIEND extends ImEvent {
  NEWFRIEND(super.user);
}

class NewUserMessage extends ImEvent {
  final String content;

  NewUserMessage(super.user, this.content);
}

class getlocalRelation extends ImEvent {
  getlocalRelation(super.user);
}

//已读
class Already extends ImEvent {
  final String timeline_id;

  Already(super.user, this.timeline_id);
}

//置顶
class RelationTop extends ImEvent {
  final String timeline_id;

  RelationTop(super.user, this.timeline_id);
}

//取消置顶
class RelationTopCancel extends ImEvent {
  final String timeline_id;

  RelationTopCancel(super.user, this.timeline_id);
}

//删除
class RelationDel extends ImEvent {
  final String timeline_id;

  RelationDel(super.user, this.timeline_id);
}

//获取用户评论,回复，系统通知
class getUserCommentReplyNotice extends ImEvent {
  int id;
  UserNotice? userNotice;
  getUserCommentReplyNotice(super.user, this.id, {this.userNotice});
}
