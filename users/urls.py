from django.urls import path

from . import views

urlpatterns = [
    path("signup", views.SignUpAPIView.as_view()),
    path("me", views.MeAPIView.as_view()),
    path("signin", views.SignInAPIView.as_view()),
    path("signout", views.SignOutAPIView.as_view()),
]
