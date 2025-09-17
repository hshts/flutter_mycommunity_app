import 'dart:io';
import 'dart:math';
import 'dart:typed_data';
import 'dart:ui';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:image_cropper/image_cropper.dart';
import 'package:image_picker/image_picker.dart';
import 'package:loading_more_list/loading_more_list.dart';
import 'package:path_provider/path_provider.dart';
import 'package:crypto/crypto.dart';
import 'package:flutter/foundation.dart';
import 'package:extended_nested_scroll_view/extended_nested_scroll_view.dart';

import '../../model/user.dart';
import '../../model/aliyun/securitytoken.dart';
import '../../page/activity/myactivity.dart';
import '../../widget/message_dialog.dart';
import '../../service/aliyun.dart';
import '../../bloc/user/authentication_bloc.dart';
import '../../util/common_util.dart';
import '../../widget/photo/playvoice.dart';
import '../../global.dart';
import 'square/mymoment.dart';

class MyProfile extends StatefulWidget {
  const MyProfile({super.key});

  @override
  _MyProfileState createState() => _MyProfileState();
}

class _MyProfileState extends State<MyProfile> with TickerProviderStateMixin {
  late User user;
  final AliyunService _aliyunService = AliyunService();

  ///当前滑动的位置
  double offsetDistance = 0.0;
  final double offsetRange = 70;
  bool isUpdateImage = false; //是否更新过头像，如果更新过需要刷新缓存

  ///动画控制器
  late AnimationController animationColorController;
  late AnimationController animationColorControllerIsDown;

  ///动画值是否重置
  bool isShowDiv = false;

  ///屏幕高度
  late TabController mController;
  String title = "编辑资料";
  double headContainer = 310;
  double pageHeight = 0;
  double tabContent = 0;
  final double statebar = MediaQueryData.fromView(window).padding.top; //状态栏高度
  Color barbackgroundColor = Colors.transparent;
  Color textbarbackgroundColor = Colors.transparent;
  double appbarHeight = 50;
  bool isScroll = false;
  bool isBlack = false;

  final ScrollController _scrollController = ScrollController();
  bool isShowAll = false;
  String strpersonalInfo = "";
  double personalInfoHeight = 20;
  final _picker = ImagePicker();

  void srollChange() {
    if (mounted) {
      setState(() {
        isScroll = false;
      });
    }
  }

  void _onDragUpdate(double offest) {
    //print(offest);
    if (offest.floor() >= 220) {
      if (mounted) {
        setState(() {
          isBlack = true;
          textbarbackgroundColor = Colors.black87;
        });
      }
    }

    if (offest.floor() < 220 && textbarbackgroundColor != Colors.transparent) {
      if (mounted) {
        setState(() {
          isBlack = false;
          textbarbackgroundColor = Colors.transparent;
        });
      }
    }
  }

