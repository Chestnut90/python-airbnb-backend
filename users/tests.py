from rest_framework.test import APITestCase

from .models import User


class SignUpTest(APITestCase):

    base_url = "/api/v1/users/signup"
    data = {
        "username": "hello_user",
        "email": "hello_user@google.com",
        "password": "hello_user",
        "gender": "male",
    }

    def test_create_user(self):
        response = self.client.post(self.base_url, data=self.data)

        self.assertEqual(
            response.status_code,
            200,
            response.data,
        )

        # single object
        user = User.objects.get(username=self.data["username"])

        self.assertEqual(
            user.check_password(self.data["password"]),
            True,
            "password not matched.",
        )

    def test_create_user_without_password(self):

        self.data.pop("password")
        response = self.client.post(self.base_url, self.data)

        self.assertEqual(response.status_code, 400, response.data)
