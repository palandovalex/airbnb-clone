from django.urls import path
from . import views

app_name="users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),

    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/google/", views.google_login, name="google-login"),
    path("login/google/callback/", views.google_callback, name="google-callback"),

    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("verify/<str:key>/", views.complite_verification,
         name="complite-verification"),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update-password/", views.UpdatePasswordView.as_view(), name="password"),
    path("add-sotial/", views.UpdatePasswordView.as_view(), name="add-sotial"),
    path("avatar/", views.UpdateAvatarView.as_view(), name="avatar"),
    path("switch-hosting/", views.switch_hosting, name="switch-hosting"),
    path("switch-language/", views.switch_language, name="switch-language"),
]
