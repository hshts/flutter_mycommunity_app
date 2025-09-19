// ignore_for_file: avoid_print

import 'dart:async';
import 'dart:io';
// import 'dart:isolate'; // 未使用，已移除

import 'package:badges/badges.dart' as badges;
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
// import 'package:flutter_downloader/flutter_downloader.dart'; // 未使用，已移除
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:package_info_plus/package_info_plus.dart';

import '../bloc/im/im_bloc.dart';
import '../bloc/user/authentication_bloc.dart';
import '../model/appinfo.dart';
import '../service/commonjson.dart';
import '../service/userservice.dart';
import '../util/appupdate_util.dart';
import '../util/showmessage_util.dart';
import '../common/iconfont.dart';
import '../page/home.dart';
import '../page/user/square/momentlist.dart';

import '../global.dart';
import 'im/relation.dart';
import 'shop/grouppurchase.dart';
import 'user/userhome.dart';

class IndexPage extends StatefulWidget {
  final Object? arguments;
  final bool isPop;

  const IndexPage({super.key, this.arguments}) : isPop = arguments != null;

  @override
  _IndexPageState createState() => _IndexPageState();
}

class _IndexPageState extends State<IndexPage> {
  late List _pages;
  final _pageController = PageController();
  final CommonJSONService _commonJSONService = CommonJSONService();
  final UserService _userService = UserService();
  // final ReceivePort _port = ReceivePort(); // 未使用，已移除
  AppInfo? _appInfo;
  int _currentIndex = 0;

  Widget _drawer = SizedBox.shrink();
  final List<String> _categorytypes = [];
  List<String> _selectList = [];
  GlobalKey<ScaffoldState> indexkey = GlobalKey<ScaffoldState>();
  AuthenticationBloc? _authenticationBloc;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _appUpdate();
    _getCategoryType();

