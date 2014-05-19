import netifaces

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
