import copy
import logging
import os
import json
import argparse
import secrets
import string

import cherrypy
from .example_files import APIKEY_CONF_FOLDER, SERVER_CONF_EXAMPLE, APIKEY_CONF_EXAMPLE
from .deployer import Deployer
from .config_file import ConfigFile

def folder_check(path):
    """ Funzione di controllo delle cartelle passate via linea di comando """
    if not os.path.isabs(path):
        # path non assoluto
        raise argparse.ArgumentTypeError('The path must be absolute')
    if not os.path.isdir(path):
        # file non trovato
        raise argparse.ArgumentTypeError('Cannot find specified folder {}'.format(path))
    return path


def file_check(path):
    """ Funzione di controllo dei file passati via linea di comando """
    if not os.path.isabs(path):
        # path non assoluto
        raise argparse.ArgumentTypeError('The path must be absolute')
    if not os.path.isfile(path):
        # file non trovato
        raise argparse.ArgumentTypeError('Cannot find specified file {}'.format(path))
    return path


def get_payload_data(request, requested_fields):
    """
    Funzione che data la richiesta restituisce il dizionario contenente il payload parsato
    :param request:             richiesta
    :param requested_fields:    campi che devono essere presenti
    :throw RuntimeError:        nel caso si verificasse qualche problema con la richiesta
                                nel caso venga sollevata un'eccezione, conterrà una stringa contenente il dizionario da restituire al chiamante
    :return:                    dizionario contenente i dati
    """

    verbose = cherrypy.config.get('lisp.verbose_errors_responses', False)

    try:
        # ottengo la dimensione del payload
        content_length = int(request.headers['Content-Length'])

        # ottengo la dimensione massima ammissibile (definita ad hoc) dalla configurazione
        max_request_size = cherrypy.config.get('lisp.request.max_size_mb', 2) * 1000**2

        # controllo sulla dimensione massima ammissibile
        if content_length > max_request_size:
            # la dimensione della richiesta supera la dimensione massima consentita
            raise RuntimeError(build_response(status=1, substatus=1, message="Payload content-length greater than maximum allowed", data="Max size: {} MB".format(max_request_size) if verbose else ''))

        # per ovviare al fatto che la grandezza del payload potrebbe non coincidere con quella dichiarata nel content-length,
        # andiamo a leggere solo content_length dati
        payload = json.loads(request.body.read(content_length))
    except json.JSONDecodeError:
        # errore nella decodifica del json
        raise RuntimeError(build_response(status=1, substatus=2, message="Json content cannot be parsed" if verbose else ''))
    except ValueError:
        # errore nel casting per il content_length
        raise RuntimeError(build_response(status=1, substatus=3, message="Content-length not specified or not valid integer" if verbose else ''))

    # controllo che tutti i campi richiesti siano presenti nel payload
    if not all(k in payload for k in requested_fields):
        raise RuntimeError(build_response(status=1, substatus=4, message="Missing fields in JSON" if verbose else '', data=requested_fields if verbose else None))

    return payload


def build_response(status, substatus, message="", data=None):
    """
    Funzione per la creazione della risposta del server
    :param status:      stato della richiesta (int)
    :param substatus:   sotto-stato della richiesta (int)
    :param message:     messaggio descrittivo del sottostato
    :param data:        eventuali dati di output
    """
    return json.dumps({
        "status": status,
        "substatus": substatus,
        "message": message,
        "data": data
    })


def create_config_dir(path):
    """
    Funzione per la creazione dei file di configurazione di esempio del server e delle apikey
    :param path:            cartella nella quale vengono creati gli esempi
    :throw RuntimeError:    nel caso si verifichi un errore
    """
    if not os.path.isdir(path):
        # la cartella non si trova
        raise RuntimeError('Cannot find specified directory "{}".'.format(path))

    # creo la directory per le configurazioni dell'apikey
    apikey_conf_folder = os.path.join(path, APIKEY_CONF_FOLDER)
    try:
        # la cartella non viene sovrascritta, nel caso esista si deve eliminarla
        os.mkdir(apikey_conf_folder)
    except (OSError, FileExistsError) as e:
        raise RuntimeError('Something went wrong creating folder {}. Error: {}'.format(apikey_conf_folder, e))

    # ottengo i path dei file di esempio
    server_conf_path = os.path.join(path, 'server.conf.example')
    apikey_conf_path = os.path.join(apikey_conf_folder, 'dashboard.ini.example')

    # scrivo i file di esempio
    try:
        # i file nel caso dovessero esistere vengono sovrascritti

        with open(server_conf_path, 'w') as fh:
            # file conf server
            fh.write(SERVER_CONF_EXAMPLE)
        with open(apikey_conf_path, 'w') as fh:
            # file conf apikey
            fh.write(APIKEY_CONF_EXAMPLE)
    except OSError as e:
        # nel caso qualcosa vada storto con la scrittura dei file segnalo il problema al chiamante
        raise RuntimeError('Something went wrong trying to create example files. Error: {}'.format(e))


