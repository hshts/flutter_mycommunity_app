import 'package:json_annotation/json_annotation.dart';

import 'activity.dart';

part 'activityevaluate.g.dart';

@JsonSerializable()
class ActivityEvaluate {
  int? actevaluateid;
  Activity? activity;
  String? createtime;
  int? evaluatestatus;

  ActivityEvaluate({
    this.actevaluateid,
    this.activity,
    this.createtime,
    this.evaluatestatus,
  });

  Map<String, dynamic> toJson() => _$ActivityEvaluateToJson(this);
  factory ActivityEvaluate.fromJson(Map<String, dynamic> json) =>
      _$ActivityEvaluateFromJson(json);

  ActivityEvaluate.fromMap(Map<String, dynamic> data) {
    //    User user = User.fromJson(data['sender'] as Map<String, dynamic>);
    actevaluateid = data['actevaluateid'];
    createtime = data['createtime'];
    evaluatestatus = data['evaluatestatus'];
    activity = Activity.fromNullObject();
    activity!.actid = data['actid'];
    activity!.content = data['content'];
    activity!.coverimg = data['coverimg'];
    activity!.coverimgwh = data['coverimgwh'];

    activity!.peoplenum = data['peoplenum'];
    activity!.currentpeoplenum = data['currentpeoplenum'];
    activity!.user!.uid = data['actuid'];
    activity!.user!.profilepicture = data['profilepicture'];
  }
}
