import sys
sys.path.append("../")
import os
import random
import pickle
from timeseries import ArrayTimeSeries
import click
import numpy as np
import json
from API.app.models import Metadata
from API.app import db


def genMeta(sm):
	'''This is the function that generate the metadata DB when the server starts. 
		Param:
			sm: SM FileManager
		Return:
			None
	'''

	# number of ts data in ts_data/
	abspath = os.path.abspath(os.path.dirname(__file__))
	path = abspath + '/../timeseriesDB'
	num_ts = len(os.listdir(path))
	print(num_ts)

	for i in range(num_ts):
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
		db.session.add(t)
	db.session.commit()
