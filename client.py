#!/usr/bin/python
# -*- coding: utf-8 -*-
host = 'localhost'
port = 1459


import socket,  threading,select
import sys                           

connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    print ("La connexion a échoué.")
    sys.exit()    
print ("Connexion établie avec le serveur.")


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