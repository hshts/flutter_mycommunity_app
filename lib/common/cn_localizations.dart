import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

class ChineseCupertinoLocalizations implements CupertinoLocalizations {
  final materialDelegate = GlobalMaterialLocalizations.delegate;
  final widgetsDelegate = GlobalWidgetsLocalizations.delegate;
  final local = const Locale('zh');

  late MaterialLocalizations ml;

  Future init() async {
    ml = await materialDelegate.load(local);
    print(ml.pasteButtonLabel);
  }

  @override
  String get alertDialogLabel => ml.alertDialogLabel;

  @override
  String get anteMeridiemAbbreviation => ml.anteMeridiemAbbreviation;

  @override
  String get copyButtonLabel => ml.copyButtonLabel;

  @override
  String get cutButtonLabel => ml.cutButtonLabel;

  @override
  DatePickerDateOrder get datePickerDateOrder => DatePickerDateOrder.mdy;

  @override
  DatePickerDateTimeOrder get datePickerDateTimeOrder =>
      DatePickerDateTimeOrder.date_time_dayPeriod;

  @override
  String datePickerDayOfMonth(int dayIndex, [int? monthIndex]) {
    return dayIndex.toString();
  }

  @override
  String datePickerHour(int hour) {
    return hour.toString().padLeft(2, "0");
  }

  @override
  String datePickerHourSemanticsLabel(int hour) {
    return "$hour" + "时";
  }

  @override
  String datePickerMediumDate(DateTime date) {
    return ml.formatMediumDate(date);
  }

  @override
  String datePickerMinute(int minute) {
    return minute.toString().padLeft(2, '0');
  }

  @override
  String datePickerMinuteSemanticsLabel(int minute) {
    return "$minute" + "分";
  }

  @override
  String datePickerMonth(int monthIndex) {
    return "$monthIndex";
  }

  @override
  String datePickerYear(int yearIndex) {
    return yearIndex.toString();
  }

  @override
  String get pasteButtonLabel => ml.pasteButtonLabel;

  @override
  String get postMeridiemAbbreviation => ml.postMeridiemAbbreviation;

  @override
  String get selectAllButtonLabel => ml.selectAllButtonLabel;

  @override
  String timerPickerHour(int hour) {
    return hour.toString().padLeft(2, "0");
  }

  @override
  String timerPickerHourLabel(int hour) {
    return "$hour".toString().padLeft(2, "0") + "时";
  }

  @override
  String timerPickerMinute(int minute) {
    return minute.toString().padLeft(2, "0");
  }

  @override
  String timerPickerMinuteLabel(int minute) {
    return minute.toString().padLeft(2, "0") + "分";
  }

  @override
  String timerPickerSecond(int second) {
    return second.toString().padLeft(2, "0");
  }

  @override
  String timerPickerSecondLabel(int second) {
    return second.toString().padLeft(2, "0") + "秒";
  }

  static const LocalizationsDelegate<CupertinoLocalizations> delegate =
      _ChineseDelegate();

  static Future<CupertinoLocalizations> load(Locale locale) async {
    var localizaltions = ChineseCupertinoLocalizations();
    await localizaltions.init();
    return SynchronousFuture<CupertinoLocalizations>(localizaltions);
  }

  @override
  String get modalBarrierDismissLabel => ml.modalBarrierDismissLabel;

  @override
  String tabSemanticsLabel({int? tabIndex, int? tabCount}) {
    return ml.tabLabel(tabIndex: tabIndex ?? 0, tabCount: tabCount ?? 0);
  }

  @override
  String get todayLabel => "今天"; // 直接提供中文文本，因为ml.todayLabel不存在

  @override
  String get searchTextFieldPlaceholderLabel => ml.searchFieldLabel;

  @override
  List<String> get timerPickerHourLabels => const <String>['时'];

  @override
  List<String> get timerPickerMinuteLabels => const <String>['分'];

  @override
  List<String> get timerPickerSecondLabels => const <String>['秒'];

  @override
  String datePickerStandaloneMonth(int monthIndex) {
    return "$monthIndex月";
  }

  @override
  String get backButtonLabel => ml.backButtonTooltip;

  @override
  String get cancelButtonLabel => ml.cancelButtonLabel;

  @override
  String get clearButtonLabel => ml.clearButtonTooltip;

  @override
  String get closeButtonLabel => ml.closeButtonTooltip;

  @override
  String get collapseButtonLabel => "收起"; // 直接提供中文文本

  @override
  String get expandButtonLabel => "展开"; // 直接提供中文文本

  @override
  String get lookUpButtonLabel => "查询";

  @override
  String get menuButtonLabel => ml.showMenuTooltip;

  @override
  String get shareButtonLabel => "分享";

  @override
  String get menuDismissLabel => "关闭菜单";

  @override
  String get noSpellCheckReplacementsLabel => "未找到替换项";

  @override
  String get searchWebButtonLabel => "网页搜索";
}

class _ChineseDelegate extends LocalizationsDelegate<CupertinoLocalizations> {
  const _ChineseDelegate();

  @override
  bool isSupported(Locale locale) {
    return locale.languageCode == 'zh';
  }

  @override
  Future<CupertinoLocalizations> load(Locale locale) {
    return ChineseCupertinoLocalizations.load(locale);
  }

  @override
  bool shouldReload(LocalizationsDelegate<CupertinoLocalizations> old) {
    return false;
  }
}
