import 'package:bloc/bloc.dart';
import '../../model/activity.dart';
import '../../model/dynamic.dart';
import '../../model/user.dart';
import '../../service/activity.dart';
import '../../service/userservice.dart';

import '../../bloc/user/event/myfollow_event.dart';
import '../../bloc/user/state/myfollow_state.dart';

export 'event/myfollow_event.dart';
export 'state/myfollow_state.dart';

class MyFollowBloc extends Bloc<MyFollowEvent, MyFollowState> {
  final UserService _userService = UserService();
  final ActivityService _activityService = ActivityService();

  List<User> users = [];
  List<Activity> activitys = [];

  MyFollowBloc() : super(PostInitial()) {
    on<PostFetched>(_onPostFetched);
    on<PostActvityFetched>(_onPostActivityFetched);
    on<PostCommunityFetched>(_onPostCommunityFetched);
    on<Refreshed>(_onRefreshed);
  }

  Future<void> _onPostFetched(
    PostFetched event,
    Emitter<MyFollowState> emit,
  ) async {
    final currentState = state;
    try {
      if (currentState is PostInitial) {
        if (event.user == null) {
          emit(NoLogin());
          return;
        }
        emit(PostLoading());
        users = await _userService.getFollowUsers(
          0,
          event.user!.uid,
          event.user!.token!,
        );
        if (users.isNotEmpty) {
          activitys = await _activityService.getActivityListByFollow(0, users);
        }
        emit(
          PostSuccess(
            users: users,
            activitys: activitys,
            hasReachedActivityMax: false,
            hasReachedUserMax: false,
          ),
        );
      }
    } catch (_) {
      emit(PostFailure());
    }
  }

  Future<void> _onPostActivityFetched(
    PostActvityFetched event,
    Emitter<MyFollowState> emit,
  ) async {
    final currentState = state;
    try {
      if (currentState is PostSuccess && !currentState.hasReachedActivityMax) {
        int currentindex = currentState.activitys.length;
        if (currentState.users.isNotEmpty) {
          activitys = await _activityService.getActivityListByFollow(
            currentindex,
            currentState.users,
          );
        }

        if (activitys.isNotEmpty) currentState.activitys.addAll(activitys);
        emit(
          activitys.isEmpty
              ? currentState.copyWith(hasReachedActivityMax: true)
              : PostSuccess(
                  users: currentState.users,
                  activitys: currentState.activitys,
                  hasReachedActivityMax: false,
                  hasReachedUserMax: currentState.hasReachedUserMax,
                  time: DateTime.now().toString(),
                ),
        );
      }
    } catch (_) {
      emit(PostFailure());
    }
  }

  Future<void> _onPostCommunityFetched(
    PostCommunityFetched event,
    Emitter<MyFollowState> emit,
  ) async {
    final currentState = state;
    try {
      if (currentState is PostSuccess && !currentState.hasReachedUserMax) {
        int currentindex = currentState.users.length;

        users = await _userService.getFollowUsers(
          currentindex,
          event.user.uid,
          event.user.token!,
        );
        if (users.isNotEmpty) {
          currentState.users.addAll(users);
          activitys = await _activityService.getActivityListByFollow(
            0,
            currentState.users,
          );
          currentState.activitys.clear();
          currentState.activitys.addAll(activitys);
        }
        emit(
          users.isEmpty
              ? currentState.copyWith(hasReachedUserMax: true)
              : PostSuccess(
                  users: currentState.users,
                  activitys: currentState.activitys,
                  hasReachedUserMax: false,
                  hasReachedActivityMax: currentState.hasReachedActivityMax,
                  time: DateTime.now().toString(),
                ),
        );
      }
    } catch (_) {
      emit(PostFailure());
    }
  }

  Future<void> _onRefreshed(
    Refreshed event,
    Emitter<MyFollowState> emit,
  ) async {
    try {
      users = await _userService.getFollowUsers(
        0,
        event.user.uid,
        event.user.token!,
      );
      if (users.isNotEmpty) {
        activitys = await _activityService.getActivityListByFollow(0, users);
      }
      emit(
        PostSuccess(
          users: users,
          activitys: activitys,
          hasReachedActivityMax: false,
          hasReachedUserMax: false,
        ),
      );
    } catch (_) {
      emit(PostFailure());
    }
  }

  @override
  void onTransition(Transition<MyFollowEvent, MyFollowState> transition) {
    //print(transition);
    super.onTransition(transition);
  }
}

Map<String, List<Dynamic>> groupData(List<Dynamic> myDynamics) {
  Map<String, List<Dynamic>> map = {
    for (var e in myDynamics)
      e.createtime.substring(0, 10): myDynamics
          .where(
            (item) =>
                (item.createtime.substring(0, 10) ==
                e.createtime.substring(0, 10)),
          )
          .toList(),
  };
  return map;
}
