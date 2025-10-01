// import 'dart:convert' as convert;

class ApiFieldsConverter {
  static Map<String, dynamic> convertUserData(Map<String, dynamic> userData) {
    return {
      "id": userData["id"],
      "username": userData["name"],
      "email": userData["email"],
      "mobile": userData["mobile"],
      "updatetime": userData["updated_at"],
      "profilepicture": userData["avatar"],
    };
  }
  //  int uid;
  // String username = "";
  // String email = "";
  // String? sex;
  // String? country;
  // String? province;
  // String? city;
  // String signature = "";
  // String? profilepicture;
  // int? pwerrorcount;
  // String? birthday;
  // int? followers; //关注我的人
  // int? following; //我关注的人
  // bool isFollow = false;

  // String? updatetime; //更新时间
  // int? likenum;
  // String? token = "";

  // int? likeact;
  // int? collectionact;
  // int likecomment;
  // int? likeevaluate;
  // int? collectionproduct;
  // String aliuserid = "";
  // String wxuserid = "";
  // String iosuserid = "";
  // int likebug = 0;
  // int likesuggest = 0;
  // int likebugcomment = 0;
  // int likesuggestcomment = 0;
  // int likemoment = 0;
  // int likemomentcomment = 0;
  // int likegoodpricecomment = 0;
  // String mobile = "";
  // String? notinteresteduids;
  // String? blacklist;
  // String? goodpricenotinteresteduids;

  // int? usertype;
  // String? interest;
  // String? voice;
  // bool? isNew; //是否是新注册用户，用于广告监测统计
  // int business = 0; //是否是商户
  // String subject; //关注的主题
}
