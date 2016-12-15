import os
import logging
import numpy as np
from API.app import app, db
from flask import request, abort, jsonify, make_response
from flask import render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy, DeclarativeMeta
from json import JSONEncoder

log = logging.getLogger(__name__)

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from sqlalchemy import and_

from socket import socket, AF_INET, SOCK_STREAM
import pickle
from sockets.serialization import *


from .models import Metadata 

class ProductJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return obj.to_dict()
        return super(ProductJSONEncoder, self).default(obj)


app.json_encoder = ProductJSONEncoder

# user = 'postgres'
# password = 'cs207mima'
# host = 'localhost'
# port = '5432'
# dbname = 'timeseries'
# url = 'postgresql://{}:{}@{}:{}/{}'
# # Posgres url
# # postgres_url = url.format(user, password, host, port, dbname)

def connectDBServer(requestDict):
    """"This is the function that connect to the database server 
    Param:
        requestDict: the query that sent from server to client
    Return:
        response: the rsponse sent back from the server to the clients
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 12342))
    s2 = serialize(json.dumps(requestDict))
    s.send(s2)
    msg = s.recv(8192)
    print(msg)
    ds = Deserializer()
    ds.append(msg)
    ds.ready()
    response = ds.deserialize()
    print(response)
    return response

@app.route('/')
@app.route('/index')
def index():
    log.info('Getting Home html')
    return send_from_directory('static', os.path.join('html', 'home.html'))

@app.route('/timeseries', methods=['GET'])
def get_metadata_range():
    """This is the function that send back a json with metadata from all the time series.
    /timeseries?mean_in=1.5-1.53 type queries should now be supported and send back 
    only metadata. For continuous variables you only need to support range queries with 
    string mean_in=1.5-1.53 whereas for discrete variables(level here) you need to support 
    equals and in level_in=A,B,C or level=A. For simpilicity we wont support equals or 
    less-than/greater-than type queries on continuous variables. Finally we'll support only 
    one query at a time (so no combined SELECTs on the database). This will enable you to develop 
    either in DBAPI2 or SQLAlchemy (your choice, although I think that using Flask-SQLAlchemy is a 
    bit easier).
    """
    if 'mean_in' in request.args:
        mean_in = request.args.get('mean_in')
        mean_range = mean_in.split('-')
        m_min = float(mean_range[0])
        m_max = float(mean_range[1])
        query = Metadata.query.filter(and_(Metadata.mean>=m_min, Metadata.mean<=m_max)).all()
        log.info('Get timeseries whose mean is in the range')
        return jsonify(dict(metadata=query))

    if 'level_in' in request.args:
        level_in = request.args.get('level_in')
        level_range = level_in.split(',')
        query = Metadata.query.filter(Metadata.level.in_(level_in)).all()
        log.info('Get timeseries whose level is in the range')
        return jsonify(dict(metadata=query))

    if 'level' in request.args:
        level = request.args.get('level')
        query = Metadata.query.filter_by(level=level).all()
        log.info('Get timeseries whose level is queried')
        return jsonify(dict(metadata=query))

    log.info('Getting all metadata')
    return jsonify(dict(metadata=Metadata.query.all())) #tasks???


@app.route('/timeseries', methods=['POST'])
def create_ts():
    """adds a new timeseries into the database given a json which has a key 
    for an id and a key for the timeseries, and returns the timeseries.
    """
    if not request.json:
        abort(400)
    log.info('Getting data from user')

    data = json.loads(request.json)
    if data['id']<=999 and data['id']>=0:
        print("timeseries already in the file.")
        log.info('showing the timeseries on the screen.')
    else:
        print("timeseries not in database.")
        log.info('adding time series to the meta database.')
        ts = Metadata(id=data['id'],
                          blarg=np.random.choice([0,1]),
                          level=np.random.choice(['A','B','C','D','E','F']),
                          mean=np.mean(data['ts'][1]),
                          std=np.std(data['ts'][1]))
        db.session.add(ts)
        db.session.commit()
        toSend = {'op':'insert_ts','id':data['id'], 'ts': data['ts']}
        print("REQUEST IS", toSend)
        response = connectDBServer(toSend)
        print("-----------received------------")
        print(jsonify(response))
        log.info('adding time series to the meta SMDB.')
        return jsonify(response)


@app.route('/timeseries/<ts_id>', methods=['GET'])
def get_timeseries_by_id(ts_id):
    """this function should send back metadata and the timeseries itself in a JSON payload
    """
    #send back metdata
    query = Metadata.query.filter_by(id=ts_id).all()
    if query is None:
        log.info('Failed to get timeseries with ID=%s', ts_id)
        abort(404)

    #send back timeseries in a JSON payload
    toSend = {'op':'get_id','id':ts_id}
    print("REQUEST IS", toSend)
    response = connectDBServer(toSend)
    log.info('Getting timeseries from input id')
    return jsonify(response)



@app.route('/simquery', methods=['GET'])
def get_simts_by_id():
    '''this function should take a id=the_id querystring and use that as an id into the database 
    to find the timeseries that are similar, sending back the ids of (say) the top 5.
    '''
    if 'id' in request.args:
        ts_id = request.args.get('id')
        #default n is 5
        n = 5
        toSend = {'op':'simquery_id','id':int(ts_id),'n':n}
        print("REQUEST IS", toSend)
        response = connectDBServer(toSend)
        log.info('getting the id of 5 most silimar timeseries from input')
        return jsonify(response)


@app.route('/simquery', methods=['POST'])
def simquery_post():
    '''this function shoulf take a timeseries as an input in a JSON, carry out the 
    query, and return the appropriate ids as well. This is an unusual use of POST.
    '''
    if not request.json or 'ts' not in request.json:
        abort(400)

    data = json.loads(request.json)
    #data = request.get_json(force=True)
    print(data)
    n = 5
    toSend = {'op':'simquery_ts','ts':data['ts'],'n':n}
    print("REQUEST IS", toSend)
    response = connectDBServer(toSend)
    log.info('getting the id of 5 most silimar timeseries from input')
    return jsonify(response)

db.create_all()


