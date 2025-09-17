class HisSearch {
  String? content;
  String? time;
  int? type; //0 社团搜索  1 活动搜索

  Map<String, dynamic> toMap(int type) {
    final Map<String, dynamic> data = <String, dynamic>{};

    data['content'] = content;
    data['time'] = time;
    data['type'] = this.type;

    return data;
  }

  HisSearch.fromMap(Map<String, dynamic> data) {
    //    User user = User.fromJson(data['sender'] as Map<String, dynamic>);
    content = data['content'];
    time = data['time'];
    type = data['type'];
  }

  HisSearch(this.content, this.time, this.type);
}
