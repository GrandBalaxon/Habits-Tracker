from django.urls import path

from habits.views import HabitsListApiView, HabitRetrieveApiView, HabitCreateApiView, HabitUpdateApiView, \
    HabitDestroyApiView

app_name = 'habits'

urlpatterns = [
    path('list/', HabitsListApiView.as_view(), name='list'),
    path('create/', HabitCreateApiView.as_view(), name='create'),
    path('<int:pk>/', HabitRetrieveApiView.as_view(), name='detail'),
    path('<int:pk>/update/', HabitUpdateApiView.as_view(), name='update'),
    path('<int:pk>/delete/', HabitDestroyApiView.as_view(), name='delete'),
    ]
