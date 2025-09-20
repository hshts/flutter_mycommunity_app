// ignore_for_file: non_constant_identifier_names

import 'package:json_annotation/json_annotation.dart';

import '../../global.dart';
import '../user.dart';

part 'timelinesync.g.dart';

enum ContentType {
  Type_Text,
  Type_System,
  Type_Image,
  Type_Sound,
  Type_Location,
  Type_shared,
} //Type_localSystem本地的系统通知，不从服务器取数据

@JsonSerializable()
class TimeLineSync {
  String? timeline_id;
  int? sequence_id;
  int? conversation;
  String? send_time;
  int? sender;
  String? serdername;
  String? serderpicture;
  String? content;
  int? contenttype; //0文本 1 系统 2 图片 3声音 4地图 5分享
  User? senderUser;
  bool? isplay = false;
  String? localpath;
  int? isopen = 0; //是否打开过红包
  String? source_id = ""; //来源ID

  Map<String, dynamic> toMap() {
    final Map<String, dynamic> data = <String, dynamic>{};

    data['timeline_id'] = timeline_id;
    data['sequence_id'] = sequence_id;
    data['conversation'] = conversation;
    data['send_time'] = send_time;
    data['serdername'] = senderUser == null ? serdername : senderUser!.username;
    data['serderpicture'] = senderUser == null
        ? serderpicture
        : senderUser!.profilepicture;
    data['content'] = content;
    data['contenttype'] = contenttype;
    if (sender != null && sender == 0) {
      data['sender'] = sender;
    } else {
      data['sender'] = senderUser == null ? sender : senderUser!.uid;
    }
    data['uid'] = Global.profile.user!.uid;
    data['localpath'] = localpath;
    data['isopen'] = isopen;
    data['source_id'] = source_id;
    return data;
  }

  TimeLineSync.fromMap(Map<String, dynamic> data) {
    //    User user = User.fromJson(data['sender'] as Map<String, dynamic>);
    timeline_id = data['timeline_id'];
    sequence_id = data['sequence_id'];
    conversation = data['conversation'];
    send_time = data['send_time'];
    sender = data['sender'];
    serdername = data['serdername'];
    serderpicture = data['serderpicture'];
    content = data['content'];
    contenttype = data['contenttype'];
    localpath = data['localpath'];
    isopen = data['isopen'];
    source_id = data['source_id'];
  }

  TimeLineSync.fromMapByServer(Map<String, dynamic> data) {
    //    User user = User.fromJson(data['sender'] as Map<String, dynamic>);
    timeline_id = data['timeline_id'];
    sequence_id = data['sequence_id'];
    conversation = data['conversation'];
    send_time = data['send_time'];
    senderUser = (data['sender'] == null
        ? null
        : User.fromJson(data['sender'] as Map<String, dynamic>));
    serdername = senderUser!.username;
    serderpicture = senderUser!.profilepicture;
    content = data['content'];
    contenttype = data['contenttype'];
    localpath = '';
    source_id = data['source_id'];
  }

  TimeLineSync(
    this.timeline_id,
    this.sequence_id,
    this.conversation,
    this.send_time,
    this.senderUser,
    this.content,
    this.contenttype,
    this.localpath,
    this.source_id,
  ) {
    if (conversation == 0) {
      //拉黑取消拉黑举报等本地提示
      sender = 0;
      serdername = "system";
      serderpicture = "";
    } else {
      sender = senderUser!.uid;
      serdername = senderUser!.username;
      serderpicture = senderUser!.profilepicture;
    }
  }

  //  Map<String, dynamic> toJson() => _$TimeLineSyncToJson(this);
  factory TimeLineSync.fromJson(Map<String, dynamic> json) =>
      _$TimeLineSyncFromJson(json);
}
