import os
import sys
import signal
import argparse
from .kaomi_client import KaomiClient, ServerError, ActionError
from .globals import PERMS_MASK, SERVER_PORT_DEFAULT, API_PATHS
from .functions import get_client_output, upload_directory, display_output_and_exit, upload_directory_by_regex


def check_perms(value):
    """
    Funzione di controllo dei permessi passati via linea di comando
    Viene applicata conversione e maschera
    :param value:                   valore passato come argomento del parametro indicante i permessi
    :throw ArgumentTypeError:       nel caso il permesso non sia un numero
    :return:                        permessi validi
    """

    try:
        permissions = int(value, 8)
    except ValueError:
        # il numero passato non è convertibile in binario
        raise argparse.ArgumentTypeError('Permissions must be specified as an octal number (eg. 0o777, 0o0777, 0777, 777, etc.)')

    # maschero i permessi per eliminare configurazioni non ammissibili
    perms = permissions & PERMS_MASK

    # vedo se la maschera ha modificato i permessi
    if perms != permissions:
        print('Warning: specified permissions have been masked to {}'.format(oct(perms)))

    return perms


def check_node_type(value):
    value = value.lower().strip()

    allowed = {'file', 'folder', 'both'}
    if value not in allowed:
        raise argparse.ArgumentTypeError('The allowed node types are: {}'.format(allowed))

    return value

def err_on_unused_flags(default, *args):
    for name, value in args:

        if default is None:
            err = value is not None
        else:
            err = value != default

        if err:
            print("The flag {} can't be used with the current mode".format(name))
            sys.exit(1)

def get_arg_parser():
    """
    Funzione per l'inizializzazione dell'argparser da utilizzare
    :return:            istanza dell'arg_parser
    """
    p = argparse.ArgumentParser(description="""
    Kaomi deployer client script.
    This script can be used to deploy folders, files or to execute actions on a server that runs kaomi deployer.

    """, prog="python -m kaomi_client")

    requested_action = p.add_mutually_exclusive_group(required=True)

    # aggiunta degli argomenti da linea di comanda
    p.add_argument('-k', '--key',    type=str, dest='apikey',      metavar="apikey",      required=True,                               help="apikey to be used for authentication.")
    p.add_argument('-s', '--server', type=str, dest='server_host', metavar="server_host", required=True,                               help="server protocol and host.")
    p.add_argument('-p', '--port',   type=int, dest='server_port', metavar="server_port", required=False, default=SERVER_PORT_DEFAULT, help="port of the server to be deployed (default: %(default)s)")

    requested_action.add_argument('-d', '--directory',         nargs=2, dest='directory',        metavar=("local_dir", "remote_dir"),            help="upload directory 'local_dir' to 'remote_dir'.")
    requested_action.add_argument('-dr', '--directory-regex',  nargs=3, dest='directory_regex',  metavar=("local_dir", "remote_dir", "regex"),   help="upload directory files and folders in 'local_dir' to 'remote_dir' only if they (not) match a regex.")
    requested_action.add_argument('-f', '--file',              nargs=2, dest='file',             metavar=("local_file", "remote_file"),          help="upload file 'local_file' to 'remote_file'.")
    requested_action.add_argument('-a', '--action',                     dest='action',           metavar="action_name",                          help="action to be executed")
    requested_action.add_argument('-x', '--delete',                     dest='delete',           metavar="remote_path",                          help="delete specified remote file or directory")
    requested_action.add_argument('-xr', '--delete-regex',     nargs=2, dest='delete_regex',     metavar=("remote_path", "regex"),               help="delete specified files or (sub)directories that (does not) matches a regex")

    p.add_argument('-dp', '--dir-perms',  type=check_perms, dest='dir_perms',  metavar="permissions", required=False, help="permissions to be applied to uploaded folders (default: server defined ones)")
    p.add_argument('-fp', '--file-perms', type=check_perms, dest='file_perms', metavar="permissions", required=False, help="permissions to be applied to uploaded files (default: server defined ones)")

    p.add_argument('-nt', '--node-type',       type=check_node_type, dest='node_type',            metavar="node_type",                      required=False, default='both', help="node types to delete when using regex deletion, can be 'file', 'folder' or 'both' (default: %(default)s)")
    p.add_argument('-is', '--include-subdirs',                       dest='include_subdirs_flag',                      action='store_true', required=False, default=False,  help="specifies whether to include subdirectories when using regex deletion (default: %(default)s)")
    p.add_argument('-i', '--inverted',                               dest='inverted_flag',                             action='store_true', required=False, default=False,  help="specifies whether to delete the not matching files/folders instead of the matching ones when using regex deletion (default: %(default)s)")

    p.add_argument('-o', '--overwrite', dest='overwrite_flag', action='store_true', required=False, default=False, help="specifies if folder/file that already exists on server should be deleted or not (default: %(default)s)")
    p.add_argument('-v', '--verbose',   dest='verbose_flag',   action='store_true', required=False, default=False, help="verbose output (default: %(default)s)")

    return p

