import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:push_message_register/push_message_register.dart';

import '../service/userservice.dart';
import '../util/showmessage_util.dart';
import '../model/im/grouprelation.dart';
import '../model/evaluateactivity.dart';
import '../service/activity.dart';
import '../util/imhelper_util.dart';
import '../service/gpservice.dart';
import '../model/grouppurchase/goodpice_model.dart';
import '../global.dart';

class TokenUtil {
  final PushMessageRegister _pushMessageRegister = PushMessageRegister();
  final UserService _userService = UserService();
  String _brand = "other";
  final ImHelper _imHelper = ImHelper();
  final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;
  final FlutterLocalNotificationsPlugin _localNotifications =
      FlutterLocalNotificationsPlugin();

  Future<void> getDeviceToken() async {
    await _getDeviceToken();
  }

  Future<void> _getDeviceToken() async {
    if (Global.profile.user != null) {
      if (Platform.isAndroid) {
        _pushMessageRegister.onReceiveMessage().listen((event) {
          if (event["result"] == "success") {
            Global.devicetoken = event["token"].toString();
            Global.brand = event["brand"].toString();
            if (Global.profile.user != null) {
              _userService.updatePushToken(
                Global.profile.user!.uid,
                Global.profile.user!.token!,
                Global.brand,
                Global.devicetoken,
                (error, msg) {
                  ShowMessage.showToast(msg);
                },
              );
            }
          }
        });
        //vivo配置在AndroidManifest.xml
        Map apikey = {
          "XIAOMI_APP_ID": "2882303761519957474",
          "XIAOMI_APP_KEY": "5621995751474",
          "HUAWEI_APP_ID": "104414629",
          "HUAWEI_APP_KEY": "",
          "OPPO_APP_KEY": "bd433ec5604645a88acdd28456a67aef",
          "OPPO_APP_SECRET": "52e07d9d047543168a1d213439e95336",
          "MEIZU_APP_ID": "146976",
          "MEIZU_APP_KEY": "dfdffa4965214f31b75047c058483b89",
        };
        _brand = await PushMessageRegister.registerApi(apikey);
      }

      if ((!kIsWeb && Platform.isIOS) || _brand == "other") {
        await _initializeFirebaseMessaging();
      }
    }
  }

  Future<void> _initializeFirebaseMessaging() async {
    // 请求通知权限
    NotificationSettings settings = await _firebaseMessaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      announcement: false,
      carPlay: false,
      criticalAlert: false,
      provisional: false,
    );

    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      // 初始化本地通知
      await _initializeLocalNotifications();

      // 获取FCM token
      String? token = await _firebaseMessaging.getToken();
      if (token != null) {
        Global.devicetoken = token;
        _updatePushToken(token);
      }

      // 监听token刷新
      _firebaseMessaging.onTokenRefresh.listen((String token) {
        Global.devicetoken = token;
        _updatePushToken(token);
      });

      // 设置消息处理器
      FirebaseMessaging.onMessage.listen(_handleForegroundMessage);
      FirebaseMessaging.onMessageOpenedApp.listen(_handleBackgroundMessage);

