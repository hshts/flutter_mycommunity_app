import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';

import '../global.dart';

//圆形头像，跳转到用户信息,使用内存缓存
class NoCacheCircleHeadImage extends StatelessWidget {
  final String imageUrl;
  final double width;
  final int imgwidthxp;
  final int uid;
  NoCacheCircleHeadImage({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    if (uid != 0 &&
        (Global.profile.user != null && Global.profile.user!.uid == uid)) {
      temimageUrl = imageUrl;
    } else {
      temimageUrl = '$imageUrl?x-oss-process=image/resize,w_300/quality,q_90';
    }

    return GestureDetector(
      child: SizedBox(
        height: width,
        width: width,
        child: ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(50)),
          child: temimageUrl.isEmpty
              ? Image(image: AssetImage(Global.headimg))
              : Image(image: NetworkImage(temimageUrl)),
        ),
      ),
      onTap: () {
        if (Global.profile.user == null) {
          Navigator.pushNamed(
            context,
            '/OtherProfile',
            arguments: {"uid": uid},
          );
        } else if (uid != Global.profile.user!.uid) {
          Navigator.pushNamed(
            context,
            '/OtherProfile',
            arguments: {"uid": uid},
          );
        } else if (uid == Global.profile.user!.uid)
          Navigator.pushNamed(context, '/MyProfile');
      },
    );
  }
}

//圆形头像，跳转到用户信息,使用内存缓存
class NoCacheClipRRectHeadImage extends StatelessWidget {
  final String imageUrl;
  final double width;
  final int imgwidthxp;
  final int uid;
  final double cir;
  NoCacheClipRRectHeadImage({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";

    if (uid != 0 &&
        (Global.profile.user != null && Global.profile.user!.uid == uid)) {
      temimageUrl = imageUrl;
    } else {
      temimageUrl =
          '$imageUrl?x-oss-process=image/resize,m_fixed,w_300/quality,q_90';
    }
    return InkWell(
      child: SizedBox(
        height: width,
        width: width,
        child: ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(cir)),
          child: temimageUrl.isEmpty
              ? Image(image: AssetImage(Global.headimg))
              : Image(image: NetworkImage(temimageUrl), fit: BoxFit.cover),
        ),
      ),
      onTap: () {
        if (Global.profile.user == null) {
          Navigator.pushNamed(
            context,
            '/OtherProfile',
            arguments: {"uid": uid},
          );
        } else if (uid == Global.profile.user!.uid)
          Navigator.pushNamed(context, '/MyProfile');
        else
          Navigator.pushNamed(
            context,
            '/OtherProfile',
            arguments: {"uid": uid},
          );
      },
    );
  }
}

//没有定义默认事件, 长方形,使用内存缓存
class NoCacheClipRRectOhterHeadImage extends StatelessWidget {
  final String imageUrl;
  final double width;
  final int imgwidthxp;
  final int uid;
  final double cir;
  NoCacheClipRRectOhterHeadImage({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";

    if (uid != 0 &&
        (Global.profile.user != null && Global.profile.user!.uid == uid)) {
      temimageUrl = imageUrl;
    } else {
      temimageUrl =
          '$imageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50/quality,q_80';
    }
    return SizedBox(
      width: width,
      child: ClipRRect(
        borderRadius: BorderRadius.all(Radius.circular(cir)),
        child: temimageUrl.isEmpty
            ? Image(image: AssetImage(Global.headimg))
            : Image(image: NetworkImage(temimageUrl), fit: BoxFit.cover),
      ),
    );
  }
}

//正方形的
class NoCacheClipRRectOhterHeadImageContainer extends StatelessWidget {
  final String imageUrl;
  final double width;
  final double height;
  final int imgwidthxp;
  final int uid;
  final double cir;
  final double borderwidth;

  NoCacheClipRRectOhterHeadImageContainer({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.height = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
    this.borderwidth = 2,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";

    if (uid != 0 &&
        (Global.profile.user != null && Global.profile.user!.uid == uid)) {
      temimageUrl = imageUrl;
    } else {
      temimageUrl =
          '$imageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50/quality,q_80';
    }
    return Container(
      height: height,
      width: width,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(cir),
        border: Border.all(color: Colors.white, width: borderwidth),
        image: DecorationImage(
          fit: BoxFit.cover,
          image: NetworkImage(temimageUrl),
        ),
      ),
    );
  }
}

class CircleHeadImage extends StatelessWidget {
  final String imageUrl;
  final double width;
  final int imgwidthxp;
  final int uid;
  CircleHeadImage({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;
    return InkWell(
      child: SizedBox(
        height: width,
        width: width,
        child: ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(50)),
          child: temimageUrl.isEmpty
              ? Image(image: AssetImage(Global.headimg))
              : CachedNetworkImage(
                  imageUrl:
                      '$temimageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50/quality,q_80',
                ),
        ),
      ),
      onTap: () {
        if (Global.profile.user == null) {
          Navigator.pushNamed(
            context,
            '/OtherProfile',
            arguments: {"uid": uid},
          );
        } else if (uid != Global.profile.user!.uid) {
          Navigator.pushNamed(
            context,
            '/OtherProfile',
            arguments: {"uid": uid},
          );
        } else if (uid == Global.profile.user!.uid)
          Navigator.pushNamed(context, '/MyProfile');
      },
    );
  }
}

//正方形用户头像，跳转到用户信息
class ClipRRectHeadImage extends StatelessWidget {
  final String imageUrl;
  final double width;
  final int imgwidthxp;
  final int uid;
  final double cir;
  ClipRRectHeadImage({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;

    return InkWell(
      child: SizedBox(
        height: width,
        width: width,
        child: ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(cir)),
          child: temimageUrl.isEmpty
              ? Image(image: AssetImage(Global.headimg))
              : CachedNetworkImage(
                  imageUrl:
                      '$temimageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50/quality,q_80',
                  fit: BoxFit.cover,
                ),
        ),
      ),
      onTap: () {
        if (Global.profile.user == null) {
          Navigator.pushNamed(
            context,
            '/OtherProfile',
            arguments: {"uid": uid},
          );
        } else if (uid == Global.profile.user!.uid)
          Navigator.pushNamed(context, '/MyProfile');
        else
          Navigator.pushNamed(
            context,
            '/OtherProfile',
            arguments: {"uid": uid},
          );
      },
    );
  }
}

//没有定义默认事件, 长方形
class ClipRRectOhterHeadImage extends StatelessWidget {
  final String imageUrl;
  final double width;
  final int imgwidthxp;
  final int uid;
  final double cir;
  ClipRRectOhterHeadImage({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;

    return SizedBox(
      width: width,
      child: ClipRRect(
        borderRadius: BorderRadius.all(Radius.circular(cir)),
        child: temimageUrl.isEmpty
            ? Image(image: AssetImage(Global.headimg))
            : CachedNetworkImage(
                imageUrl:
                    '$temimageUrl?x-oss-process=image/resize,m_fixed,w_600/sharpen,50/quality,q_80',
                fit: BoxFit.cover,
              ),
      ),
    );
  }
}

//正方形的
class ClipRRectOhterHeadImageContainer extends StatelessWidget {
  final String imageUrl;
  final double width;
  final double height;
  final int imgwidthxp;
  final int uid;
  final double cir;
  final double borderwidth;

  ClipRRectOhterHeadImageContainer({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.height = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
    this.borderwidth = 2,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;

    return Container(
      height: height,
      width: width,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(cir),
        border: Border.all(color: Colors.white, width: borderwidth),
        image: DecorationImage(
          fit: BoxFit.cover,
          image: CachedNetworkImageProvider(
            '$temimageUrl?x-oss-process=image/resize,m_fixed,w_600/sharpen,50/quality,q_80',
          ),
        ),
      ),
    );
  }
}

///IM中显示地图用
class ClipRRectOhterHeadImageContainerLocation extends StatelessWidget {
  final String imageUrl;
  final double width;
  final double height;
  final int imgwidthxp;
  final int uid;
  final double cir;
  final String lat;
  final String lng;
  final String title;
  final String address;

  ClipRRectOhterHeadImageContainerLocation({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.height = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
    this.lat = "0",
    this.lng = "0",
    this.title = "",
    this.address = "",
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;

    return InkWell(
      child: Container(
        height: height,
        width: width,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(cir),
          border: Border.all(color: Colors.white, width: 2),
          image: DecorationImage(
            fit: BoxFit.cover,
            image: CachedNetworkImageProvider(
              '$temimageUrl?x-oss-process=image/resize,m_fixed,w_600/sharpen,50/quality,q_80',
            ),
          ),
        ),
      ),
      onTap: () {
        Navigator.pushNamed(
          context,
          '/MapLocationShowNav',
          arguments: {
            "lat": lat,
            "lng": lng,
            "title": title,
            "address": address,
          },
        );
      },
    );
  }
}

class ClipRRectOhterHeadImageContainerLocationNoEvent extends StatelessWidget {
  final String imageUrl;
  final double width;
  final double height;
  final int imgwidthxp;
  final int uid;
  final double cir;
  final String lat;
  final String lng;
  final String title;
  final String address;