def get_client_or_die():
    # provo ad aprire una connessione con il server
    try:
        kaomi_client = KaomiClient(server_host=args.server_host, server_port=args.server_port, apikey=args.apikey, api_paths=API_PATHS)
    except ConnectionError as e:
        display_output_and_exit({'status': 2, 'message': 'Error establishing new connection', 'data': 'ConnectionError: {}'.format(e)})
    # noinspection PyUnboundLocalVariable
    return kaomi_client

def signal_handler(sig, frame):
    print('SIGINT received, exiting.')
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

##########################
########## MAIN ##########
##########################

# inizializzo il parser per gli argomenti via linea di comando
parser = get_arg_parser()
args = parser.parse_args(sys.argv[1:])


# il funzionamento del main risente delle modifiche
if args.action is not None:
    # verifico che le combinazioni siano valide, nel caso che non lo siano esco
    err_on_unused_flags(None,
        ('-dp/--dir-perms', args.dir_perms),
        ('-fp/--file-perms', args.file_perms),
    )
    err_on_unused_flags('both',
        ('-nt/--node-type', args.node_type),
    )
    err_on_unused_flags(False,
        ('-is/--include-subdirs', args.include_subdirs_flag),
        ('-i/--inverted', args.inverted_flag),
        ('-o/--overwrite', args.overwrite_flag),
    )

    kaomi_client = get_client_or_die()

    # è stata richiesta l'esecuzione di un'azione
    try:
        # noinspection PyUnboundLocalVariable
        server_resp = kaomi_client.execute_action(action_name=args.action)
    except ActionError as e:
        # l'azione ha ritornato un exit-code diverso da zero
        exit_code = e.args[0]
        exit_message = e.args[1]
        display_output_and_exit({'status': 4, 'message': 'Action\'s execution returned a non-zero exit code', 'data': '{}\nExit code: {}'.format(exit_message, exit_code)})
    except ConnectionError as e:
        display_output_and_exit({'status': 2, 'message': 'ConnectionError executing action', 'data': 'ConnectionError: {}'.format(e)})
    except RuntimeError as e:
        display_output_and_exit({'status': 1, 'message': 'RuntimeError executing action', 'data': 'RuntimeError: {}'.format(e)})
    # non ci sono stati errori nella richiesta, analizzo cosa ho ottenuto
    # noinspection PyUnboundLocalVariable
    display_output_and_exit(client_output=get_client_output(server_output=server_resp), verbose_flag=args.verbose_flag)

elif args.file is not None:
    # è stato richiesto l'upload di un file

    # verifico che le combinazioni siano valide, nel caso che non lo siano esco
    err_on_unused_flags(None,
        ('-dp/--dir-perms', args.dir_perms),
    )
    err_on_unused_flags('both',
        ('-nt/--node-type', args.node_type),
    )
    err_on_unused_flags(False,
        ('-is/--include-subdirs', args.include_subdirs_flag),
        ('-i/--inverted', args.inverted_flag),
    )

    # ottengo il path del file di origine e quello del file di destinazione
    local_file, remote_file = args.file

    # come prima cosa controllo che il file locale esista
    if not os.path.isfile(local_file):
        # il file che si vuole uploadare non esiste, allora ritorno errore
        display_output_and_exit({'status': 1, 'message': 'Cannot find selected file', 'data': 'File: {}'.format(local_file)})

    kaomi_client = get_client_or_die()

    # se il file esiste procedo al deployment
    try:
        # noinspection PyUnboundLocalVariable
        server_resp = kaomi_client.upload_file(local_file=local_file, dest_file=remote_file, overwrite=args.overwrite_flag, perms=args.file_perms)
    except ConnectionError as e:
        display_output_and_exit({'status': 2, 'message': 'ConnectionError uploading file', 'data': 'ConnectionError: {}'.format(e)})
    except RuntimeError as e:
        display_output_and_exit({'status': 1, 'message': 'RuntimeError uploading file', 'data': 'RuntimeError: {}'.format(e)})

    # non ci sono stati errori nella richiesta, analizzo cosa ho ottenuto
    # noinspection PyUnboundLocalVariable
    display_output_and_exit(client_output=get_client_output(server_output=server_resp), verbose_flag=args.verbose_flag)

