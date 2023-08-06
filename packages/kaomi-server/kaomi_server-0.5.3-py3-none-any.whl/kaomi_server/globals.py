from . import __version__

# dizionario che conterrà i deployers
DEPLOYERS = {}


# Dizionario contenente la configurazione del logging
# Nota: i file di output vengono sovrascritti all'accensione del server da quelli specificati nella configurazione kaomi

LOG_CONF = {
    'version': 1,

    'formatters': {
        'void': {
            'format': ''
        },
        'standard': {
            'format': '[%(asctime)s][%(levelname)s][%(name)s] %(message)s'
        },
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(message)s'
        }
    },
    
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'cherrypy_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': 'ext://sys.stdout'
        },
        'cherrypy_access': {
            'level': 'INFO',
            'class': 'kaomi_server.log.CompressingRotatingFileHandler',
            'formatter': 'standard',
            'filename': 'access.log',
            'maxBytes': 52428800,
            'backupCount': 100,
            'encoding': 'utf8'
        },
        'cherrypy_error': {
            'level': 'INFO',
            'class': 'kaomi_server.log.CompressingRotatingFileHandler',
            'formatter': 'standard',
            'filename': 'error.log',
            'maxBytes': 52428800,
            'backupCount': 100,
            'encoding': 'utf8'
        },
        'cherrypy_app': {
            'level': 'DEBUG',
            'class': 'kaomi_server.log.CompressingRotatingFileHandler',
            'formatter': 'standard',
            'filename': 'app.log',
            'maxBytes': 52428800,
            'backupCount': 100,
            'encoding': 'utf8'
        },
    },

    'loggers': {
        '': {
            'handlers': ['cherrypy_app'],
            'level': 'DEBUG'
        },
        'cherrypy.app': {
            'handlers': ['cherrypy_app'],
            'level': 'DEBUG'
        },
        'cherrypy.access': {
            'handlers': ['cherrypy_access'],
            'level': 'DEBUG',
            'propagate': False
        },
        'cherrypy.error': {
            'handlers': ['cherrypy_console', 'cherrypy_error'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


# la versione del server viene presa dall'init
SERVER_VERSION = __version__


# conterrà l'umask iniziale del processo, da utilizzare dopo, prima che i thread abbiano l'occasione di creare race conditions
original_umask = None
# lock che dovrà essere acquisito prima di fare ogni operazione che è influenzata dall'umask del processo (creare file/directory, lanciare sottoprocessi, etc)
# dovrà essere rilasciato appena è stato creato il file/cartella o lanciato il sottoprocesso
umask_lock = None