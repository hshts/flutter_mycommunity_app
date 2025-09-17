part 'usershared.g.dart';

class UserShared {
  int? sharedid;
  int? uid;
  String? content;
  String? contentid;
  String? image;
  int? sharedtype;
  String? createtime;

  int? fromuid;
  String? fromusername;
  String? fromprofilepicture;
  double? mincost;
  double? maxcost;
  double? lat; //坐标
  double? lng; //坐标

  UserShared(
    this.sharedid,
    this.uid,
    this.content,
    this.contentid,
    this.image,
    this.sharedtype,
    this.createtime,
    this.fromuid,
    this.fromusername,
    this.fromprofilepicture,
    this.mincost,
    this.maxcost,
    this.lat,
    this.lng,
  );

  factory UserShared.fromJson(Map<String, dynamic> json) =>
      _$UserSharedFromJson(json);

  Map<String, dynamic> toMap() {
    final Map<String, dynamic> data = <String, dynamic>{};

    data['sharedid'] = sharedid;
    data['uid'] = uid;
    data['content'] = content;
    data['contentid'] = contentid;
    data['image'] = image;
    data['sharedtype'] = sharedtype;
    data['createtime'] = createtime;
    data['fromuid'] = fromuid;
    data['fromusername'] = fromusername;
    data['fromprofilepicture'] = fromprofilepicture;
    data['mincost'] = mincost;
    data['maxcost'] = maxcost;
    data['lat'] = lat;
    data['lng'] = lng;
    data['isread'] = 0;

    return data;
  }

  UserShared.fromMap(Map<String, dynamic> data) {
    //    User user = User.fromJson(data['sender'] as Map<String, dynamic>);
    sharedid = data['sharedid'];
    uid = data['uid'];
    fromuid = data['touid'];
    content = data['content'];
    createtime = data['createtime'];
    contentid = data['contentid'];
    image = data['image'];
    sharedtype = data['sharedtype'];

    fromprofilepicture = data['fromprofilepicture'];
    fromusername = data['fromusername'];
    mincost = data['mincost'];
    maxcost = data['maxcost'];

    lat = data['lat'];
    lng = data['lng'];
  }
}
