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
          emit(
            PostLoaded(
              activitys: activitys,
              hasReachedMax: activitys.length < 6,
              error: false,
              notinteresteduids: notinteresteduids,
            ),
          );
          return;
        }

        // 加载更多
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
          emit(
            activitys.isEmpty
                ? currentState.copyWith(hasReachedMax: true)
                : PostLoaded(
                    activitys: currentState.activitys! + activitys,
                    hasReachedMax: false,
                    error: false,
                    notinteresteduids: notinteresteduids,
                  ),
          );
        }
      }
    } catch (_) {
      emit(PostUninitedError());
    }
  }

  Future<void> _onRefresh(
    Refresh event,
    Emitter<ActivityDataState> emit,
  ) async {
    final currentState = state;

    try {
      if (currentState is PostLoaded) {
        final activitys = await _activityService.getActivityListByUpdateTime(0);
        currentlength = activitys.length;
        if (Global.profile.user != null) {
          notinteresteduids = await _imHelper.getNotInteresteduids(
            Global.profile.user!.uid,
          );
        }
        emit(
          PostLoaded(
            activitys: activitys,
            hasReachedMax: activitys.length < 6,
            error: false,
            notinteresteduids: notinteresteduids,
          ),
        );
      } else if (currentState is PostUninitedError ||
          currentState is PostUninitialized) {
        emit(PostLoading());
        final activitys = await _activityService.getActivityListByUpdateTime(0);
        currentlength = activitys.length;
        if (Global.profile.user != null) {
          notinteresteduids = await _imHelper.getNotInteresteduids(
            Global.profile.user!.uid,
          );
        }
        emit(
          PostLoaded(
            activitys: activitys,
            hasReachedMax: activitys.length < 6,
            error: false,
            notinteresteduids: notinteresteduids,
          ),
        );
      }
    } catch (_) {
      emit(PostUninitedError());
    }
  }

  bool _hasReachedMax(ActivityDataState state) =>
      state is PostLoaded && state.hasReachedMax!;
}
