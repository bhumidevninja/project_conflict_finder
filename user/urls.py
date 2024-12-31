from django.urls import path
from .views import RegisterView, ForgotPasswordView, ResetPasswordView,UserInfoView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("forget-password/", ForgotPasswordView.as_view()),
    path(
        "reset-password/<uidb64>/<token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path('user-info/', UserInfoView.as_view(),name="user-info")
]
