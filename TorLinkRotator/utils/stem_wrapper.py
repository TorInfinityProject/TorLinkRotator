from django.conf import settings
from django.http import HttpResponse
from rest_framework.exceptions import APIException

import random
import logging
from functools import wraps
from stem.control import Controller


stem_logger = logging.getLogger('tor-stem')


def stem_wrapper(function=None, rest=False, config_index=None):
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            nonlocal config_index
            try:
                if config_index is None:
                    config_index = random.choice(range(len(settings.TOR_CONTROL_PORTS)))
                conn, auth = settings.TOR_CONTROL_PORTS[config_index]
                if isinstance(conn, tuple) and len(conn) == 2:
                    controller = Controller.from_port(address=conn[0], port=conn[1])
                elif isinstance(conn, str):
                    controller = Controller.from_socket_file(path=conn)
                else:
                    raise Exception("Wrong format for TOR_CONTROL_PORTS var or creditinals.")
                controller.authenticate(password=auth)
                setattr(controller, '_config_index', config_index)
            except Exception as e:
                msg = "Error while creating stem connection, please check tor-stem.log file."
                stem_logger.critical(f"{msg}{e}", exc_info=True)
                if isinstance(rest, bool):
                    if rest:
                        raise APIException(detail=msg, code=500)
                    else:
                        return HttpResponse(content=msg, status=500)
                else:
                    return msg
            
            func_response = view_func(stem_controller=controller, *args, **kwargs)
            controller.close()
            return func_response
        
        return _wrapped_view
    
    if function:
        return decorator(function)    
    return decorator
