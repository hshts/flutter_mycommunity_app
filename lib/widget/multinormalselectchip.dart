import 'package:flutter/material.dart';

class MyMultiNormalSelectChip extends StatefulWidget {
  /// 标签的list
  final List<String> dataList;

  /// 标签的list
  final List<String> selectList;
  final Function(List<String>) onSelectionChanged;

  const MyMultiNormalSelectChip(
    this.dataList, {
    super.key,
    required this.selectList,
    required this.onSelectionChanged,
  });

  @override
  _MyMultiNormalSelectChipState createState() =>
      _MyMultiNormalSelectChipState(selectList);
}

class _MyMultiNormalSelectChipState extends State<MyMultiNormalSelectChip> {
  List<String> selectList;

  _MyMultiNormalSelectChipState(this.selectList);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        selectList.isNotEmpty
            ? Padding(
                padding: EdgeInsets.only(left: 10, bottom: 10),
                child: Text(
                  "已选话题",
                  style: TextStyle(color: Colors.grey, fontSize: 13),
                ),
              )
            : Container(),
        Wrap(
          alignment: WrapAlignment.start,
          children: _buildselectedChoiceList(),
        ),
        Padding(
          padding: EdgeInsets.only(left: 10, bottom: 10, top: 10),
          child: Text(
            "热门话题",
            style: TextStyle(color: Colors.grey, fontSize: 13),
          ),
        ),
        SizedBox(
          height: 188,
          child: ListView(
            children: <Widget>[
              Wrap(
                alignment: WrapAlignment.start,
                children: _buildChoiceList(),
              ),
            ],
          ),
        ),
      ],
    );
  }

  ///创建标签
  List<Widget> _buildChoiceList() {
    List<Widget> choices = [];
    for (var item in widget.dataList) {
      choices.add(
        Container(
          margin: EdgeInsets.only(left: 10),
          child: ChoiceChip(
            label: Text(
              '#$item',
              style: TextStyle(
                fontSize: 14,
                color: Colors.black54,
                fontWeight: selectList.contains(item)
                    ? FontWeight.bold
                    : FontWeight.w100,
              ),
            ),
            shape: StadiumBorder(
              side: BorderSide(
                width: 1,
                color: Colors.black12,
                style: BorderStyle.solid,
              ),
            ),

            selected: selectList.contains(item),
            materialTapTargetSize: MaterialTapTargetSize.padded,
            selectedColor: Colors.white,
            backgroundColor: Colors.white,
            onSelected: (selected) {
              setState(() {
                if (selectList.contains(item)) {
                  selectList.remove(item);
                } else {
                  // if(selectList.length >= 1){
                  //   return;
                  // }
                  selectList.removeRange(0, selectList.length);
                  selectList.add(item);
                }
                widget.onSelectionChanged(selectList);
              });
            },
          ),
        ),
      );
    }
    return choices;
  }

  ///已选标签
  List<Widget> _buildselectedChoiceList() {
    List<Widget> choices = [];
    for (var item in selectList) {
      choices.add(
        Container(
          margin: EdgeInsets.only(left: 10),
          child: ChoiceChip(
            label: Text(
              '#$item x',
              style: TextStyle(
                fontSize: 14,
                color: Colors.black54,
                fontWeight: selectList.contains(item)
                    ? FontWeight.bold
                    : FontWeight.w100,
              ),
            ),
            shape: StadiumBorder(
              side: BorderSide(
                width: 1,
                color: Colors.black12,
                style: BorderStyle.solid,
              ),
            ),
            selected: selectList.contains(item),
            selectedColor: Colors.white,
            backgroundColor: Colors.white,
            onSelected: (selected) {
              setState(() {
                selectList.contains(item)
                    ? selectList.remove(item)
                    : selectList.add(item);
                widget.onSelectionChanged(selectList);
              });
            },
          ),
        ),
      );
    }
    return choices;
  }

  Widget selectedChoice() {
    return Column(
      children: <Widget>[
        Padding(
          padding: EdgeInsets.only(left: 10, bottom: 10),
          child: Text(
            "已选标签",
            style: TextStyle(color: Colors.grey, fontSize: 13),
          ),
        ),
        Wrap(alignment: WrapAlignment.start, children: _buildChoiceList()),
      ],
    );
  }
}
