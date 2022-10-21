from rest_framework import serializers

from TorLinkRotator.apps.rotator.validators import OnionV3Validator


class OnionV3Serializer(serializers.Serializer):
    
    onion_id = serializers.RegexField(
        regex=OnionV3Validator.regex,
        min_length=56,
        max_length=56,
        allow_blank=False
    )
