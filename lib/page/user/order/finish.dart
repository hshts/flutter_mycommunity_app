import 'package:flutter/material.dart';

import '../../../model/order.dart';
import '../../../model/im/grouprelation.dart';
import '../../../widget/circle_headimage.dart';
import '../../../widget/captcha/block_puzzle_captcha.dart';
import '../../../service/activity.dart';
import '../../../service/userservice.dart';
import '../../../model/grouppurchase/goodpice_model.dart';
import '../../../service/gpservice.dart';
import '../../../util/showmessage_util.dart';
import '../../../util/imhelper_util.dart';
import '../../../global.dart';

class MyOrderFinish extends StatefulWidget {
  const MyOrderFinish({super.key});

  @override
  _MyOrderFinishState createState() => _MyOrderFinishState();
}

class _MyOrderFinishState extends State<MyOrderFinish> {
  final UserService _userService = UserService();
  final ActivityService _activityService = ActivityService();
  List<Order> _orderList = [];
  int _pagestatus = 0; //简单处理载入状态
  final ImHelper _imhelper = ImHelper();
  final GPService _gpservice = GPService();

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _getMyOrder();
  }

  Future<void> _getMyOrder() async {
    _orderList = await _userService.getMyOrderFinish(
      Global.profile.user!.token!,
      Global.profile.user!.uid,
      (String statecode, String error) {
        ShowMessage.showToast(error);
      },
    );
    _pagestatus = 1;
    if (mounted) {
      setState(() {});
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios, size: 18),
          color: Colors.black,
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        title: Text(
          '待收货的订单',
          textAlign: TextAlign.center,
          style: TextStyle(color: Colors.black, fontSize: 16),
        ),
        centerTitle: true,
      ),
      body: Container(
        margin: EdgeInsets.all(5.0),
        child: _pagestatus == 0
            ? Center(
                child: CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation(Global.profile.backColor),
                ),
              )
            : _buildOrderList(),
      ),
    );
  }

  Widget _buildOrderList() {
    Widget ret = SizedBox.shrink();
    List<Widget> lists = [];

    if (_orderList.isNotEmpty) {
      for (var e in _orderList) {
        lists.add(
          Container(
            padding: EdgeInsets.only(left: 10, right: 10, top: 10),
            decoration: BoxDecoration(
              //背景
              color: Colors.white,
              borderRadius: BorderRadius.all(Radius.circular(4.0)),
              //设置四周边框
            ),
            child: Column(
              children: [
                SizedBox(height: 12),
                InkWell(
                  child: SizedBox(
                    height: 109,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              e.goodpricepic != ""
                                  ? ClipRRectOhterHeadImageContainer(
                                      imageUrl: e.goodpricepic,
                                      width: 109,
                                      height: 109,
                                      cir: 5,
                                    )
                                  : SizedBox.shrink(),
                              SizedBox(width: 10),
                              Expanded(
                                child: SizedBox(
                                  height: 109,
                                  child: Column(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Expanded(
                                        child: Text(
                                          e.goodpricetitle,
                                          overflow: TextOverflow.ellipsis,
                                          maxLines: 3,
                                          style: TextStyle(
                                            color: Colors.black87,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ),
                                      Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceBetween,
                                        children: [
                                          Text(
                                            '下单时间: ${e.createtime}',
                                            style: TextStyle(
                                              color: Colors.black45,
                                              fontSize: 12,
                                            ),
                                          ),
                                        ],
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        Column(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            Row(
                              children: [
                                Text(
                                  "x",
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.black45,
                                  ),
                                ),
                                Text(
                                  e.productnum.toString(),
                                  style: TextStyle(
                                    fontSize: 14,
                                    color: Colors.black45,
                                  ),
                                ),
                              ],
                            ),
                            Row(
                              children: [
                                Text("￥", style: TextStyle(fontSize: 12)),
                                Text(
                                  e.gpprice.toString(),
                                  style: TextStyle(fontSize: 14),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  onTap: () {
                    _gotoGoodPrice(e.goodpriceid);
                  },
                ),
                SizedBox(height: 9),
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.all(Radius.circular(9)),
                        ),
                      ),
                      child: Text('联系客服', style: TextStyle(fontSize: 12)),
                      onPressed: () async {
                        _telCustomerCare("", e.touid);
                      },
                    ),
                    SizedBox(width: 10),
                    OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.all(Radius.circular(9)),
                        ),
                      ),
                      child: Text('我要退货', style: TextStyle(fontSize: 12)),
                      onPressed: () async {
                        await _asked(e.gpactid!, e.orderid!);
                      },
                    ),
                    SizedBox(width: 10),
                    TextButton(
                      style: TextButton.styleFrom(
                        backgroundColor: Global.profile.backColor,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.all(Radius.circular(9)),
                        ),
                      ),
                      child: Text(
                        '确定收货',
                        style: TextStyle(color: Colors.white, fontSize: 12),
                      ),
                      onPressed: () async {
                        await _askedConfirm(e.gpactid!, e.orderid!);
                      },
                    ),
                  ],
                ),
                SizedBox(height: 9),
              ],
            ),
          ),
        );
        lists.add(Container(height: 6, color: Colors.grey.shade200));
      }

      lists.add(SizedBox(height: 10));

      ret = ListView(children: lists);
    } else {
      ret = Center(
        child: Text(
          '没有发现待确认的订单',
          style: TextStyle(color: Colors.black54, fontSize: 14),
        ),
      );
    }

    return ret;
  }

  Future<void> _gotoGoodPrice(String goodpriceid) async {
    GoodPiceModel? goodprice = await _gpservice.getGoodPriceInfo(goodpriceid);
    if (goodprice != null) {
      Navigator.pushNamed(
        context,
        '/GoodPriceInfo',
        arguments: {"goodprice": goodprice},
      );
    }
  }

  Future<void> _asked(String gpactid, String orderid) async {
    return showDialog<Null>(
      context: context,
      barrierDismissible: true,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(
            '如果商家已经发货可能无法完成退款，确定要退货吗?',
            style: TextStyle(fontSize: 17.0),
          ),
          actions: <Widget>[
            TextButton(
              child: Text('确定'),
              onPressed: () async {
                Navigator.of(context).pop();
                bool ret = await _activityService.refundActivityOrder(
                  gpactid,
                  Global.profile.user!.uid,
                  Global.profile.user!.token!,
                  orderid,
                  (String statusCode, String msg) {
                    ShowMessage.cancel();
                    ShowMessage.showToast(msg);
                  },
                );
                if (ret) {
                  ShowMessage.showToast("退货成功");
                  await _imhelper.updateUserOrder(1); //已确认数量-1
                  _getMyOrder();
                }
              },
            ),
            TextButton(
              child: Text('取消'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  Future<void> _askedConfirm(String gpactid, String orderid) async {
    return showDialog<Null>(
      context: context,
      barrierDismissible: true,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('确定已经收到商品了吗?', style: TextStyle(fontSize: 17.0)),
          actions: <Widget>[
            TextButton(
              child: Text('确定'),
              onPressed: () async {
                Navigator.of(context).pop();
                bool ret = await _activityService.activityFundTransfer(
                  gpactid,
                  Global.profile.user!.uid,
                  Global.profile.user!.token!,
                  orderid,
                  (String statusCode, String msg) {
                    ShowMessage.cancel();
                    ShowMessage.showToast(msg);
                  },
                );
                if (ret) {
                  ShowMessage.showToast("确定成功");
                  await _imhelper.updateUserOrder(1); //已确认数量-1
                  _getMyOrder();
                }
              },
            ),
            TextButton(
              child: Text('取消'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  Future<void> _telCustomerCare(String vcode, int touid) async {
    String timelineId = "";
    //获取客服
    int uid = Global.profile.user!.uid;
    if (uid == touid) {
      ShowMessage.showToast("不能联系自己");
      return;
    }

    if (uid > touid) {
      timelineId = touid.toString() + uid.toString();
    } else {
      timelineId = uid.toString() + touid.toString();
    }
    GroupRelation? groupRelation = await _imhelper.getGroupRelationByGroupid(
      uid,
      timelineId,
    );
    groupRelation ??= await _userService.joinSingleCustomer(
      timelineId,
      uid,
      touid,
      Global.profile.user!.token!,
      vcode,
      (String statusCode, String msg) {
        if (statusCode == "-1008") {
          _loadingBlockPuzzle(context, touid: touid);
          return;
        } else {
          ShowMessage.showToast(msg);
        }
      },
      isCustomer: 1,
    );
    if (groupRelation != null) {
      List<GroupRelation> groupRelations = [];
      groupRelations.add(groupRelation);
      int ret = await _imhelper.saveGroupRelation(groupRelations);
      if (Global.isInDebugMode) {
        print("保存本地是否成功：-----------------------------------");
        print(groupRelations[0].group_name1);
        //print(ret);
      }
      if (ret > 0) {
        Navigator.pushNamed(
          context,
          '/MyMessage',
          arguments: {"GroupRelation": groupRelation},
        );
      }
    }
  }

  //滑动拼图
  void _loadingBlockPuzzle(
    BuildContext context, {
    barrierDismissible = true,
    required int touid,
  }) {
    showDialog<Null>(
      context: this.context,
      barrierDismissible: barrierDismissible,
      builder: (_) {
        return BlockPuzzleCaptchaPage(
          onSuccess: (v) {
            _telCustomerCare(v, touid);
          },
          onFail: () {},
        );
      },
    );
  }
}
