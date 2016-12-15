import socket
from serialization import *
from error import *
from tsdb_op import *
from concurrent.futures import ThreadPoolExecutor 
import threading
import json
import socketserver
import sys
sys.path.append('../')
from p7_simsearch.search_engine import searchEngine
from timeseries.FileStorageManager import FileStorageManager
from timeseries.SMTimeSeries import SMTimeSeries
import os


#from socketserver import BaseRequestHandler, ThreadingTCPServer#???


LENGTH_FIELD_LENGTH = 4

class TSDB_Server(socketserver.BaseRequestHandler):

	def __init__(self, database1,database2, port = ("localhost", 12342)):
		self.rbdb = database1
		self.smdb = database2
		self.addr = port
		self.deserializer = Deserializer()


	def run(self):
		pool = ThreadPoolExecutor(12)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(self.addr)
		sock.listen(5)
		
		while True:
			print("Connecting...")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
			client_sock, client_addr = sock.accept()
			pool.submit(self.echo_client, client_sock, client_addr)


	def echo_client(self, socket, client_addr):
		print('Got connection from', client_addr) 
		while True:
			msg = socket.recv(8192)
			if not msg:
				break
			result = self.data_received(msg)
			socket.send(result)
			print("Client closed connection")
			socket.close()


	def data_received(self, data):
		print("data received")
		print(data)
		self.deserializer.append(data)
		print("successfully deserialized")
		if self.deserializer.ready():
			msg = self.deserializer.deserialize()
			print(msg)
			status = TSDBStatus.OK  # until proven otherwise.
			response = TSDBOp_Return(status, None)  # until proven otherwise.
			try:
				print("1")
				op = TSDBOp.from_json(msg)
				print(op)
			except TypeError as e:
				status = TSDBStatus.INVALID_OPERATION
				response = TSDBOp_Return(status, None)
			if status is TSDBStatus.OK:
				print("OK")
				if isinstance(op, TSDBOp_Simquery_WithTS):
					response = self._simquery_with_ts(op)
				elif isinstance(op, TSDBOp_Simquery_WithID):
					print("getin")
					response = self._simquery_with_id(op)
				elif isinstance(op, TSDBOp_GetTS_WithID):
					print("TS")
					response = self._getts_with_id(op)
					print("response", response)
				#########
				elif isinstance(op, TSDBOp_InsertTS):
					print("Insertion")
					response = self._insert_ts(op)
					print("response", response)
				########
				else:
					response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, op['op'])
			print(type(response))
			print(response.to_json())
			print(type(response.to_json()))
			print("----")
			print(serialize(json.dumps(response.to_json())))
			return serialize(json.dumps(response.to_json()))
			#socket.send(serialize("Hello"))
			#self.request.send(serialize(json.dumps(response.to_json())))
			# send it out

	def _simquery_with_ts(self, op):
		id_list = self.rbdb.search_by_ts(op['ts'], op['n'])

		result = TSDBOp_Simquery_WithTS('simquery_ts')
		result['id'] = id_list
		return result

	def _simquery_with_id(self, op):
		print("insideID")
		id_list = self.rbdb.search_by_id(op['id'], op['n'],self.smdb)
		result = TSDBOp_Simquery_WithID('simquery_id')
		result['id'] = id_list
		return result

	def _getts_with_id(self, op):
		ts = self.rbdb.getts_with_id(op['id'], self.smdb)
		ts_list = [{"times":list(ts.times())}, {"values":list(ts.values())}]
		print(ts_list)
		print("my result before op")
		result = TSDBOp_GetTS_WithID('get_id')  
		result['id'] = op['id']
		result['ts'] = ts_list
		print("type", type(ts_list))
		print("result",result)
		return result

	def _insert_ts(self, op):
		ts = SMTimeSeries(op['ts'].times(),op['ts'].values(), self.smdb)
		result = TSDBOp_InsertTS('insert_ts')
		result['ts'] = ts
		result['id'] = ts.f_id
		return result

if __name__ == '__main__':

	

	print("abs_path" + str(os.path.abspath('')))
	print("cwd" + str(os.getcwd()))
	s = searchEngine()
	abspath = os.path.abspath(os.path.dirname(__file__))
	f = FileStorageManager(abspath + "/../timeseriesDB")
	tsdb = TSDB_Server(s,f)
	tsdb.run()
	


