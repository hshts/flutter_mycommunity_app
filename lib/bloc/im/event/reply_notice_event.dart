import 'package:equatable/equatable.dart';

import '../../../model/usernotice.dart';
import '../../../model/user.dart';
import '../../../model/commentreply.dart';

abstract class ReplyNoticeEvent extends Equatable {
  final User user;
  const ReplyNoticeEvent(this.user);

  @override
  List<Object> get props => [user];
}

//获取用户评论,回复，系统通知
// ignore: must_be_immutable
class getUserCommentReplyNotice extends ReplyNoticeEvent {
  int id;
  UserNotice? userNotice;
  getUserCommentReplyNotice(super.user, this.id, {this.userNotice});
}

class OrderExpiration extends ReplyNoticeEvent {
  const OrderExpiration(super.user);
}

//获取本地用户回复列表
class getlocalNotice extends ReplyNoticeEvent {
  const getlocalNotice(super.user);
}

//获取本地系统通知列表
class getlocalSysNotice extends ReplyNoticeEvent {
  const getlocalSysNotice(super.user);
}

//初始化状态
class initStateNoticeAndReply extends ReplyNoticeEvent {
  const initStateNoticeAndReply(super.user);
}

class readed extends ReplyNoticeEvent {
  final ReplyMsgType? replyMsgType;
  const readed(super.user, {this.replyMsgType});
}
