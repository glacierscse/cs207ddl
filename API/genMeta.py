import sys
sys.path.append("../")
import os
import random
import pickle
from timeseries import ArrayTimeSeries
#from calculateDistance import calcDist, standardize
#from tsbtreedb import *
import click
import numpy as np
import json
#from .models import Metadata #???
from API.app.models import Metadata
from API.app import db

def genMeta(sm):
	# number of ts data in ts_data/
	abspath = os.path.abspath(os.path.dirname(__file__))
	path = abspath + '/../timeseriesDB'
	num_ts = len(os.listdir(path))
	print(num_ts)

	for i in range(num_ts):
		#ts = pickle.load(open(path + '/ts_' + str(i) + '.dat', 'rb'))
		ts = sm.get(i)
		tsid = i
		mean = ts.mean()
		std = ts.std()
		blarg = np.random.uniform(0,1,1)[0]
		levels = ['A', 'B', 'C', 'D', 'E', 'F']
		level = levels[np.random.randint(0,5,1)[0]]
		meta = [tsid,mean,std,blarg,level]
		print (meta)

		t = Metadata(id=tsid,
					blarg=blarg,
					level=level,
					mean=mean,
					std=std)
		# row = Metadata(meta)
		db.session.add(t)
	db.session.commit()

#if __name__ == '__main__':
#	genMeta()