import json
import os
import re
import sys

from .kaomi_client import ServerError
from .globals import EXIT_STATUS_RESOLVER


def display_output_and_exit(client_output, verbose_flag=False):
    """
    Dato un dizionario rappresentante lo stato di uscita del server, costruisce lo stato di uscita del client ed esce dallo script
    :param client_output:       dizionario che contiene le informazioni sull'output
    :param verbose_flag:        flag che indica se l'output deve essere verbose, nei casi di errore viene sempre considerato (True)

    WARNING: la funzione termina lo script

    """

    # ottengo il significato dell'exit status del client, per poterlo stampare all'utente nel caso l'output sia verbose
    status = client_output.get('status', -1)
    status_meaning = EXIT_STATUS_RESOLVER.get(status, '{}: Unknown'.format(status))

    # ottengo il flag che indica se ci sono stati errori
    error_flag = client_output.get('error', True)           # se non esiste il campo, c'è stato un errore

    # ottengo il message d'uscita e i dati
    message = client_output.get('message', '')
    data = client_output.get('data', '')

    # stampo l'output

    # si è verificato un errore
    if error_flag:
        # stampo gli errori sia sui log che sul
        print('{} \nError: {} \nData: {}'.format(status_meaning, message, data))

    # non si è verificato un errore
    elif not error_flag:

        if verbose_flag:
            # nel caso lo script sia stato chiamato con verbose, mostro anche l'output sul terminale
            print('{} \nOutput: {} \nData: {}'.format(status_meaning, message, data))

    # esco dallo script con l'exit status specificato
    sys.exit(status)


def create_directory_tree(kaomi_client, local_dir, remote_dir, dir_perms=None, verbose=False):
    """
    Funzione per creare sul server un albero di directory uguale a quello sul client, ma senza i file al suo interno
    Nota: all'interno della funzione non mi devo preoccupare dell'overwrite perché so che remote_dir è vuota
    :param kaomi_client:        client da utilizzare per l'upload
    :param local_dir:           cartella da uploadare
    :param remote_dir:          posizione di upload per la cartella specificata
    :param dir_perms:           permessi da assegnare alle cartelle
    :param verbose:             indica se l'output deve essere verbose
    :throw RuntimeError:        (anche dal kaomi-client) per problemi generici della funzione o delle operazione di uplaod
    :throw ConnectionError:     (re-raise dalle operazioni del kaomi-client) per problemi di comunicazione con il server
    """

    if verbose: print('Local folder "{}" structure is being mirrored in "{}"'.format(local_dir, remote_dir))

    if not os.path.isdir(local_dir) or os.path.islink(local_dir):
        # la cartella passata non è una cartella o è un link ad una cartella
        raise RuntimeError('Wrong argument: "{}" is not a valid directory'.format(local_dir))

    for entry in os.listdir(local_dir):
        # scorro tutte le entry presenti all'interno della cartella

        # ottengo il path assoluto dell'entry
        entry_abs_path = os.path.join(local_dir, entry)

        # salto le entry che non mi interessano
        if os.path.islink(entry_abs_path):
            # tipologie di entry che non ci interessano, le saltiamo
            continue

        if os.path.isdir(entry_abs_path):
            # LA ENTRY È UNA DIRECTORY

            # ottengo la nuova cartella di destinazione per la dir considerata
            new_remote_dir = os.path.join(remote_dir, entry)

            # come prima cosa devo creare la cartella, i vari catch ad eccezioni vengono fatti dal chiamante
            server_resp = kaomi_client.create_directory(dest_dir=new_remote_dir, perms=dir_perms)
            if server_resp.get('status') != 0:
                # controllo se l'azione ha avuto successo, altrimenti sollevo un'eccezione
                raise ServerError(server_resp)

            # arrivato qui sono sicuro che la creazione ha avuto successo
            # allora posso chiamare ricorsivamente la funzione di creazione directory sulla cartella
            create_directory_tree(kaomi_client=kaomi_client, local_dir=entry_abs_path, remote_dir=new_remote_dir, dir_perms=dir_perms, verbose=verbose)

    # ho terminato di caricare la cartella, segnalo il successo se verbose è attivo
    if verbose: print('Local folder "{}" structure mirrored in "{}"'.format(local_dir, remote_dir))


