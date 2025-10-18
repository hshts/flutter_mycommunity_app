import 'dart:convert';
import 'dart:io';

import 'package:dio/dio.dart';
import 'package:convert/convert.dart';
import 'package:crypto/crypto.dart';
import 'package:tobias/tobias.dart' as tobias;

import '../model/user.dart';
import '../model/dynamic.dart';
import '../model/im/grouprelation.dart';
import '../model/im/timelinesync.dart';
import '../model/order.dart';
import '../util/imhelper_util.dart';
import '../util/net_util.dart';
import '../util/showmessage_util.dart';
import '../global.dart';

class UserService {
  ImHelper imHelper = ImHelper();

  //登录
  Future<User?> loginByPASSS(
    String mobile,
    String email,
    String password,
    String captchaVerification,
    Function errorCallBack,
  ) async {
    User? user;
    // String refreshtoken = "";
    String accesstoken = "";
    int uid = 0;
    Map<String, dynamic>? requestData = {"mobile": mobile, "email": email, "password": generateMd5(password)};
    await NetUtil.getInstance().post(requestData, asJson: true, "/user/login", (data) {
      print("EmailPASS validity ok");
      // refreshtoken = data["data"]["refresh_token"].toString();
      accesstoken = data["data"]["access_token"].toString();
      uid = data["data"]["uid"];
      print(uid);

      // 拿到用户信息后补充 token，并持久化
      getUserInfo(uid, errorCallBack).then((userInfo) {
        if (userInfo != null) {
          user = userInfo;
          user!.token = accesstoken;
          Global.profile.user = user;
          Global.saveProfile();
        }
      });
    }, errorCallBack);

    return user;
  }

  //通过手机号发送验证码
  Future<bool> sendMobileOTP(String mobile) async {
    bool vsendstatus = false;
    await NetUtil.getInstance().get(
      "/user/sendMobileOTP",
      (Map<String, dynamic> data) {
        vsendstatus = true;
      },
      params: {"mobile": mobile},
      errorCallBack: errorResponse,
    );
    return vsendstatus;
  }

  //通过email发送验证码
  Future<String> sendEmailOTP(String email, Function errorCallBack) async {
    String token = "";
    // FormData formData = FormData.fromMap({"email": email});
    await NetUtil.getInstance().post({"email": email}, "/user/email-code-login", asJson: true, (
      Map<String, dynamic> data,
    ) {
      token = data["data"].toString();
    }, errorCallBack);
    return token;
  }

  //通过uid发送验证码
  Future<bool> sendVCodeByUid(int uid, String token) async {
    bool vsendstatus = false;
    await NetUtil.getInstance().get(
      "/user/sendVCodeByUid",
      (Map<String, dynamic> data) {
        vsendstatus = true;
      },
      params: {"uid": uid.toString(), "token": token},
      errorCallBack: errorResponse,
    );
    return vsendstatus;
  }

  //手机验证登录
  Future<User?> loginMobileOTP(String mobile, String vcode, String country, Function errorCallBack) async {
    User? user;
    // FormData formData = FormData.fromMap({"mobile": mobile, "vcode": vcode, "country": country});
    Map<String, dynamic> requestData = {"mobile": mobile, "vcode": vcode, "country": country};
    await NetUtil.getInstance().post(
      requestData,
      "/user/loginmobile",
      (data) {
        if (data["data"]["user"].toString() != "") {
          user = User.fromJson(data["data"]["user"]);
          user!.token = data["data"]["token"].toString();
        }
      },
      errorCallBack,
      asJson: true,
    );
    return user;
  }

  //邮箱登录
  Future<User?> loginEmailOTP(String email, String vcode, String token, Function errorCallBack) async {
    User? user;
    String accesstoken = "";
    int uid = 0;
    // FormData formData = FormData.fromMap({"email": email, "code": vcode, "token": token});
    Map<String, dynamic>? requestDate = {"email": email, "code": vcode, "token": token};
    await NetUtil.getInstance().post(requestDate, asJson: true, "/user/email-code-login/validity", (data) {
      print("EmailOTP validity ok");
      accesstoken = data["data"]["access_token"].toString();
      uid = data["data"]["uid"];
      Map<String, dynamic> usermap = {"uid": uid, "username": email, "email": email, "token": accesstoken};

      user = User.fromJson(usermap);
    }, errorCallBack);
    return user;
  }

  //微信登录
  Future<User?> loginweixin(String code, Function errorCallBack) async {
    User? user;
    // FormData formData = FormData.fromMap({"code": code});
    Map<String, dynamic> requestData = {"code": code};
    await NetUtil.getInstance().post(
      requestData,
      "/user/loginweixin",
      (data) {
        if (data["data"]["user"].toString() != "") {
          user = User.fromJson(data["data"]["user"]);
          user!.token = data["data"]["token"].toString();
        }
      },
      errorCallBack,
      asJson: true,
    );
    return user;
  }

  //ios登录
  Future<User?> loginIos(String identityToken, String iosuserid, Function errorCallBack) async {
    User? user;
    // FormData formData = FormData.fromMap({"identityToken": identityToken, "iosuserid": iosuserid});
    Map<String, dynamic> requestData = {"identityToken": identityToken, "iosuserid": iosuserid};
    await NetUtil.getInstance().post(
      requestData,
      "/user/loginios",
      (data) {
        if (data["data"]["user"].toString() != "") {
          user = User.fromJson(data["data"]["user"]);
          user!.token = data["data"]["token"].toString();
        }
      },
      errorCallBack,
      asJson: true,
    );
    return user;
  }

  //支付宝登录注册
  Future<User?> updateLoginali(String authurl, Function errorCallBack) async {
    User? user;
    String authCode = "";
    if (authurl.isNotEmpty) {
      Map ret = await tobias.aliPayAuth(authurl);
      if (ret["result"] != null) {
        String responsestr = ret["result"].toString();
        List<String> parms = responsestr.split('&');
        for (int i = 0; i < parms.length; i++) {
          if (parms[i].contains("auth_code")) {
            authCode = parms[i].split('=')[1];
            // FormData formData = FormData.fromMap({"auth_code": authCode});
            Map<String, dynamic> requestData = {"auth_code": authCode};

            await NetUtil.getInstance().post(
              requestData,
              "/user/AliPay/loginali",
              (Map<String, dynamic> data) {
                if (data["data"]["user"].toString() != "") {
                  user = User.fromJson(data["data"]["user"]);
                  user!.token = data["data"]["token"].toString();
                }
              },
              errorCallBack,
              asJson: true,
            );
          }
        }
      }
    }

    return user;
  }

  //绑定支付宝账号
  Future<User?> updateAliPay(int uid, String token, String authurl, bool confirm, Function errorCallBack) async {
    User? user;
    String authCode = "";
    if (authurl.isNotEmpty) {
      Map ret = await tobias.aliPayAuth(authurl);
      if (ret["result"] != null) {
        String responsestr = ret["result"].toString();
        List<String> parms = responsestr.split('&');
        for (int i = 0; i < parms.length; i++) {
          if (parms[i].contains("auth_code")) {
            authCode = parms[i].split('=')[1];
            // FormData formData = FormData.fromMap({
            //   "uid": uid,
            //   "token": token,
            //   "auth_code": authCode,
            //   "confirm": confirm,
            // });
            Map<String, dynamic> requestData = {"uid": uid, "token": token, "auth_code": authCode, "confirm": confirm};

            await NetUtil.getInstance().post(
              requestData,
              "/user/AliPay/updateali",
              (Map<String, dynamic> data) {
                if (data["data"] != "") {
                  user = User.fromJson(data["data"]);
                }
              },
              errorCallBack,
              asJson: true,
            );
          }
        }
      }
    }

    return user;
  }

  //绑定微信账号
  Future<User?> updateWeixin(int uid, String token, String code, bool confirm, Function errorCallBack) async {
    User? user;

    // FormData formData = FormData.fromMap({"uid": uid, "token": token, "code": code, "confirm": confirm});
    Map<String, dynamic> requestData = {"uid": uid, "token": token, "code": code, "confirm": confirm};

    await NetUtil.getInstance().post(
      requestData,
      "/user/updateweixin",
      (Map<String, dynamic> data) {
        if (data["data"] != "") {
          user = User.fromJson(data["data"]);
        }
      },
      errorCallBack,
      asJson: true,
    );

    return user;
  }

