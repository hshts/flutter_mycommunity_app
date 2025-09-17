import 'package:bloc/bloc.dart';

import '../../service/activity.dart';
import '../../util/imhelper_util.dart';
import '../../global.dart';
import 'event/activity_data_event.dart';
import 'state/activity_data_state.dart';

export 'event/activity_data_event.dart';
export 'state/activity_data_state.dart';

class ActivityDataBloc extends Bloc<ActivityDataEvent, ActivityDataState> {
  final ActivityService _activityService = ActivityService();
  final ImHelper _imHelper = ImHelper();
  List<int> notinteresteduids = [];
  int currentlength = 0;

  ActivityDataBloc() : super(PostUninitialized()) {
    on<Fetch>(_onFetch);
    on<Refresh>(_onRefresh);
  }

  Future<void> _onFetch(Fetch event, Emitter<ActivityDataState> emit) async {
    final currentState = state;

    try {
      if (!_hasReachedMax(currentState)) {
        if (currentState is PostUninitialized) {
          emit(PostLoading());
          final activitys = await _activityService.getActivityListByUpdateTime(
            0,
          );
          if (Global.profile.user != null) {
            notinteresteduids = await _imHelper.getNotInteresteduids(
              Global.profile.user!.uid,
            );
          }
          currentlength = activitys.length;
          emit(PostLoaded(
            activitys: activitys,
            hasReachedMax: activitys.length < 6 ? true : false,
            error: false,
            notinteresteduids: notinteresteduids,
          ));
          return;
        }
        //加载更多
        if (currentState is PostLoaded) {
          final activitys = await _activityService.getActivityListByUpdateTime(
            currentlength,
          );
          if (activitys.isNotEmpty) currentlength += activitys.length;
          if (Global.profile.user != null) {
            notinteresteduids = await _imHelper.getNotInteresteduids(
              Global.profile.user!.uid,
            );
          }
          emit(activitys.isEmpty
              ? currentState.copyWith(hasReachedMax: true)
              : PostLoaded(
                  activitys: currentState.activitys! + activitys,
                  hasReachedMax: false,
                  error: false,
                  notinteresteduids: notinteresteduids,
                ));
        }
      }
    } catch (_) {
      emit(PostUninitedError());
    }
  }

  Future<void> _onRefresh(Refresh event, Emitter<ActivityDataState> emit) async {
    // Implementation for refresh
    emit(PostUninitialized());
    add(Fetch());
  }
              : PostLoaded(
                  activitys: currentState.activitys! + activitys,
                  hasReachedMax: false,
                  notinteresteduids: notinteresteduids,
                );
        }
      }

      if (event is Refresh) {
        if (currentState is PostLoaded) {
          final activitys = await _activityService.getActivityListByUpdateTime(
            0,
          );
          currentlength = activitys.length;
          if (Global.profile.user != null) {
            notinteresteduids = await _imHelper.getNotInteresteduids(
              Global.profile.user!.uid,
            );
          }
          yield PostLoaded(
            activitys: activitys,
            hasReachedMax: activitys.length < 6 ? true : false,
            error: false,
            notinteresteduids: notinteresteduids,
          );
        }
        if (currentState is PostUninitedError) {
          yield PostLoading();
          final activitys = await _activityService.getActivityListByUpdateTime(
            0,
          );
          currentlength = activitys.length;
          if (Global.profile.user != null) {
            notinteresteduids = await _imHelper.getNotInteresteduids(
              Global.profile.user!.uid,
            );
          }
          yield PostLoaded(
            activitys: activitys,
            hasReachedMax: activitys.length < 6 ? true : false,
            error: false,
            notinteresteduids: notinteresteduids,
          );
        }
        if (currentState is PostUninitialized) {
          yield PostLoading();
          final activitys = await _activityService.getActivityListByUpdateTime(
            0,
          );
          currentlength = activitys.length;
          if (Global.profile.user != null) {
            notinteresteduids = await _imHelper.getNotInteresteduids(
              Global.profile.user!.uid,
            );
          }
          yield PostLoaded(
            activitys: activitys,
            hasReachedMax: activitys.length < 6 ? true : false,
            error: false,
            notinteresteduids: notinteresteduids,
          );
        }
      }
    } catch (_) {
      ///初始化时异常
      if (currentState is PostUninitialized ||
          currentState is PostUninitedError ||
          (currentState is PostLoaded && event is Refresh)) {
        yield PostUninitedError();
      }

      ///加载更多时异常  注意：state内容一致时不会rebuild
      if ((currentState is PostLoaded && event is Fetch)) {
        if (Global.profile.user != null) {
          notinteresteduids = await _imHelper.getNotInteresteduids(
            Global.profile.user!.uid,
          );
        }
        PostLoaded tem = PostLoaded(
          activitys: currentState.activitys,
          hasReachedMax: false,
          isRebuild: currentState.isRebuild! ? false : true,
          error: true,
          notinteresteduids: notinteresteduids,
        );
        if (tem == currentState) {
          //          print(111);
        }
        yield tem;
      }
    }
  }

  @override
  void onTransition(
    Transition<ActivityDataEvent, ActivityDataState> transition,
  ) {
    print(transition);
    super.onTransition(transition);
  }

  bool _hasReachedMax(ActivityDataState state) =>
      state is PostLoaded && state.hasReachedMax!;
}
