from django.urls import path

from TorLinkRotator.apps.rotator.views import (
    GenerateLinkAPIView, RemoveLinkAPIView, 
    CheckLinkAPIView, TotalLinksAPIView
)


urlpatterns = [
    path('generate', GenerateLinkAPIView.as_view(), name='generate-link'),
    path('remove', RemoveLinkAPIView.as_view(), name='remove-link'),
    path('check', CheckLinkAPIView.as_view(), name='check-link'),
    path('total', TotalLinksAPIView.as_view(), name='total-links'),
]
