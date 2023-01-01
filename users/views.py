from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import User


class SignUpAPIView(APIView):
    """sign up api"""

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise exceptions.ParseError("no password input")  # no password

        # TODO : check password condition.
        serializer = serializers.UserPrivateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(
                serializers.UserPrivateSerializer(user).data,
            )

        return exceptions.ParseError(serializer.errors)


class MeAPIView(APIView):
    """Private User API"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            serializers.UserPrivateSerializer(request.user).data,
        )

    def put(self, request):
        serializer = serializers.UserPrivateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated = serializer.save()
            return Response(serializers.UserPrivateSerializer(updated).data)
        raise exceptions.ParseError(serializer.errors)

    def delete(self, request):
        # TODO : how to check password before deletion to account
        user = request.user
        logout(request)  # release session
        user.delete()
        return Response(status.HTTP_200_OK)


class SignInAPIView(APIView):
    """Sign in API"""

    def post(self, request):
        # TODO : add email sign-in
        username = request.data.get("username")
        password = request.data.get("password")

        if not username and not password:
            raise exceptions.ParseError("no data")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(
                serializers.UserPublicSerialzier(user).data,
                status=status.HTTP_200_OK,
            )

        if not User.objects.filter(username=username).exists():
            raise exceptions.ParseError("no matched id")
        raise exceptions.ParseError("invaid password")


class SignOutAPIView(APIView):
    """Sign out API"""

    def post(self, request):
        logout(request)
        return Response(status.HTTP_200_OK)
