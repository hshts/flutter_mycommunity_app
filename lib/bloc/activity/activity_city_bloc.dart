import 'package:flutter_bloc/flutter_bloc.dart';
import '../../service/activity.dart';
import 'event/activity_city_event.dart';
import 'state/activity_city_state.dart';

export './event/activity_city_event.dart';
export './state/activity_city_state.dart';

class CityActivityDataBloc extends Bloc<PostEvent, CityActivityState> {
  final ActivityService _activityService = ActivityService();

  CityActivityDataBloc() : super(PostInitial()) {
    on<PostFetched>(_onPostFetched);
    on<Refreshed>(_onRefreshed);
  }

  //@override
  // TODO: implement initialState
  //CityActivityState get initialState => PostInitial();

  Future<void> _onPostFetched(
    PostFetched event,
    Emitter<CityActivityState> emit,
  ) async {
    final currentState = state;
    try {
      if (!_hasReachedMax(currentState)) {
        if (currentState is PostInitial || currentState is PostFailure) {
          emit(PostLoading());
          final activitys = await _activityService.getActivityListByCity(
            0,
            event.locationCode,
          );
          emit(
            PostSuccess(
              activitys: activitys,
              hasReachedMax: activitys.length < 6 ? true : false,
              isRefreshed: true,
            ),
          );
          return;
        }
        //加载更多
        if (currentState is PostSuccess) {
          final activitys = await _activityService.getActivityListByCity(
            currentState.activitys!.length,
            event.locationCode,
          );
          emit(
            activitys.isEmpty
                ? currentState.copyWith(hasReachedMax: true)
                : PostSuccess(
                    activitys: currentState.activitys! + activitys,
                    hasReachedMax: false,
                    isRefreshed: false,
                  ),
          );
        }
      }
    } catch (_) {
      emit(PostFailure());
    }
  }

  Future<void> _onRefreshed(
    Refreshed event,
    Emitter<CityActivityState> emit,
  ) async {
    try {
      emit(PostLoading());
      final activitys = await _activityService.getActivityListByCity(
        0,
        event.locationCode,
      );
      emit(
        PostSuccess(
          activitys: activitys,
          hasReachedMax: activitys.length < 6 ? true : false,
          isRefreshed: true,
        ),
      );
    } catch (_) {
      emit(PostFailure());
    }
  }

  @override
  void onTransition(Transition<PostEvent, CityActivityState> transition) {
    //print(transition);
    super.onTransition(transition);
  }

  bool _hasReachedMax(CityActivityState state) =>
      state is PostSuccess && state.hasReachedMax;
}
