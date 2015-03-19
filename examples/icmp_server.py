from scapy.all import ICMP, IP, Raw, send, sniff


def new_msg(msg):
    data = msg['Raw'].load
    if data.startswith("1337:"):
        print data[5:]

if __name__ == "__main__":
    sniff(lfilter=lambda x: x.haslayer(Raw), filter="icmp and host 127.0.0.1", prn=lambda x: new_msg(x))