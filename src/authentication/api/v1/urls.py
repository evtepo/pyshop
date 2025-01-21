from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from .views import LoginView, LogoutView, RefreshTokenView, RegisterView, UserProfileView


schema_view = get_schema_view(
    openapi.Info(
        title="Auth API",
        default_version="v1",
        description="API for authentication",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", UserProfileView.as_view(), name="profile"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path("register/", RegisterView.as_view(), name="register"),

    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
