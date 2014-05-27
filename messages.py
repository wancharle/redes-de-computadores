#! -*- coding: utf-8 -*-

import socket, struct, binascii
from nodo import Nodo
class Message:
    CODIGO = 'M'
    UDP_PORT = 12345
    
    def __init__(self,node, message=None):
        self.node = node
        self.message = ['s',message]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP  
       
    def envia(self,UDP_IP):  
        data = struct.pack("!B"+self.message[0],int(self.CODIGO), *self.message[1:])
        print "mensagem enviada (%s): ||%s||" % (UDP_IP, binascii.hexlify(data))        
        self.sock.sendto(data, (UDP_IP, self.UDP_PORT)) 

    def envia_resposta(self,UDP_IP):
        data = struct.pack("!B"+self.message[0],int(self.CODIGO_RESPOSTA), *self.message[1:])
        print "resposta enviada (%s): ||%s||" % (UDP_IP, binascii.hexlify(data))       
        self.sock.sendto(data, (UDP_IP, self.UDP_PORT)) 

    def recebe(self,datagram):
        pass

class Texto(Message):
    CODIGO = 'T' # 84

    @classmethod
    def recebe(self, datagram): 
        return datagram[1:]

class Lookup(Message):
    CODIGO = chr(2)
    CODIGO_RESPOSTA = chr(66)

    def envia(self,node_origem, nid_procurado, ip_destino):
        self.message = node_origem.nid + node_origem.getBytesIP() + nid_procurado
        Message.envia(self, ip_destino)       
    
    def responde(self, remetente, data):
        nid_origem = data[1:5]
        bip_origem = data[5:9]
        nid_procurado = data[9:13]
        
        node_origem = Nodo(bip=bip_origem, nid=nid_origem) 
 
        # 1 - se o nid existe
        if nid_procurado == self.node.nid:
             sucessor = self.node.sucessor
        # 2 - se o nid não existe
        elif nid_procurado < self.node.nid:
            # 2.1 - procura nid proximo caminhando para o inicio
            if self.node.nid <= self.node.antecessor.nid:
                # se esta no inicio do circulo ou só tem 1 no na rede 
                # entao o novo sucessor é no atual, ou seja, o primeiro
                sucessor = self.node
            else:
                if nid_procurado > self.node.antecessor.nid:
                    # se antecessor nao pode ser sucessor o novo sucessor eh o nó atual
                    sucessor = self.node
                else:
                    # se nao pergunte para ele quem é o novo sucessor
                    self.envia(node_origem, nid_procurado, self.node.antecessor.ip)
                    print "LOOKUP BACKWARD enviado para antecessor de %s (%s)" % (self.node.nid,self.node.ip)
                    return # finaliza pois ja tratou

        elif nid_procurado > self.node.nid:
            # 2.2 - procura nid proximo caminhando para o fim
            if self.node.nid >= self.node.sucessor.nid:
                # se esta no fim do circulo ou so tem 1 no na rede  
                # entao o sucessor é o sucessor do no atual
                sucessor = self.node.sucessor
            else:
                if nid_procurado > self.node.sucessor.nid:
                    # se o sucessor nao pode ser sucessor o novo sucessor eh o no atual
                    sucessor = self.node
                else:
                    # se nao pergunte para ele quem é o novo sucessor
                    self.envia(node_origem, nid_procurado, self.node.sucessor.ip)
                    print "LOOKUP FORWARD enviado para sucessor de %s (%s)" % (self.node.nid,self.node.ip)
                    return # finaliza pois ja tratou

        
        # responde para node_origem apenas
        self.message = nid_procurado + sucessor.nid + sucessor.getBytesIP()
        self.envia_resposta(node_origem.ip)           
        print "LOOKUP respondido para %s (%s):\n--- sucessor = %s (%s)" % (node_origem.nid, node_origem.ip, sucessor.nid, sucessor.ip)
        return
    
    def recebe_resposta(self,data):
        nid_procurado = data[1:5]
        nid_sucessor = data[5:9]
        bip_sucessor = data[9:13]
        sucessor = Nodo(bip=bip_sucessor,nid=nid_sucessor)
        if self.node.esta_na_rede:
            # apenas imprime a resposta
            print "resposta de LOOKUP recebida:\n --- nid_procurado = %s\n --- sucessor = %s (%s)" % (nid_procurado, sucessor.nid, sucessor.ip)
            self.node.recebe_lookup(nid_procurado,sucessor)
        else:
            if nid_procurado == self.node.nid:
                # se for uma resposta de pedido proprio efetua join
                j = Join(self.node)
                j.envia(sucessor.ip)
            else:
                print "resposta de LOOKUP recebida:\n --- nid_procurado = %s\n --- sucessor = %s (%s)" % (nid_procurado, sucessor.nid, sucessor.ip)