  ClipRRectOhterHeadImageContainerLocationNoEvent({
    super.key,
    this.imageUrl = "",
    this.width = 45,
    this.height = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
    this.lat = "0",
    this.lng = "0",
    this.title = "",
    this.address = "",
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;

    return Container(
      height: height,
      width: width,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(cir),
        border: Border.all(color: Colors.white, width: 2),
        image: DecorationImage(
          fit: BoxFit.cover,
          image: CachedNetworkImageProvider(
            '$temimageUrl?x-oss-process=image/resize,m_fixed,w_600/sharpen,50/quality,q_80',
          ),
        ),
      ),
    );
  }
}

//形状不固定按宽度的自适应
class ClipRRectOhterHeadImageContainerByWidth extends StatelessWidget {
  final String imageUrl;
  final double pagewidth;
  final int imgwidthxp;
  final int uid;
  final double cir;
  final double sourceWidth;
  final double sourceHeight;

  ClipRRectOhterHeadImageContainerByWidth({
    super.key,
    this.imageUrl = "",
    this.pagewidth = 45,
    this.sourceWidth = 0,
    this.sourceHeight = 0,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;

    return InkWell(
      onTap: () {
        Navigator.pushNamed(
          context,
          '/PhotoViewImageHead',
          arguments: {"image": temimageUrl},
        );
      },
      child: Container(
        height: getImageWH(sourceWidth, sourceHeight),
        width: pagewidth,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(cir),
          border: Border.all(color: Colors.white, width: 2),
          image: DecorationImage(
            fit: BoxFit.cover,
            image: CachedNetworkImageProvider(
              '$temimageUrl?x-oss-process=image/resize,m_fixed,w_600/sharpen,50/quality,q_80',
            ),
          ),
        ),
      ),
    );
  }

  //计算图片高度和宽度
  double getImageWH(double width1, double height1) {
    double width = width1;
    double height = height1;
    double ratio = width / height; //宽高比
    double retheight = (pagewidth) / ratio;
    if (retheight > 200) {
      retheight = 200;
    }
    return retheight; //图片缩放高度
  }
}

//固定高宽，按宽度从oss中取回处理好的图片,指定高度裁剪
class ClipRRectOhterHeadImageContainerByWidthNoEvent extends StatelessWidget {
  final String imageUrl;
  final double pagewidth;
  final double pageheight;
  final int imgwidthxp;
  final int uid;
  final double cir;
  final double sourceWidth;
  final double sourceHeight;

  ClipRRectOhterHeadImageContainerByWidthNoEvent({
    super.key,
    this.imageUrl = "",
    this.pageheight = 45,
    this.pagewidth = 45,
    this.sourceWidth = 0,
    this.sourceHeight = 0,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;

    return Container(
      height: pageheight,
      width: pagewidth,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(cir),
        border: Border.all(color: Colors.white, width: 2),
        image: DecorationImage(
          fit: BoxFit.cover,
          image: CachedNetworkImageProvider(
            '$temimageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50/quality,q_80',
          ),
        ),
      ),
    );
  }

  //计算图片高度和宽度
  double getImageWH(double width1, double height1) {
    double width = width1;
    double height = height1;
    double ratio = width / height; //宽高比
    double retheight = (pagewidth) / ratio;
    if (retheight > 200) {
      retheight = 200;
    }
    return retheight; //图片缩放高度
  }
}

//形状不固定按宽度的自适应
class ClipRRectOhterHeadImageContainerByWidthNoEventNoHeight
    extends StatelessWidget {
  final String imageUrl;
  final double pagewidth;
  final int imgwidthxp;
  final int uid;
  final double cir;
  final double sourceWidth;
  final double sourceHeight;

  ClipRRectOhterHeadImageContainerByWidthNoEventNoHeight({
    super.key,
    this.imageUrl = "",
    this.pagewidth = 45,
    this.sourceWidth = 0,
    this.sourceHeight = 0,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;

    return Container(
      height: getImageWH(sourceWidth, sourceHeight),
      width: pagewidth,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(cir),
        border: Border.all(color: Colors.white, width: 2),
        image: DecorationImage(
          fit: BoxFit.cover,
          image: CachedNetworkImageProvider(
            '$temimageUrl?x-oss-process=image/resize,m_fixed,w_600/sharpen,50/quality,q_80',
          ),
        ),
      ),
    );
  }

  //计算图片高度和宽度
  double getImageWH(double width1, double height1) {
    double width = width1;
    double height = height1;
    double ratio = width / height; //宽高比
    double retheight = (pagewidth) / ratio;
    if (retheight > 200) {
      retheight = 200;
    }
    return retheight; //图片缩放高度
  }
}

//没有宽度，能弹出大图
class ClipRRectOhterHeadImageContainerByBigImg extends StatelessWidget {
  final String imageUrl;
  final double pagewidth;
  final int imgwidthxp;
  final int uid;
  final double cir;

  ClipRRectOhterHeadImageContainerByBigImg({
    super.key,
    this.imageUrl = "",
    this.pagewidth = 45,
    this.imgwidthxp = 130,
    this.uid = 0,
    this.cir = 5,
  });

  @override
  Widget build(BuildContext context) {
    String temimageUrl = "";
    temimageUrl = imageUrl;

    return InkWell(
      onTap: () {
        Navigator.pushNamed(
          context,
          '/PhotoViewImageHead',
          arguments: {"image": temimageUrl},
        );
      },
      child: Container(
        width: pagewidth,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(cir),
          border: Border.all(color: Colors.white, width: 2),
          image: DecorationImage(
            fit: BoxFit.cover,
            image: CachedNetworkImageProvider(
              '$temimageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50',
            ),
          ),
        ),
      ),
    );
  }
}

//修改图片缓存可以配置
class CommunityCircleHeadImage extends StatelessWidget {
  final String? imageUrl;
  final double width;
  final int imgwidthxp;
  final String cid;
  final int uid;
  CommunityCircleHeadImage({
    super.key,
    this.imageUrl,
    this.width = 45,
    this.imgwidthxp = 130,
    this.cid = "",
    this.uid = 0,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      child: SizedBox(
        width: width,
        child: ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(50)),
          child: imageUrl == null || imageUrl!.isEmpty
              ? Image(image: AssetImage(Global.headimg))
              : CachedNetworkImage(
                  imageUrl:
                      '$imageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50/quality,q_80',
                ),
        ),
      ),
      onTap: () {
        Navigator.pushNamed(
          context,
          '/CommunityInfo',
          arguments: {"cid": cid, "uid": uid},
        );
      },
    );
  }
}

class CommunityClipRRectHeadImage extends StatelessWidget {
  final String? imageUrl;
  final double width;
  final int imgwidthxp;
  final String cid;
  final int uid;

  CommunityClipRRectHeadImage({
    super.key,
    this.imageUrl,
    this.width = 45,
    this.imgwidthxp = 130,
    this.cid = "",
    this.uid = 0,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      child: SizedBox(
        width: width,
        child: ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(5)),
          child: imageUrl == null || imageUrl!.isEmpty
              ? Image(image: AssetImage(Global.headimg))
              : CachedNetworkImage(
                  errorWidget: (context, url, error) =>
                      Image.asset('images/image-failed.png'),
                  imageUrl:
                      '$imageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50/quality,q_80',
                  fit: BoxFit.cover,
                ),
        ),
      ),
      onTap: () {
        //Navigator.pushNamed(context, '/CommunityInfo', arguments: {"cid": this.cid, "uid": this.uid});
      },
    );
  }
}

class ActivityClipRRectHeadImage extends StatelessWidget {
  final String? imageUrl;
  final double width;
  final int imgwidthxp;
  final String actid;
  final int uid;

  ActivityClipRRectHeadImage({
    super.key,
    this.imageUrl,
    this.width = 45,
    this.imgwidthxp = 130,
    this.actid = "",
    this.uid = 0,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      child: SizedBox(
        width: width,
        child: ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(5)),
          child: imageUrl == null || imageUrl!.isEmpty
              ? Image(image: AssetImage(Global.headimg))
              : CachedNetworkImage(
                  imageUrl:
                      '$imageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50/quality,q_80',
                  fit: BoxFit.cover,
                  errorWidget: (context, url, error) =>
                      Image.asset(Global.nullimg),
                ),
        ),
      ),
      onTap: () {
        Navigator.pushNamed(
          context,
          '/ActivityInfo',
          arguments: {"actid": actid},
        ); //从消息列表进入活动详情，进行中或已结束
      },
    );
  }
}

///这个是消息页面活动的头像，，如果9宫格没有生成就显示自己的头像
class ActivityClipRRectHeadShortCacheImage extends StatelessWidget {
  final String? imageUrl;
  final double width;
  final int imgwidthxp;
  final String actid;
  final int uid;

  ActivityClipRRectHeadShortCacheImage({
    super.key,
    this.imageUrl,
    this.width = 45,
    this.imgwidthxp = 130,
    this.actid = "",
    this.uid = 0,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      child: SizedBox(
        width: width,
        child: ClipRRect(
          borderRadius: BorderRadius.all(Radius.circular(5)),
          child: imageUrl == null || imageUrl!.isEmpty
              ? Image(image: AssetImage(Global.headimg))
              : CachedNetworkImage(
                  imageUrl:
                      '$imageUrl?x-oss-process=image/resize,m_fixed,w_300/sharpen,50/quality,q_80',
                  fit: BoxFit.cover,
                  progressIndicatorBuilder: (context, url, downloadProgress) =>
                      LinearProgressIndicator(value: downloadProgress.progress),
                  errorWidget: (context, url, error) =>
                      Image.asset('images/image-failed.png'),
                ),
        ),
      ),
      onTap: () {
        Navigator.pushNamed(
          context,
          '/ActivityInfo',
          arguments: {"actid": actid},
        ); //从消息列表进入活动详情，进行中或已结束
      },
    );
  }
}
