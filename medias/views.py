from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PhotoSerializer
from .models import Photo


def get_photo(pk: int):
    try:
        return Photo.objects.get(pk=pk)
    except Photo.DoesNotExist:
        raise NotFound


class PhotoAPIView(APIView):
    """Photo api"""

    def get(self, request, pk):
        photo = get_photo(pk)
        return Response(PhotoSerializer(photo).data)
