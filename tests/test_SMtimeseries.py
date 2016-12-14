#import numbers
import numpy as np
import math
#from pytest import raises
#from ArrayTimeSeries import ArrayTimeSeries
#from timeseries.ArrayTimeSeries import ArrayTimeSeries
import os, sys
curr_dir = os.getcwd().split('/')
sys.path.append('/'.join(curr_dir[:-1]))
ts_dir = curr_dir[:-1]
ts_dir.append('timeseries')
sys.path.append('/'.join(ts_dir))
from timeseries.SMTimeSeries import SMTimeSeries
from timeseries.ArrayTimeSeries import ArrayTimeSeries
from pytest import raises
#from timeseries.FileStorageManager import *

#-------ArrayTimeSeries constructor test cases----------
# test init when id is provided
def test_id_provided():
    data = [1, 2, 3]
    time = [4, 5, 6]
    id = 1000
    SMTimeSeries(time, data, id)


# test init when id is already in the dictionary
def test_id_already_taken():
    data = [1, 2, 3]
    time = [4, 5, 6]
    id = 1000
    with raises(Exception):
        SMTimeSeries(time, data, id)

# test no id provided
def test_id_not_provided():
    data = [1, 2, 3]
    time = [4, 5, 6]
    SMTimeSeries(time, data)


#test no input argument
def test_init_no_argument():
    with raises(TypeError):
        SMTimeSeries()

#test one input argument
def test_init_argument():
    data = [1, 2, 3]
    with raises(TypeError):
        SMTimeSeries(data)

#test multiple arguments
def test_two_arguments():
    data = [1, 2, 3]
    time = [4, 5, 6]
    SMTimeSeries(time, data)

#test the length of the input argument is zero
def test_init_zero_length_argument():
    data = []
    time = []
    SMTimeSeries(time, data)

#test different length arguments
def test_init_diff_length_argument():
    data = []
    time = [1,2,3]
    with raises(Exception):
        SMTimeSeries(time, data)


#——————from_db cases------------
def test_from_db():
    data = [1,2,3]
    time = [4,5,6]
    ts = SMTimeSeries(time, data)
    assert SMTimeSeries.from_db(ts.f_id) == ts


#-------len test cases----------
def test_length():
    data = [1,2,3]
    time = [4,5,6]
    ts = SMTimeSeries(time,data)
    assert len(ts) == 3

def test_zero_length():
    data = []
    time = []
    ts = SMTimeSeries(time,data)
    assert len(ts) == 0

#-------getitem test cases----------
def test_getitem_range():
    #input_range = [1,3]#range(1,4,2)
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time,data)
    smts = SMTimeSeries([6,7],[1,2])
    assert ts[1:3] == smts

def test_getitem_index():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time,data)
    assert all(ts[2] == np.array((7,2)))

#-------setitem test cases----------
# norm case
def test_setitem():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = SMTimeSeries(time,data)
    index = 0
    val = 0
    ts[index] = val
    print(ts)
    assert ts == SMTimeSeries([1,2,3],[0, 5, 6])

# index out of range
def test_setitem_index_error():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = SMTimeSeries(time,data)
    index = 5
    val = 0

    with raises(IndexError):
        ts[index] = val

#--------repr test cases---------
# length less or equal than five 
def test_repr_less_than_five():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = SMTimeSeries(time, data)
    assert repr(ts) == 'SMTimeSeries([(1.0, 4.0), (2.0, 5.0), (3.0, 6.0)])'

# length greater than five
def test_repr_greater_than_five():
    data = [4, 5, 6, 7, 8, 9]
    time = [1, 2, 3, 4, 5, 6]
    ts = SMTimeSeries(time, data)
    assert repr(ts) == 'SMTimeSeries([(1.0, 4.0), (2.0, 5.0), (3.0, 6.0), (4.0, 7.0), (5.0, 8.0), (6.0, 9.0)])'

#test unsorted time argument
def test_unsorted_time():
    data = [4,6,5]
    time = [1,3,2]
    ts = SMTimeSeries(time, data)
    assert repr(ts) == 'SMTimeSeries([(1.0, 4.0), (2.0, 5.0), (3.0, 6.0)])'

#--------str test cases-----------
# length less or equal than five 
def test_str_less_than_five():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = SMTimeSeries(time, data)
    assert str(ts) == '[(1.0, 4.0), (2.0, 5.0), (3.0, 6.0)]'

# length greater than five
def test_str_greater_than_five():
    data = [4, 5, 6, 7, 8, 9]
    time = [1, 2, 3, 4, 5, 6]
    ts = SMTimeSeries(time, data)
    assert str(ts) == '[(1.0, 4.0), (2.0, 5.0), (3.0, 6.0), (4.0, 7.0), (5.0, 8.0) ... (6.0, 9.0)]'

#-------iter test cases----------
def test_iter():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time, data)
    l = iter(ts)
    next(l)
    assert next(l) == 1

#-------itervalues test cases----------
def test_itervalues():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time, data)
    l = ts.itervalues()
    next(l)
    assert next(l) == 1

#-------itertimes test cases----------
def test_itertimes():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time, data)
    l = ts.itertimes()
    next(l)
    assert next(l) == 6.0

