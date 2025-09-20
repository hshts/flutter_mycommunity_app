// Web 平台的 TokenUtil 实现
// 完全移除 Firebase 依赖以避免 Web 平台编译错误

import 'package:flutter/foundation.dart';
import '../global.dart';

class TokenUtil {
  static final TokenUtil _instance = TokenUtil._internal();
  factory TokenUtil() => _instance;
  TokenUtil._internal();

  bool _isInitialized = false;

  // Web 平台获取设备令牌 - 返回模拟令牌
  Future<void> getDeviceToken() async {
    if (!kIsWeb) {
      throw UnsupportedError('此实现仅适用于 Web 平台');
    }

    try {
      if (!_isInitialized) {
        print('Web 平台初始化 TokenUtil (不使用 Firebase)');

        // Web 平台使用模拟的设备标识
        Global.devicetoken =
            'web_device_token_${DateTime.now().millisecondsSinceEpoch}';

        _isInitialized = true;
        print('Web 平台 TokenUtil 初始化完成');
      }
    } catch (e) {
      print('Web 平台 TokenUtil 初始化失败: $e');
    }
  }

  // 处理推送消息 - Web 平台不支持
  Future<dynamic> onPush(String name, dynamic payload) async {
    print('Web 平台不支持推送消息处理: $name');
    return null;
  }

  // 处理深度链接导航
  Future<void> deeplinkNav(String deeplink) async {
    try {
      print('Web 平台深度链接导航: $deeplink');

      // 在 Web 平台上可以使用 window.location 进行导航
      // 这里暂时只打印日志
      if (deeplink.isNotEmpty) {
        // 可以在这里实现 Web 平台的路由导航逻辑
        print('导航到: $deeplink');
      }
    } catch (e) {
      print('Web 平台深度链接导航失败: $e');
    }
  }
}
