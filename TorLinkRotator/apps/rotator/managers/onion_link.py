from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import uuid
import logging
from stem.control import Controller


stem_logger = logging.getLogger('tor-stem')


class OnionLinkManager(models.Manager):
    
    def _create_ephemeral_hidden_service(self, stem_controller):
        return stem_controller.create_ephemeral_hidden_service(
            ports={k: (':'.join([str(_) for _ in v]) if isinstance(v, tuple) else v) for k, v in settings.TOR_HIDDEN_SERVICE_PORTS.items()},
            key_type='NEW',
            key_content='ED25519-V3',
            discard_key=True,
            detached=True,
            await_publication=False,
            timeout=30,
            max_streams=settings.TOR_HIDDEN_SERVICE_MAX_STREAMS
        )
    
    def _create_hidden_service(self, stem_controller):
        path = f"{settings.TOR_HIDDEN_SERVICE_FOLDER}{str(uuid.uuid4()).replace('-', '')}"
        first_port, first_target = next(iter(settings.TOR_HIDDEN_SERVICE_PORTS.items()))
        response = stem_controller.create_hidden_service(
            path=path,
            port=first_port,
            target_address=first_target[0] if isinstance(first_target, tuple) else first_target,
            target_port=first_target[1] if isinstance(first_target, tuple) else None
        )
        
        conf = response.config
        conf_changed = False
        
        if len(settings.TOR_HIDDEN_SERVICE_PORTS.keys()) > 1:
            conf[path].update({
                'HiddenServicePort': [(k, v[0], v[1]) if isinstance(v, tuple) else (k, v) for k, v in settings.TOR_HIDDEN_SERVICE_PORTS.items()],
            })
            conf_changed = True
        
        if settings.TOR_HIDDEN_SERVICE_MAX_STREAMS is not None:
            conf[path].update({
                'HiddenServiceMaxStreams': settings.TOR_HIDDEN_SERVICE_MAX_STREAMS,
                'HiddenServiceMaxStreamsCloseCircuit': 1
            })
            conf_changed = True
        
        if conf_changed:
            stem_controller.set_hidden_service_conf(conf)
        
        return response
    
    def create_link(self, stem_controller: Controller, recipient=None):
        try:
            if settings.TOR_HIDDEN_SERVICE_FOLDER is None:
                response = self._create_ephemeral_hidden_service(stem_controller)
                onion_id = getattr(response, 'service_id', None)
                path = None
            else:
                response = self._create_hidden_service(stem_controller)
                onion_id = getattr(response, 'hostname', None)
                if onion_id is not None:
                    onion_id = onion_id.split('.')[0]
                path = response.path
            assert onion_id is not None, "Unable to read hidden service hostname."
        except Exception as e:
            stem_logger.critical(f"Unable to create hidden service. {e}", exc_info=True)
            return None
        
        return self.create(
            recipient=recipient,
            onion_id=onion_id,
            config_index=stem_controller._config_index,
            physical_folder_path=path
        )
    
    def get_or_create_link(self, stem_controller: Controller, recipient=None):
        if recipient is not None:
            try:
                return self.get_queryset().get(recipient=recipient)
            except ObjectDoesNotExist:
                pass
        
        return self.create_link(stem_controller, recipient)
