from pytest import raises
import sys, os
sys.path.append("../")
from sockets.Server import TSDB_Server
from sockets.tsdb_op import *
from sockets.serialization import *
from p7_simsearch.search_engine import searchEngine
from timeseries.FileStorageManager import FileStorageManager

import random
import json
from p7_simsearch.calculateDistance import *
from socket import socket, AF_INET, SOCK_STREAM
from pytest import raises



s = searchEngine()
abspath = os.path.abspath(os.path.dirname(__file__))
f = FileStorageManager(abspath + "/../timeseriesDB")
f1 = FileStorageManager()
tsdb = TSDB_Server(s,f)
tsdb1 = TSDB_Server(s,f1)
n = 1000
m_a, m_b = -100, 100
s_a, s_b = 0.1, 10
j_a, j_b = 1, 50
m = [random.uniform(m_a, m_b) for i in range(n)]
s = [random.uniform(s_a, s_b) for i in range(n)]
j = [random.randint(j_a, j_b) for i in range(n)]
arrayTS = tsmaker(m[0], s[0], j[0])

#-------insert timeseries test cases-----------------
# def test_insert_ts():
# 	op = {'ts':arrayTS,'id':1000,'op':'insert_ts'}
# 	result = tsdb._insert_ts(op)
# 	assert type(result['id']) == int


#-------serializing and deserializing test cases-----------------
def test_serializing():
	msg = {'op':'simquery_id','id':2}
	serialized = serialize(json.dumps(msg))
	assert isinstance(serialized, bytes)
	ds = Deserializer()
	ds.append(serialized)
	ds.ready()
	response = ds.deserialize() 
	assert response == msg   

#-------serializing and deserializing exception test cases-----------------
def test_serializing_exception():
	msg = {'op':'simquery_id','id':2}
	assert None == serialize(msg)


#-------similarity search using ID test cases-----------------
def test_simquery_with_id():
	d2 = {'op':'simquery_id','id':2,'n':5}
	response = tsdb._simquery_with_id(d2)
	j_son = serialize(json.dumps(response.to_json()))
	assert type(j_son) == bytes
	assert len(response['id']) == 5 #returned back two ids
	assert type(response['id'][0]) == type(response['id'][1]) == str


#-------similarity search using ts test cases-----------------
def test_simquery_with_ts():
	d3 = {'op':'simquery_ts','ts':arrayTS,'n':5}
	response = tsdb._simquery_with_ts(d3)
	assert len(response['id']) == 5 #returned back two ids
	assert type(response['id'][0]) == type(response['id'][1]) == str 

#-------get ts using id test cases-----------------
def test_getts_with_id():
	d4 = {'op':'get_id','id':5}
	response = tsdb._getts_with_id(d4)
	print(response)
	assert 5 == response['id']
	assert len(response['ts'][1]['values']) == 100

#-------run test-----------------
def test_to_json():
	test_str = {'op':'get_id','id':5}
	tsdb = TSDBOp('add')
	j_son = serialize(json.dumps(tsdb.to_json(test_str)))
	assert type(j_son) == bytes
	



