# Mini-Projet Réseau

##### A rendre pour le 30.04.

### ─

#### LUWEH ADJIM NGARTI Exaucé

#### LAAMOUMRI Yassine


### Vue d'ensemble

Le but de ce projet est d'implémenter un serveur/client chat.
On abordera la version minimaliste de ce projet comme étant la version v0 puis la
version étendu comme v1.

### Objectifs

Ce compte rendu mettra en valeur nos choix techniques et les protocoles de
communications utilisés ainsi qu’une documentation et une justification d’utilisation de ces
derniers.

### Grandes étapes

#### I. Utilisation de Thread

```
Dans cette partie, on retrouvera la justification de notre protocole de
communication ainsi que son fonctionnement
```
#### II. Architecture de nos données

```
Dans cette partie, on élaborera quelles types de données avons nous utilisés et
pourquoi.
```
#### III. Nos extensions implémentés

```
Ici, on expliquera comment nous avons implémentés les extensions présentes dans
notre serveur/client chat.
```
#### IV. Fichier Client

```
Puis, on évoquera les différentes fonctionnalités de notre fichier client.py
```
#### V. Schéma Bilan

```
Pour terminer, un schéma bilan appuiera le fonctionnement de notre chat.
```

## I. Utilisation de Thread

##### A)Notre choix de protocole de communication

Tout d’abord, le premier dilemme qui s’offre à nous se trouve sur le choix de notre
protocole de communication.
Nous avons décidé de choisir la méthode TCP multi-thread car elle permet de créer
un thread pour chaque client connecté et donc un espace mémoire lui est alloué ce
qui permet de traiter tous les clients simultanément.

##### B)Utilisation de Thread
```python
class ThreadClient(threading.Thread):
    ##'''dérivation d'un objet thread pour gérer la connexion avec un client'''
        def __init__(self, conn):
            threading.Thread.__init__(self)
            self.connexion = conn
```

De cette façon, on crée une classe ThreadClient afin de traiter chaque client
indépendamment


## II. ​Architecture de nos données
```python
liste_des_nick=[]
data={}
administrateur_nick = {}
clients_channels={}

```
Dans cette partie on expliquera en détails le format de nos données utilisées.
Tout d’abord la variable data est un dictionnaire comportant comme clé
les chaînes créées dans le serveur.

Elle prend comme valeur un dictionnaire dans un tableau ( car impossibilité d’avoir
un dictionnaire comme valeur).

Ce dictionnaire a pour clé ​ **nom​** , ​ **socket​** , ​ **nick​** et respectivement comme valeur le
**nom du Thread​** , le ​ **socket client​** et le ​ **nom du client​**.
Voici la structure de la variable en détail :
**data = {“chaîne1” : [{“nom” : nom_Thread, “socket” : socket_client, “nick” :
nick_client}]..}**

Grâce à la fonction ​ **self.getName()​** , on récupére le nom de chaque Thread qui est
unique et qui permet de différencier chaque Thread.
La variable liste_des_nicks est un tableau comportant l’ensemble des nicks utilisés
et présent dans un channel.

La variable client_channels est un dictionnaire comportant comme clé
les noms des clients présents dans le serveur.
Elle prend comme valeur un dictionnaire dans un tableau.


Ce dictionnaire a pour clé ​ **current_channel​** , ​ **all_channel​** et respectivement comme
valeur la ​ **chaîne actuelle​** et un tableau contenant ​ **toutes les chaînes où le client
est connecté​**.

Voici la structure de la variable en détail : ​ **client_channels = { “nom_client” :
[{“current_channel” : current_channel, “all_channel :
[toutes_les_chaînes_connecté]}],..}**

La variable administrateur_nick est un dictionnaire comportant comme clé le nom
des chaînes disponibles sur le serveur.
Elle prend comme valeur un dictionnaire dans un tableau.

Ce dictionnaire a pour clé ​ **first​** , ​ **all_admin​** et respectivement comme valeur le ​ **nom
de l’admin principal ​** et un ​ **tableau​** contenant ​ **toutes les client ayant des droits
d’administrateurs.**

La principal différence entre l’admin principal et les autres administrateurs se
trouvent dans les commandes exécutables telles que ​ **/REVOKE​** , ​ **/GRANT​** et ​ **/KICK​**.
Voici la structure de la variable en détail : ​ **administrateur_nick = {“nom_chaîne” :
[{“first” : main_admin, “all_admin” : [client_ayant_droits_admin]}],..}**

<span style="color:red">
**Attention**​ :
Dans notre rendu final , deux versions finale ont été proposé, l’une avec les
fonctions qui satisfont tous les tests VPL et l’autre avec une version amélioré qui
utilise une fonction supplémentaire : les administrateurs principaux et secondaires
Et ce compte-rendu met en évidence la version amélioré que nous considérons
comme plus pertinent vu que cela modère plus efficacement la gestion des admins.
C’est pourquoi nous avons décidé d’établir une hiérarchie dans le système
d’admins.
Ce qui change concrètement est notre variable administrateur_nick et par la même
occasion les commandes /WHO, /KICK, /GRANT, /REVOKE et /KILL.
Détail variable ​ **administrateur_nick = {“nom_chaîne” : [{“all_admin” :
[client_ayant_droits_admin]}],..}**</span>


## III. ​Nos extensions implémentés

##### A)Extension projet v

Voici la liste des extensions implémentés ainsi qu’un descriptif de ces derniers :
La fonction /HELP permet d’afficher un message au client afin qu’il soit en
connaissance de toutes les commandes utilisables.

```python
def help(self):
    message ="* /HELP: print this message\n* /LIST: list all available channels on server\n* /JOIN <channel>: join (or create) a channel\n* /LEAVE: leave current channel\n* /WHO: list users in current channel\n* <message>: send a message in current channel\n* /MSG <nick> <message>: send a private message in current channel\n* /BYE: disconnect from server\n* /KICK <nick>: kick user from current channel [admin]\n* /REN <channel>: change the current channel name [admin]\n* /CURRENT: print current channel name\n* /CURRENT <channel>: set current channel\n* /MSG <nick1;nick2;...> <message>: send a private message to several users in current channel\n* /NICK <nick>: change user nickname on server\n* /GRANT <nick>: grant admin privileges to a user [admin]\n* /REVOKE <nick>: revoke admin privileges [admin]\n"
    self.connexion.sendall(message.encode())


```

On stocke une chaîne de caractères dans une variable que l’on envoie au client.
La fonction /LIST permet d’afficher le nom de tous les chaînes disponibles sur
le serveur.

```python
def liste(self):
    if(len(data) == 0):
        liste_alerte = "Il n'Inline-style: 
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
y a pas de chaines en cours\n"
        self.connexion.sendall(liste_alerte.encode())
    else:
        message = "Les chaines en cours sont:" 
        for c in list(data):
            message = message+" "+c
        message = message+"\n"
        self.connexion.sendall(message.encode())

```

En premier lieu, on vérifie si la variable data n’est pas vide, si c’est le cas on envoie
un message d’information aux clients indiquant qu’il n’y a aucune chaîne
disponible sinon on stocke l’ensemble des chaînes disponibles dans une variable
sous forme de chaînes de caractères afin de l’envoyer au client.
La commande /JOIN permet de rejoindre une chaîne disponible au choix ou bien
d’en créer une le cas échéant.


```python
def join(self,commande,nom,nick):
    commande = commande.replace("JOIN ","",1)
    commande = commande.replace("\n","")
    commande = commande.split()
    if(len(commande) != 1):
        error_commande(self)
    else:
        commande = commande[0]
        cmd = 1
        if commande in list(data):
            data[commande].append({"socket":self.connexion,"nom":nom,"nick":nick})
            clients_channels[nick]={"actif":1,"current_channel":commande , "all_channel":[commande]}
            if(len(data[commande]) == 0):
                administrateur_nick[commande]["first"] = nick
                administrateur_nick[commande]["all_admin"].append(nick)
        else:
            data[commande]=[{"socket":self.connexion,"nom":nom,"nick":nick}]
            clients_channels[nick]={"actif": 1,"current_channel":commande , "all_channel":[commande]}
            administrateur_nick[clients_channels[nick]["current_channel"]]={"first" :nick,"all_admin":[nick]}
```



```python


def join_v1(self,nom,nick,commande):
    commande = commande.replace("\n","")
    commande = commande.split()
    if(len(commande) < 1):
        error_commande(self)
    else:
        commande = commande[1]
        cmd = 1
        if(commande in clients_channels[nick]["all_channel"]):
            message = "Vous êtes déjà dans cette chaine"
            self.connexion.sendall(message.encode())
        elif commande in list(data):
            data[commande].append({"socket":self.connexion,"nom":nom,"nick":nick})
            clients_channels[nick]["current_channel"] = commande
            clients_channels[nick]["all_channel"].append(commande)
            if(len(data[commande]) == 0):
                administrateur_nick[commande]["first"] = nick
        else:
            data[commande]=[{"socket":self.connexion,"nom":nom,"nick":nick}]
            clients_channels[nick]["all_channel"].append(commande)
            clients_channels[nick]["current_channel"] = commande
            administrateur_nick[clients_channels[nick]["current_channel"]]={"first":nick,"all_admin":[nick]}

```


Étant donné que cette commande est de type : /JOIN <nom_chaîne> alors nous
avons décidé de récupérer seulement le nom de la chaîne communiqué pour
traiter la demande.
Si le client ne communique aucun nom de chaîne alors une erreur lui sera envoyé,
sinon deux cas s’offre à nous :

- Soit le nom de chaîne n’existe pas, alors une nouvelle chaîne prenant
    ce nom est créer et le client rejoint la chaîne en devenant
    l’administrateur
- Soit le nom de la chaîne existe, alors le client rejoint la chaîne, s’il n’y a
    personne dans cette chaîne alors il devient l’administrateur.
La commande /LEAVE permet de quitter notre chaîne actuelle.



```python

def leave(self,nom,nick):
    client_deconnecte = nick+" est parti"
    if(administrateur_nick[clients_channels[nick]["current_channel"]]["first"] == nick and len(data[clients_channels[nick]["current_channel"]])>1):
        nouveau_admin = data[clients_channels[nick]["current_channel"]][1]
        administrateur_nick[clients_channels[nick]["current_channel"]]["first"] = nouveau_admin["nick"]
        administrateur_nick[clients_channels[nick]["all_channel"]].append(nouveau_admin["nick"])
        administrateur_nick[clients_channels[nick]["all_channel"]].remove(nick)
        message_nouveau_admin = "Vous êtes le nouveau administrateur de la chaine"
        nouveau_admin["socket"].sendall(message_nouveau_admin.encode())
    
    if(nick in administrateur_nick[clients_channels[nick]["current_channel"]]["all_admin"]):
        administrateur_nick[clients_channels[nick]["current_channel"]]["all_admin"].remove(nick)

    for cle in data[clients_channels[nick]["current_channel"]]:
        if(cle["nom"] != nom):
            cle["socket"].sendall(client_deconnecte.encode())
        else:
            data[clients_channels[nick]["current_channel"]].remove(cle)
            clients_channels[nick]["all_channel"].remove(clients_channels[nick]["current_channel"])
    clients_channels[nick]["actif"] = 0
    leave_alerte= "Vous n'êtes plus dans la chaine.\nRejoingnez une autre chaine.\nFaites la commande /HELP pour plus d'aides.\n" 
    self.connexion.sendall(leave_alerte.encode())
    while(1):
        commande = self.connexion.recv(1024)
        commande = commande.decode()
        if(commande.startswith("JOIN")):        
            join_after_kick(self,commande,nom,nick)
        elif(commande.startswith("LIST")):
            liste(self)
        elif(commande.startswith("HELP")):
            help(self)
        elif(commande.startswith("BYE") or commande==''):
            leave_kick = 1
            bye(self,nom,nick,leave_kick)
            break
        elif(commande.startswith("CURRENT")):
            kick=1
            current_channel(self,nick,nom,commande,kick)   
        else:
            error_commande(self)
        if(clients_channels[nick]["actif"]==1):
            chaine_choisi = "Vous avez regagné un nouveau groupe\nVous pouvez communiquer avec les menbres.\n"
            self.connexion.sendall(chaine_choisi.encode())
            break 
```


Tout d’abord, avant de faire quitter le client de la chaîne, si le client est
administrateur de la chaîne alors on désigne un nouveau administrateur puis par le
suite le client quitte la chaîne.
Ensuite, le client se trouve à “l’accueil”, où seulement trois commandes sont
possibles : /JOIN , /HELP, /CURRENT, /LIST et /BYE.
La commande /WHO permet d’afficher la liste des utilisateurs présents dans la
chaîne.

```python


def who(self,nom,nick):
    liste_des_clients="Liste des adherents:"
    if(len(data[clients_channels[nick]["current_channel"]]) == 1):
        who_alerte = "Vous êtes seul(e) dans cette chaine"
        self.connexion.sendall(who_alerte.encode())
    else:
        for client in data[clients_channels[nick]["current_channel"]]:
            if(client["nom"] != nom):
                if(administrateur_nick[clients_channels[nick]["current_channel"]]["first"] == client["nick"]):
                    liste_des_clients =liste_des_clients+"\n@"+client["nick"]+"@"
                else:
                    liste_des_clients =liste_des_clients+"\n"+client["nick"]
        liste_des_clients=liste_des_clients+"\n"
        self.connexion.sendall(liste_des_clients.encode()) 


```


Ici, on vérifie tout d’abord si le client n’est pas seul dans la chaîne si c’est le cas on
lui envoie un message l’informant de cela sinon on lui envoie la liste des clients sur
la chaîne actuelle.
La commande /MSG <nick> <message> permet d’envoyer un message privée à un
autre client.



```python


def message_(self,msgClient,nom,nick):
    msgClient = msgClient.replace("message","",1)
    if(len(data[clients_channels[nick]["current_channel"]]) == 1):
        message_alerte = "Vous êtes seul(e) dans cette chaine"
        self.connexion.sendall(message_alerte.encode())
    elif(len(msgClient)==0 or msgClient.isspace()==True):
        error_commande(self)
    else:
        msgClient = "%s: %s" % (nick, msgClient)    
        for cle in data[clients_channels[nick]["current_channel"]]:
            if cle["nom"] != nom:
                cle["socket"].sendall(msgClient.encode())
```

Dans cette fonction, on vérifie si le client est tout seul dans la chaîne, si c’est le cas
on lui envoie un message le lui informant sinon on vérifie si le destinateur se trouve
dans la chaîne et si c’est le cas le message lui est envoyé à lui seul sinon un
message d’erreur apparaît.
La commande /BYE permet de quitter le serveur.


