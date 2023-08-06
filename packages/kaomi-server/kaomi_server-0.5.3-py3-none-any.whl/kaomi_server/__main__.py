import sys
import cherrypy
import argparse
from .functions import file_check, folder_check, create_config_dir, generate_apikey
from .kaomi_server import start_server


# parser per gli argomenti via linea di comando
arg_parser = argparse.ArgumentParser(prog='python -m kaomi_server', description="Kaomi server (TM)")


subparsers = arg_parser.add_subparsers(help='help for subcommand', dest='subcommand', required=True)

# create the parser for the "start" command
parser_start = subparsers.add_parser('start', help='Starts the server')
parser_start.add_argument('--config', type=file_check, dest='server_config_path', metavar="config_path", required=True, help="Path of the configuration file for the server")
parser_start.add_argument('--apikey', type=folder_check, dest='apikey_configs_folder', metavar="apikey_configs_path", required=True, help="Path of the folder containing apikey's configs")

# create the parser for the "configure" command
parser_configure = subparsers.add_parser('configure', help='Configure a directory to store configuration files')
parser_configure.add_argument('--folder', type=folder_check, dest='configs_folder', metavar="configs_folder", required=True, help='Path where to create the example config for server and api keys')

# create the parser for the "apikey" command
parser_apikey = subparsers.add_parser('gen-api-key', help='Prints a secure apikey for the configuration')

# parso gli argomenti passati alla chiamata
args = arg_parser.parse_args(sys.argv[1:])

# svuoto il timestamp dal logging di cherrypy perché non venga stampato due volte
cherrypy._cplogging.LogManager.time = lambda self: ""

if args.subcommand == 'configure':
    try:
        create_config_dir(args.configs_folder)
    except RuntimeError as e:
        print("{}".format(e))

elif args.subcommand == 'start':
    start_server(config_file=args.server_config_path, apikey_folder=args.apikey_configs_folder)
elif args.subcommand == 'gen-api-key':
    print(generate_apikey())
else:
    print("The subcommand is invalid. This should not happen. Bug.")
