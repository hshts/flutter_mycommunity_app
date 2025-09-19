// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'follow.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Follow _$FollowFromJson(Map<String, dynamic> json) => Follow(
  (json['uid'] as num?)?.toInt(),
  json['username'] as String?,
  json['profilepicture'] as String?,
  (json['isread'] as num?)?.toInt(),
  (json['fans'] as num?)?.toInt(),
  json['createtime'] as String?,
  (json['id'] as num?)?.toInt(),
  (json['type'] as num?)?.toInt(),
);

Map<String, dynamic> _$FollowToJson(Follow instance) => <String, dynamic>{
  'id': instance.id,
  'uid': instance.uid,
  'fans': instance.fans,
  'username': instance.username,
  'profilepicture': instance.profilepicture,
  'isread': instance.isread,
  'createtime': instance.createtime,
  'type': instance.type,
};
