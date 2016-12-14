"""Commandline tool for finding the closest timeseries points to a given timeseries
"""

import sys
sys.path.append('../')

import os
import pickle
import heapq

from tsbtreedb import *
from p7_simsearch.calculateDistance import calcDist, standardize

from p7_simsearch.G_Var import NUM_TS, NUM_VP

from timeseries.FileStorageManager import FileStorageManager

class searchEngine:

	def __init__(self):
		abspath = os.path.abspath(os.path.dirname(__file__))
		self.ts_list = []
		self.vp_list = []
		for id in range(NUM_TS):
			self.ts_list.append(pickle.load(open(abspath + '/../ts_data/ts_%d.dat'%id, 'rb')))
		
		vp_ids = pickle.load(open(abspath + '/../vantage_pts.dat', 'rb'))
		for id in vp_ids:
			self.vp_list.append((self.ts_list[id], id))


	def search_by_ts(self, input_ts, n):
		"""search for n closest points to input ts, results are stored as .dat file in search_res/
		"""
		abspath = os.path.abspath(os.path.dirname(__file__))
		input_ts = standardize(input_ts)
		# calc dist from input_ts to vantage points
		dist = []
		for (vt, id) in self.vp_list:
			dist.append((calcDist(vt, input_ts), str(id)))
		# sort vantage points by distance
		dist.sort(key=lambda kv: kv[0])
	
		# print(dist)
		id_set = set()
		similar_ts_pQ = []
		for i in range(n):
			cur_dist = dist[i][0]
			cur_vt_id = dist[i][1]
			cur_db = connect(abspath + '/../ts_db_index/ts_' + cur_vt_id + '.db')
			# find ts in current circle
			radius = 2 * cur_dist
			dist_ids = cur_db.get_smaller_than(radius)
			cur_db.close()
			# calc distance from input ts to ts in current circle
			for (ds, Id) in dist_ids:
				#print('ds is', ds, 'Id is', Id)
				if Id not in id_set:
					id_set.add(Id)
					cur_ts = pickle.load(open(abspath + '/../ts_data/ts_' + Id + '.dat', 'rb'))
					ds_to_input = calcDist(input_ts, cur_ts)
					heapq.heappush(similar_ts_pQ, (-ds_to_input, Id))
					if len(similar_ts_pQ) > n:
							heapq.heappop(similar_ts_pQ)
		similar_ts = [(-ds, Id) for (ds, Id) in similar_ts_pQ]
		sorted_ts = sorted(similar_ts)
		return_id = [Id for (ds,Id) in sorted_ts]
		return return_id

	def getts_with_id(self, input_id, sm):
		print("input",input_id)
		return sm.get(input_id)

	def search_by_id(self, input_id, n,sm):
		ts = self.getts_with_id(input_id,sm)
		return self.search_by_ts(ts, n)
