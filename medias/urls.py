from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>", views.PhotoAPIView.as_view()),
]
