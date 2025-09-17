import 'package:json_annotation/json_annotation.dart';

part 'searchresult.g.dart';

@JsonSerializable()
class SearchResult {
  int? id;
  String? content;
  String? updatetime;
  int? searchnum;

  Map<String, dynamic> toMap(SearchResult type) {
    final Map<String, dynamic> data = <String, dynamic>{};

    data['id'] = id;
    data['content'] = content;
    data['updatetime'] = updatetime;
    data['searchnum'] = searchnum;

    return data;
  }

  SearchResult.fromMap(Map<String, dynamic> data) {
    //    User user = User.fromJson(data['sender'] as Map<String, dynamic>);
    id = data['id'];
    content = data['content'];
    updatetime = data['updatetime'];
    searchnum = data['searchnum'];
  }

  SearchResult(this.id, this.content, this.updatetime, this.searchnum);

  Map<String, dynamic> toJson() => _$SearchResultToJson(this);
  factory SearchResult.fromJson(Map<String, dynamic> json) =>
      _$SearchResultFromJson(json);
}
