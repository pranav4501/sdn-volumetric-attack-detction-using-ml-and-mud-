from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import SimpleSwitchAPI
import sys,pickle
import os
import glob
import time
import numpy as np


from sklearn.cluster import KMeans
#from scipy.spatial.distance import cdis
from sklearn import preprocessing

class ReadCounters(object):

	def __init__(self, sw_name):

		self.topo = Topology(db="topology.db")
		self.sw_name = sw_name
		self.thrift_port = self.topo.get_thrift_port(sw_name)
		self.controller = SimpleSwitchAPI(self.thrift_port)


	def direct(self):

		entries = self.controller.table_num_entries("data")
		for i in range(int(entries)):
			self.controller.counter_read("port_counter", i)

	def delete(self,table_name, match_keys):
		self.controller.table_delete_match( table_name=table_name, match_keys=match_keys)

	def t_dump(self, table_name):
		self.controller.table_dump(table_name= table_name)

	def t_add(self,table_name, action_name, match_keys, action_params, prio):
		self.controller.table_add(table_name=table_name, action_name=action_name, match_keys=match_keys, action_params=action_params, prio=prio)

	def indirect(self):


		udp123_p_from=0
		udp123_b_from=0
		tcp50443_p_from=0
		tcp50443_b_from=0
		udp123_p_to=0
		udp123_b_to=0
		tcp50443_p_to=0
		tcp50443_b_to=0
		

		for i in range(1,12):
			if i in list(x for x in range(1,11)):
				udp123_p_from+=self.controller.counter_read("port_counter", i).packets
				udp123_b_from+=self.controller.counter_read("port_counter", i).bytes
			else:
				tcp50443_p_from+=self.controller.counter_read("port_counter", i).packets
				tcp50443_b_from+=self.controller.counter_read("port_counter", i).bytes

		for i in range(12,23):
			if i in list(x for x in range(12,22)):
				udp123_p_to+=self.controller.counter_read("port_counter", i).packets
				udp123_b_to+=self.controller.counter_read("port_counter", i).bytes
			else:
				tcp50443_p_to+=self.controller.counter_read("port_counter", i).packets
				tcp50443_b_to+=self.controller.counter_read("port_counter", i).bytes
		ar=[tcp50443_p_from,tcp50443_b_from,tcp50443_p_to,tcp50443_b_to]

		return ar