  //绑定ios账号
  Future<User?> updateIos(
    int uid,
    String token,
    String identityToken,
    bool confirm,
    String iosuserid,
    Function errorCallBack,
  ) async {
    User? user;

    // FormData formData = FormData.fromMap({
    //   "uid": uid,
    //   "token": token,
    //   "identityToken": identityToken,
    //   "confirm": confirm,
    //   "iosuserid": iosuserid,
    // });
    Map<String, dynamic> requestData = {
      "uid": uid,
      "token": token,
      "identityToken": identityToken,
      "confirm": confirm,
      "iosuserid": iosuserid,
    };

    await NetUtil.getInstance().post(
      requestData,
      "/user/updateios",
      (Map<String, dynamic> data) {
        if (data["data"] != "") {
          user = User.fromJson(data["data"]);
        }
      },
      errorCallBack,
      asJson: true,
    );

    return user;
  }

  //获取支付宝用户授权请求
  Future<String> getAliUserAuth() async {
    String authurl = "";
    // FormData formData = FormData.fromMap({});
    Map<String, dynamic> requestData = {};
    await NetUtil.getInstance().post(
      requestData,
      "/user/AliPay/userauth",
      (Map<String, dynamic> data) {
        authurl = data["data"];
      },
      (code, msg) {
        ShowMessage.showToast(msg);
      },
      asJson: true,
    );

    return authurl;
  }

