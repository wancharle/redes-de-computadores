#! -*- coding: utf-8 -*-
import hashlib
from utils import ip2int, int2ip
   
class Nodo:
    def __init__(self, nip=None, nid=None,bip=None):
        self.bip = bip
        if not nip:
            if not bip :
                raise Exception('É preciso informar um IP!')
            else:
                self.setBytesIP(bip)
        else:
            self.ip = nip

        if not nid:
            # gerando chave md5 atráves do ip do nodo 
            # 1º converte para int o md5 gerado
            # 2º converte para string o numero POSITIVO gerado
            # 3º pega os primeiros 4 caracteres do numero gerado em string e converte para inteiro
            # esses passos garantem um identificador numerico posivito
            self.nid = int(str(int(hashlib.md5(self.ip).hexdigest(),16))[:4]) 
            self.ip = nip
        else:
            self.nid = int(nid)
        self.esta_na_rede = False
        self.antecessor = None
        self.sucessor = None

        # flag para lookup recursivo
        self.identificando_estrutura_da_rede = False
        self.nodes_conhecidos = {}

    def criaRede(self):
        self.antecessor = self
        self.sucessor = self
        self.esta_na_rede = True
        print "Rede criada com sucesso:"
        print self.info() 
        # TODO: criar visualizacao de rede.

    def saiDaRede(self):
        self.antecessor = None
        self.sucessor = None
        self.esta_na_rede = False

   
    def getBytesIP(self): 
        """ retorna o ip como inteiro nao-negativo de 4 bytes """
        if  not self.bip:
            bip = ip2int(self.ip)
            self.bip = bip
        return self.bip

    def setBytesIP(self,bip):
        self.bip = bip
        self.ip = int2ip(self.bip)

    def info(self):
            info = " ID = %s\n IP = %s\n" % (self.nid,self.ip)
            if self.antecessor:
                info += " ID ANTECESSOR = %s\n IP ANTECESSOR = %s\n" % (self.antecessor.nid, self.antecessor.ip)
            if self.sucessor:
                info += " ID SUCESSOR  = %s\n IP SUCESSOR = %s\n" % (self.sucessor.nid, self.sucessor.ip)
            return info

    def exibe_rede(self):
        #inicio
        nos = self.nodes_conhecidos.keys()
        nos.sort()
        # primeiro é o sucessor do ultimo
        primeiro = self.nodes_conhecidos[nos[-1]]
        print "\n --- ESTRUTURUA DA REDE ---" 
        s= " %s|%s " % (primeiro.nid,primeiro.ip)
        for n in nos:
            sucessor = self.nodes_conhecidos[n]
            s+= "--> %s|%s " % (sucessor.nid, sucessor.ip)
        print s, "\n"
        self.nodes_conhecidos = {}
    
    def identifica_rede(self):
    
        from messages import Lookup
        if self.esta_na_rede:      
            self.identificando_estrutura_da_rede = True
            lookup = Lookup(self)
            lookup.envia(self, self.sucessor.nid, self.sucessor.ip)
        else:
            print "ERROR: o nó ainda nao pertence a uma rede"

    def recebe_lookup(self,nid_procurado, sucessor):
        if self.identificando_estrutura_da_rede:
            self.nodes_conhecidos[nid_procurado] = sucessor
            if nid_procurado == self.nid:
                # exibe a rede
                self.exibe_rede()
            else:
                from messages import Lookup
                # faz lookup pelo sucessor do sucessor
                lookup = Lookup(self)
                lookup.envia(self, sucessor.nid, sucessor.ip)
        

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4:

