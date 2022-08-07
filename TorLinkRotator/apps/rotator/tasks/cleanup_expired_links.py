from django.apps import apps
from django.db import models
from django.conf import settings
from django.utils.timezone import make_aware

from TorLinkRotator.celery import app
from TorLinkRotator.utils import stem_wrapper

import shutil 
from datetime import datetime, timedelta


@app.task
def cleanup_expired_links():
    
    def remove(link, stem_controller):
        try:
            if link.physical_folder_path is None:
                response = stem_controller.remove_ephemeral_hidden_service(link.onion_id)
            else:
                response = stem_controller.remove_hidden_service(link.physical_folder_path)
                if response:
                    shutil.rmtree(link.physical_folder_path)
        except Exception as e:
            return False, f"[{link.onion_id}] {str(e)}"
        
        if response:
            return True, f"[{link.onion_id}] OK"
        else:
            return False, f"[{link.onion_id}] Unable to remove hidden service"
    
    filter_query = models.Q(status=1)
    if settings.TOR_HIDDEN_SERVICE_EXPIRE > 0:
        filter_query |= models.Q(date_create__lt=make_aware(datetime.now()) - timedelta(seconds=settings.TOR_HIDDEN_SERVICE_EXPIRE))
        
    expired_links = apps.get_model('rotator', 'OnionLinkModel').objects.filter(filter_query).all()
    
    ids_for_delete = []
    results = []
    for link in expired_links:
        status, *msg = stem_wrapper(function=remove, rest=None, config_index=link.config_index)(link)
        if msg is None:
            results.append(status)
        else:
            results.append(msg[0])
            if status:
                ids_for_delete.append(link.id)

    apps.get_model('rotator', 'OnionLinkModel').objects.filter(id__in=ids_for_delete).delete()
    return results
