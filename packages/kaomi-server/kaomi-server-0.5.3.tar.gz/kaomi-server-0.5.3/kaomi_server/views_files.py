import os
import json
import logging
import cherrypy

from . import globals
from .functions import build_response, get_payload_data, log_api_call


class File(object):
    """
    Api server per il deployment
    """

    @staticmethod
    def __get_and_validate_perms(value):
        """
        Funzione di controllo dei permessi ottenuti via POST e ritorna i permessi utilizzabili dal deployer
        :param value:                   permessi indicati come stringa contenente un numero ottale
        :throw ValueError:              nel caso il permesso non sia un numero ottale
        :return:                        valore dei permessi come intero decimale
        """
        try:
            permissions = int(value, 8)
        except ValueError as e:
            # il numero passato non è convertibile
            raise ValueError('Permissions must be specified as an octal number (eg. 0o777, 0o0777, 0777, 777, etc.). ValueError: {}'.format(e))

        return permissions

    @cherrypy.expose(['upload'])
    def upload_file(self, *args, **kargs):
        """
        Vista per il caricamento di un file a chunk
        Sono ammesse solo chiamate POST
        :POST param apikey:     apikey che vuole effettuare l'azione
        :POST param file:       file da caricare
        :POST param dest_path:  destinazione del file (comprensiva del nome)
        :POST param perms:      permessi da impostare sul file (default = None)
        :POST param overwrite:  indica se eliminare il file nel caso esistesse (default = False)
        """

        verbose = cherrypy.config.get('lisp.verbose_errors_responses', False)

        if cherrypy.request.method != 'POST':
            # controllo se è una chiamata GET, in tal caso specifico che sono ammesse solo chiamate POST
            res = build_response(status=1, substatus=0, message="Only POST admitted")
            log_api_call(request=cherrypy.request, data='(omitted)', result=res)
            return res

        # controllo la presenza di tutti i campi necessari
        requested_fields = ['apikey', 'file', 'dest_path']
        if not all(k in kargs for k in requested_fields):
            res = build_response(status=1, substatus=4, message="Missing fields in JSON" if verbose else '', data=requested_fields if verbose else '')
            log_api_call(request=cherrypy.request, data=kargs, result=res)
            return res

        apikey = kargs['apikey']
        input_handle = kargs['file'].file
        dest_path = kargs['dest_path']
        overwrite_flag = kargs['overwrite'].lower().strip() == 'true' if 'overwrite' in kargs else False

        # provo ad ottenere i permessi dalla richiesta, mi arrivano come stringa contenente un ottale
        if 'perms' in kargs and kargs['perms'] is not None and len(kargs['perms']) > 0:
            try:
                # provo ad ottenere i permessi
                perms = self.__get_and_validate_perms(kargs['perms'])
            except ValueError as e:
                # nel caso non riesca ad ottenere i permessi ma questi ci siano, segnalo l'errore al client
                res = build_response(status=1, substatus=5, message="ValueError in request data", data="{}".format(e))
                log_api_call(request=cherrypy.request, data=kargs, result=res)
                return res
        else:
            # non sono stati specificati dei permessi, o sono vuoti
            perms = None

        # ottengo il file handle per poter scrivere il file sul server
        try:
            deployer, allowed_ips = globals.DEPLOYERS.get(apikey, (None, None))
            if deployer is None:
                res = build_response(status=2, substatus=1, message="Invalid Apikey")
                log_api_call(request=cherrypy.request, data=kargs, result=res)
                return res

            if allowed_ips is not None:
                if cherrypy.request.remote.ip not in allowed_ips:
                    res = build_response(status=2, substatus=6, message="Client ip not allowed")
                    log_api_call(request=cherrypy.request, data=kargs, result=res)
                    return res

            output_handle, output_file_path = deployer.get_file_uploader(filepath=dest_path, overwrite=overwrite_flag, permissions=perms)
        except PermissionError as e:
            res = build_response(status=2, substatus=2, message="Action not permitted", data='PermissionError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=kargs, result=res)
            return res
        except RuntimeError as e:
            res = build_response(status=2, substatus=3, message="A RuntimeError occurred", data='RuntimeError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=kargs, result=res)
            return res
        except FileExistsError as e:
            res = build_response(status=2, substatus=4, message="File already exists", data='FileExistsError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=kargs, result=res)
            return res

        # se sono arrivato qua sono sicuro che il file handle di output è valido

        # caricamento del file per chunk

        # inizializzo i valori per la massima dimensione del file e il chunk utilizzato
        max_size_mbytes = cherrypy.config.get('lisp.file_upload.max_size_mb', 100)
        max_size_bytes = max_size_mbytes * 1000 * 1000
        chunk_size = cherrypy.config.get('lisp.file_upload.chunk_size_mb', 5) * 1024 * 1024

        while True:
            # leggo un chunk alla volta
            data = input_handle.read(chunk_size)
            if not data:
                # non ci sono più dati da scrivere, ho finito
                break
            # scrivo il file
            output_handle.write(data)

            if output_handle.tell() > max_size_bytes:
                # il file ha sforato la dimensione massima

                # chiudo gli handle aperti dei file
                input_handle.close()
                output_handle.close()

                try:
                    # provo a rimuovere il file scritto parzialmente
                    os.remove(output_file_path)
                except (OSError, Exception) as e:
                    logging.error('Something went wrong deleting partial uploaded file "{}". Exception: {}'.format(output_file_path, e))

                # ritorno l'errore al chiamante
                res = build_response(status=2, substatus=5, message="File exceed maximum dimension", data="Max size: {} MB".format(max_size_mbytes))
                log_api_call(request=cherrypy.request, data=kargs, result=res)
                return res

        # arrivato qua il file è stato completamente caricato
        # chiudo gli handle
        input_handle.close()
        output_handle.close()

        res = build_response(status=0, substatus=0, message="File uploaded correctly")
        log_api_call(request=cherrypy.request, data=kargs, result=res)
        return res

    @cherrypy.expose(['mkdir'])
    @cherrypy.tools.clear_content_type_parsers()
    def create_directory(self):
        """
        creazione di una cartella
        Sono ammesse solo chiamate POST
        :JSON param apikey:     apikey che vuole effettuare l'azione
        :JSON param path:       path della cartella da creare
        :JSON param perms:      permessi della cartella da creare (default = None)
        :JSON param overwrite:  indica se sovrascrivere la cartella nel caso esistesse (default = False)
        """
        if cherrypy.request.method != 'POST':
            # controllo se è una chiamata GET, in tal caso specifico che sono ammesse solo chiamate POST
            res = build_response(status=1, substatus=0, message="Only POST admitted")
            log_api_call(request=cherrypy.request, data='(omitted)', result=res)
            return res

        try:
            # ottengo i dati della richiesta
            requested_fields = ['apikey', 'path']
            payload = get_payload_data(request=cherrypy.request, requested_fields=requested_fields)
        except RuntimeError as e:
            res = '{}'.format(e)
            log_api_call(request=cherrypy.request, data='(omitted)', result=res)
            return res

        apikey = payload['apikey']
        path = payload['path']
        overwrite = payload['overwrite'].lower().strip() == 'true' if 'overwrite' in payload else False

        # provo ad ottenere i permessi dalla richiesta, mi arrivano come stringa contenente un ottale
        if 'perms' in payload and payload['perms'] is not None and len(payload['perms']) > 0:
            try:
                # provo ad ottenere i permessi
                perms = self.__get_and_validate_perms(payload['perms'])
            except ValueError as e:
                # nel caso non riesca ad ottenere i permessi ma questi ci siano, segnalo l'errore al client
                res = build_response(status=1, substatus=5, message="ValueError in request data", data="{}".format(e))
                log_api_call(request=cherrypy.request, data=payload, result=res)
                return res
        else:
            # non sono stati specificati dei permessi, o sono vuoti
            perms = None

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

            deployer.create_folder(folderpath=path, overwrite=overwrite, permissions=perms)
        except PermissionError as e:
            res = build_response(status=2, substatus=2, message="Action not permitted", data='PermissionError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res
        except RuntimeError as e:
            res = build_response(status=2, substatus=3, message="A RuntimeError occurred", data='RuntimeError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res
        except FileExistsError as e:
            res = build_response(status=2, substatus=4, message="Folder already exists", data='FileExistsError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res

        res = build_response(status=0, substatus=0, message="Folder created")
        log_api_call(request=cherrypy.request, data=payload, result=res)
        return res

    @cherrypy.expose('delete_node')
    @cherrypy.tools.clear_content_type_parsers()
    def delete_filesystem_node(self):
        """
        eliminazione di un nodo del filesystem
        Sono ammesse solo chiamate POST
        :JSON param apikey:     apikey che vuole effettuare l'azione
        :JSON param path:       path del nodo da eliminare
        """
        if cherrypy.request.method != 'POST':
            # controllo se è una chiamata GET, in tal caso specifico che sono ammesse solo chiamate POST
            res = json.dumps({"status": "1", "message": "Only POST admitted", "data": None})
            log_api_call(request=cherrypy.request, data='(omitted)', result=res)
            return res

        try:
            # ottengo i dati della richiesta
            requested_fields = ['apikey', 'path']
            payload = get_payload_data(request=cherrypy.request, requested_fields=requested_fields)
        except RuntimeError as e:
            res = '{}'.format(e)
            log_api_call(request=cherrypy.request, data='(omitted)', result=res)
            return res

        apikey, path = payload['apikey'], payload['path']

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

            deployer.delete_filesystem_node(to_delete_path=path)
        except PermissionError as e:
            res = build_response(status=2, substatus=2, message="Action not permitted", data='PermissionError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res
        except RuntimeError as e:
            res = build_response(status=2, substatus=3, message="A RuntimeError occurred", data='RuntimeError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res
        except FileNotFoundError:
            res = build_response(status=0, substatus=1, message="Filesystem node not found")
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res

        res = build_response(status=0, substatus=0, message="Filesystem node deleted")
        log_api_call(request=cherrypy.request, data=payload, result=res)
        return res

    @cherrypy.expose('delete_by_regex')
    @cherrypy.tools.clear_content_type_parsers()
    def delete_by_regex(self):
        """
        eliminazione di un nodo del filesystem
        Sono ammesse solo chiamate POST
        :JSON param apikey:                apikey che vuole effettuare l'azione
        :JSON param path:                  path del nodo da eliminare
        :JSON param regex:                 regex con cui verificare se eliminare un elemento
        :JSON param inverted:              parametro che indica se invertire il matche effettuato dalla regex
        :JSON param node_type:             indica se considerare solo file, solo cartelle o entrambi nell'eliminazione
        :JSON param include_subdirs:       indica se considerare solo la directory corrente o anche le sottodirectory per le eliminazioni

        """
        if cherrypy.request.method != 'POST':
            # controllo se è una chiamata GET, in tal caso specifico che sono ammesse solo chiamate POST
            res = json.dumps({"status": "1", "message": "Only POST admitted", "data": None})
            log_api_call(request=cherrypy.request, data='(omitted)', result=res)
            return res

        try:
            # ottengo i dati della richiesta
            requested_fields = ['apikey', 'path', 'regex', 'node_type']
            payload = get_payload_data(request=cherrypy.request, requested_fields=requested_fields)
        except RuntimeError as e:
            res = '{}'.format(e)
            log_api_call(request=cherrypy.request, data='(omitted)', result=res)
            return res

        apikey, path = payload['apikey'], payload['path']
        regex, node_type = payload['regex'], payload['node_type'].lower().strip(),
        inverted = payload['inverted'] if 'inverted' in payload else False
        include_subdirs = payload['include_subdirs'] if 'include_subdirs' in payload else False

        node_type_allowed_values = {'file', 'folder', 'both'}
        if node_type not in node_type_allowed_values:
            res = build_response(status=2, substatus=5, message="ValueError in JSON",  data='The value of node_type parameter is invalid. Allowed values: {}'.format(node_type_allowed_values))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res

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

            errors, too_many_errors = deployer.delete_by_regex(base_path=path, regex=regex, inverted=inverted, node_type=node_type, include_subdirs=include_subdirs)
        except PermissionError as e:
            res = build_response(status=2, substatus=2, message="Action not permitted", data='PermissionError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res
        except RuntimeError as e:
            res = build_response(status=2, substatus=3, message="A RuntimeError occurred", data='RuntimeError: {}'.format(e))
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res
        except FileNotFoundError:
            res = build_response(status=0, substatus=1, message="Filesystem node not found")
            log_api_call(request=cherrypy.request, data=payload, result=res)
            return res

        res = build_response(status=0, substatus=0 if len(errors) == 0 else 3, message="Nodes deleted successfully" if len(errors) == 0 else "Some errors occurred", data={'errors': errors, 'too_many_errors': too_many_errors})
        log_api_call(request=cherrypy.request, data=payload, result=res)
        return res