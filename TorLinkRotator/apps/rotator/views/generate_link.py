from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import make_aware

from rest_framework.views import APIView
from rest_framework.response import Response

from TorLinkRotator.utils import stem_wrapper
from TorLinkRotator.apps.rotator.serializers import RecipientSerializer
from TorLinkRotator.apps.rotator.models import OnionLinkModel

import hashlib
from datetime import datetime, timedelta


class GenerateLinkAPIView(APIView):

    @stem_wrapper(rest=True)
    def get(self, request, stem_controller, format=None):
        recipient = request.headers.get('X-RECIPIENT-ID', None)
        if recipient is not None:
            serializer = RecipientSerializer(data={'recipient': recipient})
            if not serializer.is_valid():
                recipient = None
            else:
                recipient_md5 = hashlib.md5(recipient.encode()).hexdigest()
                cached = cache.get(f"recipient_{recipient_md5}", None)
                if cached is not None:
                    return Response(
                        data={
                            'status': 'OK', 
                            'scheme': settings.TOR_HIDDEN_SERVICE_SCHEME,
                            'link': f"{cached}.onion"
                        },
                        status=200
                    )
        
        link = OnionLinkModel.objects.get_or_create_link(
            stem_controller=stem_controller, 
            recipient=recipient
        )
        
        if link is None:
            return Response(
                data={'status': 'FAIL', 'detail': 'Unable to create hidden service link.'},
                status=200,
                exception=True
            )
        elif link is not None and (
            link.status != 0 or (
                settings.TOR_HIDDEN_SERVICE_EXPIRE > 0 and link.date_create < make_aware(datetime.now()) - timedelta(seconds=settings.TOR_HIDDEN_SERVICE_EXPIRE)
            )
        ):
            return Response(
                data={'status': 'FAIL', 'detail': 'The link attached to this session has already expired. Delete cookies and refresh the page.'},
                status=200
            )
        else:
            if settings.TOR_HIDDEN_SERVICE_EXPIRE > 0:
                store_time = (link.expire_date - link.date_create).seconds
            else:
                store_time = None

            cache.set_many({
                f"onion_{link.onion_id}": True,
                **({f"recipient_{recipient_md5}": link.onion_id} if recipient is not None else {})
            }, store_time)
            
            return Response(
                data={
                    'status': 'OK',
                    'scheme': settings.TOR_HIDDEN_SERVICE_SCHEME,
                    'link': f"{link.onion_id}.onion"
                },
                status=200
            )
