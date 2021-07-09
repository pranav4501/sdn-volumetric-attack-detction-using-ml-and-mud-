import pandas as pd
import sys,pickle
import os
import glob
import time
from sklearn.cluster import KMeans
#from scipy.spatial.distance import cdis
from sklearn import preprocessing
import numpy as np
import pickle,sys



df=pd.read_csv('train_internet_2_only.csv')
df_a=pd.read_csv('attack_internet_2_only.csv')

df=df.drop(columns=['FromLocalIcmpPortAllPacket',
       'FromLocalIcmpPortAllByte', 'FromLocalUdpPort53IP192.168.1.1Packet',
       'FromLocalUdpPort53IP192.168.1.1Byte', 'FromLocalTcpPort9999Packet',
       'FromLocalTcpPort9999Byte', 'FromLocalUdpPort67IP192.168.1.1Packet',
       'FromLocalUdpPort67IP192.168.1.1Byte',
       'FromLocalIcmpPortAllIP192.168.1.1Packet',
       'FromLocalIcmpPortAllIP192.168.1.1Byte', 'FromLocalArpPortAllPacket',
       'FromLocalArpPortAllByte', 'ToLocalUdpPort67IP192.168.1.1Packet',
       'ToLocalUdpPort67IP192.168.1.1Byte',
       'ToLocalUdpPort67IP255.255.255.255/32Packet',
       'ToLocalUdpPort67IP255.255.255.255/32Byte',
       'ToLocalUdpPort53IP192.168.1.1Packet',
       'ToLocalUdpPort53IP192.168.1.1Byte',
       'ToLocalIcmpPortAllIP192.168.1.1Packet',
       'ToLocalIcmpPortAllIP192.168.1.1Byte', 'ToLocalTcpPort9999Packet',
       'ToLocalTcpPort9999Byte', 'ToLocal0x888ePortAllPacket',
       'ToLocal0x888ePortAllByte', 'ToLocalArpPortAllPacket',
       'ToLocalArpPortAllByte', ' NoOfFlows' ,'ToInternetUdpPort123Packet', 'ToInternetUdpPort123Byte',
        'ToInternetTcpPort50443Packet', 'ToInternetTcpPort50443Byte','FromInternetUdpPort123Packet', 'FromInternetUdpPort123Byte' ])

df_a=df_a.drop(columns=['FromLocalIcmpPortAllPacket',
       'FromLocalIcmpPortAllByte', 'FromLocalUdpPort53IP192.168.1.1Packet',
       'FromLocalUdpPort53IP192.168.1.1Byte', 'FromLocalTcpPort9999Packet',
       'FromLocalTcpPort9999Byte', 'FromLocalUdpPort67IP192.168.1.1Packet',
       'FromLocalUdpPort67IP192.168.1.1Byte',
       'FromLocalIcmpPortAllIP192.168.1.1Packet',
       'FromLocalIcmpPortAllIP192.168.1.1Byte', 'FromLocalArpPortAllPacket',
       'FromLocalArpPortAllByte', 'ToLocalUdpPort67IP192.168.1.1Packet',
       'ToLocalUdpPort67IP192.168.1.1Byte',
       'ToLocalUdpPort67IP255.255.255.255/32Packet',
       'ToLocalUdpPort67IP255.255.255.255/32Byte',
       'ToLocalUdpPort53IP192.168.1.1Packet',
       'ToLocalUdpPort53IP192.168.1.1Byte',
       'ToLocalIcmpPortAllIP192.168.1.1Packet',
       'ToLocalIcmpPortAllIP192.168.1.1Byte', 'ToLocalTcpPort9999Packet',
       'ToLocalTcpPort9999Byte', 'ToLocal0x888ePortAllPacket',
       'ToLocal0x888ePortAllByte', 'ToLocalArpPortAllPacket',
       'ToLocalArpPortAllByte', ' NoOfFlows' ,'ToInternetUdpPort123Packet', 'ToInternetUdpPort123Byte',
        'ToInternetTcpPort50443Packet', 'ToInternetTcpPort50443Byte','FromInternetUdpPort123Packet', 'FromInternetUdpPort123Byte' ])

df_a=df_a.drop(columns=['Unnamed: 0', 'Timestamp'])

df=df.drop(columns=['Unnamed: 0', 'Timestamp'])

print(df_a.columns)


x = df.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
b = np.array(x_scaled)

# pca = PCA(n_components=f).fit(b)
pca_2d = b



x = df_a.values #returns a numpy array
x_scaled = min_max_scaler.transform(x)
d = np.array(x_scaled)

pca_c_2d = d



km = KMeans(n_clusters = 4)
clusters=km.fit_predict(pca_2d)
# plotting data set
# plt.scatter(*zip(*pca_2d),c=clusters)

# obtaining the centers of the clusters
centroids = km.cluster_centers_
# points array will be used to reach the index easy
points = np.empty((0,len(pca_2d[0])), float)
# distances will be used to calculate outliers
distances = np.empty((0,len(pca_2d[0])), float)
# getting points and distances
for j in range(len(clusters)):
	for i, center_elem in enumerate(centroids):
		if clusters[j]==i:
			distances = np.append(distances, np.linalg.norm([center_elem]-pca_2d[j]))

np.mean(distances)

percentile = 95
# getting outliers whose distances are greater than some percentile
#outliers = points[np.where(distances > np.percentile(distances, percentile))]

d1=np.percentile(distances, percentile)

print(d1)

clusters=km.predict(pca_c_2d)

# obtaining the centers of the clusters
centroids = km.cluster_centers_
# points array will be used to reach the index easy
points_z = np.empty((0,len(pca_c_2d[0])), float)
# distances will be used to calculate outliers
distances_z = np.empty((0,len(pca_c_2d[0])), float)
# getting points and distances
for j in range(len(clusters)):
	for i, center_elem in enumerate(centroids):
		if clusters[j]==i:
			distances_z = np.append(distances_z, np.linalg.norm([center_elem]-pca_c_2d[j])) 
    		#points_z = np.append(points_z, pca_c_2d[j], axis=0)

np.mean(distances_z)

percentile=99.7

l=[]
for i in range(len(distances_z)):
	
	if distances_z[i] > np.percentile(distances, percentile):
		l.append(i)

d2=np.percentile(distances_z, 1)

print(distances_z)
print(len(clusters))
print(d2)
print(len(l))



filename = 'kmeans_internet.sav'

pickle.dump(km, open(filename, 'wb'))

scaler='kmeansscaler.sav'

pickle.dump(min_max_scaler, open(scaler, 'wb'))

loaded_model = pickle.load(open(filename, 'rb'))

loaded_scaler=pickle.load(open(scaler, 'rb'))

print(type(loaded_scaler))

print(type(loaded_model))
print(np.percentile(distances, 97))