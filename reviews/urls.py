from django.urls import path

from .views import MyReviewsAPIView

urlpatterns = [
    path("My", MyReviewsAPIView.as_view()),
]
