from scapy.all import *
import socket
import time
def main():
	#source_IP = socket.gethostbyname(sys.argv[1])
	#target_IP = socket.gethostbyname(sys.argv[2])
	#source_port = int(input("Enter Source Port Number:"))
	i = 1
	for i in range(1, 1000):
		pkt=Ether(src='00:00:0a:00:02:02', dst='9e:8d:de:80:29:28',type=0x0800)/IP(src='34.205.236.24',dst='10.0.1.1',proto=6)/TCP(dport=80,sport=50443)
		myString = "z"*(54 - 40)
		pkt = pkt/myString
		pkt.show2()
		sendp(pkt, verbose=False)
		print ("packet sent ", i)
		time.sleep(0.01-(i*(0.00001)))
if __name__ == '__main__':
	main()
	#IP1 = IP(src = '34.205.236.24', dst = '10.0.2.2')
		   #TCP1 = TCP(sport = 50442, dport = 80)
		   #pkt = IP1 / TCP1