#! -*- coding: utf-8 -*-
import os
import socket
from threading import Thread
import time,struct

from nodo import Nodo
from utils import pega_todos_os_ips
from messages import Texto, Leave, Lookup, Update, Join


global nodo

class Server:
    PORTA = 12345

    def __init__(self):
        global nodo      
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", self.PORTA))
        print "esperando mensagens na porta :", self.PORTA
        data = ""
        while 1 :
            data, addr = s.recvfrom(1024)
            print  "\nSERVER '%s' RECEBEU:  ||%s||" % (nodo.nid,data)
            ip_remetente = addr[0]
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
                lookup = Lookup(nodo)
                lookup.responde(ip_remetente, data) 
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
            elif comando.startswith('lookup'):
                l = Lookup(nodo)
                if len(parametros)==4:
                    nodo_origem = Nodo(nid=parametros[0],nip=parametros[1])
                    l.envia(nodo_origem,parametros[2],parametros[3])
                elif len(parametros)==2:
                    l.envia(nodo,parametros[0],parametros[1])
                else:
                    print "Error: numero incorreto de parametros\n Exemplos validos:\n  >>> lookup id_procurado ip_destino\n  >>> lookup id_origem ip_origem id_procurado ip_destino" 
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
# main
if __name__== "__main__":
    # criando rede
    ips = pega_todos_os_ips()
    if len(ips)>1:
        ip = None
        while (not ip):
            print "Este computador possuem mais de uma interface de rede:"
            for i,d in enumerate(ips):
                print "%d - %s (%s)" % (i+1,d[1],d[0]) 
            opcao = raw_input('informe aquela que deseja utilizar:')
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
