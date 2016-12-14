"""Commandline tool for finding the closest timeseries points to a given timeseries
"""
import sys
sys.path.append('../')

import os
import pickle
import heapq

from tsbtreedb import *
from calculateDistance import calcDist, standardize
import click

@click.command()
@click.option('--input', help='name of your input ts file')
@click.option('--n', default=10, help='number of similar points to find, default 10')
@click.option('-n', default=10, help='number of similar points to find, default 10')
@click.option('--show-dist', is_flag=True, help='set this flag to show (and store) corresponding distance from similar points to input point')
@click.option('--clear-dir', is_flag=True, help='set this flag to clear the search result directory')
def search(input, n, show_dist, clear_dir):
	"""search for n closest points to input ts, results are stored as .dat file in search_res/
	"""
	input_ts = pickle.load(open(input, 'rb'))
	
	# load vantage points
	vantage_pts = []
	vantage_ids = pickle.load(open('vantage_pts.dat', 'rb'))
	# calc dist from input_ts to vantage points
	dist = []
	for i in vantage_ids:
		vt = pickle.load(open('ts_data/ts_' + str(i) + '.dat', 'rb'))
		dist.append((calcDist(vt, input_ts), str(i)))
	# sort vantage points by distance
	dist.sort(key=lambda kv: kv[0])

	# print(dist)
	id_set = set()
	similar_ts_pQ = []
	for i in range(n):
		cur_dist = dist[i][0]
		cur_vt_id = dist[i][1]
		cur_db = connect('ts_db_index/ts_' + cur_vt_id + '.db')
		# find ts in current circle
		radius = 2 * cur_dist
		dist_ids = cur_db.get_smaller_than(radius)
		cur_db.close()
		# calc distance from input ts to ts in current circle
		for (ds, Id) in dist_ids:
			if Id not in id_set:
				id_set.add(Id)
				cur_ts = pickle.load(open('ts_data/ts_' + Id + '.dat', 'rb'))
				ds_to_input = calcDist(input_ts, cur_ts)
				heapq.heappush(similar_ts_pQ, (-ds_to_input, Id))
				if len(similar_ts_pQ) > n:
						heapq.heappop(similar_ts_pQ)

	# print and store to file
	if not os.path.exists('search_res/'):
		os.makedirs('search_res/')
	elif clear_dir:
		for f in os.listdir('search_res/'):
			os.remove(os.path.join('search_res/', f))

	if show_dist:
		sim_ts = sorted([(-ds, 'ts_%s.dat'%Id) for (ds, Id) in similar_ts_pQ])
		pickle.dump(sim_ts, open('search_res/sim_%d_ts_wdist.dat'%n, 'wb+'))
		print('Closest (up to) %d time series and their distances to input ts: '%n)
		for (ds, name) in sim_ts:
			print('%s: %.10f'%(name, ds))
	else:
		sim_ts = sorted([(-ds, 'ts_%s.dat'%Id) for (ds, Id) in similar_ts_pQ])
		sim_ts = [name for (ds, name) in sim_ts]
		pickle.dump(sim_ts, open('search_res/sim_%d_ts.dat'%n, 'wb+'))
		print('Closest (up to) %d time series: '%n)
		for name in sim_ts:
			print('%s\n'%name)
if __name__ == '__main__':
	search()
