import requests
import jwt

from django.contrib.auth import login, logout, authenticate
from django.conf import settings

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

        raise exceptions.ParseError(serializer.errors)


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
            raise exceptions.ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response(
                {"ok": "Welcome!"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error", "wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class JWTSignInAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},  # un-limited token.
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})

        return Response(
            {"error", "wrong password"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SignOutAPIView(APIView):
    """Sign out API"""

    def post(self, request):
        logout(request)
        return Response(status.HTTP_200_OK)


class SignInWithGithubAPIView(APIView):
    """Github sign in API"""

    def post(self, request):
        code = request.data.get("code")
        url = "https://github.com/login/oauth/access_token"
        client_id = "8d6ae51b717a6e62f340"
        try:
            access_token = requests.post(
                f"{url}?code={code}&client_id={client_id}&client_secret={settings.GITHUB_SECRET_KEY}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")

            # user-data
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
            )
            user_data = user_data.json()
            # user-emails
            user_email = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
            )
            user_email = user_email.json()

            try:
                user = User.objects.get(email=user_email[0]["email"])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_email[0]["email"],
                    name=user_data.get("name"),
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SignInWithKakaoAPIView(APIView):
    def post(self, request):

        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "1cfd4ec5930374d180bdefea46e9b3d8",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(username=kakao_account.get("nickname"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
