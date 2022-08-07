from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response

from TorLinkRotator.apps.rotator.serializers import OnionV3Serializer


class CheckLinkAPIView(APIView):
    
    def get(self, request, format=None):
        serializer = OnionV3Serializer(data=request.GET)
        if serializer.is_valid():
            if cache.get(f"onion_{serializer.validated_data['onion_id']}", None) is not None:
                return Response(
                    data={'status': 'OK'},
                    status=200
                )
            else:
                return Response(
                    data={'status': 'FAIL'},
                    status=200
                )
        else:
            return Response(
                data={'status': 'FAIL'},
                status=200
            )
