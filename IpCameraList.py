import nmap
import socket

def connect(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((hostname, port))
    sock.close()
    return result == 0


def getNet():
    nm = nmap.PortScanner()
    nm.scan(hosts= str(socket.gethostbyname(socket.gethostname())) + '/24', arguments='-sn')

    ip_list_all, ip_list = [], []

    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            ip_list_all.append(host)

    for a in ip_list_all:
        res = connect(a, 554)
        if res:
            ip_list.append(a)
    return ip_list
