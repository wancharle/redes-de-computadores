#! -*- coding: utf-8 -*-
import netifaces
import struct
import socket

def ip2int( addr):
        """
        Converte uma string de endereço ip em um inteiro comforme o exemplo abaixo:
            >>> ip2int('192.168.1.1')
            3232235777
        """
        return struct.unpack(">I", socket.inet_aton(addr))[0]

def int2ip( addr):
        """
        Converte um inteiro em uma string de de endreco ip comforme o exemplo abaixo:
            >>> int2ip(3232235777)
            '192.168.1.1'
        """
        return socket.inet_ntoa(struct.pack(">I", addr))
 
def pega_todos_os_ips():
    interfaces = netifaces.interfaces()
    enderecos = []
    for i in interfaces:
        if i not in "lo":
            familias = netifaces.ifaddresses(i)
            if familias.has_key(netifaces.AF_INET):
                enderecos.append((i,familias[netifaces.AF_INET][0]['addr']))
            
    return enderecos


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
