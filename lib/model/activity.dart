import 'package:json_annotation/json_annotation.dart';

import 'activityevaluate.dart';
import 'user.dart';
import 'grouppurchase/goodpice_model.dart';

part 'activity.g.dart';

@JsonSerializable()
class Activity {
  @JsonKey(defaultValue: "")
  String actid = "";
  List<User>? members;
  int? peoplenum;
  String? createtime;
  String? updatetime;
  @JsonKey(defaultValue: "")
  String content = "";
  String? score;
  String? actimagespath;
  int? status;
  User? user;
  String? actcity;
  String? actprovince;
  String? coverimg;
  @JsonKey(defaultValue: "")
  String coverimgwh = "";
  @JsonKey(defaultValue: 0)
  int likenum = 0;
  @JsonKey(defaultValue: 0)
  int collectionnum = 0;
  int? startyear;
  int? endyear;
  int? commentnum;
  int? currentpeoplenum;
  @JsonKey(defaultValue: 0.0)
  double maxcost = 0;
  @JsonKey(defaultValue: 0.0)
  double mincost = 0;
  String? address; //活动位置
  String? addresstitle;
  double? lat; //坐标
  double? lng; //坐标
  int? paytype; //0 免费  1后付款  2先付款团购
  String? goodpriceid; //goodprice

  ActivityEvaluate? activityEvaluate; //未评价 1已评价
  int? joinnum;
  int? viewnum;
  String? orderid;
  int? locked; //是否已经开始活动
  GoodPiceModel? goodPiceModel;

  Activity(
    this.actid,
    this.peoplenum,
    this.createtime,
    this.updatetime,
    this.content,
    this.score,
    this.actimagespath,
    this.status,
    this.user,
    this.actcity,
    this.actprovince,
    this.coverimg,
    this.coverimgwh,
    this.likenum,
    this.collectionnum,
    this.startyear,
    this.endyear,
    this.commentnum,
    this.currentpeoplenum,
    this.mincost,
    this.maxcost,
    this.address,
    this.lat,
    this.lng,
    this.addresstitle,
    this.paytype,
    this.orderid,
    this.goodpriceid,
    this.joinnum,
    this.viewnum,
    this.locked,
    this.goodPiceModel,
  );

  Map<String, dynamic> toJson() => _$ActivityToJson(this);
  factory Activity.fromJson(Map<String, dynamic> json) => _$ActivityFromJson(json);

  factory Activity.fromNullObject() {
    Activity activity = Activity(
      "",
      0,
      "",
      "",
      "",
      "",
      "",
      0,
      null,
      "",
      "",
      "",
      "",
      0,
      0,
      0,
      0,
      0,
      0,
      0.0,
      0.0,
      "",
      0.0,
      0.0,
      "",
      0,
      "",
      "",
      0,
      0,
      0,
      null,
    );

    activity.user = User(
      0,
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      0,
      "",
      0,
      0,
      "",
      0,
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
    return activity;
  }

  Activity.fromMap(Map<String, dynamic> data) {
    actid = data['actid'] ?? "";
    coverimgwh = data['coverimgwh'] ?? "800,600";
    coverimg = data['coverimg'] ?? "";
    content = data['content'] ?? "";
    peoplenum = data['peoplenum'];
    createtime = data['createtime'];
    updatetime = data['updatetime'];
    status = data['status'];
    startyear = data['startyear'];
    endyear = data['endyear'];
    currentpeoplenum = data['currentpeoplenum'];
    actcity = data['actcity'];
    actprovince = data['actprovince'];
    actimagespath = data['actimagespath'];
    likenum = data['likenum'] ?? 0;
    collectionnum = data['collectionnum'] ?? 0;
    commentnum = data['commentnum'] ?? 0;
    joinnum = data['joinnum'] ?? 0;
    viewnum = data['viewnum'] ?? 0;
    locked = data['locked'];
    paytype = data['paytype'];
    goodpriceid = data['goodpriceid'];

    address = data["address"] ?? "";
    lat = data["lat"];
    lng = data["lng"];
    mincost = (data["mincost"] ?? 0).toDouble();
    maxcost = (data["maxcost"] ?? 0).toDouble();
    addresstitle = data["addresstitle"] ?? "";

    // 处理嵌套的 user 对象
    if (data['user'] != null && data['user'] is Map) {
      var userData = data['user'] as Map<String, dynamic>;
      user = User(
        userData['uid'] ?? 0,
        "",
        "",
        userData['username'] ?? "",
        "",
        "",
        "",
        "",
        "",
        userData['profilepicture'] ?? "",
        userData['usertype'] ?? 0,
        "",
        0,
        0,
        "",
        0,
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
    } else {
      user = User(
        0,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        0,
        "",
        0,
        0,
        "",
        0,
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
    }
  }

  Activity.fromMapCollection(Map<String, dynamic> data) {
    actid = data['actid'] ?? "";
    coverimgwh = data['coverimgwh'] ?? "800x600";
    coverimg = data['coverimg'] ?? "";
    content = data['content'] ?? "";
    peoplenum = data['peoplenum'];

    // 处理嵌套的 user 对象
    if (data['user'] != null && data['user'] is Map) {
      var userData = data['user'] as Map<String, dynamic>;
      user = User(
        userData['uid'] ?? 0,
        "",
        "",
        userData['username'] ?? "",
        "",
        "",
        "",
        "",
        "",
        userData['profilepicture'] ?? "",
        userData['usertype'] ?? 0,
        "",
        0,
        0,
        "",
        0,
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
    }

    address = data["address"] ?? "";
    lat = data["lat"];
    lng = data["lng"];
    mincost = (data["mincost"] ?? 0).toDouble();
    maxcost = (data["maxcost"] ?? 0).toDouble();
    addresstitle = data["addresstitle"] ?? "";
  }

  Activity.fromMapCollectionTable(Map<String, dynamic> data) {
    actid = data['actid'] ?? "";
    coverimgwh = data['coverimgwh'] ?? "800,600";
    coverimg = data['coverimg'] ?? "";
    content = data['content'] ?? "";
    peoplenum = data['peoplenum'];

    // 处理嵌套的 user 对象
    if (data['user'] != null && data['user'] is Map) {
      var userData = data['user'] as Map<String, dynamic>;
      user = User(
        userData['uid'] ?? 0,
        "",
        "",
        userData['username'] ?? "",
        "",
        "",
        "",
        "",
        "",
        userData['profilepicture'] ?? "",
        userData['usertype'] ?? 0,
        "",
        0,
        0,
        "",
        0,
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
    }

    address = data["address"] ?? "";
    lat = data["lat"];
    lng = data["lng"];
    mincost = (data["mincost"] ?? 0).toDouble();
    maxcost = (data["maxcost"] ?? 0).toDouble();
    addresstitle = data["addresstitle"] ?? "";
  }
}
