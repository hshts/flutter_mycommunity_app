import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  @JsonKey(defaultValue: 0)
  int uid;
  @JsonKey(defaultValue: "")
  String mobile = "";
  @JsonKey(defaultValue: "")
  String username = "";
  @JsonKey(defaultValue: "")
  String email = "";
  String? sex;
  String? country;
  String? province;
  String? city;
  @JsonKey(defaultValue: "")
  String signature = "";
  String? profilepicture;
  int? pwerrorcount;
  String? birthday;
  int? followers; //关注我的人
  int? following; //我关注的人
  bool isFollow = false;

  String? updatetime; //更新时间
  int? likenum;
  String? token = "";

  int? likeact;
  int? collectionact;
  @JsonKey(defaultValue: 0)
  int likecomment;
  int? likeevaluate;
  int? collectionproduct;
  @JsonKey(defaultValue: "")
  String aliuserid = "";
  @JsonKey(defaultValue: "")
  String wxuserid = "";
  @JsonKey(defaultValue: "")
  String iosuserid = "";
  @JsonKey(defaultValue: 0)
  int likebug = 0;
  @JsonKey(defaultValue: 0)
  int likesuggest = 0;
  @JsonKey(defaultValue: 0)
  int likebugcomment = 0;
  @JsonKey(defaultValue: 0)
  int likesuggestcomment = 0;
  @JsonKey(defaultValue: 0)
  int likemoment = 0;
  @JsonKey(defaultValue: 0)
  int likemomentcomment = 0;
  @JsonKey(defaultValue: 0)
  int likegoodpricecomment = 0;
  String? notinteresteduids;
  String? blacklist;
  String? goodpricenotinteresteduids;

  int? usertype;
  String? interest;
  String? voice;
  bool? isNew; //是否是新注册用户，用于广告监测统计
  @JsonKey(defaultValue: 0)
  int business = 0; //是否是商户
  @JsonKey(defaultValue: "")
  String subject; //关注的主题

  User(
    this.uid,
    this.mobile,
    this.email,
    this.username,
    this.sex,
    this.country,
    this.province,
    this.city,
    this.signature,
    this.profilepicture,
    this.pwerrorcount,
    this.birthday,
    this.followers,
    this.following,
    this.updatetime,
    this.likenum,
    this.token,
    this.likeact,
    this.collectionact,
    this.likecomment,
    this.likeevaluate,
    this.collectionproduct,
    this.aliuserid,
    this.likebug,
    this.likesuggest,
    this.likebugcomment,
    this.likesuggestcomment,
    this.likegoodpricecomment,
    this.notinteresteduids,
    this.blacklist,
    this.goodpricenotinteresteduids,
    this.usertype,
    this.interest,
    this.voice,
    this.isNew,
    this.business,
    this.likemoment,
    this.likemomentcomment,
    this.wxuserid,
    this.iosuserid,
    this.subject,
  );

  Map<String, dynamic> toJson() => _$UserToJson(this);
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
