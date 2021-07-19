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

class ReadRegisters(object):

	def __init__(self, sw_name):

		self.topo = Topology(db="topology.db")
		self.sw_name = sw_name
		self.thrift_port = self.topo.get_thrift_port(sw_name)
		self.controller = SimpleSwitchAPI(self.thrift_port)



	def delete(self,table_name, match_keys):
		self.controller.table_delete_match( table_name=table_name, match_keys=match_keys)

	def t_dump(self, table_name):
		self.controller.table_dump(table_name= table_name)

	def t_add(self,table_name, action_name, match_keys, action_params, prio):
		self.controller.table_add(table_name=table_name, action_name=action_name, match_keys=match_keys, action_params=action_params, prio=prio)

	def r_read(self, register_name, index=None, show=False):
		self.controller.register_read( register_name=register_name)
	


if __name__ == "__main__":
	r=(ReadRegisters("s1").r_read('ind',0))
	print(r)