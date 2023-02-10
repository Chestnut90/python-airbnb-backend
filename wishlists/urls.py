from django.urls import path
from . import views

urlpatterns = [
    path("", views.WishlistsAPIView.as_view()),
    path("<int:pk>", views.WishlistAPIView.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", views.WishlistToggleAPIView.as_view()),
]
