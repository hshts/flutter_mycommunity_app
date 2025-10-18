// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'moment.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Moment _$MomentFromJson(Map<String, dynamic> json) => Moment(
  json['momentid'] == null ? '' : Moment._momentIdFromJson(json['momentid']),
  json['content'] as String? ?? '',
  json['images'] as String? ?? '',
  json['createtime'] as String? ?? '',
  (json['commentcount'] as num?)?.toInt() ?? 0,
  (json['likenum'] as num?)?.toInt() ?? 0,
  json['user'] == null
      ? null
      : User.fromJson(json['user'] as Map<String, dynamic>),
  json['voice'] as String? ?? '',
  json['coverimgwh'] as String? ?? '',
  json['category'] as String? ?? '',
)..islike = json['islike'] as bool? ?? false;

Map<String, dynamic> _$MomentToJson(Moment instance) => <String, dynamic>{
  'momentid': instance.momentid,
  'content': instance.content,
  'images': instance.images,
  'createtime': instance.createtime,
  'commentcount': instance.commentcount,
  'likenum': instance.likenum,
  'voice': instance.voice,
  'coverimgwh': instance.coverimgwh,
  'category': instance.category,
  'user': instance.user,
  'islike': instance.islike,
};
