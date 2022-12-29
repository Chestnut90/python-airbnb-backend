from django.urls import path

from . import views

urlpatterns = [
    path("", views.RoomsAPIView.as_view()),
    path("<int:pk>", views.RoomAPIView.as_view()),
    path("<int:pk>/reviews", views.RoomReviewsAPIView.as_view()),
    path("amenities", views.AmenitiesAPIView.as_view()),
    path("amenities/<int:pk>", views.AmenityAPIView.as_view()),
]
