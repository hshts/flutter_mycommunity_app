// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'profile.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Profile _$ProfileFromJson(Map<String, dynamic> json) =>
    Profile(
        user: json['user'] == null
            ? null
            : User.fromJson(json['user'] as Map<String, dynamic>),
        backColorval: (json['backColorval'] as num?)?.toInt() ?? 0xffff2442,
        fontColorval: (json['fontColorval'] as num?)?.toInt() ?? 0xFFFFFFFF,
        locationName: json['locationName'] as String? ?? "",
        locationCode: json['locationCode'] as String? ?? "",
        profilePicture: json['profilePicture'] ?? "",
        isLogGuided: json['isLogGuided'] as bool? ?? true,
        lat: (json['lat'] as num?)?.toDouble() ?? 0,
        lng: (json['lng'] as num?)?.toDouble() ?? 0,
        locationGoodPriceCode: json['locationGoodPriceCode'] as String? ?? "",
        locationGoodPriceName: json['locationGoodPriceName'] as String? ?? "",
      )
      ..communitys = (json['communitys'] as List<dynamic>?)
          ?.map((e) => e as String)
          .toList();

Map<String, dynamic> _$ProfileToJson(Profile instance) => <String, dynamic>{
  'user': instance.user,
  'backColorval': instance.backColorval,
  'fontColorval': instance.fontColorval,
  'locationName': instance.locationName,
  'locationCode': instance.locationCode,
  'locationGoodPriceName': instance.locationGoodPriceName,
  'locationGoodPriceCode': instance.locationGoodPriceCode,
  'lat': instance.lat,
  'lng': instance.lng,
  'profilePicture': instance.profilePicture,
  'isLogGuided': instance.isLogGuided,
  'communitys': instance.communitys,
};
