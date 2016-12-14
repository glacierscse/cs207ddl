import numpy as np
import math
from pytest import raises
from timeseries.TimeSeries import TimeSeries

#import unittest

#class TestTimeSeries(unittest.TestCase):
#smoke test
def smoke_test():
    threes = TimeSeries(range(0,1000,3))
    fives = TimeSeries(range(0,1000,5))

    s = 0
    for i in range(0,1000):
        if i in threes or i in fives:
            s += i

    print("sum",s)

#-------constructor test cases----------
#test no input argument 
def test_init_no_argument():
    with raises(TypeError):
        TimeSeries()
        #time_series_test = TimeSeries()

#test one input argument 
def test_init_argument():
    data = [1,2,3]
    TimeSeries(data)

#test multiple arguments
def test_two_arguments():
    data = [1,2,3]
    time = [-15,4.5,12] #increasing values?
    TimeSeries(data,time)

#test the length of the input argument is zero
def test_init_zero_length_argument():
    data = []
    TimeSeries(data)

#test different length arguments
def test_init_diff_length_argument():
    data = []
    time = [1,2,3]
    with raises(Exception):
        TimeSeries(data,time)

#-------len test cases----------
def test_length():
    data = [1,2,3]
    ts = TimeSeries(data)
    assert len(ts) == 3

def test_zero_length():
    data = []
    ts = TimeSeries(data)
    assert len(ts) == 0

#-------getitem test cases----------
def test_getitem_range():
    #input_range = [1,3]#range(1,4,2)
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    assert ts[1:3] == TimeSeries([1,2],[6,7])

def test_getitem_index():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    assert ts[2] == (7,2)

#-------setitem test cases----------
# norm case
def test_setitem():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = TimeSeries(data, time)
    index = 0
    val = 0
    ts[index] = val
    assert ts == TimeSeries([0, 5, 6],[1, 2, 3])

# index out of range
def test_setitem_index_error():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = TimeSeries(data, time)
    index = 5
    val = 0
    with raises(IndexError):
        ts[index] = val

#--------repr test cases---------
# length less or equal than five 
def test_repr_less_than_five():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = TimeSeries(data, time)
    assert repr(ts) == 'TimeSeries([(1, 4), (2, 5), (3, 6)])'

# length greater than five
def test_repr_greater_than_five():
    data = [4, 5, 6, 7, 8, 9]
    time = [1, 2, 3, 4, 5, 6]
    ts = TimeSeries(data, time)
    assert repr(ts) == 'TimeSeries([(1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9)])'

#test unsorted time argument
def test_unsorted_time():
    data = [4,6,5]
    time = [1,3,2]
    ts = TimeSeries(data, time)
    assert repr(ts) == 'TimeSeries([(1, 4), (2, 5), (3, 6)])'

#--------str test cases-----------
# length less or equal than five 
def test_str_less_than_five():
    data = [4, 5, 6]
    time = [1, 2, 3]
    ts = TimeSeries(data, time)
    assert str(ts) == '[(1, 4), (2, 5), (3, 6)]'

# length greater than five
def test_str_greater_than_five():
    data = [4, 5, 6, 7, 8, 9]
    time = [1, 2, 3, 4, 5, 6]
    ts = TimeSeries(data, time)
    assert str(ts) == '[(1, 4), (2, 5), (3, 6), (4, 7), (5, 8) ... (6, 9)]'

#-------iter test cases----------
def test_iter():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    l = iter(ts)
    next(l)
    assert next(l) == 1

#-------itervalues test cases----------
def test_itervalues():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    l = ts.itervalues()
    next(l)
    assert next(l) == 1

#-------itertimes test cases----------
def test_itertimes():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    l = ts.itertimes()
    next(l)
    assert next(l) == 6

#-------iteritems test cases----------
def test_iteritems():
    data = [0,1,2,3,4]
    time = [5,6,7,8,9]
    ts = TimeSeries(data, time)
    l = ts.iteritems()
    next(l)
    assert next(l) == (6,1)

#-------values test cases----------
def test_values():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    assert all(ts.values() == np.array(data))

#-------times test cases----------
def test_times():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    assert all(ts.times() == np.array(time))

