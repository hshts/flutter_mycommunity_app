import 'package:json_annotation/json_annotation.dart';

part 'goodpice_model.g.dart';

@JsonSerializable()
class GoodPiceModel {
  String goodpriceid = "";
  String title = ""; //标题
  String content = ""; //内容
  int category = 0; //分类
  String brand = ""; //品牌
  double discount = 1; //折扣
  String endtime = ""; //折扣结束时间
  String createtime = "";
  String albumpics = "";
  String pic = "";
  int sellnum = 0; //销售数量
  int collectionnum = 0; //收藏数量
  String province = ""; //所在省
  String city = ""; //所在城市
  int uid = 0; //用户id
  String username = ""; //名称
  String profilepicture = ""; //
  int likenum = 0;
  int unlikenum = 0;
  int commentnum = 0;
  int productstatus = 1; //0未审核  1已审核 2退回 3已过期
  double satisfactionrate = 0; //好评率
  int activitycount = 0; //活动数
  String tag = "";
  String msg = "";
  String addresstitle = "";
  String address = "";
  double lat = 0;
  double lng = 0;
  double mincost = 0;
  double maxcost = 0;
  int evaluatenum = 0;

  GoodPiceModel(
    this.goodpriceid,
    this.title,
    this.content,
    this.category,
    this.brand,
    this.discount,
    this.endtime,
    this.createtime,
    this.albumpics,
    this.pic,
    this.collectionnum,
    this.sellnum,
    this.province,
    this.city,
    this.uid,
    this.username,
    this.profilepicture,
    this.likenum,
    this.unlikenum,
    this.commentnum,
    this.productstatus,
    this.satisfactionrate,
    this.activitycount,
    this.tag,
    this.msg,
    this.addresstitle,
    this.address,
    this.lat,
    this.lng,
    this.mincost,
    this.maxcost,
    this.evaluatenum,
  );

  factory GoodPiceModel.fromJson(Map<String, dynamic> json) =>
      _$GoodPiceModelFromJson(json);

  GoodPiceModel.fromMap(Map<String, dynamic> data) {
    //    User user = User.fromJson(data['sender'] as Map<String, dynamic>);
    goodpriceid = data['goodpriceid'];
    title = data['title'];
    content = data['content'];
    category = data['category'];
    brand = data['brand'];
    discount = data['discount'];
    endtime = data['endtime'];
    createtime = data['createtime'];
    albumpics = data['albumpics'];
    pic = data['pic'];
    collectionnum = data['collectionnum'];
    province = data['province'];
    city = data['city'];
    uid = data['uid'];
    username = data['username'];
    profilepicture = data['profilepicture'];
    likenum = data['likenum'];
    unlikenum = data['unlikenum'];
    commentnum = data['commentnum'];
    productstatus = data['productstatus'];
    satisfactionrate = data['satisfactionrate'];
    activitycount = data['activitycount'];
    tag = data['tag'];
    addresstitle = data['addresstitle'];
    address = data['address'];
    lat = data['lat'];
    lng = data['lng'];
    sellnum = data['sellnum'] ?? 0;
    mincost = data['mincost'];
    maxcost = data['maxcost'];
    evaluatenum = data['evaluatenum'] != null ? data['evaluatenum'] as int : 0;
  }
}
