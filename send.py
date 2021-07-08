import argparse
import sys
import socket
import random
import struct
from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

def get_if():
	ifs=get_if_list()
	iface=None # "h1-eth0"
	for i in get_if_list():
		if "eth0" in i:
			iface=i
			break;
	if not iface:
		print "Cannot find eth0 interface"
		exit(1)
	return iface
def main():

	if len(sys.argv)<9:
		print 'pass 8 arguments: <destination> "<message>"'
		exit(1)
	
	saddr=sys.argv[1]     
	daddr=sys.argv[2]  #added
	typeeth=sys.argv[3] 
	srci=sys.argv[4] #added
	desti=sys.argv[5] #added
	proto=int(sys.argv[6])#added
	sport=int(sys.argv[7])#added
	dport=int(sys.argv[8]) #added
	iface = get_if()
	#typen=hex(typeeth)
	#print(type(typen))
	#ip=socket.gethostbyname(daddr)
	for i in range(0,20):
		print "sending on interface %s to %s" % (iface, str(daddr))
		pkt=Ether(src=saddr, dst=daddr,type=0x0800)/IP(src=srci,dst=desti,proto=proto)/TCP(dport=dport,sport=sport)
		pkt.show2()
		sendp(pkt, iface=iface, verbose=False)

if __name__ == '__main__':
	main()