from django.db import models
from django.conf import settings

from TorLinkRotator.apps.rotator.validators import RecipientValidator, OnionV3Validator
from TorLinkRotator.apps.rotator.managers import OnionLinkManager

from datetime import timedelta


class OnionLinkModel(models.Model):
    
    recipient = models.CharField(
        null=True,
        unique=True,
        max_length=256,
        validators=[RecipientValidator()]
    )
    onion_id = models.CharField(
        unique=True,
        max_length=56,
        validators=[OnionV3Validator()]
    )
    config_index =  models.PositiveIntegerField()
    physical_folder_path = models.FilePathField(
        null=True,
        allow_files=False,
        allow_folders=True
    )
    status = models.PositiveIntegerField(
        db_index=True,
        default=0,
        choices=[
            (0, "Active"),
            (1, "Pending deletion")
        ]
    )
    date_create = models.DateTimeField(
        verbose_name='date create',
        auto_now_add=True
    )

    objects = OnionLinkManager()

    @property
    def expire_date(self):
        return self.date_create + timedelta(seconds=settings.TOR_HIDDEN_SERVICE_EXPIRE)
