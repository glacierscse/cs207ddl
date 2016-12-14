import os
import logging
import numpy as np
from API.app import app, db
from flask import request, abort, jsonify, make_response
from flask import render_template, send_from_directory
#from flask_sqlalchemy import SQLAlchemy, DeclarativeMeta
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


from .models import Metadata #???

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
    "Connect to the custom similarity server. Send and receive a request"
    s = socket(AF_INET, SOCK_STREAM)
    #host = socket.gethostname()
    #s.connect((host, 12341))
    s.connect(('localhost', 12342))
    s2 = serialize(json.dumps(requestDict))
    s.send(s2)
    #print('send')
    #print(s.recv(1024))
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
    if not request.json:
        abort(400)
    log.info('Creating timeseries entries in metadata')

    data = json.loads(request.json)

    ts = Metadata(id=data['id'],
                blarg=np.random.choice([0,1]),
                level=np.random.choice(['A','B','C','D','E','F']),
                mean=np.mean(data['value']),
                std=np.std(data['value']))
    db.session.add(ts)
    db.session.commit()
    return jsonify({request.json})


@app.route('/timeseries/<ts_id>', methods=['GET'])
def get_timeseries_by_id(ts_id):
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


#should take a id=the_id querystring and use that as an id into the database to 
#find the timeseries that are similar, sending back the ids of (say) the top 5.
@app.route('/simquery', methods=['GET'])
def get_simts_by_id():
    if 'id' in request.args:
        ts_id = request.args.get('id')
        #default n is 5
        n = 5
        toSend = {'op':'simquery_id','id':int(ts_id),'n':n}
        print("REQUEST IS", toSend)
        response = connectDBServer(toSend)
        log.info('getting the id of 5 most silimar timeseries from input')
        return jsonify(response)

#take a timeseries as an input in a JSON, carry out the query, 
#and return the appropriate ids as well. This is an unusual use of POST.
@app.route('/simquery', methods=['POST'])
def simquery_post():
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


