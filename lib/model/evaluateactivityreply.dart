import 'package:json_annotation/json_annotation.dart';

import '../global.dart';
import 'commentreply.dart';
import 'user.dart';
part 'evaluateactivityreply.g.dart';

@JsonSerializable()
class EvaluateActivityReply {
  int? replyid;
  String? actid;
  int? evaluateid;
  User? replyuser;
  User? touser;
  String? replycontent;
  String? replycreatetime;
  bool? isread;
  String? type; //0回复 1评论
  bool? ismaster; //是否是楼主
  String? actcontent;
  String? coverimg;
  String? imagepaths;

  Map<String, dynamic> toMap(ReplyMsgType type) {
    final Map<String, dynamic> data = <String, dynamic>{};

    data['replyid'] = replyid;
    data['actid'] = actid;
    data['evaluateid'] = evaluateid;
    data['replycontent'] = replycontent;
    data['uid'] = replyuser!.uid;
    data['isread'] = isread! ? 1 : 0;
    data['replycreatetime'] = replycreatetime;
    data['username'] = replyuser!.username;
    data['profilepicture'] = replyuser!.profilepicture;
    data['touid'] = Global.profile.user!.uid;
    data['type'] = type.toString();
    data['ismaster'] = ismaster! ? 1 : 0;
    data['actcontent'] = actcontent;
    data['coverimg'] = coverimg;
    data['imagepaths'] = imagepaths;

    return data;
  }

  EvaluateActivityReply.fromMap(Map<String, dynamic> data) {
    //    User user = User.fromJson(data['sender'] as Map<String, dynamic>);
    actid = data['actid'];

    replyid = data['replyid'];
    evaluateid = data['evaluateid'];
    replycontent = data['replycontent'];
    replyuser = User(
      data['uid'],
      "",
      data['username'],
      null,
      null,
      null,
      null,
      data['profilepicture'],
      null,
      null,
      null,
      0,
      0,
      null,
      null,
      "",
      0,
      0,
      0,
      0,
      0,
      "",
      0,
      0,
      0,
      0,
      0,
      "",
      "",
      "",
      0,
      "",
      "",
      false,
      0,
      0,
      0,
      "",
      "",
      "",
    );
    touser = null;
    replycreatetime = data['replycreatetime'];
    isread = data['isread'] == 1 ? true : false;
    ismaster = data['ismaster'] == 1 ? true : false;
    actcontent = data['actcontent'];
    coverimg = data['coverimg'];
    imagepaths = data['imagepaths'];
  }

  EvaluateActivityReply(
    this.replyid,
    this.evaluateid,
    this.replyuser,
    this.touser,
    this.replycontent,
    this.replycreatetime,
    this.isread,
    this.actid,
    this.ismaster,
    this.actcontent,
    this.coverimg,
    this.imagepaths,
  );

  Map<String, dynamic> toJson() => _$EvaluateActivityReplyToJson(this);
  factory EvaluateActivityReply.fromJson(Map<String, dynamic> json) =>
      _$EvaluateActivityReplyFromJson(json);
}
