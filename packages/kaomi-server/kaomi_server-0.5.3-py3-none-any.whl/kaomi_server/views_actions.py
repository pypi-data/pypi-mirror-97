import json
import logging

import cherrypy
from .deployer import ActionNotFoundError
from .functions import get_payload_data, build_response, log_api_call
from . import globals


class Action(object):
    """
    Classe contenitore delle chiamate relative alle azioni
    """

    @cherrypy.expose(['execute'])
    @cherrypy.tools.clear_content_type_parsers()
    def execute_action(self):
        """
        esecuzione di un'azione
        Sono ammesse solo chiamate POST
        :POST param apikey:     apikey che vuole effettuare l'azione
        :POST param action:     nome dell'azione che si vuole eseguire
        """
        if cherrypy.request.method != 'POST':
            # controllo se è una chiamata GET, in tal caso specifico che sono ammesse solo chiamate POST
            res = json.dumps({"status": "1", "message": "Only POST admitted", "data": None})
            log_api_call(request=cherrypy.request, data='(omitted)', result=res)
            return res

        try:
            # ottengo i dati della richiesta
            requested_fields = ['apikey', 'action']
            payload = get_payload_data(request=cherrypy.request, requested_fields=requested_fields)
        except RuntimeError as e:
            res = '{}'.format(e)
            log_api_call(request=cherrypy.request, data='(omitted)', result=res)
            return res

        apikey, action = payload['apikey'], payload['action']

        try:
            deployer, allowed_ips = globals.DEPLOYERS.get(apikey, (None, None))
            if deployer is None:

                res = build_response(status=2, substatus=1, message="Invalid Apikey")
                log_api_call(request=cherrypy.request, data=payload, result=res)
                return res

            if allowed_ips is not None:
                if cherrypy.request.remote.ip not in allowed_ips:
                    res = build_response(status=2, substatus=6, message="Client ip not allowed")
                    log_api_call(request=cherrypy.request, data=payload, result=res)
                    return res

            action_result = deployer.execute_action(action)
        except ActionNotFoundError as e:
            res = build_response(status=2, substatus=2, message="Action not permitted", data='ActionNotFoundError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res

        except RuntimeError as e:
            res = build_response(status=2, substatus=3, message="A RuntimeError occurred", data='RuntimeError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res

        res = build_response(status=0, substatus=0, message="Action executed", data=action_result)
        log_api_call(request=cherrypy.request, data=payload, result=res)
        return res

