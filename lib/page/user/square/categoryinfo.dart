import 'package:flutter/material.dart';
import 'package:rxdart/rxdart.dart';

import '../../../service/commonjson.dart';
import '../../../widget/multinormalselectchip.dart';
import '../../../global.dart';

class CategoryInfo extends StatefulWidget {
  final List<String> initialSelectList;

  CategoryInfo(this.initialSelectList, {super.key});

  @override
  _CategoryInfoState createState() => _CategoryInfoState();
}

class _CategoryInfoState extends State<CategoryInfo> {
  final CommonJSONService _commonJSONService = CommonJSONService();
  final controller = TextEditingController();
  final subject = PublishSubject<String>();

  List<String> _selectList = [];
  List<String> allList = [];
  String _newtype = "";

  @override
  void initState() {
    super.initState();
    _selectList = List.from(widget.initialSelectList);
    _commonJSONService.getActivityTypes(_getList);
    subject.stream
        .debounceTime(Duration(milliseconds: 1000))
        .listen(_textChanged);
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      bottomNavigationBar: buildLoginButton(context),
      body: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.only(
            topLeft: Radius.circular(9.0),
            topRight: Radius.circular(9.0),
          ),
        ),
        child: ListView(children: <Widget>[buildActivityType()]),
      ),
    );
  }

  Container buildLoginButton(BuildContext context) {
    return Container(
      margin: EdgeInsets.all(10),
      height: 40,
      child: TextButton(
        style: TextButton.styleFrom(
          backgroundColor: Global.profile.backColor,
          foregroundColor: Global.profile.fontColor,
          shape: RoundedRectangleBorder(
            side: BorderSide.none,
            borderRadius: BorderRadius.all(Radius.circular(9)),
          ),
        ),
        child: Text('完成'),
        onPressed: () async {
          String types = "";

          for (int i = 0; i < _selectList.length; i++) {
            types += "${_selectList[i]},";
          }
          if (types.isNotEmpty) {
            types = types.substring(0, types.length - 1);
          }

          Navigator.of(context).pop(types);
        },
      ),
    );
  }

  //活动标签
  Widget buildActivityType() {
    return Container(
      margin: EdgeInsets.only(top: 15),
      child: MyMultiNormalSelectChip(
        allList,
        selectList: _selectList,
        onSelectionChanged: (selectedList) {
          setState(() {
            _selectList = selectedList;
          });
        },
      ),
    );
  }

  //搜索框
  Widget buildSearch() {
    return Padding(
      padding: EdgeInsets.only(left: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          SizedBox(width: 5.0),
          Text('#', style: TextStyle(color: Colors.grey)),
          Expanded(
            child: Container(
              alignment: Alignment.center,
              child: TextField(
                onChanged: (val) => (subject.add(val)),
                style: TextStyle(fontSize: 14),
                controller: controller,
                decoration: InputDecoration(
                  contentPadding: EdgeInsets.only(top: 0.0),
                  hintText: '添加话题',
                  border: InputBorder.none,
                  hintStyle: TextStyle(fontSize: 14.0), //设置提示文字样式
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _textChanged(String keyword) {
    _newtype = keyword;
    _commonJSONService.getActivityTypesByName(_getList, keyword);
  }

  void _getList(Map<String, dynamic> data) {
    List categoryTypes = [];
    if (data["data"] != null) {
      allList.clear();
      categoryTypes = data["data"];
      categoryTypes.map((item) {
        allList.add(item['typename'] as String);
      }).toList();
      if (allList.isEmpty) {
        allList.add(_newtype);
      }
      setState(() {});
    }
  }
}
