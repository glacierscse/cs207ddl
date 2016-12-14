import numbers
import numpy as np
import sys
import math
from pytest import raises
from timeseries.SimulatedTimeSeries import SimulatedTimeSeries
from random import normalvariate, random
from itertools import count


list_value = [10.50, 5.33, 10.15, 8.06, 6.75, 1.01, 7.66, 8.55, 9.68, 8.87]
list_tuple = [(1, 10.50), (2, 5.33), (3, 10.15), (4, 8.06), (5, 6.75), (6, 1.01), (7, 7.66), (8, 8.55), (9, 9.68), (10, 8.87)]

def default_mean(value):
    de_mean = []
    for i in range(len(value)):
        de_mean.append(np.mean(value[:i+1]))
    return de_mean

def default_generator(value):
    for i in value:
    	yield i

#gen = default_generator(list_value)
de_mean = default_mean(list_value)
#gen_tuple = default_generator(list_tuple)

#-------SimulatedTimeSeries constructor test cases----------
def test_init():
    gen = default_generator(list_value)
    SimulatedTimeSeries(gen)

#-------SimulatedTimeSeries len test cases------------------
def test_len():
    gen = default_generator(list_value)
    sts = SimulatedTimeSeries(gen)
    assert len(sts) == 10

#-------SimulatedTimeSeries repr test cases-----------------
def test_repr():
    gen = default_generator(list_value)
    sts = SimulatedTimeSeries(gen)
    assert repr(sts) == "this is a generator: <SimulatedTimeSeries>"

#-------SimulatedTimeSeries str test cases-----------------
def test_str():
    gen = default_generator(list_value)
    sts = SimulatedTimeSeries(gen)
    assert str(sts) == "this is a generator: <SimulatedTimeSeries>"

#-------SimulatedTimeSeries iter test cases-----------------
def test_iter_number():
    gen = default_generator(list_value)
    sts = SimulatedTimeSeries(gen)
    i = 0
    for x in iter(sts):
        assert x == list_value[i]
        i+=1

def test_iter_tuple():
    gen_tuple = default_generator(list_tuple)
    sts = SimulatedTimeSeries(gen_tuple)
    i = 0
    for x in iter(sts):
        assert x == list_value[i]
        i+=1

#-------SimulatedTimeSeries itervalues test cases-----------
def test_itervalues_number():
    gen = default_generator(list_value)
    sts = SimulatedTimeSeries(gen)
    i = 0
    for x in sts.itervalues():
        assert x == list_value[i]
        i+=1

def test_itervalues_tuple():
    gen_tuple = default_generator(list_tuple)
    sts = SimulatedTimeSeries(gen_tuple)
    i = 0
    for x in sts.itervalues():
        assert x == list_value[i]
        i+=1    

#-------SimulatedTimeSeries itertimes test cases-----------
def test_itertimes_number():
    gen = default_generator(list_value)
    sts = SimulatedTimeSeries(gen)
    i = 0
    for x in sts.itertimes():
        assert x == i
        i+=1

def test_itertimes_tuple():
    gen_tuple = default_generator(list_tuple)
    sts = SimulatedTimeSeries(gen_tuple)
    i = 0
    for x in sts.itertimes():
        assert x == list_tuple[i][0]
        i+=1

#-------SimulatedTimeSeries iteritems test cases-----------
def test_iteritems_number():
    gen = default_generator(list_value)
    sts = SimulatedTimeSeries(gen)
    i = 0
    for x in sts.iteritems():
        assert x == (i, list_value[i])
        i+=1

def test_iteritems_tuple():
    gen_tuple = default_generator(list_tuple)
    sts = SimulatedTimeSeries(gen_tuple)
    i = 0
    for x in sts.iteritems():
        assert x == list_tuple[i]
        i+=1

#-------online_mean test cases----------
def test_online_mean():
    #values = [10.68, 10.18, 4.10, 9.05, 11.68, 12.30, 9.80, 4.44, 11.40, 6.41, 9.15]
    #gen2 =  default_generator(values)
    gen = default_generator(list_value)
    sts = SimulatedTimeSeries(gen)
    mean = sts.online_mean()
    assert mean.produce(5) == de_mean[:5]   
    assert mean.produce(5) == [6.966666666666666, 7.065714285714285, 7.25125, 7.521111111111111, 7.656]

#def test_produce_mean():

def test_online_std():
    values = [10.68, 10.18, 4.10, 9.05, 11.68, 12.30, 9.80, 4.44, 11.40, 6.41, 9.15]
    gen2 =  default_generator(values)
    sts = SimulatedTimeSeries(gen2)
    std = sts.online_std()
    #print (mean.produce(5))
    assert std.produce(5) == [0, 0.3535533905932738, 3.6631680278141765, 3.0131531103922797, 2.9712993790596056]
    assert std.produce(5) == [2.9545338041728337, 2.697590635751695, 3.110504954413121, 3.0150612671129, 2.985171500749813]
