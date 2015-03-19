import sys
import subprocess
from xml.dom import minidom


def nmap_handler(host):
    nmap_params = ['nmap', '-sV', '-n', '--open', host, '-oX', '-']
    process = subprocess.Popen(nmap_params, stdout=subprocess.PIPE)
    result, _ = process.communicate()
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python {} <host>".format(__file__)
    else:
        result = nmap_handler(sys.argv[1])
        xml = minidom.parseString(result)
        ports = xml.lastChild.getElementsByTagName('port')
        hosts = xml.lastChild.getElementsByTagName('hosts')[0]
        host_status = "Up" if int(hosts.attributes['up'].value) else "Down"
        print "[*] Host is {}".format(host_status)
        for port in ports:
            port_id = port.attributes['portid'].value
            protocol = port.attributes['protocol'].value
            print "[*] Open Port: {0:5} {1:5}".format(port_id, protocol)