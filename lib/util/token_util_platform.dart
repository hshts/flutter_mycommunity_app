// 平台感知的 TokenUtil 导入
// 根据平台自动选择合适的实现

// 条件导入：Web 平台使用 token_util_web.dart，其他平台使用 token_util.dart
export 'token_util_stub.dart'
    if (dart.library.html) 'token_util_web.dart'
    if (dart.library.io) 'token_util.dart';