    _pages = [
      HomePage(parentJumpMyProfile: _pageJump, isPop: widget.isPop),
      GroupPurchase(),
      MomentList(indexkey, () {
        if (Global.profile.user != null) {
          if (!indexkey.currentState!.isEndDrawerOpen) {
            print(Global.profile.user!.subject);
            if (Global.profile.user!.subject.isNotEmpty) {
              _selectList = Global.profile.user!.subject.split(",");
            } else {
              _selectList = [];
            }
            setState(() {});
          }
        }
      }),
      RelationList(),
      MyHome(),
    ];
    WidgetsBinding.instance.addPostFrameCallback((data) {
      _pageJump(0);
    });
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _authenticationBloc = BlocProvider.of<AuthenticationBloc>(context);
    FToast().init(context); //初始化提示框，其他页面需要使用
    ScreenUtil.init(context, designSize: Size(360, 690));
  }

  Future<void> _appUpdate() async {
    _appInfo = await _commonJSONService.getSysVersionConfig();
    PackageInfo packageInfo = await PackageInfo.fromPlatform();
    if (_appInfo != null && packageInfo.version != _appInfo!.versionName) {
      //版本不匹配就更新
      if (!kIsWeb && Platform.isAndroid) {
        if (_appInfo!.androidUpdate!) {
          _isshowUpdate(_appInfo!.apkUrl!);
        }
      }

      if (!kIsWeb && Platform.isIOS) {
        if (_appInfo!.iosUpdate!) {
          _isshowUpdate("https://itunes.apple.com/cn/app/id1570133391");
        }
      }
    }
  }

  void _isshowUpdate(String appurl) {
    double pagewidth = MediaQuery.of(context).size.width;
    showDialog(
      context: context,
      //强制更新，不可以点击空白区域关闭，不需要可以不要
      barrierDismissible: true,
      builder: (BuildContext context) {
        return UnconstrainedBox(
          child: Container(
            padding: EdgeInsets.only(left: 15, right: 15, top: 20, bottom: 20),
            width: pagewidth * 0.9,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.all(Radius.circular(6.0)),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                GestureDetector(
                  child: Container(
                    alignment: Alignment.topRight,
                    child: Icon(Icons.close, size: 16),
                  ),
                  onTap: () {
                    Navigator.of(context).pop();
                  },
                ),
                Container(
                  alignment: Alignment.center,
                  color: Colors.white,
                  child: Text(
                    '发现新版本:${_appInfo!.versionName}',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.black,
                      decoration: TextDecoration.none,
                    ),
                  ),
                ),
                SizedBox(height: 19),
                Text(
                  '${_appInfo!.updateLog}',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.black,
                    decoration: TextDecoration.none,
                  ),
                ),
                SizedBox(height: 29),
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Expanded(
                      child: Container(
                        height: 39,
                        decoration: BoxDecoration(
                          color: Global.defredcolor,
                          borderRadius: BorderRadius.all(Radius.circular(39)),
                        ),
                        child: TextButton(
                          child: Text(
                            '立即更新',
                            style: TextStyle(color: Colors.white, fontSize: 14),
                          ),
                          onPressed: () {
                            AppupdateUtil.launcherApp(appurl);
                            Navigator.of(context).pop();
                          },
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    super.dispose();
    AppupdateUtil.dispose();
    _pageController.dispose();
  }

  void _pageJump(index) {
    if (index == 0 || index == 1 || index == 2) {
      _currentIndex = index;
      _pageController.jumpToPage(index);
    } else if (Global.profile.user == null) {
      Navigator.pushNamed(context, '/Login').then((value) {
        if (Global.profile.user != null) {
          if (mounted) {
            setState(() {
              _currentIndex = index;
              _pageController.jumpToPage(index);
            });
          }
        }
      });
      return;
    } else {
      _currentIndex = index;
      _pageController.jumpToPage(index);
    }

    if (mounted) {
      setState(() {});
    }
  }

  //话题
  void _getCategoryType() {
    _commonJSONService.getActivityTypes(_getList);
  }

  void _getList(Map<String, dynamic> data) {
    if (data["data"] != null) {
      data["data"].map((item) {
        _categorytypes.add(item['typename'] as String);
      }).toList();

      setState(() {});
    }
  }

  Widget _buildDarw() {
    if (_categorytypes.isNotEmpty) {
      if (Global.profile.user != null) {
        if (!indexkey.currentState!.isEndDrawerOpen) {
          print(Global.profile.user!.subject);
          if (Global.profile.user!.subject.isNotEmpty) {
            _selectList = Global.profile.user!.subject.split(",");
          } else {
            _selectList = [];
          }
        }
      }

      List<Widget> drawerchildren = [];
      for (String type in _categorytypes) {
        drawerchildren.add(
          ListTile(
            title: Row(
              children: [
                RoundCheckBox(value: _selectList.contains(type)),
                SizedBox(width: 10),
                Text(
                  type,
                  style: TextStyle(color: Colors.black87, fontSize: 14),
                ),
              ],
            ),
            onTap: () {
              if (!(_selectList.contains(type))) {
                _selectList.add(type);
              } else {
                _selectList.remove(type);
              }
              setState(() {});
            },
          ),
        );
      }
      _drawer = Drawer(
        backgroundColor: Colors.white,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Container(
              alignment: Alignment.centerLeft,
              margin: EdgeInsets.only(top: 50, left: 15),
              child: Text(
                _selectList.isNotEmpty
                    ? '选择几个你感兴趣的话题(${_selectList.length}/5)'
                    : '选择几个你感兴趣的话题',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Expanded(child: ListView(children: drawerchildren)),
            Container(
              margin: EdgeInsets.only(right: 10),
              alignment: Alignment.centerRight,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: () async {
                      if (Global.profile.user != null) {
                        String subject = "";
                        for (String s in _selectList) {
                          subject += "$s,";
                        }
                        if (subject != "") {
                          subject = subject.substring(0, subject.length - 1);
                        }

                        bool ret = await _userService.updateSubject(
                          Global.profile.user!.token!,
                          Global.profile.user!.uid,
                          subject,
                          (code, msg) {
                            ShowMessage.showToast(msg);
                          },
                        );
                        if (ret) {
                          Global.profile.user!.subject = subject;
                          Global.saveProfile();
                          _authenticationBloc ??=
                              BlocProvider.of<AuthenticationBloc>(context);
                          _authenticationBloc!.add(Refresh());
                          Navigator.pop(context, true);
                        }
                      } else {
                        Navigator.pushNamed(context, '/Login');
                      }
                    },
                    style: ButtonStyle(
                      backgroundColor: WidgetStateProperty.all(
                        Global.defredcolor,
                      ),
                      shape: WidgetStateProperty.all(
                        RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(9),
                        ),
                      ),
                    ),
                    child: Text(
                      '完成',
                      style: TextStyle(fontSize: 14, color: Colors.white),
                    ),
                  ),
                  SizedBox(width: 10),
                  TextButton(
                    onPressed: () {
                      Navigator.pop(context, false);
                    },
                    style: ButtonStyle(
                      side: WidgetStateProperty.all(
                        BorderSide(color: Colors.black45, width: 0.67),
                      ),
                      shape: WidgetStateProperty.all(
                        RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(9),
                        ),
                      ),
                    ),
                    child: Text(
                      '取消',
                      style: TextStyle(fontSize: 14, color: Colors.black45),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      );
    }

    return _drawer;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: indexkey,
      endDrawer: _buildDarw(),
      bottomNavigationBar: BlocBuilder<ImBloc, ImState>(
        builder: (context, state) {
          int newImMode = 0;
          int newActivity = 0;

          if (state is NewMessageState && Global.profile.user != null) {
            newImMode = state.sysMessage.newImMode;
            newActivity = state.sysMessage.newMyMode;
          }

          return BottomNavigationBar(
            type: BottomNavigationBarType.fixed,
            unselectedItemColor: Colors.black54,
            selectedItemColor: Global.profile.backColor ?? Global.defredcolor,
            selectedFontSize: 12,
            unselectedFontSize: 12,
            currentIndex: _currentIndex,
            items: [
              BottomNavigationBarItem(
                icon: Icon(
                  IconFont.icon_shouye,
                  size: 23,
                  color: Colors.black45,
                ),
                activeIcon: Icon(
                  IconFont.icon_shouye1,
                  color: Global.profile.backColor ?? Global.defredcolor,
                  size: 23,
                ),
                label: '首页',
              ),
              BottomNavigationBarItem(
                icon: Icon(
                  IconFont.icon_icon_shangcheng_xian,
                  color: Colors.black45,
                  size: 23,
                ),
                activeIcon: Icon(
                  IconFont.icon_icon_shangcheng_mian,
                  color: Global.profile.backColor ?? Global.defredcolor,
                  size: 23,
                ),
                label: '活动',
              ),
              BottomNavigationBarItem(
                icon: Icon(
                  IconFont.icon_yumaobi1,
                  size: 23,
                  color: Colors.black45,
                ),
                activeIcon: Icon(
                  IconFont.icon_yumaobi_tianchong,
                  color: Global.profile.backColor ?? Global.defredcolor,
                  size: 23,
                ),
                label: '动态',
              ),
              BottomNavigationBarItem(
                icon: newImMode > 0 && Global.profile.user != null
                    ? badges.Badge(
                        badgeContent: Text(
                          newImMode > 99 ? '...' : newImMode.toString(),
                          style: TextStyle(fontSize: 9, color: Colors.white),
                        ),
                        child: Icon(
                          IconFont.icon_xiaoxixuanzhong01,
                          color: Colors.black45,
                          size: 23,
                        ),
                      )
                    : Icon(
                        IconFont.icon_xiaoxixuanzhong01,
                        color: Colors.black45,
                        size: 23,
                      ),
                activeIcon: Icon(
                  IconFont.icon_xiaoxi,
                  color: Global.profile.backColor ?? Global.defredcolor,
                  size: 23,
                ),
                label: '消息',
              ),
              BottomNavigationBarItem(
                icon: newActivity > 0 && Global.profile.user != null
                    ? badges.Badge(
                        badgeContent: Text(
                          newActivity > 99 ? '...' : newActivity.toString(),
                          style: TextStyle(fontSize: 9, color: Colors.white),
                        ),
                        child: Icon(
                          IconFont.icon_wode1,
                          color: Colors.black45,
                          size: 23,
                        ),
                      )
                    : Icon(
                        IconFont.icon_wode1,
                        color: Colors.black45,
                        size: 23,
                      ),
                activeIcon: Icon(
                  IconFont.icon_navbar_wode_xuanzhong,
                  color: Global.profile.backColor ?? Global.defredcolor,
                  size: 23,
                ),
                label: '我的',
              ),
            ],
            onTap: (int index) {
              _pageJump(index);
            },
          );
        },
      ),
      //floatingActionButton: IssuedActivityButton(),
      //floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      body: PageView.builder(
        physics: NeverScrollableScrollPhysics(), //禁止页面左右滑动切换
        controller: _pageController,
        itemCount: _pages.length,
        itemBuilder: (context, index) {
          return _pages[index];
        },
      ),
    );
  }
}

class IssuedActivityButton extends StatelessWidget {
  const IssuedActivityButton({super.key});

  @override
  Widget build(BuildContext context) {
    bool inDebugMode = false;

    assert(inDebugMode = true);

    return Container(
      margin: EdgeInsets.only(top: 10),
      padding: EdgeInsets.all(3),
      height: 55,
      width: 55,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(60),
        color: Colors.white,
      ),
      child: Center(
        child: Stack(
          children: <Widget>[
            FloatingActionButton(
              heroTag: UniqueKey(),
              elevation: 0,
              backgroundColor: Global.profile.backColor ?? Global.defredcolor,
              child: IconButton(
                padding: EdgeInsets.only(bottom: 5),
                icon: Icon(
                  IconFont.icon_tianjiajiahaowubiankuang,
                  size: 25,
                  color: Global.profile.fontColor ?? Colors.white,
                ),
                color: Colors.black,
                onPressed: () {},
              ),
              onPressed: () {
                if (Global.profile.user == null) {
                  Navigator.pushNamed(context, '/Login');
                } else {
                  Navigator.pushNamed(context, '/IssuedActivity');
                }
              },
            ),
            Container(
              width: 55,
              height: 50,
              margin: EdgeInsets.only(top: 35),
              decoration: BoxDecoration(
                color: Colors.yellow,
                borderRadius: inDebugMode
                    ? null
                    : BorderRadius.only(
                        bottomLeft: Radius.circular(8.0),
                        bottomRight: Radius.circular(8.0),
                      ),
              ),
              child: Center(
                child: Text(
                  '超多人来',
                  style: TextStyle(fontSize: 8, color: Colors.black),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// class _TaskInfo { // 未使用的类，已移除
//   String? name;
//   String? link;
//   String? taskId;
//   int? progress = 0;
//   DownloadTaskStatus? status = DownloadTaskStatus.undefined;
//   _TaskInfo({this.link});
// }

class RoundCheckBox extends StatefulWidget {
  const RoundCheckBox({super.key, required this.value});

  final bool value;
  @override
  State<StatefulWidget> createState() {
    return RoundCheckBoxWidgetBuilder();
  }
}

class RoundCheckBoxWidgetBuilder extends State<RoundCheckBox> {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: 24,
      height: 24,
      decoration: BoxDecoration(
        border: Border.all(
          width: 1,
          color: widget.value
              ? (Global.profile.backColor ?? Global.defredcolor)
              : Color(0xff999999),
        ),
        color: widget.value
            ? (Global.profile.backColor ?? Global.defredcolor)
            : Color(0xffffffff),
        borderRadius: BorderRadius.circular(24),
      ),
      child: Center(
        child: Icon(Icons.check, color: Color(0xffffffff), size: 20),
      ),
    );
  }
}
