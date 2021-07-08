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
	inf=df['Info'].tolist()
	S,D=[],[]
	for j in range(len(inf)):
		if(inf[j].find("50443")):
			if((inf[j].find("9999  >  50443"))!=1 or (inf[j].find("50443  >  9999"))!=1):
				S.append(s[j])
				D.append(d[j])
			
	S=set(S)
	D=set(D)
	print(len(S))
	print(len(D))
	print(S)

if __name__ == '__main__':
	main()