def upload_files_in_tree(kaomi_client, local_dir, remote_dir, futures_list, file_perms=None, verbose=False):
    """
    Funzione per caricare sul server i file presenti in un albero di directory locale in un identico albero di dirextory remoto. Assume che l'albero remoto esista già
    L'upload dei file avviene in un ordine non definito

    Nota: all'interno della funzione non mi devo preoccupare dell'overwrite perché so che remote_dir è vuota
    :param kaomi_client:        client da utilizzare per l'upload
    :param local_dir:           cartella da uploadare
    :param remote_dir:          posizione di upload per la cartella specificata
    :param futures_list:        lista dove verranno aggiunti i futures
    :param file_perms:          permessi da assegnare ai file
    :param verbose:             indica se l'output deve essere verbose
    :throw RuntimeError:        (anche dal kaomi-client) per problemi generici della funzione o delle operazione di uplaod
    :throw ConnectionError:     (re-raise dalle operazioni del kaomi-client) per problemi di comunicazione con il server
    """

    if not os.path.isdir(local_dir) or os.path.islink(local_dir):
        # la cartella passata non è una cartella o è un link ad una cartella
        raise RuntimeError('Wrong argument: "{}" is not a valid directory'.format(local_dir))

    for entry in os.listdir(local_dir):
        # scorro tutte le entry presenti all'interno della cartella

        # ottengo il path assoluto dell'entry
        entry_abs_path = os.path.join(local_dir, entry)

        # salto le entry che non mi interessano
        if os.path.islink(entry_abs_path):
            # tipologie di entry che non ci interessano, le saltiamo
            continue

        if os.path.isdir(entry_abs_path):
            # LA ENTRY È UNA DIRECTORY

            # ottengo la nuova cartella di destinazione per la dir considerata
            new_remote_dir = os.path.join(remote_dir, entry)

            # allora posso chiamare ricorsivamente la funzione di upload sulla cartella
            upload_files_in_tree(kaomi_client=kaomi_client, local_dir=entry_abs_path, remote_dir=new_remote_dir, futures_list=futures_list, file_perms=file_perms, verbose=verbose)

        elif os.path.isfile(entry_abs_path):
            # LA ENTRY È UN FILE

            # ottengo il path del file di destinazione
            new_remote_file = os.path.join(remote_dir, entry)

            # procedo con l'upload del file, i vari catch ad eccezioni vengono fatti dal chiamante
            futures_list.append(kaomi_client.upload_file_future(local_file=entry_abs_path, dest_file=new_remote_file, perms=file_perms))

            # se è impostato il verbose, segnalo il successo dell'operazione
            if verbose: print('Local file "{}" uploaded in "{}"'.format(entry_abs_path, new_remote_file))


def wait_for_results(kaomi_client, futures_list):
    for f in futures_list:
        server_resp = f.result()

        try:
            server_resp = server_resp.json()
        except json.JSONDecodeError as e:
            # il server non ha risposto con un json
            raise ConnectionError('{}:  Server response is not a JSON {}\nData: {}'.format("upload_file", e, server_resp.text))

        if server_resp.get('status') != 0:
            # controllo se l'azione ha avuto successo, altrimenti sollevo un'eccezione
            # annullo gli upload rimanenti
            kaomi_client.close_future_session()
            raise ServerError(server_resp)



def upload_directory(kaomi_client, local_dir, remote_dir, dir_perms=None, file_perms=None, verbose=False):
    """
    Funzione per il caricamento di una directory.
    Per essere più efficente la funzione inizialmente uploada solo la struttura delle directory in modalità sequenziale per evitare race conditions nella scrittura lato server
    Successivamente uploada i file in modo concorrente, dato che non sussistono più race conditions
    Nota: all'interno della funzione non mi devo preoccupare dell'overwrite perché so che remote_dir è vuota
    :param kaomi_client:        client da utilizzare per l'upload
    :param local_dir:           cartella da uploadare
    :param remote_dir:          posizione di upload per la cartella specificata
    :param dir_perms:           permessi da assegnare alle cartelle
    :param file_perms:          permessi da assegnare ai file
    :param verbose:             indica se l'output deve essere verbose
    :throw RuntimeError:        (anche dal kaomi-client) per problemi generici della funzione o delle operazione di uplaod
    :throw ConnectionError:     (re-raise dalle operazioni del kaomi-client) per problemi di comunicazione con il server
    """

    create_directory_tree(kaomi_client=kaomi_client, local_dir=local_dir, remote_dir=remote_dir, dir_perms=dir_perms, verbose=verbose)

    if verbose: print('Starting files upload...')

    futures_list = []

    upload_files_in_tree(kaomi_client=kaomi_client, local_dir=local_dir, remote_dir=remote_dir, futures_list=futures_list, file_perms=file_perms, verbose=verbose)

    if verbose: print('Waiting for file uploads to complete...')

    wait_for_results(kaomi_client=kaomi_client, futures_list=futures_list)

