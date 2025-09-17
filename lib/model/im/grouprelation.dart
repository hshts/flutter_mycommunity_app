import 'package:json_annotation/json_annotation.dart';

import '../../global.dart';
part 'grouprelation.g.dart';

@JsonSerializable()
class GroupRelation {
  int? id;
  String timeline_id = "";
  int? uid;
  String? jointime;
  int? readindex;
  int unreadcount = 0;
  String? group_name1;
  String? clubicon;
  String? name;
  String? newmsgtime;
  String? newmsg;
  int? timelineType;
  int? istop;
  int? relationtype; //0活动群，1社团群 //2私聊  //3活动群团购
  int? status; //是否拉黑 1正常 2拉黑
  int? locked; //订单是否已经锁定（发货）0未锁定  1已锁定 2已完成
  String? memberupdatetime; //活动成员更新的时间
  String? oldmemberupdatetime; //上次更新的时间
  int? isnotservice;
  String? source_id;
  String goodpriceid = "";

  GroupRelation(
    this.id,
    this.timeline_id,
    this.readindex,
    this.unreadcount,
    this.group_name1,
    this.clubicon,
    this.name,
    newmsgtime,
    newmsg,
    this.timelineType,
    this.relationtype,
    this.status,
    this.locked,
    this.memberupdatetime,
    this.isnotservice,
    this.source_id,
    this.goodpriceid,
  ) {
    this.newmsgtime = newmsgtime ?? '';
    this.newmsg = newmsg ?? '';
  }

  Map<String, dynamic> toMap() {
    final Map<String, dynamic> data = <String, dynamic>{};

    data['id'] = id;
    data['timeline_id'] = timeline_id;
    data['readindex'] = readindex;
    data['unreadcount'] = unreadcount;
    data['group_name1'] = group_name1;
    data['clubicon'] = clubicon;
    data['name'] = name;
    data['newmsgtime'] = newmsgtime;
    data['newmsg'] = newmsg;
    data['timelineType'] = timelineType;
    data['uid'] = Global.profile.user!.uid;
    data['istop'] = 0;
    data['isdel'] = 0;
    data['relationtype'] = relationtype;
    data['status'] = status;
    data['locked'] = locked;
    data['memberupdatetime'] = memberupdatetime;
    data['oldmemberupdatetime'] = "1999-01-01 00:00:01";
    data['isnotservice'] = 0;
    data['source_id'] = source_id;
    data['goodpriceid'] = goodpriceid;
    return data;
  }

  GroupRelation.fromMap(Map<String, dynamic> data) {
    id = data['id'];
    timeline_id = data['timeline_id'];
    readindex = data['readindex'];
    unreadcount = data['unreadcount'];
    group_name1 = data['group_name1'];
    clubicon = data['clubicon'];
    name = data['name'];
    newmsgtime = data['newmsgtime'];
    newmsg = data['newmsg'];
    timelineType = data['timelineType'];
    istop = data['istop'];
    relationtype = data['relationtype'];
    status = data['status'];
    locked = data['locked'];
    memberupdatetime = data['memberupdatetime'];
    oldmemberupdatetime = data['oldmemberupdatetime'];
    isnotservice = data['isnotservice'];
    source_id = data['source_id'];
    goodpriceid = data['goodpriceid'];
    uid = data['uid'];
  }

  Map<String, dynamic> toJson() => _$GroupRelationToJson(this);
  factory GroupRelation.fromJson(Map<String, dynamic> json) =>
      _$GroupRelationFromJson(json);
}
