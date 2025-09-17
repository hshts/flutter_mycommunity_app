import 'package:flutter/material.dart';

class MessageDialog extends Dialog {
  final Widget? title;
  final Widget? message;
  final String? negativeText;
  final String? positiveText;
  final void Function()? onCloseEvent;
  final void Function()? onPositivePressEvent;
  final double? containerHeight;

  const MessageDialog({
    super.key,
    @required this.title,
    @required this.message,
    this.negativeText,
    this.positiveText,
    this.onPositivePressEvent,
    @required this.onCloseEvent,
    @required this.containerHeight,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(15.0),
      child: Material(
        type: MaterialType.transparency,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
              decoration: ShapeDecoration(
                color: Color(0xffffffff),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(8.0)),
                ),
              ),
              margin: const EdgeInsets.all(12.0),
              child: Column(
                children: <Widget>[
                  Padding(
                    padding: const EdgeInsets.all(10.0),
                    child: Stack(
                      alignment: AlignmentDirectional.centerEnd,
                      children: <Widget>[
                        Center(child: title),
                        GestureDetector(
                          onTap: onCloseEvent,
                          child: Padding(
                            padding: const EdgeInsets.all(5.0),
                            child: Icon(Icons.close, color: Color(0xffe0e0e0)),
                          ),
                        ),
                      ],
                    ),
                  ),
                  Container(color: Color(0xffe0e0e0), height: 1.0),
                  Container(
                    constraints: BoxConstraints(minHeight: containerHeight!),
                    child: Padding(
                      padding: const EdgeInsets.all(12.0),
                      child: IntrinsicHeight(child: message),
                    ),
                  ),
                  _buildBottomButtonGroup(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBottomButtonGroup() {
    var widgets = <Widget>[];
    if (negativeText != null && negativeText!.isNotEmpty) {
      widgets.add(_buildBottomCancelButton());
    }
    if (positiveText != null && positiveText!.isNotEmpty) {
      widgets.add(_buildBottomPositiveButton());
    }
    return Flex(direction: Axis.horizontal, children: widgets);
  }

  Widget _buildBottomCancelButton() {
    return Flexible(
      fit: FlexFit.tight,
      child: TextButton(
        onPressed: onCloseEvent,
        child: Text(
          negativeText!,
          style: TextStyle(fontSize: 16.0, color: Colors.black),
        ),
      ),
    );
  }

  Widget _buildBottomPositiveButton() {
    return Flexible(
      fit: FlexFit.tight,
      child: TextButton(
        onPressed: onPositivePressEvent,
        child: Text(
          positiveText!,
          style: TextStyle(color: Colors.red, fontSize: 16.0),
        ),
      ),
    );
  }
}
