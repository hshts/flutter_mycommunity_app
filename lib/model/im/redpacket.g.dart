// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'redpacket.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

RedPacketModel _$RedPacketModelFromJson(Map<String, dynamic> json) =>
    RedPacketModel(
      json['redpacketid'] as String,
      (json['uid'] as num).toInt(),
      (json['amount'] as num).toDouble(),
      (json['redpackettype'] as num).toInt(),
      (json['redpacketstatus'] as num).toInt(),
      (json['redpacketnum'] as num).toInt(),
      json['createtime'] as String,
      json['timeline_id'] as String,
      json['content'] as String,
      json['username'] as String,
      json['profilepicture'] as String,
      json['original_order_id'] as String,
      (json['touid'] as num).toInt(),
      json['tocreatetime'] as String,
      (json['tofund'] as num).toDouble(),
      json['isexpire'] as bool,
      (json['currentnum'] as num).toInt(),
    );

Map<String, dynamic> _$RedPacketModelToJson(RedPacketModel instance) =>
    <String, dynamic>{
      'redpacketid': instance.redpacketid,
      'uid': instance.uid,
      'amount': instance.amount,
      'redpackettype': instance.redpackettype,
      'redpacketstatus': instance.redpacketstatus,
      'redpacketnum': instance.redpacketnum,
      'createtime': instance.createtime,
      'timeline_id': instance.timeline_id,
      'content': instance.content,
      'username': instance.username,
      'profilepicture': instance.profilepicture,
      'original_order_id': instance.original_order_id,
      'tofund': instance.tofund,
      'touid': instance.touid,
      'tocreatetime': instance.tocreatetime,
      'isexpire': instance.isexpire,
      'currentnum': instance.currentnum,
    };
