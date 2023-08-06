import os
import grp
import pwd

"""
Implementazione di un parser per il formato del file di configurazione simil-INI usato dall'applicazione.
"""


class ConfigFile(object):
    """
    Classe per il parsing delle configurazioni di deployment presenti sul server
    """
    # nome del file di configurazione rappresentato dalla classe
    __filename = None
    # contenuto della configurazione
    __config = None
    # formato del placeholder
    __placeholder_format = '##{}##'

    def __init__(self, filename):
        """
        Inizializzazione della configurazione e del suo stato interno
        :throw FileNotFoundError:       nel caso il file non venga trovato
        :throw RuntimeError:            nel caso ci siano problemi con gli aliases
        :throw ValueError:              nel caso la configurazione segua la struttura definita
        """

        if not os.path.isfile(filename):
            # il file non esiste, sollevo un'eccezione
            raise FileNotFoundError('Il file della configurazione non è stato trovato')

        # imposto il nome del file e lo leggo
        self.__filename = filename
        data = open(filename, 'r').read()

        # parso il file di configurazione, allo stato attuale la configurazione non è detto che sia consistente
        unvalidated_config = self.__parse(data)                         # può sollevare un ValueError

        # risolvo gli alias della configurazione
        self.__resolve_config_aliases(unvalidated_config)               # può sollevare un RuntimeError

        # verifico e fixo la configurazione e imposto effettivamente lo stato interno
        self.__config = self.__validate_and_fix(unvalidated_config)     # può sollevare un ValueError

    @staticmethod
    def __parse(data):
        """
        Funzione per parsare la configurazione e ottenere un dizionario
        :param data:            Dati grezzi letti dal file di config
        :throw ValueError:      se i separatori o le sezioni non sono state riconosciute
        :return: Dizionario che rappresenta il contenuto del file di config, parsato
        """
        # dizionario che conterrà la configurazione
        conf = {}

        # variabili per tenere in memoria la sezione corrente
        current_section = None
        current_subsection = None

        # separa il file in righe
        for l in data.split('\n'):
            # elimina gli spazi iniziali e finali
            l = l.strip('\r\t ')

            # ignora le righe inutili, ovvero i commenti e le righe bianche
            if len(l) == 0 or l.startswith('#'):
                continue

            # SEZIONI E SOTTOSEZIONI
            if l.startswith('['):
                # gestisco gli inizi di sezione
                if l.lower().startswith(('[aliases]', '[default]')):
                    current_section, current_subsection = l.lower().strip('[]'), None
                elif l.lower().startswith(('[folder:', '[action:')):
                    l = l.strip('[]').split(':')
                    current_section, current_subsection = l[0].lower().strip('[]'), ':'.join(l[1:]).strip()
                else:
                    raise ValueError("Il separatore di sezione '{}' non è valido.".format(l))

                # creo le sezioni e sottosezioni se non esistono
                if current_section not in conf:
                    conf[current_section] = {}

                if current_subsection is not None and current_subsection not in conf[current_section]:
                    if current_section in ['action']:
                        # se è una sottosezione di action allora conterrà una stringa
                        conf[current_section][current_subsection] = ''
                    else:
                        # altrimenti conterrà un dizionario chiave - valore
                        conf[current_section][current_subsection] = {}
                # se la riga conteneva una sezione o sottosezione ho finito l'elaborazione e vado alla prossima
                continue


            # gestisco le righe che sono contenute nelle sezioni, in base alla sezione che le contiene
            # se siamo arrivati qui, significa che stiamo gestendo una riga che non è un separatore di sezione

            # sezioni che usano la struttura chiave = valore
            if current_section in ['default', 'aliases', 'folder']:
                l = l.split('=')
                key, value = l[0].strip(), '='.join(l[1:]).strip()

            # sezioni che usano la struttura valore e basta
            elif current_section in ['action']:
                key, value = l, None

            else:
                # la sezione non è stata riconosciuta
                raise ValueError("La sezione '{}' è sconosciuta.".format(current_section))


            # aggiungo la chiave e valore decodificati alla conf finale
            if current_section in ['action']:
                # aggiungo il comando alla lista dei comandi da eseguire per questa azione
                # new line necessario per la separazione dei comandi
                conf[current_section][current_subsection] += '\n{}'.format(key)

            elif current_section in ['default']:
                # gestione delle chiavi multivalore, i valori vengono aggiunti alla lista
                if key not in conf[current_section]:
                    # prima volta che incontro la chiave, inizializzo la lista
                    conf[current_section][key] = []
                conf[current_section][key].append(value)

            elif current_section in ['aliases']:
                # gli aliases vengono risolti con un dizionario
                if key not in conf[current_section]:
                    conf[current_section][key] = {}

                conf[current_section][key] = value

            elif current_section in ['folder']:
                if key not in conf[current_section][current_subsection]:
                    conf[current_section][current_subsection][key] = {}

                conf[current_section][current_subsection][key] = value

        return conf

    def __validate_and_fix(self, data):
        """
        Validazione della configurazione e piccoli fix automatici
        :param data:            Dizionario parsato da parte e che deve essere validato
        :throw ValueError:      Sezioni mancanti, non ammesse, permessi o utenti non validi
        :return:                Dizionario come definito per le configurazioni
        """

        # verifico che le sezioni necessarie esistano
        needed_sections = {'default'}
        if not all(sec in data for sec in needed_sections):
            raise ValueError("Le sezioni obbligatorie ({}) non sono tutte presenti. Nel file di configurazione '{}'".format(needed_sections, self.__filename))

        # verifico che le sezioni esistenti siano dentro quelle ammesse
        allowed_sections = {'default', 'aliases', 'folder', 'action', 'owner', 'group', 'dir-perms', 'file-perms'}
        if not all(sec in allowed_sections for sec in data):
            raise ValueError("Alcune delle sezioni specificate non sono ammesse, sezioni valide: {}. Nel file di configurazione '{}'".format(allowed_sections, self.__filename))

        # verifico che se sottosezioni siano valide

        # verifico che le chiavi necessarie esistano in DEFAULT
        needed_keys = {'key'}           # il campo dell'apikey non può mancare
        if not all(sec in data['default'] for sec in needed_keys):
            raise ValueError("Le chiavi obbligatorie ({}) per la sezione '[{}]' non sono tutte presenti. Nel file di configurazione '{}'".format(needed_keys, 'default', self.__filename))

        # verifico che le chiavi esistenti siano dentro quelle ammesse in DEFAULT
        allowed_keys = {'key', 'allow-ip', 'owner', 'group', 'dir-perms', 'file-perms', 'actions-shell', 'actions-timeout'}
        if not all(sec in allowed_keys for sec in data['default']):
            raise ValueError("Alcune delle chiavi specificate non sono ammesse, chiavi valide: {} nella sezione '[{}]'. Nel file di configurazione '{}'".format(allowed_keys, 'default', self.__filename))

        # trasformo le direttiva da liste al tipo corretto

        for k in data['default'].keys():
            # trasformazione delle liste in sets in modo da non aver duplicati
            if k in {'allow-ip'}:
                data['default'][k] = set(data['default'][k])

            elif k in {'dir-perms', 'file-perms'}:
                # verifico che i permessi specificati siano validi
                if self.__are_permissions_valid(data['default'][k][0]):
                    data['default'][k] = data['default'][k][0]
                else:
                    raise ValueError("I permessi directory '{}' non sono validi. Nella sezione '[{}]'. Nel file di configurazione '{}'.".format(data['default'][k][0], 'default', self.__filename))

            elif k in {'owner'}:
                # verifico che owner e group sia esistente

                if self.__to_user_id(data['default'][k][0]) is not None:
                    data['default'][k] = data['default'][k][0]
                else:
                    raise ValueError("L'utente '{}' non è valido. Nella sezione '[{}]'. Nel file di configurazione '{}'.".format(data['default'][k][0], 'default', self.__filename))

            elif k in {'group'}:
                # verifico che group sia esistente

                if self.__to_group_id(data['default'][k][0]) is not None:
                    data['default'][k] = data['default'][k][0]
                else:
                    raise ValueError("Il utente '{}' non è valido. Nella sezione '[{}]'. Nel file di configurazione '{}'.".format(data['default'][k][0], 'default', self.__filename))

            else:
                # per ogni altro campo, nel caso ci fossero più valori allora tengo il primo
                data['default'][k] = data['default'][k][0]


        # verifico che le chiavi necessarie esistano in FOLDER
        # tolgo dalle chiavi richieste quelle già specificate nella sezione default
        needed_keys = {'group', 'owner', 'dir-perms', 'file-perms'} - set(data['default'].keys())
        for f in data['folder']:
            if not os.path.isabs(f):
                raise ValueError("La sezione '[{}:{}]' descrive un percorso non assoluto. I percorsi devono essere assoluti. Nel file di configurazione '{}'.".format('folder', f, self.__filename))

            if not os.path.isdir(f):
                raise ValueError("La sezione '[{}:{}]' non descrive una directory oppure è inesistente. I percorsi devono essere assoluti. Nel file di configurazione '{}'.".format('folder', f, self.__filename))

            if not all(sec in data['folder'][f] for sec in needed_keys):
                raise ValueError("Le chiavi obbligatorie ({}) per la sezione '[{}:{}]' non sono tutte presenti. Aggiungerle nella sezione specificata o nella sezione di default. Nel file di configurazione '{}'".format(needed_keys, 'folder', f, self.__filename))

        # verifico che le chiavi esistenti siano dentro quelle ammesse
        allowed_keys = {'group', 'owner', 'dir-perms', 'file-perms'}
        for f in data['folder']:
            if not all(sec in allowed_keys for sec in data['folder'][f]):
                raise ValueError("Alcune delle chiavi specificate non sono ammesse, chiavi valide: {} nella sezione '[{}:{}]'. Nel file di configurazione '{}'".format(allowed_keys, 'folder', f, self.__filename))

        # aggiungo alle singole folder i permessi ereditati dal master
        needed_keys = {'group', 'owner', 'dir-perms', 'file-perms'}
        for f in data['folder']:
            for nk in needed_keys:
                if nk not in data['folder'][f]:
                    data['folder'][f][nk] = data['default'][nk]

        # verifico che le folder abbiano permessi validi
        for f in data['folder']:

            if self.__are_permissions_valid(data['folder'][f]['dir-perms']):
                data['folder'][f]['dir-perms'] = int(data['folder'][f]['dir-perms'], 8)
            else:
                raise ValueError("I permessi directory '{}' non sono validi. Nella sezione '[{}:{}]'. Nel file di configurazione '{}'.".format(data['folder'][f]['dir-perms'], 'folder', f, self.__filename))

            if self.__are_permissions_valid(data['folder'][f]['file-perms']):
                data['folder'][f]['file-perms'] = int(data['folder'][f]['file-perms'], 8)
            else:
                raise ValueError("I permessi directory '{}' non sono validi. Nella sezione '[{}:{}]'. Nel file di configurazione '{}'.".format(data['folder'][f]['file-perms'], 'folder', f, self.__filename))

            gid = self.__to_group_id(data['folder'][f]['group'])

            if gid is not None:
                data['folder'][f]['group'] = gid
            else:
                raise ValueError("Il gruppo '{}' non è valido. Nella sezione '[{}:{}]'. Nel file di configurazione '{}'.".format(data['folder'][f]['group'], 'folder', f, self.__filename))

            uid = self.__to_user_id(data['folder'][f]['owner'])

            if uid is not None:
                data['folder'][f]['owner'] = uid
            else:
                raise ValueError("Il gruppo '{}' non è valido. Nella sezione '[{}:{}]'. Nel file di configurazione '{}'.".format(data['folder'][f]['owner'], 'folder', f, self.__filename))


        # elimino i default dalla configurazione, ora che hanno terminato il loro scopo
        data['default'].pop('owner', None)
        data['default'].pop('group', None)
        data['default'].pop('dir-perms', None)
        data['default'].pop('file-perms', None)


        return data

    def __resolve_config_aliases(self, config_dict):
        """
        Procedura che risolve gli alias all'interno della configurazione
        Da chiamare in seguito alla lettura e validazione della configurazione

        Gli alias vengono risolti all'interno delle sezioni: folder e actions

        :throw RuntimeError:            nel caso in seguito alla risoluzione degli alias due cartelle siano duplicate
        """

        # inizio risolvendo quelli all'interno delle sezioni folders
        for old_folder, old_folder_value in config_dict.get('folder', {}).copy().items():
            # scorro le chiavi, i nomi delle cartelle sono nelle chiavi e non nei valori
            # ottengo il nome della cartella con gli alias risolti
            new_folder = os.path.abspath(self.__resolve_aliases(old_folder, config_dict))

            # devo rimuovere la chiave (salvando il suo valore) in modo che se non sono stati risolti alias, non entri in conflitto con se stessa
            config_dict['folder'].pop(old_folder)

            if new_folder in config_dict['folder']:
                raise RuntimeError('Durante la risoluzione degli alias sono state ottenute due cartelle duplicate. '
                                   'La cartella "{}" viene risolta in "{}" che è già presente'.format(old_folder, new_folder))
            else:
                # vado a sostituire la chiave all'interno del dizionario
                config_dict['folder'][new_folder] = old_folder_value

        # ora risolvo gli alias all'interno delle azioni
        for action_name, old_action in config_dict.get('action', {}).copy().items():
            # scorro le azioni, i placeholder devono essere sostituiti all'interno delle stringhe delle azioni
            action = "".join(old_action)            # uso un join in modo da poter gestire allo stesso modo stringhe e liste di stringhe

            # risolvo gli alias nell'azione e la sostituisco
            new_action = self.__resolve_aliases(action, config_dict)
            config_dict['action'][action_name] = new_action

    def __resolve_aliases(self, path, config_dict):
        """
        Funzione che dato un path risolve eventuali alias al suo interno e restituisce il path assoluto
        Se il path passato non dovesse contenere aliases allora viene restituito invariato

        :param path:                path nel quale risolvere gli aliases
        :throw RuntimeError:        nel caso non esiste un alias con il quale risolvere un placeholder

        :return:                    path con gli aliases risolti
        """
        # aliases => dizionario con chiave = nome placeholder, valore = valore da sostituire
        for alias in config_dict.get('aliases', []):
            # mettere uno slash in coda
            # per ogni alias definito nel dizionario degli aliases verifico se è presente nel path e in caso lo sostituisco
            # il formato del placeholder è definito come variabile privata della classe
            placeholder = self.__placeholder_format.format(alias)
            path = path.replace(placeholder, config_dict['aliases'][alias] + '/')

        return path

    def to_dict(self):
        return self.__config

    @staticmethod
    def __are_permissions_valid(permissions):
        """
        Verifica che dei permessi in formato ottale siano validi
        :param permissions: Stringa che contiene i permessi in ottale da validare
        """
        try:
            # converto da ottale i permessi
            int(permissions, 8)
        except ValueError:
            return False

        return True

    @staticmethod
    def __to_user_id(user):
        """
        Converte un nome di un gruppo nel relativo id
        :param user: Nome dell'utente
        :return: Id linux del gruppo
        """
        try:
            # ottengo l'id del gruppo
            uid = pwd.getpwnam(user).pw_uid
        except KeyError:
            return None

        return uid

    @staticmethod
    def __to_group_id(group):
        """
        Converte un nome di un gruppo nel relativo id
        :param group: Nome del gruppo
        :return: Id linux del gruppo
        """
        try:
            # ottengo l'id del gruppo
            gid = grp.getgrnam(group).gr_gid
        except KeyError:
            return None

        return gid