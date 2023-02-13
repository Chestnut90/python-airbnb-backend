import requests

from django.conf import settings

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


class GetUploadURLAPIView(APIView):
    """cloud flare images get upload image api"""

    def post(self, request):

        account_id = settings.CLOUD_FLARE_ACCOUNT_ID
        api_token = settings.CLOUD_FLARE_API_TOKEN
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v2/direct_upload"

        cloudflare = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_token}",
            },
        )
        # format of cloudflare response
        # {
        #     "result": {
        #         "id": "2cdc28f0-017a-49c4-9ed7-87056c83901",
        #         "uploadURL": "https://upload.imagedelivery.net/Vi7wi5KSItxGFsWRG2Us6Q/2cdc28f0-017a-49c4-9ed7-87056c83901",
        #     },
        #     "result_info": null,
        #     "success": true,
        #     "errors": [],
        #     "messages": [],
        # }

        # TODO : error handling
        one_time_url = cloudflare.json()
        result = one_time_url.get("result")
        return Response(
            {
                "id": result.get("id"),
                "uploadURL": result.get("uploadURL"),
            }
        )
