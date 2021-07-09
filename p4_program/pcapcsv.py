import os
os.system("tshark -r 18-06-05.pcap -T fields -e ip.src -e frame.len -e     ip.proto -E separator=, -E occurrence=f > 5june.csv")