def upload_directory_by_regex(kaomi_client, local_dir, remote_dir, regex, inverted, node_type, overwrite, dir_perms=None, file_perms=None, verbose=False):
    """
    Funzione per il caricamento del contenuto di una directory, in base al match di una regex

    :param kaomi_client:        client da utilizzare per l'upload
    :param local_dir:           cartella da uploadare
    :param remote_dir:          posizione di upload per la cartella specificata
    :param regex:               regex da utilizzare per decidere se caricare un file/cartella
    :param inverted:            indica se considerare le cartelle/file che marchano o non matchano
    :param node_type            indica se considerare solo file, solo cartelle o entrambi
    :param overwrite            indica se sovrascrivere un file/cartella già esistente sul sistema remoto
    :param dir_perms:           permessi da assegnare alle cartelle
    :param file_perms:          permessi da assegnare ai file
    :param verbose:             indica se l'output deve essere verbose
    :throw RuntimeError:        (anche dal kaomi-client) per problemi generici della funzione o delle operazione di uplaod
    :throw ConnectionError:     (re-raise dalle operazioni del kaomi-client) per problemi di comunicazione con il server
    """

    include_files = (node_type in {'file', 'both'})
    include_folders = (node_type in {'folder', 'both'})

    try:
        regex = re.compile(regex)
    except re.error as e:
        # errore durante la preparazione della regex
        raise RuntimeError('Wrong argument: "{}" is not a valid regex: {}'.format(regex, e))

    if not os.path.isdir(local_dir) or os.path.islink(local_dir):
        # la cartella passata non è una cartella o è un link ad una cartella
        raise RuntimeError('Wrong argument: "{}" is not a valid directory'.format(local_dir))

    for entry in os.listdir(local_dir):
        # scorro tutte le entry presenti all'interno della cartella

        # ottengo il path assoluto dell'entry
        entry_abs_path = os.path.join(local_dir, entry)

        # salto le entry che non mi interessano
        if os.path.islink(entry_abs_path):
            # tipologie di entry che non ci interessano, le saltiamo
            continue

        if os.path.isdir(entry_abs_path):
            # LA ENTRY È UNA DIRECTORY

            # se le directory devono essere considerate
            if include_folders:
                # verifico se matcha la regex
                m = regex.fullmatch(entry) is not None

                if (m and not inverted) or (not m and inverted):
                    # carico la directory
                    # ottengo la nuova cartella di destinazione per la dir considerata
                    new_remote_dir = os.path.join(remote_dir, entry)

                    server_resp = kaomi_client.create_directory(dest_dir=new_remote_dir, overwrite=overwrite, perms=dir_perms)

                    # procedo solo se la creazione della cartella ha avuto successo
                    # noinspection PyUnboundLocalVariable
                    if server_resp.get('status') != 0:
                        # la creazione della cartella non ha avuto successo, allora esco
                        raise ServerError(server_resp)

                    # se la cartella è stata creata corretamente allora provo a caricare il suo contenuto
                    upload_directory(kaomi_client=kaomi_client, local_dir=entry_abs_path, remote_dir=new_remote_dir, dir_perms=dir_perms, file_perms=file_perms, verbose=verbose)

        elif os.path.isfile(entry_abs_path):
            # LA ENTRY È UN FILE

            # se i file devono essere considerati
            if include_files:
                # verifico se matcha la regex
                m = regex.fullmatch(entry) is not None

                if (m and not inverted) or (not m and inverted):
                    # carico il file

                    # ottengo il path del file di destinazione
                    new_remote_file = os.path.join(remote_dir, entry)

                    # procedo con l'upload del file, i vari catch ad eccezioni vengono fatti dal chiamante
                    server_resp = kaomi_client.upload_file(local_file=entry_abs_path, dest_file=new_remote_file, overwrite=overwrite, perms=file_perms)
                    if server_resp.get('status') != 0:
                        # controllo se l'azione ha avuto successo, altrimenti sollevo un'eccezione
                        raise ServerError(server_resp)

                    # se è impostato il verbose, segnalo il successo dell'operazione
                    if verbose: print('Local file "{}" uploaded in "{}"'.format(entry_abs_path, new_remote_file))


def get_client_output(server_output):
    """
    Funzione che dato il dizionario ottenuto come risposta, ne ricava le informazioni da fornire in output al client
    :param server_output:       dizionario ottenuto dal server come risposta
    :return:                    dizionario con la risposta del server
    """
    requested_fields = ['status', 'substatus', 'message', 'data']
    if not all(k in server_output for k in requested_fields):
        # non ci sono le chiavi che ci aspetteremmo nel dizionario del server, quindi errore nel client
        return {'status': 1, 'error': True, 'message': 'Missing fields in server response: {}. Response: {}'.format(list(server_output.keys()), server_output), '': ''}

    # ottengo i campi dal dizionario del server
    status, substatus, message, data = server_output.get('status'), server_output.get('substatus'), server_output.get('message'), server_output.get('data')

    # analizzo lo stato di uscita del server e converto il valore di uscita in quello del client
    if status == 0:
        # il comando ha avuto successo
        return {'status': 0, 'error': False, 'message': '(server {}:{}) {}'.format(status, substatus, message), 'data': data}
    elif status == 1:
        # problema di connessione
        return {'status': 2, 'error': True, 'message': '(server error {}:{}) {}'.format(status, substatus, message), 'data': data}
    elif status == 2 and (substatus == 1 or substatus == 2):
        # problema di autorizzazioni
        return {'status': 3, 'error': True, 'message': '(server error {}:{}) {}'.format(status, substatus, message), 'data': data}
    else:
        # problema applicativo
        return {'status': 4, 'error': True, 'message': '(server error {}:{}) {}'.format(status, substatus, message), 'data': data}