def default_error_handler(status, message, traceback, version):
    """
    Funzione per la mascheratura degli errori del server (500, etc)
    """
    # gli errori vengono loggati in automatico da cherrypy

    logging.info("Default error handler called: status={}, message='{}', traceback:{}".format(status, message, traceback))

    # imposto lo stato della risposta
    cherrypy.response.status = 500

    # imposto il contenuto della risposta
    return json.dumps({'status': 2, 'substatus': 0, 'message': 'Oops, something went wrong', 'data': None})

    # volendo si possono fare altre azioni come inviare un email

def err_404_error_handler(status, message, traceback, version):
    """
    Funzione per gestire gli errori 404
    """
    # gli errori vengono loggati in automatico da cherrypy

    logging.info("Default error handler called: {} {} {}".format(status, message, traceback))

    # imposto lo stato della risposta
    cherrypy.response.status = 404

    # imposto il contenuto della risposta
    return json.dumps({'status': 2, 'substatus': 0, 'message': 'The requested path does not exist.'})


def load_apikey_configs(apikey_folder):
    """
    Procedura per l'ottenimento del dizionario
    :param apikey_folder:   cartella in cui sono presenti le configs
    :throw RuntimeError:    cartella non esiste, errore nel parse delle config, etc.
    :return:                dizionario con i deployers { 'apikey' : <Deployer> }
    """
    # dizionario che verrà restituito come output
    deployers_dict = {}

    l = logging.getLogger('app')

    loaded_configs = []

    try:
        # lettura delle configurazioni dalla cartella delle config
        for config_file in os.listdir(apikey_folder):
            # controllo che la configurazione abbia il formato corretto
            if os.path.splitext(config_file)[-1].lower() == '.ini':
                # inizializzo un oggetto configurazione
                this_config = ConfigFile(os.path.join(apikey_folder, config_file))
                this_config_dict = this_config.to_dict()

                this_apikey = this_config_dict['default']['key']

                # creo il deployer per questa configurazione
                deployers_dict[this_apikey] = Deployer(configuration=this_config_dict), this_config_dict['default'].get('allow-ip', None)

                # il caricamento ha avuto successo
                loaded_configs.append(os.path.basename(config_file))
            else:
                # altrimenti ignoro il file
                continue
        # finito il caricamento di tutte le config, restituisco il dizionario con i deployer
        l.info('Api configurations loaded successfully: {}'.format(', '.join(loaded_configs)))

        return deployers_dict
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        # try/except esterno al for in modo da bloccare il funzionamento se esiste anche un'unica config errata
        l.error('An error occurred loading api key configs. Error {}: {}'.format(type(e), e))
        raise RuntimeError('An error occurred loading api key configs. Error {}: {}'.format(type(e), e))


def log_api_call(request, data, result):
    l = logging.getLogger('app')

    if isinstance(data, dict):
        # evito di modifcare il dizionario del chiamante
        data = data.copy()
        # se è presente un api key la tolgo
        if 'apikey' in data:
            data['apikey'] = '(omitted)'

        data = json.dumps(data, default=str)

    if len(data) > 300:
        data = data[:300] + '...(truncated)'

    if isinstance(result, dict):
        result = json.dumps(result, default=str)

    if len(result) > 300:
        result = result[:300] + '...(truncated)'

    l.debug('{} {} {} {}'.format(request.remote.ip, cherrypy.url(qs=cherrypy.request.query_string, relative="server"), data, result))


def generate_apikey():
    alphabet = string.ascii_letters + string.digits
    generated_key = ''.join(secrets.choice(alphabet) for i in range(48))
    return generated_key