```python


def bye(self,nom,nick,leave_kick):
    client_deconnecte = nick+" est parti"
    if(administrateur_nick[clients_channels[nick]["current_channel"]]["first"] == nick and len(data[clients_channels[nick]["current_channel"]])>1):
        nouveau_admin = data[clients_channels[nick]["current_channel"]][1]
        administrateur_nick[clients_channels[nick]["current_channel"]]["first"] = nouveau_admin["nick"]
        message_nouveau_admin = "Vous êtes le nouveau administrateur de la chaine"
        nouveau_admin["socket"].sendall(message_nouveau_admin.encode())
    for cle in data[clients_channels[nick]["current_channel"]]:
        if(cle["nom"] != nom and leave_kick ==0):
            cle["socket"].sendall(client_deconnecte.encode())
        else:
            data[clients_channels[nick]["current_channel"]].remove(cle)
            del clients_channels[nick]
    liste_des_nick.remove(nick) 
    self.connexion.close()


```
Ici, on prend le soin de vérifier si le client est administrateur d’une des chaînes, si
c’est le cas on le destitue de ces droits pour les octroyer à un autre client.
Puis,on supprime le client de notre base de
données(data,clients_channels,liste_des_nicks) puis on ferme le thread qui lui est
associé.


La commande /KICK permet d’éjecter un client d’une chaîne, seulement un client
ayant les droits d’administrateurs peut effectuer cette commande.

```python


def kick(self,msgClient,nom,nick):
    if(administrateur_nick[clients_channels[nick]["current_channel"]]["first"] != nick):
        commande_aministrateur_uniquement = "Calme toi t'es pas l'administrateur du groupe"
        self.connexion.sendall(commande_aministrateur_uniquement.encode())
    else:   
        kick = msgClient.split()
        if(len(kick) !=2):
            error_commande(self)
        elif(kick[1] == nick):
            message= "Utilisez la commande /LEAVE pour quitter la chaine"
            self.connexion.sendall(message.encode())
        else:
            destinateur_kick_trouve =0 
            for cle in data[clients_channels[nick]["current_channel"]]:    
                if cle["nick"] == kick[1] and not(kick[1] in administrateur_nick[clients_channels[nick]["current_channel"]]["all_admin"]):
                    you_is_kick  = nick+" vous a retiré de la chaine"
                    cle["socket"].sendall(you_is_kick.encode())
                    data[clients_channels[nick]["current_channel"]].remove(cle)
                    clients_channels[cle["nick"]]["actif"] = 0
                    destinateur_kick_trouve =1
            if(destinateur_kick_trouve ==0 ):
                destinateur_kick_non_trouve = kick[1]+" n'est pas dans cette chaine"
                self.connexion.sendall(destinateur_kick_non_trouve.encode())


```
Dans cette fonction, on vérifie en premier lieu si le client a les droits
d’administrateur, si ce n’est pas le cas un message d’erreur apparaît.
Si un administrateur essaie de s’éjecter alors un message d’erreur apparaît.
Si l’administrateur essaie d’éjecter un client qui ne se trouve pas de cette chaîne, un
message d’erreur apparaît , et si le client se trouve dans la chaîne alors il est éjecté.


La commande /REN <channel> permet de renommer le nom de la chaîne actuelle,
seul un client ayant les droits d’administrateur peut effectuer cette commande.


```python
def ren(self,msgClient,nom,nick):
    if(administrateur_nick[clients_channels[nick]["current_channel"]]["first"] != nick):
        commande_aministrateur_uniquement = "Calme toi t'es pas l'administrateur de la chaine"
        self.connexion.sendall(commande_aministrateur_uniquement.encode())
    else:
        msgClient = msgClient.replace("REN ","",1)
        if(msgClient.isspace()==True ):
            error_commande(self)
        if(msgClient in list(data)):
            ren_error = "Cette chaine existe déjà"
            self.connexion.sendall(ren_error.encode())
        else:   
            channel_new_name_msg = "Votre chaine est renommée  "+msgClient
            for cle in data[clients_channels[nick]["current_channel"]]:
                if(cle["nom"] != nom):
                    clients_channels[cle["nick"]]["current_channel"] = msgClient
                    cle["socket"].sendall(channel_new_name_msg.encode())
                else:
                    ren_succes = "Votre a été bien renommée"
                    self.connexion.sendall(ren_succes.encode())       
            data[msgClient] = data.pop(clients_channels[nick]["current_channel"])
            administrateur_nick[msgClient] = administrateur_nick.pop(clients_channels[nick]["current_channel"]) 
            clients_channels[nick]["all_channel"].remove(clients_channels[nick]["current_channel"])
            clients_channels[nick]["all_channel"].append(msgClient)
            clients_channels[nick]["current_channel"] = msgClient ```


