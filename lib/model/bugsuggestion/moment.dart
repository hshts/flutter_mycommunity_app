import 'package:json_annotation/json_annotation.dart';

import '../user.dart';
part 'moment.g.dart';

@JsonSerializable()
class Moment {
  @JsonKey(defaultValue: "", fromJson: _momentIdFromJson)
  String momentid = "";
  @JsonKey(defaultValue: "")
  String content = "";
  @JsonKey(defaultValue: "")
  String images = "";
  @JsonKey(defaultValue: "")
  String createtime = "";
  @JsonKey(defaultValue: 0)
  int commentcount = 0;
  @JsonKey(defaultValue: 0)
  int likenum = 0;
  @JsonKey(defaultValue: "")
  String voice = "";
  @JsonKey(defaultValue: "")
  String coverimgwh = "";
  @JsonKey(defaultValue: "")
  String category = "";

  User? user;
  @JsonKey(defaultValue: false)
  bool islike = false;

  Moment(
    this.momentid,
    this.content,
    this.images,
    this.createtime,
    this.commentcount,
    this.likenum,
    this.user,
    this.voice,
    this.coverimgwh,
    this.category,
  );

  Map<String, dynamic> toJson() => _$MomentToJson(this);
  factory Moment.fromJson(Map<String, dynamic> json) => _$MomentFromJson(json);

  // Helper function to convert momentid (can be int or String) to String
  static String _momentIdFromJson(dynamic value) {
    if (value == null) return "";
    return value.toString();
  }
}