#-------items test cases----------
def test_items():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    assert ts.items() == [(5,0),(6,1),(7,2),(8,3),(9,4)]

#-------contains test cases----------
def test_contains_no_value():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    assert not 5 in ts

def test_contains_no_value():
    data = [0,1,2,3,4]#range(0,5)
    time = [5,6,7,8,9]#range(5,10)
    ts = TimeSeries(data, time)
    assert 3 in ts

#-------contains test cases----------
def test_interpolate1():
    ts = TimeSeries([1,2,3], [0,5,10])
    # Simple cases
    assert ts.interpolate([1]) == TimeSeries([1.2],[1])

def test_interpolate2():
    ts = TimeSeries([1,2,3], [0,5,10])
    # Simple cases
    assert ts.interpolate([-100,100]) == TimeSeries([1,3],[-100,100])

#def test_interpolate3():???
#    ts1 = TimeSeries([0,5,10], [1,2,3])
#    ts2 = TimeSeries([100, -100], [2.5,7.5])
    # Simple cases
#    assert ts1.interpolate(ts2.itertimes()).lazy.eval() == TimeSeries([1.5, 2.5],[2.5,7.5])
    #a.interpolate(b.itertimes()) == TimeSeries([2.5,7.5], [1.5, 2.5])

#-------lazy test cases----------
def test_lazy():
    ts = TimeSeries([1,2,3], [0,5,10])
    # Simple cases
    assert ts.interpolate([-100,100]).lazy.eval() == TimeSeries([1,3],[-100,100])

#--------eq test cases--------
# correct cases
def test_eq_correct():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5, 6], [1, 2, 3])
    assert (ts1 == ts2) == True

# different types
def test_eq_diff_type():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = 3
    assert (ts1 == ts2) ==  False

# different length
def test_eq_diff_len():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5], [1, 2])
    assert (ts1 == ts2) == False

# different value
def test_eq_diff_value():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5, 7], [1, 2, 3])
    assert (ts1 == ts2) == False

# different key
def test_eq_diff_time():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5, 6], [1, 2, 4])
    assert (ts1 == ts2) == False
 
#-------add test cases----------------------------------
# test different length
def test_add_diff_len():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5, 6, 7], [1, 2, 3, 4])
    with raises(ValueError):
        ts1 + ts2

#test different time domain
def test_add_diff_time():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([4, 5, 6], [1, 2, 4])
    with raises(ValueError):
        ts1 + ts2

#correct case
def test_add_correct():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([6, 5, 4], [1, 2, 3])
    assert (ts1 + ts2 == TimeSeries([10, 10, 10], [1, 2, 3]))

#-------sub test cases---------------------------------
def test_sub_correct():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([6, 5, 4], [1, 2, 3])
    assert (ts1 - ts2 == TimeSeries([-2, 0, 2], [1, 2, 3]))

#--------mul test cases---------------------------------
def test_mul_correct():
    ts1 = TimeSeries([4, 5, 6], [1, 2, 3])
    ts2 = TimeSeries([6, 5, 4], [1, 2, 3])
    assert (ts1 * ts2 == TimeSeries([24, 25, 24], [1, 2, 3]))

#-------pos test cases----------
def test_pos():
    ts = TimeSeries([4,5,6],[1,2,3])
    assert +ts == TimeSeries([4,5,6],[1,2,3])

#-------neg test cases----------
def test_neg():
    ts = TimeSeries([4,5,6],[1,2,3])
    assert -ts == TimeSeries([-4,-5,-6],[1,2,3])

#-------abs test cases----------
def test_abs():
    ts = TimeSeries([4,5,6],[1,2,3])
    assert abs(ts) == math.sqrt(77)

#-------bool test cases----------
def test_bool_true():
    ts = TimeSeries([4,5,6],[1,2,3])
    assert bool(ts) 

def test_bool_false():
    ts = TimeSeries([])
    assert not bool(ts) 

def test_bool_zero():
    ts = TimeSeries([0,0,0],[1,2,3])
    assert bool(ts) 
    #your constructor, which should take one mandatory argument which represents 
    #data to fill the time series instance with. 
    #This argument should be any object that can be treated like a sequence. 
    #The argument can be zero-length, but it can't be omitted.	

#if __name__ == '__main__':
#    unittest.main()
