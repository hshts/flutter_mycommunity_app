import 'package:flutter/material.dart';

import '../../widget/my_divider.dart';

class ReportActivity extends StatefulWidget {
  final String actid;
  final int sourcetype;
  final int touid;
  final Object? arguments;

  ReportActivity({super.key, this.arguments})
    : actid = arguments != null ? (arguments as Map)["actid"] ?? "" : "",
      sourcetype = arguments != null
          ? (arguments as Map)["sourcetype"] ?? 0
          : 0,
      touid = arguments != null ? (arguments as Map)["touid"] ?? 0 : 0;

  @override
  _ReportActivityState createState() => _ReportActivityState();
}

class _ReportActivityState extends State<ReportActivity> {
  final List<String> myList = ["疑似欺诈", "低俗引起不适的图片", "其他类型"];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, color: Colors.black, size: 18),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        title: Text(
          '选择举报原因',
          style: TextStyle(color: Colors.black, fontSize: 16),
        ),
        centerTitle: true,
      ),
      body: ListView.separated(
        scrollDirection: Axis.vertical,
        separatorBuilder: (BuildContext context, int index) {
          return MyDivider();
        },
        itemBuilder: (BuildContext context, int position) {
          return Container(
            color: Colors.white,
            child: ListTile(
              trailing: Icon(Icons.navigate_next),
              title: Text(
                myList[position],
                style: TextStyle(color: Colors.black87, fontSize: 14),
              ),
              onTap: () {
                if (position == 0) {
                  Navigator.pushNamed(
                    context,
                    '/FraudActivity',
                    arguments: {
                      "actid": widget.actid,
                      "sourcetype": widget.sourcetype,
                      "touid": widget.touid,
                    },
                  );
                }
                if (position == 1) {
                  Navigator.pushNamed(
                    context,
                    '/ReportImageActivity',
                    arguments: {
                      "actid": widget.actid,
                      "sourcetype": widget.sourcetype,
                      "touid": widget.touid,
                    },
                  );
                }
                if (position == 2) {
                  Navigator.pushNamed(
                    context,
                    '/ReportOtherActivity',
                    arguments: {
                      "actid": widget.actid,
                      "sourcetype": widget.sourcetype,
                      "touid": widget.touid,
                    },
                  );
                }
              },
            ),
          );
        },
        itemCount: myList.length,
      ),
      bottomNavigationBar: InkWell(
        child: Container(
          color: Colors.white,
          height: 50,
          alignment: Alignment.center,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.assignment, color: Colors.blue, size: 19),
              SizedBox(width: 10),
              Text('我的举报', style: TextStyle(color: Colors.blue, fontSize: 14)),
            ],
          ),
        ),
        onTap: () {
          Navigator.pushNamed(
            context,
            '/MyReportList',
            arguments: {"isAppbar": true},
          );
        },
      ),
    );
  }
}
