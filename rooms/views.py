from django.db import transaction
from django.utils import timezone
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)

from reviews.serializers import ReviewSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
from medias.serializers import PhotoSerializer
from .models import Amenity, Room
from . import serializers


def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "Hello! this see all room",
        },
    )


def get_amenity(pk):
    """Get Amenity with primary key"""
    try:
        return Amenity.objects.get(pk=pk)
    except Amenity.DoesNotExist:
        raise NotFound("Amenity Not Found.")


class AmenitiesAPIView(APIView):
    """Amenities API"""

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = serializers.AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.AmenitySerializer(data=request.data)
        data = None
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                serializers.AmenitySerializer(amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityAPIView(APIView):
    """Single Amenity API"""

    def get(self, request, pk):
        serializer = serializers.AmenitySerializer(get_amenity(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = get_amenity(pk)
        serializer = serializers.AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                serializers.AmenitySerializer(amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        amenity = get_amenity(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomsAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = serializers.RoomSimpleSerializer(
            rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.RoomSerializer(data=request.data)
        if serializer.is_valid():
            # check amenities
            try:
                amenities = [
                    Amenity.objects.get(pk=pk) for pk in request.data.get("amenities")
                ]
            except Amenity.DoesNotExist:
                raise ParseError("Amenity not founded.")

            with transaction.atomic():
                room = serializer.save(owner=request.user, amenities=amenities)
            serializer = serializers.RoomSerializer(room)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


def get_room(pk):
    try:
        return Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        raise NotFound("Room Not Found.")


class RoomAPIView(APIView):
    # check permission of request user info.
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        room = get_room(pk)
        serializer = serializers.RoomSerializer(room)
        return Response(data=serializer.data)

    def post(self, request, pk):
        pass

    def delete(self, request, pk):
        room = self._get_room(pk)
        room.delete()
        return Response(HTTP_204_NO_CONTENT)


class RoomReviewsAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    _page_size = 2

    def get_reviews_with_page(self, room, page):
        # TODO : no empty list return-able.
        try:
            page = int(page)
        except ValueError:
            page = 1

        page_size = 2  # global value
        start = (page - 1) * page_size
        end = start + page_size

        # room.reviews.all() => query set.
        return room.reviews.all()[start:end]

    def get(self, request, pk):
        room = get_room(pk)

        serializer = ReviewSerializer(
            self.get_reviews_with_page(room, request.query_params.get("page", 1)),
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = get_room(pk)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                review = serializer.save(
                    user=request.user,
                    room=room,
                )
            return Response(ReviewSerializer(review).data)
        else:
            return Response(serializer.errors)


class RoomBookingsAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            check_in__gt=now,
        )
        serializers = PublicBookingSerializer(bookings, many=True)
        return Response(serializers.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data,
            context={"room": room},
        )
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomBookingCheckAPIView(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        # TODO : check_in and out value validation
        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")
        exists = Booking.objects.filter(
            room=room,
            check_in__lte=check_out,
            check_out__gte=check_in,
        ).exists()
        return Response({"ok": not exists})


class RoomPhotoAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_ojbect(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_ojbect(pk)
        if request.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        # print(request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )
