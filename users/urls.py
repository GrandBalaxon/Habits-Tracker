from django.urls import path

from users.views import UserCreateApiView, UserRetrieveApiView, UserUpdateApiView, UserDestroyApiView, \
    UserHabitsListApiView

app_name = 'users'

urlpatterns = [
    path("profile/", UserRetrieveApiView.as_view(), name='profile'),
    path("create/", UserCreateApiView.as_view(), name="create"),
    path("update/", UserUpdateApiView.as_view(), name="update"),
    path("destroy/", UserDestroyApiView.as_view(), name="destroy"),
    path("habits/", UserHabitsListApiView.as_view(), name="user-habits"),
]
