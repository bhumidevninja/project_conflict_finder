from django.urls import path, include
from .views import RegisterView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("forget-password/", ForgotPasswordView.as_view()),
    path(
        "reset-password/<uidb64>/<token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
]
