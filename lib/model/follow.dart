import 'package:json_annotation/json_annotation.dart';

part 'follow.g.dart';

@JsonSerializable()
class Follow {
  int? id;
  int? uid;
  int? fans;
  String? username;
  String? profilepicture;
  int? isread;
  String? createtime;
  int? type; //0关注 1点赞

  Map<String, dynamic> toMap(Follow type) {
    final Map<String, dynamic> data = <String, dynamic>{};

    data['id'] = id;
    data['uid'] = uid;
    data['fans'] = fans;
    data['username'] = username;
    data['profilepicture'] = profilepicture;
    data['isread'] = 0;
    data['createtime'] = createtime;
    data['type'] = this.type;

    return data;
  }

  Follow.fromMap(Map<String, dynamic> data) {
    //    User user = User.fromJson(data['sender'] as Map<String, dynamic>);
    id = data['id'];
    uid = data['uid'];
    fans = data['fans'];
    username = data['username'];
    profilepicture = data['profilepicture'];
    isread = data['isread'];
    createtime = data['createtime'];
    type = data['type'];
  }

  Follow(
    this.uid,
    this.username,
    this.profilepicture,
    this.isread,
    this.fans,
    this.createtime,
    this.id,
    this.type,
  );

  Map<String, dynamic> toJson() => _$FollowToJson(this);
  factory Follow.fromJson(Map<String, dynamic> json) => _$FollowFromJson(json);
}
