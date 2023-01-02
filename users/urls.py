from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("token-login", obtain_auth_token),
    path("jwt-login", views.JWTSignInAPIView.as_view()),
    path("signup", views.SignUpAPIView.as_view()),
    path("me", views.MeAPIView.as_view()),
    path("signin", views.SignInAPIView.as_view()),
    path("signout", views.SignOutAPIView.as_view()),
]
