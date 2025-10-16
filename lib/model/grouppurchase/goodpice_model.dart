import 'package:json_annotation/json_annotation.dart';

part 'goodpice_model.g.dart';

@JsonSerializable()
class GoodPiceModel {
  @JsonKey(defaultValue: "")
  String goodpriceid;
  @JsonKey(defaultValue: "")
  String title; //标题
  @JsonKey(defaultValue: "")
  String content; //内容
  @JsonKey(defaultValue: 0)
  int category; //分类
  @JsonKey(defaultValue: "")
  String brand; //品牌
  @JsonKey(defaultValue: 1.0)
  double discount; //折扣
  @JsonKey(defaultValue: "")
  String endtime; //折扣结束时间
  @JsonKey(defaultValue: "")
  String createtime;
  @JsonKey(defaultValue: "")
  String albumpics;
  @JsonKey(defaultValue: "")
  String pic;
  @JsonKey(defaultValue: 0)
  int sellnum; //销售数量
  @JsonKey(defaultValue: 0)
  int collectionnum; //收藏数量
  @JsonKey(defaultValue: "")
  String province; //所在省
  @JsonKey(defaultValue: "")
  String city; //所在城市
  @JsonKey(defaultValue: 0)
  int uid; //用户id
  @JsonKey(defaultValue: "")
  String username; //名称
  @JsonKey(defaultValue: "")
  String profilepicture; //
  @JsonKey(defaultValue: 0)
  int likenum;
  @JsonKey(defaultValue: 0)
  int unlikenum;
  @JsonKey(defaultValue: 0)
  int commentnum;
  @JsonKey(defaultValue: 1)
  int productstatus; //0未审核  1已审核 2退回 3已过期
  @JsonKey(defaultValue: 0.0)
  double satisfactionrate; //好评率
  @JsonKey(defaultValue: 0)
  int activitycount; //活动数
  @JsonKey(defaultValue: "")
  String tag;
  @JsonKey(defaultValue: "")
  String msg;
  @JsonKey(defaultValue: "")
  String addresstitle;
  @JsonKey(defaultValue: "")
  String address;
  @JsonKey(defaultValue: 0.0)
  double lat;
  @JsonKey(defaultValue: 0.0)
  double lng;
  @JsonKey(defaultValue: 0.0)
  double mincost;
  @JsonKey(defaultValue: 0.0)
  double maxcost;
  @JsonKey(defaultValue: 0)
  int evaluatenum;

  GoodPiceModel({
    this.goodpriceid = "",
    this.title = "",
    this.content = "",
    this.category = 0,
    this.brand = "",
    this.discount = 1.0,
    this.endtime = "",
    this.createtime = "",
    this.albumpics = "",
    this.pic = "",
    this.collectionnum = 0,
    this.sellnum = 0,
    this.province = "",
    this.city = "",
    this.uid = 0,
    this.username = "",
    this.profilepicture = "",
    this.likenum = 0,
    this.unlikenum = 0,
    this.commentnum = 0,
    this.productstatus = 1,
    this.satisfactionrate = 0.0,
    this.activitycount = 0,
    this.tag = "",
    this.msg = "",
    this.addresstitle = "",
    this.address = "",
    this.lat = 0.0,
    this.lng = 0.0,
    this.mincost = 0.0,
    this.maxcost = 0.0,
    this.evaluatenum = 0,
  });

  factory GoodPiceModel.fromJson(Map<String, dynamic> json) => _$GoodPiceModelFromJson(json);

  Map<String, dynamic> toJson() => _$GoodPiceModelToJson(this);

  GoodPiceModel.fromMap(Map<String, dynamic> data)
    : goodpriceid = data['goodpriceid'] ?? "",
      title = data['title'] ?? "",
      content = data['content'] ?? "",
      category = data['category'] ?? 0,
      brand = data['brand'] ?? "",
      discount = (data['discount'] ?? 1.0).toDouble(),
      endtime = data['endtime'] ?? "",
      createtime = data['createtime'] ?? "",
      albumpics = data['albumpics'] ?? "",
      pic = data['pic'] ?? "",
      collectionnum = data['collectionnum'] ?? 0,
      sellnum = data['sellnum'] ?? 0,
      province = data['province'] ?? "",
      city = data['city'] ?? "",
      uid = data['uid'] ?? 0,
      username = data['username'] ?? "",
      profilepicture = data['profilepicture'] ?? "",
      likenum = data['likenum'] ?? 0,
      unlikenum = data['unlikenum'] ?? 0,
      commentnum = data['commentnum'] ?? 0,
      productstatus = data['productstatus'] ?? 1,
      satisfactionrate = (data['satisfactionrate'] ?? 0.0).toDouble(),
      activitycount = data['activitycount'] ?? 0,
      tag = data['tag'] ?? "",
      msg = data['msg'] ?? "",
      addresstitle = data['addresstitle'] ?? "",
      address = data['address'] ?? "",
      lat = (data['lat'] ?? 0.0).toDouble(),
      lng = (data['lng'] ?? 0.0).toDouble(),
      mincost = (data['mincost'] ?? 0.0).toDouble(),
      maxcost = (data['maxcost'] ?? 0.0).toDouble(),
      evaluatenum = data['evaluatenum'] ?? 0;
}
