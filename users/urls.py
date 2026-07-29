from django.urls import path

from users.views import UserCreateApiView


app_name = 'users'

urlpatterns = [
    path("create/", UserCreateApiView.as_view(), name="create"),
]
