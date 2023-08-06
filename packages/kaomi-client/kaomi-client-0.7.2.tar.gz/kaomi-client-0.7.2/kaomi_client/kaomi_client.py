import os
import json
import requests
from requests_toolbelt.multipart import encoder
from requests_futures.sessions import FuturesSession

from . import globals


class ServerError(Exception):
    """
    classe di eccezioni utilizzata per distinguere tra gli errori del server e quelli del client
    Quando si solleva l'eccezione va passato il dizionario contente la risposta del server
    """


class ActionError(Exception):
    """
    Classe di eccezioni utilizzata per segnalare un errore che ha avuto luogo durante l'esecuzione di un'azione lato server.
    In particolare, indica un errore durante l'esecuzione dello script
    Quando si solleva l'eccezione va passato il dizionario contente la risposta del server
    """


class KaomiClient:
    """
    Classe per la comunicazione con il server da deplyare
    """
    __host = ""             # host con il quale comunicare
    __port = ""             # porta sulla quale ascolta il kaomi server
    __apikey = ""           # apikey con cui autenticarsi al server
    __server = ""           # indirizzo completo del server

    __user_agent = ""       # user-agent utilizzato dal client

    __api_paths = {}        # dizionario contenente i path delle varie API

    __session = None
    __concurrent_session = None

    def __init__(self, server_host, server_port, apikey, api_paths):
        """
        Inizializzazione della comunicazione con il server
        :rtype:
        :param server_host:     host con il quale comunicare
        :param server_port:     porta sulla quale ascolta il kaomi server
        :param apikey:          apikey con cui autenticarsi al server
        :param api_paths:       dizionario contenente le risoluzioni dei path delle api
        :throw ConnectionError: se qualcosa va storto con la connessione con il server
        :throw TypeError:       nel caso sia sbagliato il type di un parametro
        """
        # provo a connettermi al server per verificare se è raggiungibile e up
        server = "{}:{}".format(server_host, server_port)

        self.__user_agent = 'kaomi-python-client/{}'.format(globals.AGENT_VERSION)

        self.__session = requests.Session()
        self.__concurrent_session = FuturesSession(max_workers=8)

        try:
            # effettuo una chiamata get sull'index del server
            resp = self.__session.get(server, headers={'User-Agent': self.__user_agent})
        except requests.exceptions.RequestException as e:
            raise ConnectionError('Cannot connect to server: {}. Please check if it is correct and up. Exception: {}'.format(server, e))

        # controllo che il server risponda
        if not resp.status_code == 200:
            raise ConnectionError('Cannot connect to server: {}. Please check if it is correct and up.'.format(server))
        resp = resp.json()          # ottengo il contenuto della risposta
        if not (resp.get('status') == 0 and resp.get('substatus') == 0):
            raise ConnectionError('Server responds but with wrong status or substatus codes'.format(server))

        if not isinstance(api_paths, dict):
            raise TypeError('Server paths must be specified as a dictionary')

        # il server ha risposto, allora inizializzo lo stato interno della classe
        self.__apikey = apikey
        self.__host = server_host
        self.__port = server_port
        self.__server = server
        self.__api_paths = api_paths

    def __get_api_url(self, requested_api):
        """
        Funzione che data un api richiesta (che deve essere presente in __api_paths)
        :param requested_api:       api del quale si vuole ottenere l'url
        :throw RuntimeError:        se l'api non è definita
        :return:                    url completo, utilizzabile nella richiesta post
        """
        if requested_api not in self.__api_paths:
            # se non esiste la enrty nei path definiti, non possiamo ottenere l'url corretto
            raise RuntimeError('API URL for "{}" not found'.format(requested_api))

        # ottengo l'url
        api_url = '{}/{}'.format(self.__server, self.__api_paths.get(requested_api))

        return api_url

    def upload_file(self, local_file, dest_file, overwrite=False, perms=None):
        """
        Funzione per l'upload di un file sul server
        :param local_file:      path del file locale da caricare sul server, si suppone che esista
        :param dest_file:       path di destinazione del file
        :param overwrite:       flag che indica se il file debba essere sovrascritto nel caso esista già
        :param perms:           permessi da assegnare al file
        :throw ConnectionError:     nel caso ci siano problemi con la richiesta verso il kaomi server
        :throw RuntimeError:        per tutti gli altri problemi
        :return:                dizionario con la risposta del server
        """
        try:
            # ottengo l'url da utilizzare
            api_url = self.__get_api_url("upload_file")         # might raise RuntimeError

            if not os.path.isfile(local_file):
                raise RuntimeError('Cannot find local file "{}"'.format(local_file))

            with open(local_file, 'rb') as fd:
                perms = oct(perms) if perms is not None else None

                # costruisco il payload della richiesta
                payload = {
                    "file": (os.path.basename(local_file), fd, "application/octet-stream"),
                    "apikey": self.__apikey,
                    "dest_path": dest_file,
                    "overwrite": 'true' if overwrite else 'false',
                    "perms": perms         # perché l'encoding funzioni i permessi devono essere passati come stringa
                }

                # utilizzo di un multipart encoder per poter caricare il file non tutto insieme
                # questo è dato dal fatto di usare il parametro "data" della richiesta post e non quello "files"
                form = encoder.MultipartEncoder(payload)
                headers = {"Prefer": "respond-async", "Content-Type": form.content_type, 'User-Agent': self.__user_agent}

                try:
                    resp = self.__session.post(api_url, headers=headers, data=form)
                except (requests.exceptions.RequestException, ConnectionError) as e:
                    raise ConnectionError('[{}: "{}"->"{}"] Something went wrong with request. Exception: {}'.format("upload_file", local_file, dest_file, e))

            return resp.json()         # might raise JSONDecodeError
        except RuntimeError as e:
            # aggiungo l'informazione su quale operazione ha sollevato l'errore
            raise RuntimeError('[{}: "{}"->"{}"] {}'.format("upload_file", local_file, dest_file, e))
        except json.JSONDecodeError as e:
            # il server non ha risposto con un json
            raise ConnectionError('[{}: "{}"->"{}"] Server response is not a JSON {}\nData: {}'.format("upload_file", local_file, dest_file, e, resp.text))

    def upload_file_future(self, local_file, dest_file, overwrite=False, perms=None):
        """
        Funzione per l'upload di un file sul server, ritorna un futures in modo da operare in modo concorrente
        :param local_file:         path del file locale da caricare sul server, si suppone che esista
        :param dest_file:          path di destinazione del file
        :param overwrite:          flag che indica se il file debba essere sovrascritto nel caso esista già
        :param perms:              permessi da assegnare al file
        :throw ConnectionError:    nel caso ci siano problemi con la richiesta verso il kaomi server
        :throw RuntimeError:       per tutti gli altri problemi
        :return:                   future sul quale chiamare i risultati
        """

        try:
            # ottengo l'url da utilizzare
            api_url = self.__get_api_url("upload_file")         # might raise RuntimeError

            if not os.path.isfile(local_file):
                raise RuntimeError('Cannot find local file "{}"'.format(local_file))

            fh = open(local_file, 'rb')

            perms = oct(perms) if perms is not None else None

            # costruisco il payload della richiesta
            payload = {
                "file": (os.path.basename(local_file), fh, "application/octet-stream"),
                "apikey": self.__apikey,
                "dest_path": dest_file,
                "overwrite": 'true' if overwrite else 'false',
                "perms": perms         # perché l'encoding funzioni i permessi devono essere passati come stringa
            }

            # utilizzo di un multipart encoder per poter caricare il file non tutto insieme
            # questo è dato dal fatto di usare il parametro "data" della richiesta post e non quello "files"
            form = encoder.MultipartEncoder(payload)
            headers = {"Prefer": "respond-async", "Content-Type": form.content_type, 'User-Agent': self.__user_agent}

            try:
                # aggiungo un hook che chiuda il file descriptor aperto per l'upload quando la richiesta è completata
                fut = self.__concurrent_session.post(api_url, headers=headers, data=form, hooks={'response': lambda resp, *args, **kwargs: fh.close()})

            except (requests.exceptions.RequestException, ConnectionError) as e:
                raise ConnectionError('[{}: "{}"->"{}"] Something went wrong with request. Exception: {}'.format("upload_file", local_file, dest_file, e))

            return fut
        except RuntimeError as e:
            # aggiungo l'informazione su quale operazione ha sollevato l'errore
            raise RuntimeError('[{}: "{}"->"{}"] {}'.format("upload_file", local_file, dest_file, e))


    def create_directory(self, dest_dir, overwrite=False, perms=None):
        """
        Funzione per la creazione di una cartella sul server
        :param dest_dir:            cartella da creare sul server
        :param overwrite:           indica se la cartella deve essere sovrascritta nel caso esista
        :param perms:               permessi da assegnare alla cartella
        :throw ConnectionError:     nel caso ci siano problemi con la richiesta verso il kaomi server
        :throw RuntimeError:        per tutti gli altri problemi
        :return:                    dizionario con la risposta del server
        """
        try:
            # ottengo l'url da utilizzare
            api_url = self.__get_api_url("create_directory")         # might raise RuntimeError

            perms = oct(perms) if perms is not None else None

            # costruisco il payload
            payload = {
                "apikey": self.__apikey,
                "path": dest_dir,
                "overwrite": 'true' if overwrite else 'false',
                "perms": perms}

            try:
                # effettuo la richiesta
                resp = self.__session.post(api_url, data=json.dumps(payload), headers={'User-Agent': self.__user_agent})
            except (requests.exceptions.RequestException, ConnectionError) as e:
                raise ConnectionError('[{}: "{}"] Something went wrong with request. Exception: {}'.format("create_directory", dest_dir, e))

            # analizzo e ritorno il risultato
            return resp.json()  # might raise JSONDecodeError
        except RuntimeError as e:
            # aggiungo l'informazione su quale operazione ha sollevato l'errore
            raise RuntimeError('[{}: "{}"] {}'.format("create_directory", dest_dir, e))
        except json.JSONDecodeError as e:
            # il server non ha risposto con un json
            # noinspection PyUnboundLocalVariable
            raise ConnectionError('[{}: "{}"] Server response is not a JSON {}\nData: {}'.format("create_directory", dest_dir, e, resp.text))

    def delete_filesystem_node(self, path):
        """
        Funzione per l'eliminazione di un file o di una directory sul server
        :param path:    path del nodo da eliminare
        :throw ConnectionError:     nel caso ci siano problemi con la richiesta verso il kaomi server
        :throw RuntimeError:        per tutti gli altri problemi
        :return:        dizionario con la risposta del server
        """
        try:
            # ottengo l'url da utilizzare
            api_url = self.__get_api_url("delete_filesystem_node")         # might raise RuntimeError

            # costruisco il payload
            payload = {"apikey": self.__apikey, "path": path}

            try:
                # effettuo la richiesta
                resp = self.__session.post(api_url, data=json.dumps(payload), headers={'User-Agent': self.__user_agent})
            except (requests.exceptions.RequestException, ConnectionError) as e:
                raise ConnectionError('[{}: "{}"] Something went wrong with request. Exception: {}'.format("delete_filesystem_node", path, e))

            # analizzo e ritorno il risultato
            return resp.json()         # might raise JSONDecodeError
        except RuntimeError as e:
            # aggiungo l'informazione su quale operazione ha sollevato l'errore
            raise RuntimeError('[{}: "{}"] {}'.format("delete_filesystem_node", path, e))
        except json.JSONDecodeError as e:
            # il server non ha risposto con un json
            # noinspection PyUnboundLocalVariable
            raise ConnectionError('[{}: "{}"] Server response is not a JSON {}\nData: {}'.format("delete_filesystem_node", path, e, resp.text))

    def delete_by_regex(self, path, regex, inverted, node_type, include_subdirs):
        """
        Funzione per l'eliminazione di un file o di una directory sul server
        :param path:           path della cartella da cui cominciare per le eliminazioni
        :param regex:               regex con cui verificare se eliminare un elemento
        :param inverted:            booleano che indica se invertire il matche effettuato dalla regex
        :param node_type:           indica se considerare solo file, solo cartelle o entrambi nell'eliminazione
        :param include_subdirs:     indica se considerare solo la directory corrente o anche le sottodirectory per le eliminazioni
        :throw ConnectionError:     nel caso ci siano problemi con la richiesta verso il kaomi server
        :throw RuntimeError:        per tutti gli altri problemi
        :return:                    dizionario con la risposta del server
        """
        try:
            # ottengo l'url da utilizzare
            api_url = self.__get_api_url("delete_by_regex")     # might raise RuntimeError

            # costruisco il payload
            payload = {"apikey": self.__apikey, "path": path, "regex": regex, "inverted": inverted, "node_type": node_type, "include_subdirs": include_subdirs}

            try:
                # effettuo la richiesta
                resp = self.__session.post(api_url, data=json.dumps(payload), headers={'User-Agent': self.__user_agent})
            except (requests.exceptions.RequestException, ConnectionError) as e:
                raise ConnectionError('[{}: "{}"] Something went wrong with request. Exception: {}'.format("delete_by_regex", path, e))

            # analizzo e ritorno il risultato
            return resp.json()         # might raise JSONDecodeError
        except RuntimeError as e:
            # aggiungo l'informazione su quale operazione ha sollevato l'errore
            raise RuntimeError('[{}: "{}"] {}'.format("delete_by_regex", path, e))
        except json.JSONDecodeError as e:
            # il server non ha risposto con un json
            # noinspection PyUnboundLocalVariable
            raise ConnectionError('[{}: "{}"] Server response is not a JSON {}\nData: {}'.format("delete_by_regex", path, e, resp.text))

    def execute_action(self, action_name):
        """
        Funzione per l'esecuzione di un'azione sul server
        :param action_name:         nome dell'azione da eseguire, i nomi sono definiti per apikey
        :throw ConnectionError:     nel caso ci siano problemi con la richiesta verso il kaomi server
        :throw RuntimeError:        per tutti gli altri problemi
        :return:                    dizionario con la risposta del server
        """
        try:
            # ottengo l'url da utilizzare
            api_url = self.__get_api_url("execute_action")         # might raise RuntimeError

            # costruisco il payload
            payload = {"apikey": self.__apikey, "action": action_name}

            try:
                # effettuo la richiesta
                resp = self.__session.post(api_url, data=json.dumps(payload), headers={'User-Agent': self.__user_agent})
            except (requests.exceptions.RequestException, ConnectionError) as e:
                raise ConnectionError('[{}: "{}"] Something went wrong with request. Exception: {}'.format("execute_action", action_name, e))

            # analizzo e ritorno il risultato
            response = resp.json()         # might raise JSONDecodeError
            resp_data = response.get('data')

            # retrocompatibilità con le vecchie versioni del server
            if not isinstance(resp_data, dict):
                # il server non ha mandato un dizionario come campo "data", probabilmente è una versione vecchia
                # ritorniamo subito la risposta senza elaborarla
                return response

            if not all(k in resp_data for k in ['exit_code', 'exit_message']):
                # il server ha ritornato come "data" un dizionario, ma non completo
                raise ConnectionError('[{}: "{}"] Something went wrong with request. Server has returned an invalid dict as "data" field.'.format("execute_action", action_name))

            if resp_data.get('exit_code') != 0:
                # il codice di uscita dello script eseguito lato server è diverso da zero
                raise ActionError(response['data']['exit_code'], response['data']['exit_message'])
            # tutto ha funzionato, ritorno la risposta ottenuta dal server
            # sovrascrivo il campo data con il messaggio perché nel caso di successo non ho bisogno dell'exit code
            response['data'] = response['data']['exit_message']
            return response
        except RuntimeError as e:
            # aggiungo l'informazione su quale operazione ha sollevato l'errore
            raise RuntimeError('[{}: "{}"] {}'.format("execute_action", action_name, e))
        except json.JSONDecodeError as e:
            # il server non ha risposto con un json
            # noinspection PyUnboundLocalVariable
            raise ConnectionError('[{}: "{}"] Server response is not a JSON {}\nData: {}'.format("execute_action", action_name, e, resp.text))

    def close_future_session(self):
        self.__concurrent_session.close()