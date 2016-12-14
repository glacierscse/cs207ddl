import sys
sys.path.append('../')

import os
import random
import pickle

from p7_simsearch.calculateDistance import calcDist, standardize
from tsbtreedb import *
import click

@click.command()
@click.option('-n', default=20, help='number of vantage points to generate, default 20')
@click.option('--n', default=20, help='number of vantage points to generate, default 20')
def genVantage(n):
	"""generate n vantage points for our ts data
	"""

	# if folder not exists, create one
	# else clear folder
	if not os.path.exists('ts_db_index/'):
		os.makedirs('ts_db_index/')
	else:
		files = os.listdir('ts_db_index/')
		for f in files:
			os.remove(os.path.join('ts_db_index/', f))

	# number of ts data in ts_data/
	num_ts = len(os.listdir('ts_data/')) - 1
	if n > num_ts:
		raise ValueError('number of vantage points cannot exceed the number of ts data')

	# random sample 20 vantage points and store the id
	rand_vantage = random.sample(range(num_ts), n)
	pickle.dump(rand_vantage, open('vantage_pts.dat', 'wb+'))

	for i in rand_vantage:
		ts = pickle.load(open('ts_data/ts_' + str(i) + '.dat', 'rb'))
		db = connect('ts_db_index/ts_' + str(i) + '.db')
		for j in range(num_ts):
				other_ts = pickle.load(open('ts_data/ts_' + str(j) + '.dat', 'rb'))
				dist = calcDist(ts, other_ts)
				# if j < 100:
				# 	print(dist)
				db.set(dist, str(j))
		db.commit()
		db.close()

if __name__ == '__main__':
	genVantage()