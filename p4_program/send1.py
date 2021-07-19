import argparse
import sys
import socket
import random
import struct
from scapy.all import sendp, send, get_if_list, get_if_hwaddr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP
import pandas as pd
import pickle
from scapy.all import *
from scapy.base_classes import Gen, SetGen
import scapy.plist as plist
from scapy.utils import PcapReader
from scapy.data import MTU, ETH_P_ARP
import os
import sys
import threading
import signal
import time
import scapy.layers.inet as inet

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

	iface = get_if()
	df=pd.read_csv('5-6-18tplink.csv')
	s=df['Source'].tolist()
	d=df['Destination'].tolist()
	p=df['Protocol'].tolist()
	l=df['length'].tolist()
	i=0
	t=df['Time'].tolist()

	for i in range(1256,2000):
					if(p[i]=='TCP' or p[i]=='TLSv1'):
						if d[i]=='192.168.1.227':
							ipd='10.0.1.1'
							ips='34.205.236.24'
							smac='00:00:0a:00:02:02'
							dmac='9e:8d:de:80:29:28'
							pkt = Ether(src=smac, dst=dmac)
							pkt = pkt /IP(src=ips,dst=ipd) / TCP(dport=123, sport=50443)
							pkt.show2()
							sendp(pkt, iface=iface, verbose=False)
							ti=t[i]
							k=i
							break
			
	for i in range(k+1 ,2298):
		time.sleep((t[i]-ti)/25)
		ti=t[i]
		if(p[i]=='TCP' or p[i]=='TLSv1'):
			smac='00:00:0a:00:02:02'
			dmac='9e:8d:de:80:29:28'
			if d[i]=='192.168.1.227':
				ipd='10.0.1.1'
				ips='34.205.236.24'
				pkt = Ether(src=smac, dst=dmac)
				pkt = pkt /IP(src=ips,dst=ipd) / TCP(dport=123, sport=50443)
				if len(pkt)<l[i]:
					myString = "z"*(l[i] - len(pkt))
					pkt = pkt/myString
				pkt.show2()
				sendp(pkt, iface=iface, verbose=False)
				print(i,"--------",t[i],"length",l[i])

	
	
if __name__ == '__main__':
	main()




##1256 #2298--TcpSynDevice1W2D

##713 #2455-- 6-6-18-TcpSynReflection