#-------iteritems test cases----------
def test_iteritems():
    data = [0,1,2,3,4]
    time = [5,6,7,8,9]
    ts = SMTimeSeries(time, data)
    l = ts.iteritems()
    next(l)
    assert next(l) == (6.0,1.0)

#-------values test cases----------
def test_values():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time, data)
    assert all(ts.values() == np.array(data))

#-------times test cases----------
def test_times():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time, data)
    assert all(ts.times() == np.array(time))

#-------items test cases----------
def test_items():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time, data)
    assert ts.items() == [(5.0,0.0),(6.0,1.0),(7.0,2.0),(8.0,3.0),(9.0,4.0)]

#-------contains test cases----------
def test_contains_no_value():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time, data)
    assert not 5 in ts

def test_contains_no_value():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = SMTimeSeries(time, data)
    assert 3 in ts


#-------interpolate test cases----------
def test_interpolate1():
    ts = SMTimeSeries([0,5,10], [1,2,3])
    # Simple cases
    assert ts.interpolate([1.0]) == SMTimeSeries([1.0], [1.2])

def test_interpolate2():
    ts = SMTimeSeries([0,5,10], [1,2,3])
    # Simple cases
    assert ts.interpolate([-100.0,100.0]) == SMTimeSeries([-100,100], [1.0,3.0])
#def test_interpolate3():???
#    ts1 = TimeSeries([0,5,10], [1,2,3])
#    ts2 = TimeSeries([100, -100], [2.5,7.5])
    # Simple cases
#    assert ts1.interpolate(ts2.itertimes()).lazy.eval() == TimeSeries([1.5, 2.5],[2.5,7.5])
    #a.interpolate(b.itertimes()) == TimeSeries([2.5,7.5], [1.5, 2.5])

#--------eq test cases--------
# correct cases
def test_eq_correct():
    #ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    #ts2 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    #assert (ts1 == ts2) == True
    assert (SMTimeSeries([1, 2, 3], [4, 5, 6]) == SMTimeSeries([1, 2, 3], [4, 5, 6])) == True

# different types
def test_eq_diff_type():
    ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    ts2 = 3
    assert (ts1 == ts2) ==  False

# different length
def test_eq_diff_len():
    ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    ts2 = SMTimeSeries([1, 2],[4, 5])
    assert (ts1 == ts2) == False

# different value
def test_eq_diff_value():
    ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    ts2 = SMTimeSeries([1, 2, 3], [4, 5, 7])
    assert (ts1 == ts2) == False
# different key
def test_eq_diff_time():
    ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    ts2 = SMTimeSeries([1, 2, 4], [4, 5, 6])
    assert (ts1 == ts2) == False


#-------add test cases----------------------------------
# test different length
def test_add_diff_len():
    ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    ts2 = SMTimeSeries([1, 2, 3, 4], [4, 5, 6, 7])
    with raises(ValueError):
        ts1 + ts2

#test different time domain
def test_add_diff_time():
    ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    ts2 = SMTimeSeries([1, 2, 4], [4, 5, 6])
    with raises(ValueError):
        ts1 + ts2

#correct case
def test_add_correct():
    ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    ts2 = SMTimeSeries([1, 2, 3], [6, 5, 4])
    assert (ts1 + ts2 == SMTimeSeries([1,2,3], [10, 10, 10]))

#-------sub test cases---------------------------------
def test_sub_correct():
    ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    ts2 = SMTimeSeries([1, 2, 3], [6, 5, 4])
    assert (ts1 - ts2 == SMTimeSeries([1, 2, 3], [-2, 0, 2]))

#--------mul test cases---------------------------------
def test_mul_correct():
    ts1 = SMTimeSeries([1, 2, 3], [4, 5, 6])
    ts2 = SMTimeSeries([1, 2, 3], [6, 5, 4])
    assert (ts1 * ts2 == SMTimeSeries([1, 2, 3], [24, 25, 24]))

#-------pos test cases----------
def test_pos():
    ts = SMTimeSeries([1, 2, 3], [4,5,6])
    assert +ts == SMTimeSeries([1, 2, 3], [4,5,6])
#-------neg test cases----------
def test_neg():
    ts = SMTimeSeries([1,2,3], [4,5,6])
    assert -ts == SMTimeSeries([1,2,3], [-4,-5,-6])

#-------abs test cases----------
def test_abs():
    ts = SMTimeSeries([1,2,3], [4,5,6])
    assert abs(ts) == math.sqrt(77)

#-------bool test cases----------
def test_bool_true():
    ts = SMTimeSeries([1,2,3], [4,5,6])
    assert bool(ts)

def test_bool_false():
    ts = SMTimeSeries([],[])
    assert not bool(ts)

def test_bool_zero():
    ts = SMTimeSeries([1,2,3], [0,0,0])
    assert bool(ts)

#-------mean test case--------------
def test_mean():
    ts = SMTimeSeries([1,2,3], [3,4,5])
    assert ts.mean() == 4


#-------std test case----------------

def test_std():
    ts = SMTimeSeries([1,2,3], [3,4,5])
    assert ts.std() == np.std([3,4,5])

