from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ReviewSerializer

# for testing.
class MyReviewsAPIView(APIView):

    """My Reviews API"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            ReviewSerializer(request.user.reviews.all(), many=True).data,
        )
