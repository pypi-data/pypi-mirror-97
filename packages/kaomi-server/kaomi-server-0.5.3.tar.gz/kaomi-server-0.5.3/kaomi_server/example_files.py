SERVER_CONF_EXAMPLE = """
[global]

# connection info
server.socket_host: "0.0.0.0"
server.socket_port: 47000
server.thread_pool: 8
server.socket_timeout: 60
response.timeout: 3600
server.max_request_body_size: 0

# ad hoc max request size
lisp.request.max_size_mb: 2

# max size for file uploads
lisp.file_upload.max_size_mb: 200

# chunk size for file upload
lisp.file_upload.chunk_size_mb: 5

# ssl (to enable ssl de-comment lines below and replace placeholders)
#server.ssl_certificate: '< PEM CERT ABS. PATH>'
#server.ssl_private_key: '< PEM KEY ABS. PATH>'

# disabilitazione dell'auto-reload
engine.autoreload.on: False

# set log files
lisp.logging.cherrypy_access.file: '< ACCESS LOG FILE ABS. PATH >'
lisp.logging.cherrypy_error.file: '< ERROR LOG FILE ABS. PATH >'
lisp.logging.cherrypy_app.file: '< APP LOG FILE ABS. PATH >'

lisp.logging.cherrypy_access.level: 'ERROR'
lisp.logging.cherrypy_error.level: 'ERROR'
lisp.logging.cherrypy_app.level: 'DEBUG'
lisp.logging.cherrypy_console.level: 'ERROR'

lisp.verbose_errors_responses: False

"""

APIKEY_CONF_FOLDER = "conf.d"

APIKEY_CONF_EXAMPLE = """
# CONFIGURAZIONE DI BASE

[DEFAULT]
# apikey
key = <SET API KEY HERE>

# ip autorizzati
allow-ip = 127.0.0.1
allow-ip = 1.1.1.1
owner = pippo
group = pippo

actions-shell = /bin/bash
actions-timeout = 100

dir-perms = 0750
file-perms = 0640

##########################################
########## ALIASES DEPLOYMENT ############
##########################################

[ALIASES]

BASE = /home/pippo

##########################################
########## DIRECTORY DEPLOYMENT ##########
##########################################

[folder:/tmp]
# the files written in this directory will have the following owner/group and permissions
dir-perms = 0750

[folder:/home/pippo/Downloads]
# the files written in this directory will have the following owner/group and permissions
owner = redis
group = redis

file-perms = 0640

[folder:##BASE##/Downloads/folder1]
[folder:##BASE##/Downloads/fodler2/]

##########################################
########### AZIONI DEPLOYMENT ############
##########################################

[action:riavvia_nginx]
# commands executed on the server when the action is called
service nginx restart

[action:migra_database]
# commands executed on the server when the action is called
echo "Migrating database!"

"""

