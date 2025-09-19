// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'activity.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Activity _$ActivityFromJson(Map<String, dynamic> json) =>
    Activity(
        json['actid'] as String,
        (json['peoplenum'] as num?)?.toInt(),
        json['createtime'] as String?,
        json['updatetime'] as String?,
        json['content'] as String,
        json['score'] as String?,
        json['actimagespath'] as String?,
        (json['status'] as num?)?.toInt(),
        json['user'] == null
            ? null
            : User.fromJson(json['user'] as Map<String, dynamic>),
        json['actcity'] as String?,
        json['actprovince'] as String?,
        json['coverimg'] as String?,
        json['coverimgwh'] as String,
        (json['likenum'] as num).toInt(),
        (json['collectionnum'] as num).toInt(),
        (json['startyear'] as num?)?.toInt(),
        (json['endyear'] as num?)?.toInt(),
        (json['commentnum'] as num?)?.toInt(),
        (json['currentpeoplenum'] as num?)?.toInt(),
        (json['mincost'] as num).toDouble(),
        (json['maxcost'] as num).toDouble(),
        json['address'] as String?,
        (json['lat'] as num?)?.toDouble(),
        (json['lng'] as num?)?.toDouble(),
        json['addresstitle'] as String?,
        (json['paytype'] as num?)?.toInt(),
        json['orderid'] as String?,
        json['goodpriceid'] as String?,
        (json['joinnum'] as num?)?.toInt(),
        (json['viewnum'] as num?)?.toInt(),
        (json['locked'] as num?)?.toInt(),
        json['goodPiceModel'] == null
            ? null
            : GoodPiceModel.fromJson(
                json['goodPiceModel'] as Map<String, dynamic>,
              ),
      )
      ..members = (json['members'] as List<dynamic>?)
          ?.map((e) => User.fromJson(e as Map<String, dynamic>))
          .toList()
      ..activityEvaluate = json['activityEvaluate'] == null
          ? null
          : ActivityEvaluate.fromJson(
              json['activityEvaluate'] as Map<String, dynamic>,
            );

Map<String, dynamic> _$ActivityToJson(Activity instance) => <String, dynamic>{
  'actid': instance.actid,
  'members': instance.members,
  'peoplenum': instance.peoplenum,
  'createtime': instance.createtime,
  'updatetime': instance.updatetime,
  'content': instance.content,
  'score': instance.score,
  'actimagespath': instance.actimagespath,
  'status': instance.status,
  'user': instance.user,
  'actcity': instance.actcity,
  'actprovince': instance.actprovince,
  'coverimg': instance.coverimg,
  'coverimgwh': instance.coverimgwh,
  'likenum': instance.likenum,
  'collectionnum': instance.collectionnum,
  'startyear': instance.startyear,
  'endyear': instance.endyear,
  'commentnum': instance.commentnum,
  'currentpeoplenum': instance.currentpeoplenum,
  'maxcost': instance.maxcost,
  'mincost': instance.mincost,
  'address': instance.address,
  'addresstitle': instance.addresstitle,
  'lat': instance.lat,
  'lng': instance.lng,
  'paytype': instance.paytype,
  'goodpriceid': instance.goodpriceid,
  'activityEvaluate': instance.activityEvaluate,
  'joinnum': instance.joinnum,
  'viewnum': instance.viewnum,
  'orderid': instance.orderid,
  'locked': instance.locked,
  'goodPiceModel': instance.goodPiceModel,
};
