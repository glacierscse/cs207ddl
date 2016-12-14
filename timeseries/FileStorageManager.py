import os, sys
curr_dir = os.getcwd().split('/')
sys.path.append('/'.join(curr_dir[:-1]))
ts_dir = curr_dir[:-1]
ts_dir.append('timeseries')
sys.path.append('/'.join(ts_dir))
from timeseries.StorageManagerInterface import StorageManagerInterface
from timeseries.ArrayTimeSeries import ArrayTimeSeries
from timeseries.SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from timeseries.TimeSeriesInterface import TimeSeriesInterface
import json
import numpy as np
import os



class FileStorageManager(StorageManagerInterface):
	'''
    This is the FileStorageManager class.
    FileStorageManager inherits from the StorageManagerInterface.

	Attributes:

         dictionary: the dict that stores the id of TimeSeries that already been store in the db.
         id_generator: the id_generator that generates id for TimeSeries.
         dir_name: the name of the database.


    Methods:

		 store: The function to store the TimeSeries Object as a file into the database directory.
		 get: The function to get the TimeSeries Object from the database.
		 size: The function to get the length of the TimeSeries Object according to id.
       

    Examples:
    --------
    >>> fsm = FileStorageManager()
	>>> arrayTS = ArrayTimeSeries([0,1,2,3],[4,5,6,7])
	>>> fsm.store(1, arrayTS)
	ArrayTimeSeries([(0, 4), (1, 5), (2, 6), (3, 7)])
	>>> fsm.get(1)
	ArrayTimeSeries([(0.0, 4.0), (1.0, 5.0), (2.0, 6.0), (3.0, 7.0)])
	>>> fsm.size(1)
	4
	

    '''
	def __init__(self, dir_name = "DataStorage"):
		'''The constructor to initialize a FileStorageManager object.
           Param: 
             dir_name: the directory path where all the object file 
                       will be store in.
        '''
		#create a json dict
		abspath = os.path.abspath(os.path.dirname(__file__))
		if not os.path.exists(abspath + '/../timeseriesDB/'):
			os.makedirs(abspath + '/../timeseriesDB/')

		try:
			json_file = open(abspath + '/../timeseriesDB/id.json', 'r')
			self.dictionary = json.load(json_file)
		except:
			self.dictionary = dict()

		self.id_generator = 0
		self.dir_name = abspath+'/../timeseriesDB/'
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)

	def store(self, id, t):
		'''The function to store the TimeSeries Object as a file into the 
		   database directory.
		   Param:
		     id: the id assign to the object when putting into the database.
		     t: the timeSeries object that stores into the database.
           Return: 
             t: the timeSeries object that stores into the database.
        '''
		filename = self.dir_name+"/ts_" + str(id) + ".dat"
		ts = np.array([t.times(), t.values()], dtype = 'f8')
		ts_file_dict = {}
		ts_file_dict[id] = ts.tolist()
		f = open(filename, "w")
		f.write(json.dumps(ts_file_dict))
		f.close()
		#print(os.getcwd())
		f2 = open("id.json","w")
		f2.write(json.dumps(self.dictionary))
		f2.close()
		return t

	def get(self, id):
		'''The function to get the TimeSeries Object from the database.
		   Param:
		     id: the id of the TimeSeries object that taken out from 
		         database.
           Return: 
             The TimeSeries object got from the database.
        '''
		filename = self.dir_name+"/ts_" + str(id) + ".dat"
		try:
			f = open(filename, "r")
		except FileNotFoundError:
			raise Exception("The id is not in the database")
		else:
			array = json.loads(f.read())[str(id)]
			f.close()
			return ArrayTimeSeries(array[0], array[1])
		
	def size(self, id):
		'''The function to get the length of the TimeSeries Object according to id.
		   Param:
		     id: the id of the TimeSeries object that required.
           Return: 
             The length of the TimeSeries object.
        '''
		array = self.get(str(id))
		return len(array)



