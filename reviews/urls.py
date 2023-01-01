from django.urls import path

from .views import MyReviewsAPIView, RoomReviewAPIView

urlpatterns = [
    path("My", MyReviewsAPIView.as_view()),
    path("RoomReview/<int:pk>", RoomReviewAPIView.as_view()),  # TODO : url.
]
