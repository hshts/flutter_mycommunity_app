import 'package:flutter/material.dart';
import 'package:pull_to_refresh/pull_to_refresh.dart';

import '../../model/user.dart';
import '../../util/common_util.dart';
import '../../util/showmessage_util.dart';
import '../../util/imhelper_util.dart';
import '../../service/userservice.dart';
import '../../widget/circle_headimage.dart';
import '../../global.dart';

class MyFansUser extends StatefulWidget {
  final Object? arguments;
  int uid = 0;
  MyFansUser({super.key, this.arguments}) {
    uid = (arguments as Map)["uid"];
  }

  @override
  _MyFansUserState createState() => _MyFansUserState();
}

class _MyFansUserState extends State<MyFansUser> {
  final RefreshController _refreshController = RefreshController(
    initialRefresh: true,
  );
  final UserService _userService = UserService();
  List<User> users = [];
  ImHelper imHelper = ImHelper();
  bool _ismore = true;
  double pageheight = 0.0;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    pageheight = MediaQuery.of(context).size.height - 150;
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, color: Colors.black, size: 18),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        title: Text('粉丝', style: TextStyle(color: Colors.black, fontSize: 16)),
        centerTitle: true,
      ),
      body: SmartRefresher(
        enablePullDown: true,
        enablePullUp: users.length >= 25,
        onRefresh: _getFollowList,
        header: MaterialClassicHeader(distance: 100),
        footer: CustomFooter(
          builder: (BuildContext context, LoadStatus? mode) {
            Widget body;
            if (mode == LoadStatus.idle) {
              body = Text(
                "加载更多",
                style: TextStyle(color: Colors.black45, fontSize: 13),
              );
            } else if (mode == LoadStatus.loading) {
              body = Center(
                child: CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation(Global.profile.backColor),
                ),
              );
            } else if (mode == LoadStatus.failed) {
              body = Text(
                "加载失败!点击重试!",
                style: TextStyle(color: Colors.black45, fontSize: 13),
              );
            } else if (mode == LoadStatus.canLoading) {
              body = Text(
                "放开我,加载更多!",
                style: TextStyle(color: Colors.black45, fontSize: 13),
              );
            } else {
              body = Text(
                "—————— 我也是有底线的 ——————",
                style: TextStyle(color: Colors.black45, fontSize: 13),
              );
            }
            print(mode);
            return SizedBox(height: 55.0, child: Center(child: body));
          },
        ),
        controller: _refreshController,
        onLoading: _onLoading,
        child:
            _refreshController.headerStatus == RefreshStatus.completed &&
                users.isEmpty
            ? Center(
                child: Text(
                  '创建活动就能受到更多关注',
                  style: TextStyle(color: Colors.black54, fontSize: 14),
                  maxLines: 2,
                ),
              )
            : ListView(
                addAutomaticKeepAlives: true,
                children: buildMemberList(),
              ),
      ),
    );
  }

  void _getFollowList() async {
    users = await _userService.getFans(widget.uid, 0);
    await getFollowInfo();
    _refreshController.refreshCompleted();
    if (mounted) setState(() {});
  }

  void _onLoading() async {
    if (!_ismore) return;
    final moredata = await _userService.getFans(widget.uid, users.length);

    if (moredata.isNotEmpty) users = users + moredata;

    await getFollowInfo();

    if (moredata.length >= 25) {
      _refreshController.loadComplete();
    } else {
      _ismore = false;
      _refreshController.loadNoData();
    }

    if (mounted) setState(() {});
  }

  List<Widget> buildMemberList() {
    List<Widget> widgets = [];
    widgets.add(SizedBox(height: 10));
    for (var element in users) {
      if (element.uid == widget.uid) {
        widgets.add(SizedBox.shrink());
      } else {
        String tem = element.isFollow ? "已关注" : " ＋ 关注";
        widgets.add(
          Padding(
            padding: EdgeInsets.only(left: 5, right: 5, top: 0),
            child: Card(
              shape: const RoundedRectangleBorder(
                borderRadius: BorderRadius.all(Radius.circular(14.0)),
              ), //设置圆角
              elevation: 0,
              child: ListTile(
                onTap: () {
                  if (Global.profile.user != null &&
                      element.uid == Global.profile.user!.uid) {
                    Navigator.pushNamed(context, '/MyProfile');
                  } else {
                    Navigator.pushNamed(
                      context,
                      '/OtherProfile',
                      arguments: {"uid": element.uid},
                    );
                  }
                },
                title: Padding(
                  padding: EdgeInsets.only(top: 5, bottom: 3),
                  child: Text(
                    element.username,
                    style: TextStyle(
                      color: Colors.black87,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Text(
                      element.signature == "" ? 'Ta很神秘' : element.signature,
                      maxLines: 2,
                      style: TextStyle(color: Colors.black87, fontSize: 13),
                    ),
                    SizedBox(height: 3),
                    Text(
                      '有${CommonUtil.getNum(element.likenum!)}个赞',
                      style: TextStyle(color: Colors.black54, fontSize: 12),
                    ),
                    SizedBox(height: 5),
                  ],
                ),
                leading: NoCacheCircleHeadImage(
                  imageUrl:
                      element.profilepicture! ?? Global.profile.profilePicture!,
                  width: 50,
                  uid: element.uid,
                ),
                trailing:
                    Global.profile.user != null &&
                        Global.profile.user!.uid == element.uid
                    ? SizedBox.shrink()
                    : SizedBox(
                        height: 36,
                        child: OutlinedButton(
                          style: OutlinedButton.styleFrom(
                            backgroundColor: element.isFollow
                                ? Colors.grey.shade200
                                : Global.profile.backColor,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.all(
                                Radius.circular(10),
                              ),
                            ),
                            side: BorderSide(
                              color: element.isFollow
                                  ? Colors.grey.shade200
                                  : Global.profile.backColor!,
                            ),
                          ),
                          child: Text(
                            tem,
                            style: TextStyle(
                              color: element.isFollow
                                  ? Colors.black54
                                  : Global.profile.backColor,
                              fontSize: 14,
                            ),
                          ),
                          onPressed: () async {
                            if (element.isFollow) {
                              bool ret = await _userService.cancelFollow(
                                Global.profile.user!.token!,
                                Global.profile.user!.uid,
                                element.uid,
                                errorCallBack,
                              );
                              if (ret) {
                                await imHelper.delFollowState(
                                  element.uid,
                                  Global.profile.user!.uid,
                                );
                                Global.profile.user!.following =
                                    Global.profile.user!.following! - 1;
                                Global.saveProfile();
                                element.isFollow = false;
                                setState(() {});
                              }
                            } else {
                              bool ret = await _userService.Follow(
                                Global.profile.user!.token!,
                                Global.profile.user!.uid,
                                element.uid,
                                errorCallBack,
                              );
                              if (ret) {
                                await imHelper.delFollowState(
                                  element.uid,
                                  Global.profile.user!.uid,
                                );
                                await imHelper.saveFollowState(
                                  element.uid,
                                  Global.profile.user!.uid,
                                );
                                Global.profile.user!.following =
                                    Global.profile.user!.following! + 1;
                                Global.saveProfile();
                                element.isFollow = true;

                                setState(() {});
                              }
                            }
                          },
                        ),
                      ),
              ),
            ),
          ),
        );
      }
    }
    return widgets;
  }

  Future<void> getFollowInfo() async {
    for (int i = 0; i < users.length; i++) {
      bool ret = await isFollow(users[i].uid, Global.profile.user!.uid);
      if (ret) {
        users[i].isFollow = true;
      }
    }
  }

  Future<bool> isFollow(int followed, int uid) async {
    bool isfollowed = false;
    List<int> list = await imHelper.selFollowState(followed, uid);
    if (list.isNotEmpty) isfollowed = true;

    return isfollowed;
  }

  void errorCallBack(String statusCode, String msg) {
    ShowMessage.showToast(msg);
  }
}
