from timeseries.FileStorageManager import FileStorageManager
from p7_simsearch.genTS import genTS
from p7_simsearch.genVantage import genVantage
from API.genMeta import genMeta
import os

if __name__ == '__main__':
	#For RBDB
	N = 1000
	print("start")
	abspath = os.path.abspath(os.path.dirname(__file__))
	s = FileStorageManager("timeseriesDB")
	#generate RBDB and SMDB
	print("start genTS")
	genTS(s,1000)
	genMeta(s)
	print("start genVan")
	genVantage()
	print("start genMeta")
	#generate metaDB
	
