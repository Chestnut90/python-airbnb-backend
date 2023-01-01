from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import ReviewSerializer

from rooms.models import Room

# for testing.
class MyReviewsAPIView(APIView):

    """My Reviews API"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            ReviewSerializer(request.user.reviews.all(), many=True).data,
        )


class RoomReviewAPIView(APIView):
    """Room Review API"""

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_room(pk)
        # TODO : pagination
        serializer = ReviewSerializer(room.reviews.all(), many=True)
        return Response(serializer.data)
