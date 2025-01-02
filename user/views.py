from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegisterSerializer,
    ForgotPasswordSerializer,
    UserInfoSerializer,
)
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from .models import CustomUser


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {"detail": "No user with this email address exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate reset token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode("utf-8"))

            # Create the reset password URL
            reset_url = (
                f"http://localhost:8001{reverse('reset-password', args=[uid, token])}"
            )

            # Send the email
            subject = "Password Reset Request"
            message = render_to_string(
                "reset_password.html", {"user": user, "reset_url": reset_url}
            )
            send_mail(subject, message, "no-reply@example.com", [user.email])
            print(f"Reset password URL: {reset_url}")
            return Response(
                {"detail": "Password reset link has been sent to your email address."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def get(self, request, uidb64, token):
        # Decode the uidb64 to get the user ID
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, CustomUser.DoesNotExist):
            return HttpResponse("Invalid or expired token.", status=400)

        # Validate the token
        if not default_token_generator.check_token(user, token):
            return HttpResponse("Invalid or expired token.", status=400)

        # Check if the token has already been used
        if request.session.get("reset_token_used", False):
            return render(
                request,
                "reset_password.html",
                {"error": "This link has already been used or expired."},
            )

        # Render the password reset form
        return render(
            request, "reset_password.html", {"uidb64": uidb64, "token": token}
        )

    def post(self, request, uidb64, token):
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return render(
                request,
                "reset_password.html",
                {"errors": {"confirm_password": "Passwords do not match."}},
            )

        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return render(
                request,
                "reset_password.html",
                {"errors": {"new_password": "Invalid user or token."}},
            )

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            user.password = make_password(new_password)
            user.save()

            # Mark the token as used in the session
            request.session["reset_token_used"] = True  # Set the flag to True

            return render(
                request,
                "reset_password.html",
                {
                    "success": "Your password has been reset successfully. You can now log in with your new password."
                },
            )
        else:
            return render(
                request,
                "reset_password.html",
                {"errors": {"new_password": "Invalid or expired token."}},
            )


class UserInfoView(APIView):
    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
