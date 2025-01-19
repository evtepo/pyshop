from django.urls import path

from .views import LoginView, LogoutView, RefreshTokenView, RegisterView, UserProfileView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", UserProfileView.as_view(), name="profile"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path("register/", RegisterView.as_view(), name="register"),
]
