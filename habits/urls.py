from django.urls import path

from habits.views import HabitsListApiView, HabitRetrieveApiView

app_name = 'habits'

urlpatterns = [
    path('list/', HabitsListApiView.as_view(), name='list'),
    path('<int:pk>/>', HabitRetrieveApiView.as_view(), name='detail'),
]
