from django.urls import path

from . import views

urlpatterns = [
    path("", views.UsersView.as_view()),
    path("me", views.MeView.as_view()),
    path("signin", views.SignInView.as_view()),
    path("signout", views.SignOutView.as_view()),
]
