from django.urls import path

from . import views

urlpatterns = [
    path("see_all_room", views.see_all_rooms),
    path("", views.RoomsAPIView.as_view()),
    path("<int:pk>", views.RoomAPIView.as_view()),
    path("<int:pk>/reviews", views.RoomReviewsAPIView.as_view()),
    path("<int:pk>/bookings", views.RoomBookingsAPIView.as_view()),
    path("amenities", views.AmenitiesAPIView.as_view()),
    path("amenities/<int:pk>", views.AmenityAPIView.as_view()),
]
