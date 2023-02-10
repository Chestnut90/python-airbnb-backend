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
        # TODO : pagination
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except:
            page = 1

        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_room(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)
