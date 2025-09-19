// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'goodpice_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

GoodPiceModel _$GoodPiceModelFromJson(Map<String, dynamic> json) =>
    GoodPiceModel(
      json['goodpriceid'] as String,
      json['title'] as String,
      json['content'] as String,
      (json['category'] as num).toInt(),
      json['brand'] as String,
      (json['discount'] as num).toDouble(),
      json['endtime'] as String,
      json['createtime'] as String,
      json['albumpics'] as String,
      json['pic'] as String,
      (json['collectionnum'] as num).toInt(),
      (json['sellnum'] as num).toInt(),
      json['province'] as String,
      json['city'] as String,
      (json['uid'] as num).toInt(),
      json['username'] as String,
      json['profilepicture'] as String,
      (json['likenum'] as num).toInt(),
      (json['unlikenum'] as num).toInt(),
      (json['commentnum'] as num).toInt(),
      (json['productstatus'] as num).toInt(),
      (json['satisfactionrate'] as num).toDouble(),
      (json['activitycount'] as num).toInt(),
      json['tag'] as String,
      json['msg'] as String,
      json['addresstitle'] as String,
      json['address'] as String,
      (json['lat'] as num).toDouble(),
      (json['lng'] as num).toDouble(),
      (json['mincost'] as num).toDouble(),
      (json['maxcost'] as num).toDouble(),
      (json['evaluatenum'] as num).toInt(),
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
