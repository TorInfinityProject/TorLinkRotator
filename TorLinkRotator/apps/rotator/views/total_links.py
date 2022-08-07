from rest_framework.views import APIView
from rest_framework.response import Response

from TorLinkRotator.apps.rotator.models import OnionLinkModel


class TotalLinksAPIView(APIView):
    
    def get(self, request, format=None):
        return Response(
            data={'status': 'OK', 'total': OnionLinkModel.objects.all().count()},
            status=200
        )
