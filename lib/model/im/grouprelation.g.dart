// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'grouprelation.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

GroupRelation _$GroupRelationFromJson(Map<String, dynamic> json) =>
    GroupRelation(
        (json['id'] as num?)?.toInt(),
        json['timeline_id'] as String,
        (json['readindex'] as num?)?.toInt(),
        (json['unreadcount'] as num).toInt(),
        json['group_name1'] as String?,
        json['clubicon'] as String?,
        json['name'] as String?,
        json['newmsgtime'],
        json['newmsg'],
        (json['timelineType'] as num?)?.toInt(),
        (json['relationtype'] as num?)?.toInt(),
        (json['status'] as num?)?.toInt(),
        (json['locked'] as num?)?.toInt(),
        json['memberupdatetime'] as String?,
        (json['isnotservice'] as num?)?.toInt(),
        json['source_id'] as String?,
        json['goodpriceid'] as String,
      )
      ..uid = (json['uid'] as num?)?.toInt()
      ..jointime = json['jointime'] as String?
      ..istop = (json['istop'] as num?)?.toInt()
      ..oldmemberupdatetime = json['oldmemberupdatetime'] as String?;

Map<String, dynamic> _$GroupRelationToJson(GroupRelation instance) =>
    <String, dynamic>{
      'id': instance.id,
      'timeline_id': instance.timeline_id,
      'uid': instance.uid,
      'jointime': instance.jointime,
      'readindex': instance.readindex,
      'unreadcount': instance.unreadcount,
      'group_name1': instance.group_name1,
      'clubicon': instance.clubicon,
      'name': instance.name,
      'newmsgtime': instance.newmsgtime,
      'newmsg': instance.newmsg,
      'timelineType': instance.timelineType,
      'istop': instance.istop,
      'relationtype': instance.relationtype,
      'status': instance.status,
      'locked': instance.locked,
      'memberupdatetime': instance.memberupdatetime,
      'oldmemberupdatetime': instance.oldmemberupdatetime,
      'isnotservice': instance.isnotservice,
      'source_id': instance.source_id,
      'goodpriceid': instance.goodpriceid,
    };