elif args.directory is not None:
    # è stato richiesto l'upload di una directory

    # verifico che le combinazioni siano valide, nel caso che non lo siano esco
    err_on_unused_flags('both',
        ('-nt/--node-type', args.node_type),
    )
    err_on_unused_flags(False,
        ('-is/--include-subdirs', args.include_subdirs_flag),
        ('-i/--inverted', args.inverted_flag),
    )

    local_dir, remote_dir = args.directory

    if not os.path.isdir(local_dir):
        # la directory che si vuole uploadare non esiste, allora ritorno errore
        display_output_and_exit({'status': 1, 'message': 'Cannot find selected directory', 'data': 'Dir: {}'.format(local_dir)})

    kaomi_client = get_client_or_die()

    # come prima cosa provo a creare la cartella sul server in modo da ottenere eventuali errori
    # ad esempio se overwrite = false e la cartella esiste già, lo si comunica all'utente
    try:
        # noinspection PyUnboundLocalVariable
        server_resp = kaomi_client.create_directory(dest_dir=remote_dir, overwrite=args.overwrite_flag, perms=args.dir_perms)
    except ConnectionError as e:
        display_output_and_exit({'status': 2, 'message': 'ConnectionError uploading folder', 'data': 'ConnectionError: {}'.format(e)})
    except RuntimeError as e:
        display_output_and_exit({'status': 1, 'message': 'RuntimeError uploading folder', 'data': 'RuntimeError: {}'.format(e)})

    # procedo solo se la creazione della cartella ha avuto successo
    # noinspection PyUnboundLocalVariable
    if server_resp.get('status') != 0:
        # la creazione della cartella non ha avuto successo, allora esco
        display_output_and_exit(client_output=get_client_output(server_output=server_resp), verbose_flag=args.verbose_flag)

    try:
        # se la cartella è stata creata corretamente allora provo a caricare il suo contenuto
        # noinspection PyUnboundLocalVariable
        upload_directory(kaomi_client=kaomi_client, local_dir=local_dir, remote_dir=remote_dir, dir_perms=args.dir_perms, file_perms=args.file_perms, verbose=args.verbose_flag)
        #upload_directory_old(kaomi_client=kaomi_client, local_dir=local_dir, remote_dir=remote_dir, dir_perms=args.dir_perms, file_perms=args.file_perms, verbose=args.verbose_flag)
    except ConnectionError as e:
        display_output_and_exit({'status': 2, 'message': 'ConnectionError uploading folder. Folder on server might be inconsistent!', 'data': 'ConnectionError: {}'.format(e)})
    except RuntimeError as e:
        display_output_and_exit({'status': 1, 'message': 'RuntimeError uploading folder. Folder on server might be inconsistent', 'data': 'RuntimeError: {}'.format(e)})
    except ServerError as exc:
        server_error = exc.args[0]
        display_output_and_exit(get_client_output(server_output=server_error))

    display_output_and_exit({'status': 0, 'message': 'Operation concluded successfully', 'data': ''}, args.verbose_flag)