  //上传设备信息
  Future<bool> updatePushToken(int uid, String token, String brand, String pushtoken, Function errorCallBack) async {
    bool ret = false;
    // FormData formData = FormData.fromMap({"uid": uid, "token": token, "brand": brand, "pushtoken": pushtoken});
    Map<String, dynamic> requestData = {"uid": uid, "token": token, "brand": brand, "pushtoken": pushtoken};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updatePushToken",
      (data) {
        ret = true;
      },
      errorCallBack,
      asJson: true,
    );
    return ret;
  }

  //手机验证码
  Future<bool> verifyVCode(int uid, String token, String vcode, Function errorCallBack) async {
    bool ret = false;
    // FormData formData = FormData.fromMap({"uid": uid, "token": token, "vcode": vcode});
    Map<String, dynamic> requestData = {"uid": uid, "token": token, "vcode": vcode};
    await NetUtil.getInstance().post(
      requestData,
      "/user/verifyVCode",
      (data) {
        ret = true;
      },
      errorCallBack,
      asJson: true,
    );
    return ret;
  }

  //手机验证码
  Future<User?> updateMobile(
    int uid,
    String token,
    String vcode,
    String mobile,
    String country,
    bool confirm,
    Function errorCallBack,
  ) async {
    User? user;
    // FormData formData = FormData.fromMap({
    //   "uid": uid,
    //   "token": token,
    //   "vcode": vcode,
    //   "mobile": mobile,
    //   "country": country,
    //   "confirm": confirm,
    // });
    Map<String, dynamic> requestData = {
      "uid": uid,
      "token": token,
      "vcode": vcode,
      "mobile": mobile,
      "country": country,
      "confirm": confirm,
    };
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateMobile",
      (data) {
        user = User.fromJson(data["data"]);
      },
      errorCallBack,
      asJson: true,
    );
    return user;
  }

  //手机验证码
  Future<bool> userexit(int uid, String token, Function errorCallBack) async {
    bool ret = false;
    // FormData formData = FormData.fromMap({"uid": uid, "token": token});
    Map<String, dynamic> requestData = {"uid": uid, "token": token};
    await NetUtil.getInstance().post(
      requestData,
      "/user/userexit",
      (data) {
        ShowMessage.cancel();
        ret = true;
      },
      errorCallBack,
      asJson: true,
    );
    return ret;
  }

  //获取用户信息
  Future<User?> getUserInfo(int uid, Function errorCallBack) async {
    User? user;
    // FormData formData = FormData.fromMap({"uid": uid});
    await NetUtil.getInstance().get(
      "/user/getProfile",
      (Map<String, dynamic> data) {
        if (data["data"]["uid"] != null) {
          print(data["data"]);
          user = User.fromJson(data["data"]);
          print(user!.toJson());
          // user!.token = data["token"] ?? Global.profile.user!.token;
          Global.profile.user = user;
          Global.profile.user!.following = user!.following;
          Global.profile.user!.followers = user!.followers;
          Global.saveProfile();
        }
      },
      params: {"uid": uid.toString()},
      errorCallBack: errorResponse,
    );

    return user;
  }

  //更新头像byte
  Future<bool> updateImage(String token, int uid, File myimg) async {
    bool isupdateImage = false;

    FormData formData = FormData.fromMap({
      "imagefile": await MultipartFile.fromFile(myimg.path),
      "token": token,
      "uid": uid,
    });
    await NetUtil.getInstance().post(formData, "/user/updateImage", (Map<String, dynamic> data) {
      isupdateImage = true;
    }, errorResponse);
    return isupdateImage;
  }

  //更新头像ossurl
  Future<bool> updateImageByUrl(String token, int uid, String imgpath, Function errorCallBack) async {
    bool isupdateImage = false;

    Map<String, dynamic> requestData = {"avatar": imgpath};
    await NetUtil.getInstance().post(requestData, "/user/updateAvatar", asJson: true, (Map<String, dynamic> data) {
      isupdateImage = true;
    }, errorCallBack);
    return isupdateImage;
  }

  //更新性别
  Future<bool> updateSex(String token, int uid, String sex, Function errorCallBack) async {
    bool isUpdate = false;

    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "sex": sex});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "sex": sex};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateSex",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //关注话题
  Future<bool> updateSubject(String token, int uid, String subject, Function errorCallBack) async {
    bool isUpdate = false;

    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "subject": subject});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "subject": subject};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateSubject",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //更新生日
  Future<bool> updateBirthday(String token, int uid, String birthday, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "birthday": birthday});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "birthday": birthday};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateBirthday",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //更新昵称
  Future<bool> updateUserName(String token, int uid, String username, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "username": username});
    Map<String, dynamic> requestData = {"name": username};
    await NetUtil.getInstance().post(requestData, "/user/updateName", asJson: true, (Map<String, dynamic> data) {
      isUpdate = true;
    }, errorCallBack);
    return isUpdate;
  }

  //更新位置
  Future<bool> updateLocation(String token, int uid, String province, String city, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "province": province, "city": city});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "province": province, "city": city};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateLocation",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //更新个人简介
  Future<bool> updateSignature(String token, int uid, String signature, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "signature": signature});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "signature": signature};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateSignature",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //更新密碼
  Future<bool> updatePassword(String token, int uid, String password, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "password": generateMd5(password)});
    await NetUtil.getInstance().post(
      {"token": token, "uid": uid, "new_password": generateMd5(password), "repeat_new_password": generateMd5(password)},
      asJson: true,
      "/user/updatePassword",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
    );
    return isUpdate;
  }

  //更新兴趣
  Future<bool> updateInterest(String token, int uid, String interest, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "interest": interest});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "interest": interest};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateInterest",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //更新录音
  Future<bool> updateVoice(String token, int uid, String voice, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "voice": voice});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "voice": voice};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateVoice",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //注销
  Future<bool> deltoken(String token, int uid, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid});
    Map<String, dynamic> requestData = {"token": token, "uid": uid};
    await NetUtil.getInstance().post(
      requestData,
      "/user/deltoken",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      isloginOut: true,
      asJson: true,
    );

    return isUpdate;
  }

  //更新活动不感兴趣用户
  Future<bool> updateNotinteresteduids(String token, int uid, int notinteresteduids, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "notinteresteduids": notinteresteduids});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "notinteresteduids": notinteresteduids};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateNotinteresteduids",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //更新好价不感兴趣用户
  Future<bool> goodpricenotinteresteduids(
    String token,
    int uid,
    int goodpricenotinteresteduids,
    Function errorCallBack,
  ) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({
    //   "token": token,
    //   "uid": uid,
    //   "goodpricenotinteresteduids": goodpricenotinteresteduids,
    // });
    Map<String, dynamic> requestData = {
      "token": token,
      "uid": uid,
      "goodpricenotinteresteduids": goodpricenotinteresteduids,
    };
    await NetUtil.getInstance().post(
      requestData,
      "/user/goodpricenotinteresteduids",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //更新黑名单
  Future<bool> updateBlacklist(String token, int uid, int blacklist, Function errorCallBack) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "blacklist": blacklist});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "blacklist": blacklist};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateBlacklist",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //获取不感兴趣列表
  Future<List<int>> getFollow(int uid) async {
    List<int> lists = [];
    // FormData formData = FormData.fromMap({"uid": uid});
    Map<String, dynamic> requestData = {"uid": uid};
    await NetUtil.getInstance().post(
      requestData,
      "/user/getFollow",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          for (int i = 0; i < data["data"].length; i++) {
            lists.add(data["data"][i]);
          }
        }
      },
      errorResponse,
      isloginOut: true,
      asJson: true,
    );
    return lists;
  }

  //获取黑名单列表
  Future<String> isFollowed(int uid, int followed, Function errorCallBack) async {
    String createtime = "";
    // FormData formData = FormData.fromMap({"uid": uid, "followed": followed});
    Map<String, dynamic> requestData = {"uid": uid, "followed": followed};
    await NetUtil.getInstance().post(
      requestData,
      "/user/selFollwerUser",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          createtime = data["data"];
        }
      },
      errorCallBack,
      isloginOut: true,
      asJson: true,
    );
    return createtime;
  }

  //关注
  Future<bool> Follow(String token, int uid, int followed, Function errorCallBack) async {
    bool ret = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "followed": followed});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "followed": followed};
    await NetUtil.getInstance().post(
      requestData,
      "/user/follwerCommunity",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          ret = true;
        }
      },
      errorCallBack,
      isloginOut: true,
      asJson: true,
    );
    return ret;
  }

  //取消关注
  Future<bool> cancelFollow(String token, int uid, int followed, Function errorCallBack) async {
    bool ret = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "followed": followed});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "followed": followed};
    await NetUtil.getInstance().post(
      requestData,
      "/user/cleanfollwerCommunity",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          ret = true;
        }
      },
      errorCallBack,
      isloginOut: true,
      asJson: true,
    );
    return ret;
  }

  //获取关注的社团
  Future<List<User>> getFollowUsers(int currentIndex, int uid, String token) async {
    List<User> users = [];
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "currentIndex": currentIndex});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "currentIndex": currentIndex};
    await NetUtil.getInstance().post(requestData, "/user/getFollowUsers", asJson: true, (Map<String, dynamic> data) {
      if (data["data"] != null) {
        for (int i = 0; i < data["data"].length; i++) {
          users.add(User.fromJson(data["data"][i]));
        }
      }
    }, errorResponse);
    return users;
  }

  //获取我关注的社团，myhome页面中使用只返回5条记录
  Future<List<User>> getFollowUsersInCommunityALL(int currentIndex, int uid, String token) async {
    List<User> users = [];
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "currentIndex": currentIndex});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "currentIndex": currentIndex};
    await NetUtil.getInstance().post(
      requestData,
      "/user/getFollowUsersInCommunityALL",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          for (int i = 0; i < data["data"].length; i++) {
            users.add(User.fromJson(data["data"][i]));
          }
        }
      },
      errorResponse,
      asJson: true,
    );
    return users;
  }

  //获取关注的用户和社团
  Future<List<User>> getFollowUsersCommunity(int uid, int currentIndex) async {
    List<User> users = [];
    // FormData formData = FormData.fromMap({"uid": uid, "currentIndex": currentIndex});
    Map<String, dynamic> requestData = {"uid": uid, "currentIndex": currentIndex};
    await NetUtil.getInstance().post(
      requestData,
      "/user/getFollowUsersCommunity",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          for (int i = 0; i < data["data"].length; i++) {
            User tem = User.fromJson(data["data"][i]);
            tem.isFollow = true;
            users.add(tem);
          }
        }
      },
      errorResponse,
      asJson: true,
    );
    return users;
  }

  //获取用户粉丝
  Future<List<User>> getFans(int uid, int currentIndex) async {
    List<User> lists = [];
    // FormData formData = FormData.fromMap({"uid": uid, "currentIndex": currentIndex});
    Map<String, dynamic> requestData = {"uid": uid, "currentIndex": currentIndex};
    await NetUtil.getInstance().post(requestData, "/user/getFansUsers", asJson: true, (Map<String, dynamic> data) {
      if (data["data"] != null) {
        for (int i = 0; i < data["data"].length; i++) {
          lists.add(User.fromJson(data["data"][i]));
        }
      }
    }, errorResponse);
    return lists;
  }

  //获取个人动态
  Future<List<Dynamic>> getUserDynamic(int currentIndex, int uid) async {
    List<Dynamic> dynamics = [];
    // FormData formData = FormData.fromMap({"currentIndex": currentIndex, "uid": uid.toString()});
    Map<String, dynamic> requestData = {"currentIndex": currentIndex, "uid": uid.toString()};
    await NetUtil.getInstance().post(
      requestData,
      "/user/selUserDynamic",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          for (int i = 0; i < data["data"].length; i++) {
            dynamics.add(Dynamic.fromJson(data["data"][i]));
          }
        }
      },
      errorResponse,
      asJson: true,
    );
    return dynamics;
  }

  //获取私聊关系
  Future<GroupRelation?> getSingleConversation(
    String timelineId,
    int uid,
    int touid,
    String token,
    Function errorCallBack,
  ) async {
    GroupRelation? groupRelation;
    // FormData formData = FormData.fromMap({"token": token, "touid": touid, "uid": uid, "timeline_id": timelineId});
    Map<String, dynamic> requestData = {"token": token, "touid": touid, "uid": uid, "timeline_id": timelineId};
    await NetUtil.getInstance().post(
      requestData,
      "/user/getSingleConversation",
      (Map<String, dynamic> data) {
        groupRelation = GroupRelation.fromJson(data['data']);
      },
      errorCallBack,
      asJson: true,
    );
    return groupRelation;
  }

  //创建私聊关系
  Future<GroupRelation?> joinSingle(
    String timelineId,
    int uid,
    int touid,
    String token,
    String captchaVerification,
    Function errorCallBack, {
    int isCustomer = 0,
  }) async {
    GroupRelation? groupRelation;
    // FormData formData = FormData.fromMap({
    //   "token": token,
    //   "touid": touid,
    //   "uid": uid,
    //   "timeline_id": timelineId,
    //   "captchaVerification": captchaVerification,
    //   "isCustomer": isCustomer,
    // });
    Map<String, dynamic> requestData = {
      "token": token,
      "touid": touid,
      "uid": uid,
      "timeline_id": timelineId,
      "captchaVerification": captchaVerification,
      "isCustomer": isCustomer,
    };
    await NetUtil.getInstance().post(
      requestData,
      "/user/joinSingle",
      (Map<String, dynamic> data) {
        groupRelation = GroupRelation.fromJson(data['data']);
      },
      errorCallBack,
      asJson: true,
    );
    return groupRelation;
  }

  //联系客服
  Future<GroupRelation?> joinSingleCustomer(
    String timelineId,
    int uid,
    int touid,
    String token,
    String captchaVerification,
    Function errorCallBack, {
    int isCustomer = 0,
  }) async {
    GroupRelation? groupRelation;
    // FormData formData = FormData.fromMap({
    //   "token": token,
    //   "touid": touid,
    //   "uid": uid,
    //   "timeline_id": timelineId,
    //   "captchaVerification": captchaVerification,
    //   "isCustomer": 1,
    // });
    Map<String, dynamic> requestData = {
      "token": token,
      "touid": touid,
      "uid": uid,
      "timeline_id": timelineId,
      "captchaVerification": captchaVerification,
      "isCustomer": 1,
    };
    await NetUtil.getInstance().post(
      requestData,
      "/user/joinSingle",
      (Map<String, dynamic> data) async {
        groupRelation = GroupRelation.fromJson(data['data'][0]);
        TimeLineSync timeLineSync = TimeLineSync.fromMapByServer(data["data"][1]);
        List<TimeLineSync> timeLineSyncs = [];
        timeLineSyncs.add(timeLineSync);
        await imHelper.saveMessageCustomer(timeLineSyncs);
      },
      errorCallBack,
      asJson: true,
    );
    return groupRelation;
  }

  String generateMd5(String data) {
    var content = Utf8Encoder().convert(data);
    var digest = md5.convert(content);
    // 这里其实就是 digest.toString()
    return hex.encode(digest.bytes);
  }

  void errorResponse(String statusCode, String msg) {
    if (statusCode == "-9015") {
      //用户不存在
    } else {
      ShowMessage.showToast(msg);
    }
  }

  //获取用户
  Future<User?> getOtherUser(int otheruid) async {
    User? user;
    // FormData formData = FormData.fromMap({"uid": otheruid});
    Map<String, dynamic> requestData = {"uid": otheruid};

    await NetUtil.getInstance().post(
      requestData,
      "/user/getuserinfo",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          user = User.fromJson(data["data"]);
        }
      },
      errorResponse,
      asJson: true,
    );

    return user;
  }

  //发送加好友请求
  Future<bool> updateMemberJoin(
    String token,
    int uid,
    int touid,
    String cid,
    String content,
    int jointype,
    Function errorCallBack,
  ) async {
    bool isUpdate = false;
    // FormData formData = FormData.fromMap({"token": token, "uid": uid, "touid": touid, "content": content});
    Map<String, dynamic> requestData = {"token": token, "uid": uid, "touid": touid, "content": content};
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateMemberJoin",
      (Map<String, dynamic> data) {
        isUpdate = true;
      },
      errorCallBack,
      asJson: true,
    );
    return isUpdate;
  }

  //分享好友
  Future<bool> updateSharedFriend(
    String token,
    int uid,
    String id,
    String content,
    String image,
    String touids,
    int sharedtype,
    Function errorCallBack,
  ) async {
    bool ret = false;
    // FormData formData = FormData.fromMap({
    //   "token": token,
    //   "uid": uid,
    //   "contentid": id,
    //   "touids": touids,
    //   "sharedtype": sharedtype,
    //   "content": content,
    //   "image": image,
    //   "fromuid": Global.profile.user!.uid,
    // });
    Map<String, dynamic> requestData = {
      "token": token,
      "uid": uid,
      "contentid": id,
      "touids": touids,
      "sharedtype": sharedtype,
      "content": content,
      "image": image,
      "fromuid": Global.profile.user!.uid,
    };
    await NetUtil.getInstance().post(
      requestData,
      "/user/updateSharedFriend",
      (Map<String, dynamic> data) {
        ret = true;
      },
      errorCallBack,
      asJson: true,
    );
    return ret;
  }

  //获取我的订单
  Future<List<Order>> getMyOrder(String token, int uid, Function errorCallBack) async {
    List<Order> orders = [];
    // FormData formData = FormData.fromMap({"token": token, "uid": uid});
    Map<String, dynamic> requestData = {"token": token, "uid": uid};
    await NetUtil.getInstance().post(
      requestData,
      "/grouppurchase/getMyPendingOrder",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          for (int i = 0; i < data["data"].length; i++) {
            orders.add(Order.fromJson(data["data"][i]));
          }
        }
      },
      errorCallBack,
      asJson: true,
    );
    return orders;
  }

  //获取已完成付款的订单
  Future<List<Order>> getMyOrderFinish(String token, int uid, Function errorCallBack) async {
    List<Order> orders = [];
    // FormData formData = FormData.fromMap({"token": token, "uid": uid});
    Map<String, dynamic> requestData = {"token": token, "uid": uid};
    await NetUtil.getInstance().post(
      requestData,
      "/grouppurchase/getMyFinishOrder",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          for (int i = 0; i < data["data"].length; i++) {
            orders.add(Order.fromJson(data["data"][i]));
          }
        }
      },
      errorCallBack,
      asJson: true,
    );
    return orders;
  }

  //获取已退款的订单
  Future<List<Order>> getMyRefundOrder(String token, int uid, Function errorCallBack) async {
    List<Order> orders = [];
    // FormData formData = FormData.fromMap({"token": token, "uid": uid});
    Map<String, dynamic> requestData = {"token": token, "uid": uid};
    await NetUtil.getInstance().post(
      requestData,
      "/grouppurchase/getMyRefundOrder",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          for (int i = 0; i < data["data"].length; i++) {
            orders.add(Order.fromJson(data["data"][i]));
          }
        }
      },
      errorCallBack,
      asJson: true,
    );
    return orders;
  }

  //获取已确认的订单
  Future<List<Order>> getMyConfirmOrder(String token, int uid, Function errorCallBack) async {
    List<Order> orders = [];
    // FormData formData = FormData.fromMap({"token": token, "uid": uid});
    Map<String, dynamic> requestData = {"token": token, "uid": uid};
    await NetUtil.getInstance().post(
      requestData,
      "/grouppurchase/getMyConfirmOrder",
      (Map<String, dynamic> data) {
        if (data["data"] != null) {
          for (int i = 0; i < data["data"].length; i++) {
            orders.add(Order.fromJson(data["data"][i]));
          }
        }
      },
      errorCallBack,
      asJson: true,
    );
    return orders;
  }
}
