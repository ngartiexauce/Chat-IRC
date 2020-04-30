#!/usr/bin/python
# -*- coding: utf-8 -*-

HOST = ''
PORT = 1459
import socket, threading
liste_des_nick=[]
data={}
administrateur_nick = {}
clients_channels={}
import sys                                                       



def error_commande(self):
        error = "Saisissez la bonne commande"
        self.connexion.sendall(error.encode())


def help(self):
    message ="* /HELP: print this message\n* /LIST: list all available channels on server\n* /JOIN <channel>: join (or create) a channel\n* /LEAVE: leave current channel\n* /WHO: list users in current channel\n* <message>: send a message in current channel\n* /MSG <nick> <message>: send a private message in current channel\n* /BYE: disconnect from server\n* /KICK <nick>: kick user from current channel [admin]\n* /REN <channel>: change the current channel name [admin]\n* /CURRENT: print current channel name\n* /CURRENT <channel>: set current channel\n* /MSG <nick1;nick2;...> <message>: send a private message to several users in current channel\n* /NICK <nick>: change user nickname on server\n* /GRANT <nick>: grant admin privileges to a user [admin]\n* /REVOKE <nick>: revoke admin privileges [admin]\n"
    self.connexion.sendall(message.encode())


def liste(self):
    if(len(data) == 0):
        liste_alerte = "Il n'y a pas de chaines en cours\n"
        self.connexion.sendall(liste_alerte.encode())
    else:
        message = "Les chaines en cours sont:" 
        for c in list(data):
            message = message+" "+c
        message = message+"\n"
        self.connexion.sendall(message.encode())


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



def join_after_kick(self,commande,nom,nick): 
    commande = commande.replace("JOIN ","",1)
    commande = commande.replace("\n","")
    if commande in list(data):
        data[commande].append({"socket":self.connexion,"nom":nom,"nick":nick})
        c=0
        clients_channels[nick]["current_channel"] = commande 
        clients_channels[nick]["all_channel"].append(commande)
        clients_channels[nick]["actif"] = 1
    else:
        data[commande]=[{"socket":self.connexion,"nom":nom,"nick":nick}]
        clients_channels[nick]["current_channel"] = commande 
        clients_channels[nick]["all_channel"].append(commande)
        clients_channels[nick]["actif"] = 1
        administrateur_nick[clients_channels[nick]["current_channel"]] = {"first": nick, "all_admin":[nick]}

   
def kill(self,commande,nom,nick):
    commande = commande.split()
    if(len(commande) != 2):
        error_commande(self)
    elif(administrateur_nick[clients_channels[nick]["current_channel"]]["first"] != nick):
        commande_aministrateur_uniquement = "Calme toi t'es pas l'administrateur principale de la chaine"
        self.connexion.sendall(commande_aministrateur_uniquement.encode())
    else:
        for client in data[clients_channels[nick]["current_channel"]]:
            if(client["nick"] == commande[1] ):
                del clients_channels[client["nick"]]
                liste_des_nick.remove(client["nick"])
                message ="Vous êtes kill"
                client["socket"].sendall(message.encode())
               # client["socket"].sendall()
                client["socket"].close()
                data[clients_channels[nick]["current_channel"]].remove(client)

                break

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
            clients_channels[nick]["current_channel"] = msgClient 

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

def send_file(self,msgClient,nom,nick):
    msgClient =  msgClient.split()
    if(len(msgClient) != 3):
        error_commande(self)
    else:
        fichier = open (msgClient[2], "r")
        l = f.read(1024)
        for client in data[clients_channels[nick]["current_channel"]]:
            if(client["nick"] == msgClient[1]):
                message = "You receve a file from "+nick+",commande /RECV to receve"
                self.connexion.sendall(message.encode())
                while (l):
                    client["socket"].send(l)
                    l = f.read(1024)
            break  
def recv_file(self,msgClient,nom,nick):
    msgClient = msgClient.split()
    if(len(msgClient) != 2):
        error_commande(self)
    else:
        fichier = open(msgClient[1],'w')  
        for client in data[clients_channels[nick]["current_channel"]]:
            l = sc.recv(1024)
            while (l):
                fichier.write(l)
                l = sc.recv(1024)
        fichier.close()  

def nickname(self,nom,nick,nick_message):
    nick_message = nick_message.replace("message","",1)  
    if nick_message in liste_des_nick:
        c=1
        pseudo_pris = "Le pseudo est déjà utilisé\n"
        self.connexion.sendall(pseudo_pris.encode())
    else:
        liste_des_nick.append(nick_message)
        return nick_message

class ThreadClient(threading.Thread):
    ##'''dérivation d'un objet thread pour gérer la connexion avec un client'''
        def __init__(self, conn):
            threading.Thread.__init__(self)
            self.connexion = conn

        def run(self):
            nom = self.getName()
             # Dialogue avec le client :
            demande_nick = "Vous êtes connecté\nChoisissez un nickname ou faites la commande /BYE pour vous deconnecter\n"
            self.connexion.sendall(demande_nick.encode())
            nick = ""
            while(1):
                nick_message = self.connexion.recv(1024)
                nick_message=nick_message.decode()
                nick_message = nick_message.replace("\n","")
                nick_message = nick_message.split()
                if(len(nick_message) != 1 or len(nick_message[0])==7 ):
                    nick_alerte = "Choisissez un nickname valide ou faites la commande /BYE pour vous deconnecter\n"
                    self.connexion.sendall(nick_alerte.encode())
                else:
                    nick_message = nick_message[0]
                    if(nick_message.startswith("message")):
                        nick = nickname(self,nom,nick,nick_message)  
                    elif(nick_message.startswith("BYE") or nick_message==b''):
                        self.connexion.close()
                        break

                    if(nick in liste_des_nick):
                        nick_alerte = "Nickname bien choisi.\nFaites la commande /HELP pour plus d'aides.\n"
                        self.connexion.sendall(nick_alerte.encode())
                        break
                    else:
                        nick_alerte = "Choisissez un nickname valide ou faites la commande /BYE pour vous deconnecter\n"
                        self.connexion.sendall(nick_alerte.encode())
            while(nick in liste_des_nick):
                commande = self.connexion.recv(1024)
                commande = commande.decode()
                c=1
                if(commande.startswith("LIST")):
                    liste(self)
                    join_alerte = "Rejoignez une chaine existante ou créez une nouvelle.\nFaites la commande /HELP pour plus d'aides.\n"
                    self.connexion.sendall(join_alerte.encode())
                elif(commande.startswith("BYE") or commande == '' ):
                    liste_des_nick.remove(nick)
                    self.connexion.close()
                    break
                elif(commande.startswith("HELP")):
                    help(self)
                elif(commande.startswith("JOIN")):
                    join(self,commande,nom,nick)
                    c=0
                else:
                    error_commande(self)
                if(c==0):
                   
                    bienvenue = "Bienvenue dans la chaine!\nVous pouvez communiquez avec les autres menbres.\nFaites la commande /HELP pour plus d'aides.\n"                                
                    self.connexion.sendall(bienvenue.encode())
                    break
            while (nick in liste_des_nick ): 
                print(liste_des_nick)  
                msgClient = self.connexion.recv(1024)
                msgClient = msgClient.decode()
                msgClient = msgClient.replace("\n","")
                if(nick not in liste_des_nick):
                    break
                elif(clients_channels[nick]["actif"] == 0): 
                    print("cccccccccc")
                    leave(self,nom,nick)
                    if not(nick in liste_des_nick):
                        break
                elif(msgClient.startswith("WHO")):
                    who(self,nom,nick)
                elif(msgClient.startswith("message")):
                    message_(self,msgClient,nom,nick)
                elif(msgClient.startswith("LIST")):
                    liste(self)
                elif(msgClient.startswith("KILL")):
                    kill(self,msgClient,nom,nick)
                elif(msgClient.startswith("HELP")):
                    help(self)
                elif(msgClient.startswith("MSG ")):
                    msg_private(self,msgClient,nom,nick)
                elif(msgClient.startswith("KICK ")):
                    kick(self,msgClient,nom,nick)
                elif(msgClient.startswith("CURRENT")):
                    kick=0
                    current_channel(self,nick,nom,msgClient,kick)
                elif(msgClient.startswith("NICK ")):
                    nick_change(self,nom,nick,msgClient)
                elif(msgClient.startswith("GRANT ")):
                    grant(self,nom,nick,msgClient)
                elif(msgClient.startswith("REVOKE ")):
                    revoke(self,nom,nick,msgClient)
                elif(msgClient.startswith("REN ")):
                    ren(self,msgClient,nom,nick)
                elif(msgClient.startswith("JOIN ")):
                    join_v1(self,nom,nick,msgClient)
                elif(msgClient.startswith("BYE") or msgClient==''):
                    leave_kick=0
                    bye(self,nom,nick,leave_kick)
                    break
                elif(msgClient.startswith("LEAVE")):
                    leave(self,nom,nick)
                    if not(nick in liste_des_nick):
                        break
                else:
                    error_commande(self)
                
            

                # Le thread se termine ici    

        # Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
        mySocket.bind((HOST, PORT))
except socket.error:
        print ("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()
print ("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)

# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}                # dictionnaire des connexions clients
while 1:
        connexion, adresse = mySocket.accept()
        th = ThreadClient(connexion)
        th.start()
