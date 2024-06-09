from django.urls import path
from .views import register, login, profile_int, logout, home, users, createinvite


urlpatterns = [
    path("register/", register.handle, name="register"),
    path("login/", login.handle, name="login"),

    path("profile/<int:uid>", profile_int.handle, name="profile"),

    path("logout/", logout.handle, name="logout"),

    path("", home.handle, name="home"),
    path("home/", home.handle),
    path("users/", users.UsersListView.as_view(), name="users"),

    path("createinvite/", createinvite.handle, name="create_invite")
]
