///
/// [Author] Alex (https://github.com/AlexV525)
/// [Date] 2020/8/19 10:36
///
library;

import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

/// Progress Indicator. Used in loading data.
class PlatformProgressIndicator extends StatelessWidget {
  const PlatformProgressIndicator({
    super.key,
    this.strokeWidth = 4.0,
    this.radius = 10.0,
    this.size = 48.0,
    this.color,
    this.value,
    this.brightness,
  });

  final double strokeWidth;
  final double radius;
  final double size;
  final Color? color;
  final double? value;
  final Brightness? brightness;

  bool get isAppleOS => !kIsWeb && (Platform.isIOS || Platform.isMacOS);

  @override
  Widget build(BuildContext context) {
    return SizedBox.fromSize(
      size: Size.square(size),
      child: isAppleOS
          ? CupertinoTheme(
              data: CupertinoThemeData(
                brightness: brightness ?? Brightness.dark,
              ),
              child: CupertinoActivityIndicator(radius: radius),
            )
          : CircularProgressIndicator(
              strokeWidth: strokeWidth,
              valueColor: color != null
                  ? AlwaysStoppedAnimation<Color>(color!)
                  : null,
              value: value,
            ),
    );
  }
}