if __name__ == "__main__":
	"""ReadCounters("s1").t_add('data','forward',['0x0&&&0x0','0x9e8dde802928&&&0x0fff',  '0x0800&&&0x0fff', 
	 '0x22cdec18&&&0x0fff', '0x0&&&0x0','0x6&&&0x0ff', '0xC50B&&&0x0ff', '0x0&&&0x0' ], ['00:00:0a:00:01:01', '1' ,'11'],'11')
	
	ReadCounters("s1").t_add('data','forward',['0x9e8dde802928&&&0x0fff', '0x0&&&0x0', '0x0800&&&0x0fff', '0x0&&&0x0',
	 '0x22cdec18&&&0x0fff', '0x6&&&0x0ff', '0x0&&&0x0', '0xC50B&&&0x0ff' ], ['00:00:0a:00:02:02', '2' ,'22'],'22')
	#ReadCounters("s1").delete('data',['0x0&&&0x0','0x928&&&0x0fff',  '0x0800&&&0x0fff','0xc18&&&0x0fff', '0x0&&&0x0',  '0x6&&&0x0ff', '0xB&&&0x0ff', '0x0&&&0x0' ])

	"""
	
	ReadCounters("s1").t_dump('data')

	loaded_model = pickle.load(open('kmeans_internet.sav', 'rb'))
	loaded_scaler=pickle.load(open('kmeansscaler.sav', 'rb'))
	loaded_model_to = pickle.load(open('kmeans_internet_to.sav', 'rb'))
	loaded_scaler_to=pickle.load(open('kmeansscaler_to.sav', 'rb'))
	print(type(loaded_scaler))
	print(type(loaded_model))
	initial=ReadCounters("s1").indirect()
	z=[0,0,0,0]
	time_out_from=0
	time_out_to=0
	while(True):
		stats=ReadCounters("s1").indirect()
		print(stats)
		time.sleep((2.4))
		#Checking timeout
		if time_out_from!=0:
			time_out_from-=1
			if time_out_from==0:
				ReadCounters("s1").t_add('data','forward',['0x0&&&0x0','0x9e8dde802928&&&0x0fff',  '0x0800&&&0x0fff', 
	 '0x22cdec18&&&0x0fff', '0x0&&&0x0','0x6&&&0x0ff', '0xC50B&&&0x0ff', '0x0&&&0x0' ], ['00:00:0a:00:01:01', '1' ,'11'],'11')

		if time_out_to!=0:
			time_out_to-=1
			if time_out_to==0:
				ReadCounters("s1").t_add('data','forward',['0x9e8dde802928&&&0x0fff', '0x0&&&0x0', '0x0800&&&0x0fff', '0x0&&&0x0',
	 '0x22cdec18&&&0x0fff', '0x6&&&0x0ff', '0x0&&&0x0', '0xC50B&&&0x0ff' ], ['00:00:0a:00:02:02', '2' ,'22'],'22')

		dif=[]
		zip_object = zip(z, stats)
		for stats_i , z_i in zip_object:
			dif.append(z_i-stats_i)
		z=stats
		print(dif)
		if dif!=[0,0,0,0]:
			if time_out_from==0:
				temp=np.array(dif[0:2]).reshape(1,-1)
				x_scaled = loaded_scaler.transform(temp)
				clusters=loaded_model.predict(x_scaled)
				centroids = loaded_model.cluster_centers_
				for j in range(len(clusters)):
					for i, center_elem in enumerate(centroids):
						if clusters[j]==i:
							dis=np.linalg.norm([center_elem]-x_scaled)
				if dis>0.0003190890930806537:
					print('anomaly')
					file1 = open("att.txt","a")
					L=' '.join(map(str, dif[0:2]))+ "anomaly--"
					file1.writelines(L)
					file1.close()
					ReadCounters("s1").delete('data',['0x0&&&0x0','0x928&&&0x0fff',  '0x0800&&&0x0fff','0xc18&&&0x0fff', '0x0&&&0x0',  '0x6&&&0x0ff', '0xB&&&0x0ff', '0x0&&&0x0' ])
					time_out_from=5
					ReadCounters("s1").t_dump('data')

				else:
					print('normal')
					file1 = open("att.txt","a")
					L= ' '.join(map(str, dif[0:2]))+ "normal--"
					file1.writelines(L)
					file1.close()

			if time_out_to==0:
				temp2=np.array(dif[2:4]).reshape(1,-1)
				x_scaled = loaded_scaler_to.transform(temp2)
				clusters=loaded_model_to.predict(x_scaled)
				centroids = loaded_model_to.cluster_centers_

				for j in range(len(clusters)):
					for i, center_elem in enumerate(centroids):
						if clusters[j]==i:
							dis_to=np.linalg.norm([center_elem]-x_scaled)
				if dis_to>0.0010388449093495992:
					print('anomaly')
					file1 = open("att.txt","a")
					L=' '.join(map(str, dif[2:4]))+ "--anomaly" +"\n"
					file1.writelines(L)
					file1.close()
					"""ReadCounters("s1").delete('data',['0x928&&&0x0fff', '0x0&&&0x0', '0x0800&&&0x0fff', '0x0&&&0x0', '0xc18&&&0x0fff', '0x6&&&0x0ff', '0x0&&&0x0', '0xB&&&0x0ff' ])
					time_out_to=5
					ReadCounters("s1").t_dump('data')"""

				else:
					print('normal')
					file1 = open("att.txt","a")
					L= ' '.join(map(str, dif[2:4]))+ "--normal" +"\n"
					file1.writelines(L)
					file1.close()