  @override
  void initState() {
    if (Platform.isAndroid) {
      WidgetsBinding.instance.renderView.automaticSystemUiAdjustment =
          false; //去掉会导致底部状态栏重绘变成黑色，系统UI重绘，，页面退出后要改成true
    }
    // TODO: implement initState
    super.initState();
    mController = TabController(vsync: this, length: 2);
    _scrollController.addListener(() {
      if (_scrollController.position.pixels <=
          _scrollController.position.minScrollExtent) {}
      _onDragUpdate(_scrollController.position.pixels);
    });
    animationColorController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 300),
    );
    animationColorControllerIsDown = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 300),
    );
  }

  @override
  void dispose() {
    if (Platform.isAndroid) {
      WidgetsBinding.instance.renderView.automaticSystemUiAdjustment =
          true; //去掉会导致底部状态栏重绘变成黑色，系统UI重绘，，页面退出后要改成true
    }
    // TODO: implement dispose
    mController.dispose();
    animationColorController.dispose();
    animationColorControllerIsDown.dispose();
    super.dispose();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    user = Global.profile.user!;
    try {
      String sexinfo = user.sex == '1' ? '男生' : (user.sex == '0' ? '女生' : '');
      strpersonalInfo =
          "${user.city != null && user.city!.isNotEmpty ? CommonUtil.getProvinceCityName(user.province, user.city) : "太阳系"} · ${CommonUtil.getAgeGroup(user.birthday!)}$sexinfo · ${CommonUtil.getConstellation(user.birthday!)}";
    } catch (ex) {
      strpersonalInfo = "什么也没有";
    }
    if (tabContent == 0) {
      pageHeight = MediaQuery.of(context).size.height;
      tabContent = pageHeight - headContainer;
    }

    return BlocListener<AuthenticationBloc, AuthenticationState>(
      listener: (context, state) {
        if (state is LoginOuted) {
          Navigator.pushNamedAndRemoveUntil(
            context,
            '/main',
            (route) => false,
            arguments: {"ispop": true},
          );
        }
      },
      child: BlocBuilder<AuthenticationBloc, AuthenticationState>(
        buildWhen: (previousState, state) {
          if (state is LoginOuted) return false;

          return true;
        },
        builder: (context, state) {
          return Scaffold(
            extendBodyBehindAppBar: true,
            body: ExtendedNestedScrollView(
              controller: _scrollController,
              onlyOneScrollInBody: true,
              pinnedHeaderSliverHeightBuilder: () {
                return 100;
              },
              headerSliverBuilder:
                  (BuildContext context, bool? innerBoxIsScrolled) {
                    return <Widget>[
                      SliverAppBar(
                        systemOverlayStyle: SystemUiOverlayStyle.light,
                        leading: InkWell(
                          child: Container(
                            alignment: Alignment.center,
                            child: ClipOval(
                              child: Container(
                                color: !isBlack
                                    ? Colors.black26
                                    : Colors.transparent,
                                alignment: Alignment.center,
                                width: 30,
                                height: 30,
                                child: Icon(
                                  Icons.arrow_back_ios_new,
                                  size: 19,
                                  color: isBlack
                                      ? textbarbackgroundColor
                                      : Colors.white,
                                ),
                              ),
                            ),
                          ),
                          onTap: () {
                            Navigator.pop(context);
                          },
                        ),
                        primary: true,
                        pinned: true,
                        centerTitle: true,
                        title: Text(
                          user.username,
                          style: TextStyle(
                            color: textbarbackgroundColor,
                            fontSize: 16,
                          ),
                        ),
                        expandedHeight: headContainer + personalInfoHeight + 20,
                        flexibleSpace: FlexibleSpaceBar(
                          background: Container(
                            //头部整个背景颜色
                            child: Stack(
                              children: <Widget>[
                                Container(
                                  height: 130,
                                  decoration: BoxDecoration(
                                    image: DecorationImage(
                                      image: NetworkImage(user.profilepicture!),
                                      fit: BoxFit.cover,
                                    ),
                                  ),
                                ),
                                Container(
                                  margin: EdgeInsets.only(top: 130),
                                  color: Colors.white,
                                ),
                                buildHeadInfo(),
                                buildFsInfo(),
                                buildPersonalInfo(),
                              ],
                            ),
                          ),
                        ),
                        elevation: 0,
                        bottom: PreferredSize(
                          preferredSize: Size.fromHeight(20),
                          child: Container(
                            child: Align(
                              alignment: Alignment.topLeft,
                              child: Column(
                                children: <Widget>[
                                  Container(
                                    color: Colors.white,
                                    height: 35,
                                    child: TabBar(
                                      indicatorSize: TabBarIndicatorSize.label,
                                      indicatorColor: Colors.white,
                                      controller: mController,
                                      labelColor: Global.profile.backColor,
                                      unselectedLabelColor: Colors.black54,
                                      unselectedLabelStyle: TextStyle(
                                        fontWeight: FontWeight.w300,
                                      ),
                                      labelStyle: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 15,
                                      ),
                                      tabs: <Widget>[
                                        Text(
                                          '我的活动',
                                          style: TextStyle(
                                            fontSize: 13,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                        Text(
                                          '我的动态',
                                          style: TextStyle(
                                            fontSize: 13,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  Divider(height: 0.1, color: Colors.black12),
                                ],
                              ),
                            ),
                          ),
                        ),
                      ),
                    ];
                  },
              body: TabBarView(
                controller: mController,
                children: [
                  GlowNotificationWidget(
                    MyActivity(
                      user: Global.profile.user!,
                      isScroll: isScroll,
                      srollChange: srollChange,
                    ),
                    showGlowLeading: false,
                  ),
                  GlowNotificationWidget(
                    MyMoment(
                      user: Global.profile.user!,
                      isScroll: isScroll,
                      srollChange: srollChange,
                    ),
                    showGlowLeading: false,
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  //头像，昵称，编辑
  Container buildHeadInfo() {
    return Container(
      margin: EdgeInsets.only(top: 115, left: 17),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          InkWell(
            child: Container(
              height: 96,
              width: 96,
              decoration: BoxDecoration(
                border: Border.all(color: Global.profile.fontColor!, width: 2),
                borderRadius: BorderRadius.circular(50),
                image: DecorationImage(
                  fit: BoxFit.cover,
                  image: NetworkImage(user.profilepicture!),
                ),
              ),
              child: SizedBox.shrink(),
            ),
            onTap: () {
              Navigator.pushNamed(
                context,
                '/PhotoViewImageHead',
                arguments: {"image": user.profilepicture, "iscache": false},
              );
            },
          ),
          Padding(padding: EdgeInsets.only(right: 10)),
          Expanded(
            child: Container(
              padding: EdgeInsets.only(top: 20, left: 0, right: 5),
              child: Column(
                mainAxisSize: MainAxisSize.max,
                children: <Widget>[
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: <Widget>[
                      InkWell(
                        onTap: () {
                          if (user.followers! > 0) {
                            Navigator.pushNamed(
                              context,
                              '/MyFansUser',
                              arguments: {"uid": Global.profile.user!.uid},
                            );
                          }
                        },
                        child: Container(
                          child: Column(
                            children: <Widget>[
                              Text(
                                user.followers == null
                                    ? '0'
                                    : CommonUtil.getNum(user.followers!),
                                style: TextStyle(
                                  color: Colors.black87,
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                '粉丝',
                                style: TextStyle(
                                  color: Colors.black45,
                                  fontSize: 13,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      Container(
                        height: 20,
                        width: 1,
                        color: Colors.white,
                        child: Text(''),
                      ),
                      InkWell(
                        onTap: () {
                          if (user.following! > 0) {
                            Navigator.pushNamed(context, '/MyFollowUser');
                          }
                        },
                        child: Container(
                          child: Column(
                            children: <Widget>[
                              Text(
                                user.following == null
                                    ? '0'
                                    : CommonUtil.getNum(user.following!),
                                style: TextStyle(
                                  color: Colors.black87,
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                '关注',
                                style: TextStyle(
                                  color: Colors.black45,
                                  fontSize: 13,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      Container(
                        height: 20,
                        width: 1,
                        color: Colors.white,
                        child: Text(''),
                      ),
                      InkWell(
                        onTap: () {
                          showDialog(
                            context: context,
                            builder: (BuildContext context) {
                              return MessageDialog(
                                title: Text(
                                  user.username,
                                  style: TextStyle(
                                    fontSize: 16.0,
                                    color: Colors.black,
                                  ),
                                ),
                                message: Column(
                                  children: [
                                    Text(
                                      "活动、留言、评论累计获赞",
                                      style: TextStyle(
                                        fontSize: 14.0,
                                        color: Colors.black45,
                                      ),
                                    ),
                                    SizedBox(height: 20),
                                    Text(
                                      user.likenum.toString(),
                                      style: TextStyle(
                                        fontSize: 16.0,
                                        color: Colors.black87,
                                      ),
                                    ),
                                  ],
                                ),
                                negativeText: "知道了",
                                containerHeight: 80,
                                onPositivePressEvent: () {
                                  Navigator.pop(context);
                                },
                                onCloseEvent: () {
                                  Navigator.pop(context);
                                },
                              );
                            },
                          );
                        },
                        child: Container(
                          child: Column(
                            children: <Widget>[
                              Text(
                                user.likenum == null
                                    ? '0'
                                    : CommonUtil.getNum(user.likenum!),
                                style: TextStyle(
                                  color: Colors.black87,
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                '获赞',
                                style: TextStyle(
                                  color: Colors.black45,
                                  fontSize: 13,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                  Container(
                    width: double.infinity,
                    margin: EdgeInsets.only(
                      right: 10,
                      left: 10,
                      bottom: 10,
                      top: 0,
                    ),
                    child: TextButton(
                      style: TextButton.styleFrom(
                        backgroundColor: Global.profile.backColor,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.all(Radius.circular(5)),
                        ),
                      ),
                      child: Text(
                        title,
                        style: TextStyle(
                          color: Global.profile.fontColor,
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      onPressed: () {
                        Navigator.pushNamed(context, '/MyProfileEdit').then((
                          value,
                        ) {
                          setState(() {});
                        });
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  //个人简介
  Container buildPersonalInfo() {
    return Container(
      alignment: Alignment.topLeft,
      padding: EdgeInsets.only(top: 260, left: 17, right: 10),
      child: Row(
        children: [
          Expanded(
            child: Container(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          user.signature == "" ? 'Ta很神秘' : user.signature,
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(fontSize: 13, color: Colors.black),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 6),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(
                        child: Text(
                          strpersonalInfo,
                          style: TextStyle(fontSize: 13.0, color: Colors.black),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 6),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(
                        child: Text(
                          user.interest != null && user.interest != ""
                              ? "喜欢${CommonUtil.getInterest(user.interest!)}"
                              : "喜欢什么就是不告诉你",
                          style: TextStyle(color: Colors.black, fontSize: 13),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 10),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  //用户名
  Container buildFsInfo() {
    return Container(
      padding: EdgeInsets.only(top: 225, left: 7),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.start,
        children: <Widget>[
          Padding(padding: EdgeInsets.only(left: 10)),
          Text(
            "${user.username}",
            textAlign: TextAlign.left,
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          user.voice != null && user.voice != ""
              ? Padding(padding: EdgeInsets.only(left: 5, top: 0))
              : SizedBox.shrink(),
          user.voice != null && user.voice != ""
              ? PlayVoice(user.voice!)
              : SizedBox.shrink(),
        ],
      ),
    );
  }

  //裁剪
  void showDemoActionSheet({
    required BuildContext context,
    required Widget child,
  }) {
    File? imageFile;
    CroppedFile? croppedFile;
    showCupertinoModalPopup<String>(
      context: context,
      builder: (BuildContext context) => child,
    ).then((String? value) async {
      if (value != null) {
        if (value == "Camera") {
          XFile? image = await _picker.pickImage(source: ImageSource.camera);
          if (image != null) {
            imageFile = File(image.path);
          }
        } else if (value == "Gallery") {
          XFile? image = await _picker.pickImage(source: ImageSource.gallery);
          if (image != null) {
            imageFile = File(image.path);
          }
        }
      }
      if (imageFile != null) {
        croppedFile = await ImageCropper().cropImage(
          sourcePath: imageFile!.path,
          maxWidth: 750,
          maxHeight: 750,
          compressQuality: 19,
          uiSettings: [
            AndroidUiSettings(
              toolbarTitle: '裁剪',
              toolbarColor: Colors.deepOrange,
              toolbarWidgetColor: Colors.white,
              initAspectRatio: CropAspectRatioPreset.square,
              lockAspectRatio: true,
            ),
            IOSUiSettings(
              title: '裁剪',
              minimumAspectRatio: 1.0,
              aspectRatioLockEnabled: true,
            ),
          ],
        );
      }
      if (croppedFile != null) {
        String ossimagpath = "";
        //转成png格式
        final Directory directory = await getTemporaryDirectory();
        final Directory imageDirectory = await Directory(
          '${directory.path}/profilepicture/images/',
        ).create(recursive: true);
        String path = imageDirectory.path;
        Uint8List imageData = await croppedFile!.readAsBytes();
        String md5name = md5.convert(imageData).toString();

        File imageFile = File('${path}originalImage_$md5name.png')
          ..writeAsBytesSync(imageData);

        //上传图片到oss
        SecurityToken? securityToken = await _aliyunService
            .getUserProfileSecurityToken(user.token!, user.uid);
        if (securityToken != null) {
          ossimagpath = await _aliyunService.uploadImage(
            securityToken,
            imageFile.path,
            '$md5name.png',
            user.uid,
          );
        }
        if (ossimagpath.isNotEmpty) {
          BlocProvider.of<AuthenticationBloc>(
            context,
          ).add(UpdateImagePressed(user: user, imgpath: ossimagpath));
        }
      }
    });
  }
}

class Workaround extends StatelessWidget {
  final Widget child;

  const Workaround({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    if (defaultTargetPlatform != TargetPlatform.android) {
      return child;
    }
    final data = MediaQuery.of(context);
    final bottomGesturesInsets = data.systemGestureInsets.bottom;
    final bottomViewInsets = data.viewInsets.bottom;

    var newBottomViewInsets = max(0.0, bottomViewInsets - bottomGesturesInsets);
    var newBottomPadding = data.padding.bottom + bottomGesturesInsets;
    var newBottomViewPadding = data.viewPadding.bottom + bottomGesturesInsets;

    final newData = data.copyWith(
      viewInsets: data.viewInsets.copyWith(bottom: newBottomViewInsets),
      padding: data.padding.copyWith(bottom: newBottomPadding),
      viewPadding: data.viewPadding.copyWith(bottom: newBottomViewPadding),
    );
    return MediaQuery(data: newData, child: child);
  }
}
