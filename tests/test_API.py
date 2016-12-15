import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json, requests
#from timeseries.StorageManager import FileStorageManager
from json import JSONEncoder
import numpy as np
sys.path.append('../../')
from timeseries.ArrayTimeSeries import ArrayTimeSeries


###-------------------------------TEST GET----------------------------
def test_ts_get():
    """
    Test timeseries GET:
    Sends back a json with metadata from all the time series
    """
    url = 'http://127.0.0.1:5000/timeseries'
    r = requests.get(url)
    print("Status",r.status_code,url)
    assert r.status_code<400



def test_mean_in():
    """
    test MEAN_IN:
    Return the metadata of timeseries with the mean in a given range.
    For example, /timeseries?mean_in=1.5-1.53 type queries should return the 
    meatadata of timeseries with mean in 1.5 and 1.53.
    """
    url = 'http://127.0.0.1:5000/timeseries?mean_in=1.2-1.5'
    req = requests.get(url)
    assert req.status_code<400

def test_level_in():
    """
    test LEVEL_IN:
    Return the metadata of timeseries within a given level range.
    For example, /timeseries?level_in=A,B,C type queries should return the 
    meatadata of timeseries of level A or B or C.
    """
    url = 'http://127.0.0.1:5000/timeseries?level_in=A,B,C'
    req = requests.get(url)
    assert req.status_code<400


def test_level():
    """
    test LEVEL:
    Return the metadata of timeseries of a given level.
    For xample, /timeseries?level_in=A type queries should return the 
    meatadata of timeseries of level A.
    """
    url = 'http://127.0.0.1:5000/timeseries?level=A'
    req = requests.get(url)
    assert req.status_code<400

def test_get_ts_by_id():
    """
    test GET timeseries by id:
    Return the timeseries from SM timeseries database given an id.
    """
    url = 'http://127.0.0.1:5000/timeseries/1'
    req = requests.get(url)
    assert req.status_code<400

def test_simq_get():
    """
    test simquery GET:
    Take a id=the_id querystring and use that as an id into the database 
    to find the timeseries that are similar, sending back the ids of (say) the top 5.
    """
    url = 'http://127.0.0.1:5000/simquery?id=20'
    req = requests.get(url)
    assert req.status_code<400


###------------------------TEST POSTS-------------------------------------

# def test_ts_post():
#     """
#     Test timeseries POST:
#     Adds a new timeseries into the database given a json which has a key
#     for an id and a key for the timeseries, and returns the timeseries.
#     """
#     time = np.arange(0.0, 1.0, 0.01)
#     values = 10*np.random.randn(100)
#     ts = ArrayTimeSeries(time, values)
#     data = {}
#     data['id'] = 1003
#     data['ts'] = [list(ts.times()), list(ts.values())]
#     payload = json.dumps(data, ensure_ascii=False)
#     print("Testing timeseries POST...")
#     url = 'http://127.0.0.1:5000/timeseries'
#     req = requests.post(url, json=payload)
#     print("Status",req.status_code, url)
#     print(req.text[0:50])
#     assert req.status_code<400

# def test_simq_post(self):
#     """
#     Test simquery POST:
#     Take a timeseries as an input in a JSON, carry out the query, 
#     and return the appropriate ids as well. This is an unusual use of POST.
#     """

#     time = np.arange(0.0, 1.0, 0.01)
#     values = 10*np.random.randn(100)
#     ts = ArrayTimeSeries(time, values)
#     data = {}
#     data['ts'] = [list(ts.times()), list(ts.values())]
#     payload = json.dumps(data, ensure_ascii=False)
#     print("Testing timeseries POST...")
#     url = 'http://127.0.0.1:5000/simquery'
#     req = requests.post(url, json=payload)
#     print("Status",req.status_code,url)
#     print(req.text[0:50])
#     assert req.status_code<400
    
