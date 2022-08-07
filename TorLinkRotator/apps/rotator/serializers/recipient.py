from rest_framework import serializers

from TorLinkRotator.apps.rotator.validators import RecipientValidator


class RecipientSerializer(serializers.Serializer):
    
    recipient = serializers.RegexField(
        regex=RecipientValidator.regex,
        min_length=1,
        max_length=256,
        allow_blank=False
    )
