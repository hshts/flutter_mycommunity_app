// TokenUtil 接口定义
// 为条件导入提供通用接口

abstract class TokenUtil {
  factory TokenUtil() {
    throw UnsupportedError('平台特定实现缺失');
  }

  Future<void> getDeviceToken();
  Future<dynamic> onPush(String name, dynamic payload);
  Future<void> deeplinkNav(String deeplink);
}