class Join(Message):
    CODIGO = chr(0)
    CODIGO_RESPOSTA = chr(64)

    def envia(self,ip_destino):
        self.message = self.node.nid
        Message.envia(self, ip_destino)

    def responde(self, remetente, data):
        ip_antecessor = remetente
        nid_antecessor = data[1:5]
        
        # atualizando antecessor do nó sucessor
        novo_antecessor = self.node.antecessor        
        self.node.antecessor = Nodo(nip=ip_antecessor,nid=nid_antecessor)
        
        # respondendo o join
        novo_sucessor = self.node
        self.message = novo_sucessor.nid + novo_sucessor.getBytesIP() + novo_antecessor.nid + novo_antecessor.getBytesIP()
        self.envia_resposta(remetente)
        print "JOIN respondido:\n --- %s foi adicionado a rede como antecessor de %s!" % (nid_antecessor, self.node.nid) 

    def recebe_resposta(self,data):
        nid_sucessor = data[1:5]
        bip_sucessor = data[5:9]
        nid_antecessor = data[9:13]
        bip_antecessor = data[13:17]
       
        # entrando na rede          
        self.node.antecessor = Nodo(bip=bip_antecessor, nid=nid_antecessor)
        self.node.sucessor = Nodo(bip=bip_sucessor, nid=nid_sucessor) 
        self.node.esta_na_rede = True
        print "resposta de JOIN recebido:\n --- %s entrou na rede!" % self.node.nid

        # atualizando sucessor do nó antecessor
        u = Update(self.node)
        novo_sucessor = self.node
        u.envia(novo_sucessor, self.node.antecessor.ip)
        print "UPDATE enviado: sucessor de %s é %s " % (self.node.antecessor.nid, self.node.nid)

class Update(Message):
    CODIGO = chr(3)
    CODIGO_RESPOSTA = chr(67)

    def envia(self,novo_sucessor, ip_destino):
        self.message = novo_sucessor.nid + novo_sucessor.getBytesIP()
        Message.envia(self,ip_destino)

    def responde(self,remetente,data):
        novo_sucessor = Nodo(nid=data[1:5],bip=data[5:9])
        self.node.sucessor = novo_sucessor
        print "UPDATE respondido: %s é novo sucessor de %s!" % (novo_sucessor.nid, self.node.nid)
        self.message = self.node.nid
        self.envia_resposta(remetente)

    def recebe_resposta(self,data):
        nid_origem=data[1:5]
        print "resposta de UPDATE recebida:\n --- %s atualizou seu sucessor" % nid_origem
        

class Leave(Message):
    CODIGO = int(1) # leave codigo = 1
    CODIGO_RESPOSTA = int(65)

    LEAVES = []

    def envia(self): 
        # monta mensagem
        if self.node.esta_na_rede == False:
            print "ATENÇÂO: este nó ainda não pertence a uma rede!"
            return
        node = self.node
        
        self.message = ["IIIII",]
        self.message += [node.nid,  node.sucessor.nid, node.sucessor.getBytesIP()]
        self.message += [node.antecessor.nid,  node.antecessor.getBytesIP()]
        

        # salva nids para esperar resposta
        self.LEAVES.append(node.sucessor.nid)
        self.LEAVES.append(node.antecessor.nid)

        # envia mensagem de leave

        print "\n---> '%s' enviou leave!" % node.nid
        Message.envia(self, self.node.sucessor.ip) 
        Message.envia(self, self.node.antecessor.ip)

    def responde(self, remetente, data):
        # desempacota os dados
        dados = struct.unpack("!BIIIII",data)
        nid_saindo = dados[1] 
        nid_sucessor = dados[2]
        bip_sucessor = dados[3]
        nid_antecessor = dados[4]
        bip_antecessor = dados[5]

        # rebalancea os nos
        if self.node.sucessor.nid == nid_saindo:
            sucessor = Nodo(nid=nid_sucessor,bip=bip_sucessor)
            self.node.sucessor = sucessor
        if self.node.antecessor.nid == nid_saindo:
            antecessor = Nodo(nid=nid_antecessor, bip=bip_antecessor)
            self.node.antecessor = antecessor
        print "\n---> '%s' respondeu LEAVE para %s!" % (self.node.nid,nid_saindo)
        # envia resposta
        self.message = ["I",self.node.nid,] 
        self.envia_resposta(remetente) # codigo resposta + nid origem

    def recebe_resposta(self,data):  
        """
        recebe resposta dos visinhos que terminaram o balanceameno
        """
        codigo, nid = struct.unpack('!BI',data)
        print "\n'%s' recebeu resposta LEAVE de '%s'" %(self.node.nid,nid)  
        Leave.LEAVES.remove(nid)        
        return len(Leave.LEAVES)==0 
        
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4:
