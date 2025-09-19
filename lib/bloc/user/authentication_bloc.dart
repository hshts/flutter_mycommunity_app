import 'dart:async';
import 'package:flutter_app/service/userservice.dart';
import 'package:flutter_app/util/token_util.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../service/activity.dart';
import '../../service/gpservice.dart';
import '../../model/user.dart';
import '../../util/networkmanager_util.dart';
import '../../global.dart';
import 'user_repository.dart';
import 'event/authentication_event.dart';
import 'state/authentication_state.dart';
export 'event/authentication_event.dart';
export 'state/authentication_state.dart';

class AuthenticationBloc
    extends Bloc<AuthenticationEvent, AuthenticationState> {
  // Services and stateful fields
  final UserRepository userRepository = UserRepository();
  final UserService _userService = UserService();
  final ActivityService activityService = ActivityService();

  String error = "";
  String errorstatusCode = "";
  String errorNet = "网络请求失败，请稍后重试";
  String errorNetCode = "-9999";

  AuthenticationBloc() : super(AuthenticationUninitialized()) {
    on<LoggedState>(_onLoggedState);
    on<LoggedIn>(_onLoggedIn);
    on<LoggedOut>(_onLoggedOut);
    on<LoginButtonPressed>(_onLoginButtonPressed);
    on<LoginAli>(_onLoginAli);
    on<LoginWeiXin>(_onLoginWeiXin);
    on<LoginIos>(_onLoginIos);

    on<UpdateImagePressed>(_onUpdateImagePressed);
    on<UpdateUserNamePressed>(_onUpdateUserNamePressed);
    on<UpdateUserLocationPressed>(_onUpdateUserLocationPressed);
    on<UpdateUserPasswordPressed>(_onUpdateUserPasswordPressed);
    on<UpdateUserSexPressed>(_onUpdateUserSexPressed);
    on<UpdateUserBirthdayPressed>(_onUpdateUserBirthdayPressed);
    on<UpdateUserSignaturePressed>(_onUpdateUserSignaturePressed);

    on<UpdateLocation>(_onUpdateLocation);
    on<Refresh>(_onRefresh);
    on<initUpdate>(_onInitUpdate);
  }

  Future<void> _onLoggedState(
    LoggedState event,
    Emitter<AuthenticationState> emit,
  ) async {
    final user = Global.profile.user;
    if (user != null) {
      emit(AuthenticationAuthenticated());
    } else {
      emit(LoginOuted());
    }
  }

  Future<void> _onLoggedIn(
    LoggedIn event,
    Emitter<AuthenticationState> emit,
  ) async {
    await LoginSuccess(event.user);
    emit(AuthenticationAuthenticated());
  }

  Future<void> _onLoggedOut(
    LoggedOut event,
    Emitter<AuthenticationState> emit,
  ) async {
    try {
      final user = Global.profile.user;
      if (user != null) {
        await userRepository.deleteToken(user, errorCallBack);
      }
    } catch (_) {}
    emit(LoginOuted());
  }

  Future<void> _onLoginButtonPressed(
    LoginButtonPressed event,
    Emitter<AuthenticationState> emit,
  ) async {
    emit(LoginLoading());
    try {
      final user = await userRepository.loginToUser(
        mobile: event.mobile,
        password: event.password,
        vcode: event.vcode,
        type: event.type,
        captchaVerification: event.captchaVerification,
        country: event.country,
        errorCallBack: errorCallBack,
      );
      if (user != null) {
        await LoginSuccess(user);
        emit(AuthenticationAuthenticated());
      } else {
        emit(
          AuthenticationUnauthenticated(
            error: error,
            errorstatusCode: errorstatusCode,
          ),
        );
      }
    } catch (_) {
      emit(
        AuthenticationUnauthenticated(
          error: errorNet,
          errorstatusCode: errorNetCode,
        ),
      );
    }
  }

  ///更新密码
  Future<void> _onUpdateUserPasswordPressed(
    UpdateUserPasswordPressed event,
    Emitter<AuthenticationState> emit,
  ) async {
    try {
      final ret = await userRepository.UpdateUserPasswordPressed(
        event.user,
        event.password,
        errorCallBack,
      );
      if (ret) {
        emit(AuthenticationAuthenticated());
      } else {
        emit(
          AuthenticationUnauthenticated(
            error: error,
            errorstatusCode: errorstatusCode,
          ),
        );
      }
    } catch (e) {
      emit(
        AuthenticationUnauthenticated(
          error: errorNet,
          errorstatusCode: errorNetCode,
        ),
      );
    }
  }

  ///更新性别
  Future<void> _onUpdateUserSexPressed(
    UpdateUserSexPressed event,
    Emitter<AuthenticationState> emit,
  ) async {
    try {
      final ret = await userRepository.UpdateUserSexPressed(
        event.user,
        event.sex,
        errorCallBack,
      );
      if (ret) {
        event.user.sex = event.sex;
        userRepository.persistToken(event.user);
        emit(AuthenticationAuthenticated());
      } else {
        emit(
          AuthenticationUnauthenticated(
            error: error,
            errorstatusCode: errorstatusCode,
          ),
        );
      }
    } catch (e) {
      emit(
        AuthenticationUnauthenticated(
          error: errorNet,
          errorstatusCode: errorNetCode,
        ),
      );
    }
  }

  ///更新生日
  Future<void> _onUpdateUserBirthdayPressed(
    UpdateUserBirthdayPressed event,
    Emitter<AuthenticationState> emit,
  ) async {
    try {
      final ret = await userRepository.UpdateUserBirthdayPressed(
        event.user,
        event.birthday,
        errorCallBack,
      );
      if (ret) {
        event.user.birthday = event.birthday;
        userRepository.persistToken(event.user);
        emit(AuthenticationAuthenticated());
      } else {
        emit(
          AuthenticationUnauthenticated(
            error: error,
            errorstatusCode: errorstatusCode,
          ),
        );
      }
    } catch (e) {
      emit(
        AuthenticationUnauthenticated(
          error: errorNet,
          errorstatusCode: errorNetCode,
        ),
      );
    }
  }

  ///更新定位（只更新状态）
  Future<void> _onUpdateLocation(
    UpdateLocation event,
    Emitter<AuthenticationState> emit,
  ) async {
    emit(
      UpdateLocationed(
        locationName: event.locationName,
        locationCode: event.locationCode,
      ),
    );
  }

  ///初始化用户信息更新（只更新状态）
  Future<void> _onInitUpdate(
    initUpdate event,
    Emitter<AuthenticationState> emit,
  ) async {
    emit(AuthenticationAuthenticated());
  }

  ///支付宝登录
  Future<void> _onLoginAli(
    LoginAli event,
    Emitter<AuthenticationState> emit,
  ) async {
    try {
      final authurl = await _userService.getAliUserAuth();
      if (authurl.isNotEmpty) {
        final user = await _userService.updateLoginali(authurl, errorCallBack);
        if (user != null) {
          await LoginSuccess(user);
          emit(AuthenticationAuthenticated());
          return;
        }
      }
      emit(
        AuthenticationUnauthenticated(
          error: error,
          errorstatusCode: errorstatusCode,
        ),
      );
    } catch (_) {
      emit(
        AuthenticationUnauthenticated(
          error: errorNet,
          errorstatusCode: errorNetCode,
        ),
      );
    }
  }

  Future<void> _onLoginWeiXin(
    LoginWeiXin event,
    Emitter<AuthenticationState> emit,
  ) async {
    User? user = await _userService.loginweixin(event.auth_code, errorCallBack);
    if (user != null) {
      await LoginSuccess(user);
      emit(AuthenticationAuthenticated());
    }
  }

  ///刷新（根据当前登录状态简单重发状态）
  Future<void> _onRefresh(
    Refresh event,
    Emitter<AuthenticationState> emit,
  ) async {
    if (Global.profile.user != null) {
      emit(AuthenticationAuthenticated());
    } else {
      emit(LoginOuted());
    }
  }

  ///ios登录
  Future<void> _onLoginIos(
    LoginIos event,
    Emitter<AuthenticationState> emit,
  ) async {
    User? user = await _userService.loginIos(
      event.identityToken,
      event.iosuserid,
      errorCallBack,
    );
    if (user != null) {
      await LoginSuccess(user);
      emit(AuthenticationAuthenticated());
    }
  }

  ///更新照片
  Future<void> _onUpdateImagePressed(
    UpdateImagePressed event,
    Emitter<AuthenticationState> emit,
  ) async {
    try {
      bool ret = await userRepository.updateImage(
        event.user,
        event.serverimgpath,
        errorCallBack,
      );
      if (ret) {
        await userRepository.updateUserPicture(event.user, event.imgpath);
        emit(AuthenticationAuthenticated(isUserImage: true));
      } else {
        ///验证未通过
        emit(
          AuthenticationUnauthenticated(
            error: error,
            errorstatusCode: errorstatusCode,
          ),
        );
      }
    } catch (error) {
      ///验证未通过
      emit(
        AuthenticationUnauthenticated(
          error: errorNet,
          errorstatusCode: errorNetCode,
        ),
      );
    }
  }

  ///更新昵称
  Future<void> _onUpdateUserNamePressed(
    UpdateUserNamePressed event,
    Emitter<AuthenticationState> emit,
  ) async {
    try {
      bool ret = await userRepository.updateUserName(
        event.user,
        event.username,
        errorCallBack,
      );
      if (ret) {
        event.user.username = event.username;
        userRepository.persistToken(event.user);
        emit(AuthenticationAuthenticated());
      } else {
        ///验证未通过
        emit(
          AuthenticationUnauthenticated(
            error: error,
            errorstatusCode: errorstatusCode,
          ),
        );
      }
    } catch (error) {
      ///验证未通过
      emit(
        AuthenticationUnauthenticated(
          error: errorNet,
          errorstatusCode: errorNetCode,
        ),
      );
    }
  }

  ///更新个人简介
  Future<void> _onUpdateUserSignaturePressed(
    UpdateUserSignaturePressed event,
    Emitter<AuthenticationState> emit,
  ) async {
    try {
      bool ret = await userRepository.UpdateUserSignaturePressed(
        event.user,
        event.signature,
        errorCallBack,
      );
      if (ret) {
        event.user.signature = event.signature;
        userRepository.persistToken(event.user);
        emit(AuthenticationAuthenticated());
      } else {
        ///验证未通过
        emit(
          AuthenticationUnauthenticated(
            error: error,
            errorstatusCode: errorstatusCode,
          ),
        );
      }
    } catch (error) {
      ///验证未通过
      emit(
        AuthenticationUnauthenticated(
          error: errorNet,
          errorstatusCode: errorNetCode,
        ),
      );
    }
  }

  ///更新位置
  Future<void> _onUpdateUserLocationPressed(
    UpdateUserLocationPressed event,
    Emitter<AuthenticationState> emit,
  ) async {
    try {
      bool ret = await userRepository.updateLocation(
        event.user,
        event.province,
        event.city,
        errorCallBack,
      );
      if (ret) {
        event.user.province = event.province;
        event.user.city = event.city;
        userRepository.persistToken(event.user);
        emit(AuthenticationAuthenticated());
      } else {
        ///验证未通过
        emit(
          AuthenticationUnauthenticated(
            error: error,
            errorstatusCode: errorstatusCode,
          ),
        );
      }
    } catch (error) {
      ///验证未通过
      emit(
        AuthenticationUnauthenticated(
          error: errorNet,
          errorstatusCode: errorNetCode,
        ),
      );
    }
  }

  // Note: Removed legacy/duplicate handler code with yield-based logic and stray event checks.

  @override
  void onTransition(
    Transition<AuthenticationEvent, AuthenticationState> transition,
  ) {
    //print(transition);
    super.onTransition(transition);
  }

  Future<void> LoginSuccess(User user) async {
    // UserRepository userRepository = new UserRepository();
    // userRepository.persistToken(user);
    //本地无数据就从服务器下载
    userRepository.persistToken(user);

    TokenUtil tokenUtil = TokenUtil();
    await tokenUtil.getDeviceToken();

    GPService gpService = GPService();
    // UmengCommonSdk.onEvent('bool', {'name':'jack', 'age':18, 'male':true});

    if (user.likeact! > 0) {
      activityService.getUserLike(user.uid, user.token!); //点赞的活动
    }
    if (user.likebug > 0) {
      activityService.getUserLikeBug(user.uid, user.token!); //点赞的活动
    }

    if (user.likemoment > 0) {
      activityService.getUserLikeMoment(user.uid, user.token!); //点赞的活动
    }

    if (user.likesuggest > 0) {
      activityService.getUserLikeSuggest(user.uid, user.token!); //点赞的活动
    }
    if (user.collectionact! > 0) {
      activityService.getUserCollection(user.uid, user.token!); //收藏的活动
    }
    if (user.likecomment > 0 || user.likeevaluate! > 0) {
      activityService.getUserComnnentLike(
        user.uid,
        user.token!,
        user.likecomment,
        user.likeevaluate!,
      ); //获取用户留言和评论的点赞情况comment和evaluate
    }
    if (user.likegoodpricecomment > 0) {
      activityService.getUserGoodPriceComnnentLike(
        user.uid,
        user.token!,
        user.likegoodpricecomment,
      ); //获取用户留言和评论的点赞情况goodprice
    }
    if (user.likebugcomment > 0 ||
        user.likesuggestcomment > 0 ||
        user.likemomentcomment > 0) {
      activityService.getUserBugAndSuggestAndMomentComnnentLike(
        user.uid,
        user.token!,
        user.likebugcomment,
        user.likesuggestcomment,
        user.likemomentcomment,
      ); //获取用户留言和评论的点赞情况comment和evaluate
    }

    if (user.collectionproduct! > 0) {
      gpService.getUserGoodPriceCollection(user.uid, user.token!); //获取用户收藏的优惠商品
    }
    if (user.notinteresteduids != null && user.notinteresteduids!.isNotEmpty) {}
    //获取用户的好友
    //          CommunityService communityService = CommunityService();
    //          await communityService.getMyCommunityListByUser(0, user.uid);
    //我的关注
    if (user.following! > 0) {
      userRepository.getfollow(user, errorCallBack);
    }
    //我的不感兴趣,不需要重新获取数据
    if (user.notinteresteduids != null && user.notinteresteduids!.isNotEmpty) {
      await userRepository.updateNotInteresteduids(user, errorCallBack);
    }
    //我的好价不感兴趣,不需要重新获取数据
    if (user.goodpricenotinteresteduids != null &&
        user.goodpricenotinteresteduids!.isNotEmpty) {
      await userRepository.updateGoodPriceNotInteresteduids(
        user,
        errorCallBack,
      );
    }
    //我的黑名单,不需要重新获取数据
    if (user.blacklist != null && user.blacklist!.isNotEmpty) {
      await userRepository.updateBlacklist(user, errorCallBack);
    }

    NetworkManager.init(user, Global.mainContext!);
  }

  void errorCallBack(String statusCode, String msg) {
    error = msg;
    errorstatusCode = statusCode;
  }
}