```


Ici, on vérifie tout d’abord si le client possède les droits d’administrateur.
Si c’est le cas, on vérifie si le nom de chaîne proposé existe déjà.
Puis, la chaîne est renommée en modifiant notre base de donnée.


##### B)Extension projet v

La commande /CURRENT permet d’afficher la chaîne actuelle et la commande
/CURRENT <channel> permet de modifier le nom de la chaîne actuelle.

```python
def current_channel(self,nick,nom,msgClient,kick):
    if(msgClient.isspace()==True ):
        error_commande(self)
    else:
        msgClient_ = msgClient.split()
        msgClient = msgClient.replace("CURRENT ","",1)
        if(len(msgClient_) >= 2 and msgClient in clients_channels[nick]["all_channel"]):
            clients_channels[nick]["current_channel"]= msgClient
            clients_channels[nick]["actif"]=1
        elif(len(msgClient_) >= 2 and not(msgClient in clients_channels[nick]["all_channel"])):
            message = "Vous n'êtes pas dans cette chaine"
            self.connexion.sendall(message.encode())
        else:
            if(kick==0):
                message = "Votre chaine actuel est: "
                message = message+clients_channels[nick]["current_channel"]
                self.connexion.sendall(message.encode())
            else:
                message = "Vous n'avez pas de chaine actuellement"
                self.connexion.sendall(message.encode())


```
Ici, on récupère le nom de la chaîne actuelle puis on la place comme étant notre
chaîne actuelle dans notre base de données
La commande /MSG <nick1;nick2;..> <message> permet d’envoyer un message
privée à plusieurs clients.


```python

def msg_private(self,msgClient,nom,nick):
    msgClient = msgClient.replace("MSG ","",1)
    msgClient_ = msgClient.split()

    if(len (msgClient_) <2):
        error_commande(self)
    else:
        nicks =msgClient_[0].split(";")
        msgClient = msgClient.replace(msgClient_[0],"",1)
        print(msgClient)
        print(msgClient_[0])
        for client in data[clients_channels[nick]["current_channel"]]:
            if client["nick"] in nicks:
                message = "Private message %s: %s" % (nick, msgClient)
                client["socket"].sendall(message.encode())


```
Dans cette fonction, on récupère la liste des destinateurs et le message en coupant
la commande envoyé grâce à la fonction split
Puis on envoie le message à chaque destinataire.


La commande /NICK <nick> permet de modifier son nickname utilisé dans le
serveur.

```python

def nick_change(self,nom,nick,msgClient):
    msgClient == msgClient.split()
    new_nick = msgClient[1]
    if(len(msgClient_) != 2):
        error_commande(self)
    elif(new_nick in liste_des_nick):
        message = "Nickname déjà utilisé"
        self.connexion.sendall(message.encode())
    else:
        for client in data[clients_channels[nick]["current_channel"]]:
            if client["nick"] == nick:
                message = "Votre identifiant est bien mis à jour"
                self.connexion.sendall(message.encode())
                liste_des_nick.remove(nick)
                liste_des_nick.append(new_nick)
                client["nick"] = new_nick
                clients_channels[new_nick] = clients_channels.pop(nick)	
                break
        if(administrateur_nick[clients_channels[new_nick]["current_channel"]]["first"]==nick):
            administrateur_nick[clients_channels[new_nick]["current_channel"]]["first"]= new_nick
            administrateur_nick[clients_channels[new_nick]["current_channel"]]["all_admin"].remove(nick)
            administrateur_nick[clients_channels[new_nick]["current_channel"]]["all_admin"].append(new_nick)
        nick = new_nick


```

Ici, on vérifie si le nickname proposé est valide( càd pas déjà utilisé et sans espaces),
puis on modifie la valeur du nickname du client dans notre base de données.
La commande /GRANT <nick> (exécutable seulement par l’admin principal )
permet d’octroyer des droits d’administrateurs secondaire à un autre client.

```python

def grant(self,nom,nick,msgClient):
	msgClient = msgClient.split()
	if(len(msgClient) != 2 ):
		error_commande(self)
	elif(administrateur_nick[clients_channels[nick]["current_channel"]]["first"] != nick):
		commande_aministrateur_uniquement = "Calme toi t'es pas l'administrateur de la chaine"
		self.connexion.sendall(commande_aministrateur_uniquement.encode())
	else:
		for client in data[clients_channels[nick]["current_channel"]]:
			if client["nick"] == msgClient[1]:
				administrateur_nick[clients_channels[nick]["current_channel"]]["all_admin"].append(msgClient[1])
				message = "Vous avez réçu de "+nick+" les privilèges d'un administrateur "
				client["socket"].sendall(message.encode())


```


Dans cette fonction, on vérifie si le client est un administrateur principal de la
chaîne actuelle puis si c’est le cas on ajoute le client renseigner comme
administrateur secondaire.


La commande /REVOKE <nick> (exécutable seulement par l’admin principal )
permet d’enlever les droits d’administrateurs à un autre client.

```python

def revoke(self,nom,nick,msgClient):
	msgClient = msgClient.split()
	if(len(msgClient) != 2):
		error_commande(self)
	elif(administrateur_nick[clients_channels[nick]["current_channel"]]["first"] != nick):
		commande_aministrateur_uniquement = "Calme toi t'es pas l'administrateur de la chaine"
		self.connexion.sendall(commande_aministrateur_uniquement.encode())
	else:
		for client in data[clients_channels[nick]["current_channel"]]:
			if client["nick"] == msgClient[1] and msgClient[1] in administrateur_nick[clients_channels[nick]["current_channel"]]["all_admin"]:
				administrateur_nick[clients_channels[nick]["current_channel"]]["all_admin"].remove(msgClient[1])
				message = "Oups vos privilèges d'administrateur ont été retirés par  "+nick
				client["socket"].sendall(message.encode())
				break


```
De la même façon que la fonction grant, on accède à notre base de donnée
représentant les droits d’administrateurs et on enlève les droits d’administrateur de
la personne concerné.

## IV. ​Descriptif de notre implémentation client

```python

while True: 
  
    sockets_list = [sys.stdin, connexion] 
  
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
    c=0
    for sock in read_sockets: 
        if sock == connexion: 
            message = sock.recv(2048)
            if(message == b'' or len(message)==0) :
               connexion.close()
               c=1
               break
            else: 
                print (message.decode()) 
        else:
            message = sys.stdin.readline()
            if message.startswith("/") :
                message = message.replace("/","",1)
                connexion.sendall(message.encode())
                if (message.startswith("BYE")):
                    print("AU REVOIR !")
                    connexion.close() 
                    c=1
                    break
            elif(message == b''):
                message = "BYE"
                connexion.sendall(message.encode())
                connexion.close() 
                break
            else: 
                message = "message"+message
                connexion.sendall(message.encode())
    if(c==1):
        break 



``` 

De notre côté client,on traite le cas où le client utilise la commande BYE afin de
fermer la connexion de son côté.
Dans le cas où le serveur se crashe, il reçoit un message nul afin de fermer la
connexion.
Bien évidemment, tous les messages reçus lui sont affichés.


## V. ​Schéma bilan représentant le fonctionnement de

## notre chat
![alt text](https://raw.githubusercontent.com/ngartiexauce/Chat-IRC/master/chat.png "Résumé du chat")


