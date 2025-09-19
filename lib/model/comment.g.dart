// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'comment.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Comment _$CommentFromJson(Map<String, dynamic> json) =>
    Comment(
        (json['commentid'] as num?)?.toInt(),
        json['actid'] as String?,
        json['user'] == null
            ? null
            : User.fromJson(json['user'] as Map<String, dynamic>),
        json['content'] as String?,
        (json['likenum'] as num?)?.toInt(),
        json['createtime'] as String?,
        (json['likeuid'] as num).toInt(),
      )
      ..replys = (json['replys'] as List<dynamic>?)
          ?.map((e) => CommentReply.fromJson(e as Map<String, dynamic>))
          .toList();

Map<String, dynamic> _$CommentToJson(Comment instance) => <String, dynamic>{
  'commentid': instance.commentid,
  'actid': instance.actid,
  'user': instance.user,
  'content': instance.content,
  'likenum': instance.likenum,
  'createtime': instance.createtime,
  'replys': instance.replys,
  'likeuid': instance.likeuid,
};
