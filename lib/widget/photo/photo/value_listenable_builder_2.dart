///
/// [Author] Alex (https://github.com/AlexV525)
/// [Date] 2021-03-27 18:53
///
library;

import 'package:flutter/material.dart';

class ValueListenableBuilder2<A, B> extends StatelessWidget {
  const ValueListenableBuilder2({
    super.key,
    required this.firstNotifier,
    required this.secondNotifier,
    required this.builder,
    this.child,
  });

  final ValueNotifier<A> firstNotifier;
  final ValueNotifier<B> secondNotifier;
  final Widget Function(BuildContext, A, B, Widget?) builder;
  final Widget? child;

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<A>(
      valueListenable: firstNotifier,
      builder: (_, A first, __) => ValueListenableBuilder<B>(
        valueListenable: secondNotifier,
        builder: (BuildContext context, B second, Widget? w) {
          return builder(context, first, second, w);
        },
        child: child,
      ),
    );
  }
}
