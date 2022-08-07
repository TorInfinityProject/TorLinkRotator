from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from TorLinkRotator.apps.rotator.models import OnionLinkModel
from TorLinkRotator.apps.rotator.serializers import OnionV3Serializer

class RemoveLinkAPIView(APIView):
    
    def get(self, request, format=None):
        serializer = OnionV3Serializer(data=request.GET)
        if serializer.is_valid():
            link_obj = get_object_or_404(OnionLinkModel, onion_id=serializer.validated_data['onion_id'], status=0)
            link_obj.status = 1
            link_obj.save()
            return Response(
                data={'status': 'OK'},
                status=200
            )
        else:
            return Response(
                data={'status': 'FAIL', 'detail': 'onion_id is wrong.'},
                status=200
            )
        