      // 检查应用启动时的消息
      RemoteMessage? initialMessage = await _firebaseMessaging
          .getInitialMessage();
      if (initialMessage != null) {
        await _handleBackgroundMessage(initialMessage);
      }
    }
  }

  Future<void> _initializeLocalNotifications() async {
    const AndroidInitializationSettings androidSettings =
        AndroidInitializationSettings('@mipmap/ic_launcher');
    const DarwinInitializationSettings iosSettings =
        DarwinInitializationSettings(
          requestAlertPermission: true,
          requestBadgePermission: true,
          requestSoundPermission: true,
        );

    const InitializationSettings settings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    await _localNotifications.initialize(
      settings,
      onDidReceiveNotificationResponse: _handleNotificationResponse,
    );
  }

  void _updatePushToken(String token) {
    if (Global.profile.user != null) {
      if (Platform.isIOS) {
        _userService.updatePushToken(
          Global.profile.user!.uid,
          Global.profile.user!.token!,
          "ios",
          token,
          (error, msg) {},
        );
      } else {
        _userService.updatePushToken(
          Global.profile.user!.uid,
          Global.profile.user!.token!,
          "fcm",
          token,
          (error, msg) {
            ShowMessage.showToast(msg);
          },
        );
      }
    }
  }

  Future<void> _handleForegroundMessage(RemoteMessage message) async {
    // 在前台显示本地通知
    await _showLocalNotification(message);
    await onPush('onMessage', message);
  }

  Future<void> _handleBackgroundMessage(RemoteMessage message) async {
    await onPush('onResume', message);
  }

  void _handleNotificationResponse(NotificationResponse response) async {
    if (response.payload != null) {
      // 处理通知点击
      await deeplinkNav(response.payload!);
    }
  }

  Future<void> _showLocalNotification(RemoteMessage message) async {
    const AndroidNotificationDetails androidDetails =
        AndroidNotificationDetails(
          'high_importance_channel',
          'High Importance Notifications',
          channelDescription:
              'This channel is used for important notifications.',
          importance: Importance.max,
          priority: Priority.high,
        );

    const DarwinNotificationDetails iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    const NotificationDetails details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    String title = message.notification?.title ?? '新消息';
    String body = message.notification?.body ?? '';
    String payload = message.data.toString();

    await _localNotifications.show(
      message.hashCode,
      title,
      body,
      details,
      payload: payload,
    );
  }

  Future<dynamic> onPush(String name, RemoteMessage payload) async {
    String content = payload.data.toString();
    if (content != "") {
      content.replaceAll('{', '').replaceAll('}', '');

      List<String> contents = content.split(',');
      for (String content in contents) {
        if (content.contains('content:')) {
          content = content.split('content:')[1];
          deeplinkNav(content);
        }
      }
    }

    return Future.value(true);
  }

  Future<void> deeplinkNav(String deeplink) async {
    //微信中打开app
    if (deeplink.contains("extmsg=")) {
      deeplink = deeplink.split("extmsg=")[1];
      String actid = deeplink.split("^_^")[0];
      Navigator.pushNamed(
        Global.navigatorKey.currentContext!,
        '/ActivityInfo',
        arguments: {"actid": actid},
      );
    }

    //消息通知pushmessage
    if (deeplink.contains("timeline_id:")) {
      String timelineId = deeplink.split("timeline_id:")[1];

      if (Global.profile.user != null) {
        GroupRelation? groupRelation = await _imHelper
            .getGroupRelationByGroupid(Global.profile.user!.uid, timelineId);
        if (groupRelation != null) {
          Global.timeline_id = timelineId;
          Navigator.pushNamed(
            Global.navigatorKey.currentContext!,
            '/MyMessage',
            arguments: {"GroupRelation": groupRelation},
          ).then((val) {});
        }
      }
    }

    //活动点赞、留言、回复
    if (deeplink.contains("actid:")) {
      String actid = deeplink.split("actid:")[1];
      Navigator.pushNamed(
        Global.navigatorKey.currentContext!,
        '/ActivityInfo',
        arguments: {"actid": actid},
      );
    }

    //新用户关注
    if (deeplink.contains("follow:")) {
      String uid = deeplink.split("follow:")[1];
      Navigator.pushNamed(
        Global.navigatorKey.currentContext!,
        '/OtherProfile',
        arguments: {"uid": uid},
      );
    }

    //新的商品点赞，回复，留言
    if (deeplink.contains("goodpriceid:")) {
      String goodpriceid = deeplink.split("goodpriceid:")[1];
      _gotoGoodPrice(goodpriceid);
    }

    //新bug点赞、回复、留言
    if (deeplink.contains("bugid:")) {
      String bugid = deeplink.split("bugid:")[1];
      Navigator.pushNamed(
        Global.navigatorKey.currentContext!,
        '/BugInfo',
        arguments: {"bugid": bugid},
      );
    }

    //新suggestid点赞、回复、留言
    if (deeplink.contains("suggestid:")) {
      String suggestid = deeplink.split("suggestid:")[1];
      Navigator.pushNamed(
        Global.navigatorKey.currentContext!,
        '/SuggestInfo',
        arguments: {"suggestid": suggestid},
      );
    }

    //新momentid点赞、回复、留言
    if (deeplink.contains("momentid:")) {
      String momentid = deeplink.split("momentid:")[1];
      Navigator.pushNamed(
        Global.navigatorKey.currentContext!,
        '/MomentInfo',
        arguments: {"momentid": momentid},
      );
    }

    //新的评价点赞、回复
    if (deeplink.contains("evaluateid:")) {
      String evaluateid = deeplink.split("evaluateid:")[1];
      ActivityService activityService = ActivityService();
      EvaluateActivity? evaluateactivity = await activityService
          .getEvaluateActivityByEvaluateid(int.parse(evaluateid));
      if (evaluateactivity != null) {
        Navigator.pushNamed(
          Global.navigatorKey.currentContext!,
          '/EvaluateInfo',
          arguments: {"evaluateActivity": evaluateactivity},
        );
      }
    }
  }

  Future<void> _gotoGoodPrice(String goodpriceid) async {
    GPService gpservice = GPService();
    GoodPiceModel? goodprice = await gpservice.getGoodPriceInfo(goodpriceid);
    if (goodprice != null) {
      Navigator.pushNamed(
        Global.navigatorKey.currentContext!,
        '/GoodPriceInfo',
        arguments: {"goodprice": goodprice},
      );
    }
  }
}