elif args.directory_regex is not None:
    # è stato richiesto l'upload di una directory con filtro regex

    # verifico che le combinazioni siano valide, nel caso che non lo siano esco
    err_on_unused_flags(False,
        ('-is/--include-subdirs', args.include_subdirs_flag),
    )

    local_dir, remote_dir, regex = args.directory_regex

    if not os.path.isdir(local_dir):
        # la directory che si vuole uploadare non esiste, allora ritorno errore
        display_output_and_exit({'status': 1, 'message': 'Cannot find selected directory', 'data': 'Dir: {}'.format(local_dir)})

    kaomi_client = get_client_or_die()

    try:
        # se la cartella è stata creata corretamente allora provo a caricare il suo contenuto
        # noinspection PyUnboundLocalVariable
        upload_directory_by_regex(kaomi_client=kaomi_client, local_dir=local_dir, remote_dir=remote_dir, regex=regex, inverted=args.inverted_flag, node_type=args.node_type, overwrite=args.overwrite_flag, dir_perms=args.dir_perms, file_perms=args.file_perms, verbose=args.verbose_flag)
    except ConnectionError as e:
        display_output_and_exit({'status': 2, 'message': 'ConnectionError uploading folder. Folder on server might be inconsistent!', 'data': 'ConnectionError: {}'.format(e)})
    except RuntimeError as e:
        display_output_and_exit({'status': 1, 'message': 'RuntimeError uploading folder. Folder on server might be inconsistent', 'data': 'RuntimeError: {}'.format(e)})
    except ServerError as exc:
        server_error = exc.args[0]
        display_output_and_exit(get_client_output(server_output=server_error))

    display_output_and_exit({'status': 0, 'message': 'Operation concluded successfully', 'data': ''}, args.verbose_flag)


elif args.delete is not None:
    # è stata richiesta l'eliminazione di un file o una cartella

    # verifico che le combinazioni siano valide, nel caso che non lo siano esco
    err_on_unused_flags(None,
        ('-dp/--dir-perms', args.dir_perms),
        ('-fp/--file-perms', args.file_perms),
    )
    err_on_unused_flags('both',
        ('-nt/--node-type', args.node_type),
    )
    err_on_unused_flags(False,
        ('-is/--include-subdirs', args.include_subdirs_flag),
        ('-i/--inverted', args.inverted_flag),
        ('-o/--overwrite', args.overwrite_flag),
    )

    file_to_delete = args.delete

    kaomi_client = get_client_or_die()

    try:
        # noinspection PyUnboundLocalVariable
        server_resp = kaomi_client.delete_filesystem_node(path=file_to_delete)
    except ConnectionError as e:
        display_output_and_exit({'status': 2, 'message': 'ConnectionError deleting node', 'data': 'ConnectionError: {}'.format(e)})
    except RuntimeError as e:
        display_output_and_exit({'status': 1, 'message': 'RuntimeError deleting node', 'data': 'RuntimeError: {}'.format(e)})

    # noinspection PyUnboundLocalVariable
    display_output_and_exit(client_output=get_client_output(server_output=server_resp), verbose_flag=args.verbose_flag)

elif args.delete_regex is not None:
    # è stata richiesta l'eliminazione tramite regex

    # verifico che le combinazioni siano valide, nel caso che non lo siano esco
    err_on_unused_flags(None,
        ('-dp/--dir-perms', args.dir_perms),
        ('-fp/--file-perms', args.file_perms),
    )
    err_on_unused_flags(False,
        ('-o/--overwrite', args.overwrite_flag),
    )

    base_path, regex = args.delete_regex

    kaomi_client = get_client_or_die()

    try:
        # noinspection PyUnboundLocalVariable
        server_resp = kaomi_client.delete_by_regex(path=base_path, regex=regex, inverted=args.inverted_flag, node_type=args.node_type, include_subdirs=args.include_subdirs_flag)
    except ConnectionError as e:
        display_output_and_exit({'status': 2, 'message': 'ConnectionError deleting by regex', 'data': 'ConnectionError: {}'.format(e)})
    except RuntimeError as e:
        display_output_and_exit({'status': 1, 'message': 'RuntimeError deleting by regex', 'data': 'RuntimeError: {}'.format(e)})

    # noinspection PyUnboundLocalVariable
    display_output_and_exit(client_output=get_client_output(server_output=server_resp), verbose_flag=args.verbose_flag)

else:
    # non è stato riconosciuto cosa è stato richiesto
    display_output_and_exit({'status': 1, 'message': 'Client called without an operation'})
