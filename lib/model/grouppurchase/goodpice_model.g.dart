// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'goodpice_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

GoodPiceModel _$GoodPiceModelFromJson(Map<String, dynamic> json) =>
    GoodPiceModel(
      goodpriceid: json['goodpriceid'] as String? ?? '',
      title: json['title'] as String? ?? '',
      content: json['content'] as String? ?? '',
      category: (json['category'] as num?)?.toInt() ?? 0,
      brand: json['brand'] as String? ?? '',
      discount: (json['discount'] as num?)?.toDouble() ?? 1.0,
      endtime: json['endtime'] as String? ?? '',
      createtime: json['createtime'] as String? ?? '',
      albumpics: json['albumpics'] as String? ?? '',
      pic: json['pic'] as String? ?? '',
      collectionnum: (json['collectionnum'] as num?)?.toInt() ?? 0,
      sellnum: (json['sellnum'] as num?)?.toInt() ?? 0,
      province: json['province'] as String? ?? '',
      city: json['city'] as String? ?? '',
      uid: (json['uid'] as num?)?.toInt() ?? 0,
      username: json['username'] as String? ?? '',
      profilepicture: json['profilepicture'] as String? ?? '',
      likenum: (json['likenum'] as num?)?.toInt() ?? 0,
      unlikenum: (json['unlikenum'] as num?)?.toInt() ?? 0,
      commentnum: (json['commentnum'] as num?)?.toInt() ?? 0,
      productstatus: (json['productstatus'] as num?)?.toInt() ?? 1,
      satisfactionrate: (json['satisfactionrate'] as num?)?.toDouble() ?? 0.0,
      activitycount: (json['activitycount'] as num?)?.toInt() ?? 0,
      tag: json['tag'] as String? ?? '',
      msg: json['msg'] as String? ?? '',
      addresstitle: json['addresstitle'] as String? ?? '',
      address: json['address'] as String? ?? '',
      lat: (json['lat'] as num?)?.toDouble() ?? 0.0,
      lng: (json['lng'] as num?)?.toDouble() ?? 0.0,
      mincost: (json['mincost'] as num?)?.toDouble() ?? 0.0,
      maxcost: (json['maxcost'] as num?)?.toDouble() ?? 0.0,
      evaluatenum: (json['evaluatenum'] as num?)?.toInt() ?? 0,
    );

Map<String, dynamic> _$GoodPiceModelToJson(GoodPiceModel instance) =>
    <String, dynamic>{
      'goodpriceid': instance.goodpriceid,
      'title': instance.title,
      'content': instance.content,
      'category': instance.category,
      'brand': instance.brand,
      'discount': instance.discount,
      'endtime': instance.endtime,
      'createtime': instance.createtime,
      'albumpics': instance.albumpics,
      'pic': instance.pic,
      'sellnum': instance.sellnum,
      'collectionnum': instance.collectionnum,
      'province': instance.province,
      'city': instance.city,
      'uid': instance.uid,
      'username': instance.username,
      'profilepicture': instance.profilepicture,
      'likenum': instance.likenum,
      'unlikenum': instance.unlikenum,
      'commentnum': instance.commentnum,
      'productstatus': instance.productstatus,
      'satisfactionrate': instance.satisfactionrate,
      'activitycount': instance.activitycount,
      'tag': instance.tag,
      'msg': instance.msg,
      'addresstitle': instance.addresstitle,
      'address': instance.address,
      'lat': instance.lat,
      'lng': instance.lng,
      'mincost': instance.mincost,
      'maxcost': instance.maxcost,
      'evaluatenum': instance.evaluatenum,
    };
