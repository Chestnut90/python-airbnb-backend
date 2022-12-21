from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions as rf_exceptions
from rest_framework import status as rf_status
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import User


class UsersView(APIView):
    """user list"""

    def get(self, request):
        serializer = serializers.UserPublicSerialzier(User.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        """create user (sign up)"""
        serializer = serializers.UserPrivateSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get("password")
            if password is None:
                return Response({"error": "invalid password"})

            new_user = serializer.save()
            new_user.set_password(password)
            new_user.save()
            return Response(serializers.UserPublicSerialzier(new_user).data)
        return Response(serializer.errors)

    def delete(self, request):
        """delete user"""
        serializer = serializers.UserPrivateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "invalid user info"})


class MeView(APIView):
    """Private User API"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            serializers.UserPrivateSerializer(request.user).data,
        )

    def post(self, request):
        serializer = serializers.UserPrivateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated = serializer.save()
            return Response(serializers.UserPrivateSerializer(updated).data)
        return Response(serializer.errors)

    def delete(self, request):
        # TODO : how to check password before deletion to account
        user = request.user
        logout(request)  # release session
        user.delete()
        return Response(rf_status.HTTP_200_OK)


class SignInView(APIView):
    """Sign in API"""

    def post(self, request):
        # TODO : add email sign-in
        username = request.data.get("username")
        password = request.data.get("password")

        if not username and not password:
            raise rf_exceptions.ParseError("no data")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(serializers.UserPublicSerialzier(user).data)

        if not User.objects.filter(username=username).exists():
            return Response({"status": "no id"})
        return Response({"status": "invaid password"})


class SignOutView(APIView):
    """Sign out API"""

    def post(self, request):
        logout(request)
        return Response(rf_status.HTTP_200_OK)
