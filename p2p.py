#! -*- coding: utf-8 -*-
import os
import socket
from threading import Thread
import time,struct
import binascii
from nodo import Nodo
from utils import pega_todos_os_ips
from messages import Texto, Leave, Lookup, Update, Join, Message


global nodo

class Server:
    PORTA = 12345

    def __init__(self):
        global nodo      
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP  
        Message.sock = sock
        Leave.sock = sock
        Lookup.sock = sock
        Join.sock = sock
        Update.sock = sock

        s = sock 
        s.bind(("", self.PORTA))
        print "esperando mensagens na porta :", self.PORTA
        data = ""
        while 1 :
            data, addr = s.recvfrom(1024)
            print  "\nSERVER '%s' RECEBEU:  ||%s||" % (nodo.nid,binascii.hexlify(data))
            ip_remetente = addr[0]
            if len(data)==0:
                print "\nERROR:: mensagem não tratada foi recebida: ||%s||" % data
                continue

            codigo = struct.unpack("!B",data[0])[0]
            if codigo ==Texto.CODIGO:
                texto =  Texto.recebe(data)
                print "mensagem recebida:'%s'" % texto

            # trata LEAVE
            elif codigo == Leave.CODIGO:
                leave = Leave(nodo)
                leave.responde(ip_remetente, data)
            elif codigo == Leave.CODIGO_RESPOSTA:
                leave = Leave(nodo)
                sair = leave.recebe_resposta(data) 
                if sair:
                    nodo.saiDaRede()

            # trata LOOKUP
            elif codigo == Lookup.CODIGO:
                if nodo.esta_na_rede:
                    lookup = Lookup(nodo)
                    lookup.responde(ip_remetente, data) 
                else:
                    print "\n AVISO: Este nó não esta na rede, por isso não pode responder lookups!"
            elif codigo == Lookup.CODIGO_RESPOSTA:
                lookup = Lookup(nodo)
                lookup.recebe_resposta(data)

            # trata JOIN
            elif codigo == Join.CODIGO:
                join = Join(nodo)
                join.responde(ip_remetente, data)
            elif codigo == Join.CODIGO_RESPOSTA:
                join = Join(nodo)
                join.recebe_resposta(data)

            # trata UPDATE
            elif codigo == Update.CODIGO:
                update = Update(nodo)
                update.responde(ip_remetente,data)
            elif codigo == Update.CODIGO_RESPOSTA:
                update = Update(nodo)
                update.recebe_resposta(data)

            else:
                print "\nERROR:: mensagem não tratada foi recebida: ||%s||" % data


class Console:
    def __init__(self):
        comando =""
        global nodo
        while not comando.startswith('quit'):
            time.sleep(2);
            comando = raw_input('>>> ').strip()
            parametros = comando.split(' ')[1:]
            if comando.startswith('send'):
                 t=Texto(node=None,message=comando.split('send')[1])
                 t.envia()	
            elif comando.startswith('info'):
                print nodo.info()
            elif comando.startswith('start'):
                nodo.criaRede() 
            elif comando.startswith('leave'):
                l = Leave(nodo)
                l.envia()
            elif comando.startswith('join'):
                ip_join = raw_input('Informe o IP de entrada do join: ').strip()
                j = Join(nodo)
                j.envia(ip_join)

            elif comando.startswith('lookup'):
                ip =  raw_input('Informe IP de algun nó da rede: ').strip()
                nid_procurado = raw_input('Informe identificador do no procurado: ').strip()

                l = Lookup(nodo)
                l.envia(nodo,nid_procurado,ip)
            elif comando.startswith('netinfo'):
                nodo.identifica_rede()
            elif comando.startswith('quit'):
                if nodo.esta_na_rede:
                    l = Leave(nodo)
                    l.envia()
                    time.sleep(3)# espera respostas
                os._exit(0)
            else:
                if comando.strip():
                    print "Error: comando \"%s\" nao existe" % comando.split(' ')[0]
                
        os._exit(0)


def informeOpcao(opcoes):
    r = None
    while  not r:
        r = raw_input("\nInforme o numero da opção desejada: ").strip()
        if r not in opcoes:
            r = None
            print "ERROR: opção invalida!"
    return r

# main
if __name__== "__main__":
    # criando rede

    ips = pega_todos_os_ips()
    if len(ips)>1:
        ip = None

        print "\n----------------------------------------------------"
        while (not ip):
            print "Este computador possui mais de uma interface de rede:"
            for i,d in enumerate(ips):
                print "%d - %s (%s)" % (i+1,d[1],d[0]) 
            opcao = raw_input('Informe o numero da opção desejada: ')
            try:
                ip = ips[int(opcao) -1][1]
            except:
                print "ERROR: opção inválida!!!\n"
    else:
        ip = ips[0][1]

    # iniciando rede
    nodo = Nodo(ip) 

    try:
        # iniciando server e console
        tserver = Thread(target=Server)
        tclient = Thread(target=Console )
    except:
        print "Error: Não foi possível iniciar thread"
    tserver.start()
    tclient.start()
    tserver.join()
    tclient.join()




# vim: set ts=4 sw=4 sts=4 expandtab:
