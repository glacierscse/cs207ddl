import numbers
import reprlib
import numpy as np
import sys
from timeseries.lazy import LazyOperation
import math
from timeseries.SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from timeseries.TimeSeriesInterface import TimeSeriesInterface

class TimeSeries(SizedContainerTimeSeriesInterface):
    '''This is the TimeSeries class implemented using Python.
       The TimeSeries class can store time series data.

       Implements:

         SizedContainerTimeSeriesInterface.


       Attributes:

         key: the time in the time series.
         value: the data in the time series corresponding to time.


       Methods:

         __len__: The function to get the length of the TimeSeries.
         __getitem__: The function to get a time series item.
         __setitem__: Set the data to the input value at the position specified by index.
         __repr__: return formal string representation of the timeseries data.
         __str__: The function to return a string representation of the timeseries data.

         __iter__: The function that iterates over time series' values.
         itervalues: The function that iterates over the time series' values.
         itertimes: The function that iterates over the time series' times.
         iteritems: The function that iterates over the time series' time-value tuple pairs.
         values: The function to get time series' values.
         times: The function to get time series' times.
         items: The function to get a list of time-value tuple pairs.

         __contains__: The function to check whether a value is in the time series.
         interpolate: for every new time point passed in, compute a value for the TimeSeries class.
         _binary_search: The private helper function. For a time point, find the nearest two time points.
         __eq__: The function to check whether the new TimeSeries object is the same as the current one.
         lazy: The function is to change from the lazy decorator on a function to a property of 
           the ArratTimeSeries CLass.

         _check_time: The function is a decorator function for checking two TimeSeries objects have the same
           time domain before doing all the arithmetic operations.
         __add__: The arithmetic operation function to add two TimeSeries objects.
         __sub__: The arithmetic operation function to get the difference of two TimeSeries objects.
         __mul__: The arithmetic operation function to multiply two TimeSeries objects elementwise.
         __pos__: The uniary operation function to have a new TimeSeries that have the same time
           domain and value
         __neg__: The uniary operation function negative to have a new ArrayTimeSeries that have 
           the same time domain and negative of the self.value.
         __abs__: returns the 2-norm of self.value
         __bool__: The function that returns false when the length of self is 0, otherwise true.
         mean: The function that returns the mean of the time series.
         std: The function that returns the standard deviation of the time series data.
       
       Examples:
       --------     
       >>> TimeSeries([1,2,3],[-15,4.5,12])
       TimeSeries([(-15.0, 1), (4.5, 2), (12.0, 3)])
       >>> len(TimeSeries([1,2,3])) 
       3
       >>> TimeSeries([0,1,2,3,4], [5,6,7,8,9])[1:3] 
       TimeSeries([(6, 1), (7, 2)])
       >>> TimeSeries([4,5,6],[1,2,3])[0] = 0
       >>> repr(TimeSeries([4,5,6],[1,2,3]))
       'TimeSeries([(1, 4), (2, 5), (3, 6)])'
       >>> str(TimeSeries([4,5,6],[1,2,3])) 
       '[(1, 4), (2, 5), (3, 6)]'
       >>> TimeSeries([0,1,2,3,4],[5,6,7,8,9]).values()
       array([0, 1, 2, 3, 4])
       >>> TimeSeries([0,1,2,3,4],[5,6,7,8,9]).times()
       array([5, 6, 7, 8, 9])
       >>> TimeSeries([0,1,2,3,4],[5,6,7,8,9]).items()
       [(5, 0), (6, 1), (7, 2), (8, 3), (9, 4)]
       >>> 3 in TimeSeries([0,1,2,3,4],[5,6,7,8,9])
       True
       >>> TimeSeries([1,2,3], [0,5,10]).interpolate([1])
       TimeSeries([(1, 1.2)])
       >>> TimeSeries([4, 5, 6], [1, 2, 3]) == TimeSeries([4, 5, 6], [1, 2, 3])
       True
       >>> TimeSeries([4, 5, 6], [1, 2, 3]) + TimeSeries([6, 5, 4], [1, 2, 3])
       TimeSeries([(1, 10), (2, 10), (3, 10)])
       >>> TimeSeries([4, 5, 6], [1, 2, 3]) - TimeSeries([6, 5, 4], [1, 2, 3])
       TimeSeries([(1, -2), (2, 0), (3, 2)])
       >>> TimeSeries([4, 5, 6], [1, 2, 3]) * TimeSeries([6, 5, 4], [1, 2, 3])
       TimeSeries([(1, 24), (2, 25), (3, 24)])
       >>> +TimeSeries([4, 5, 6], [1, 2, 3]) 
       TimeSeries([(1, 4), (2, 5), (3, 6)])
       >>> -TimeSeries([6, 5, 4], [1, 2, 3])
       TimeSeries([(1, -6), (2, -5), (3, -4)])
       >>> abs(TimeSeries([4,5,6],[1,2,3]))
       8.774964387392123
       >>> bool(TimeSeries([4,5,6],[1,2,3]))
       True
    '''
    def __init__(self, data, time = None):
        '''The constructor to initialize a TimeSeries object.
           Param: 
             data: the initial sequence-like data to fill the time series. Data can have length 0, but must be given.
             time: the initial time to fill the time series. Time is an optional argument.
        '''
        ##the time has to be in order when pass in -- precondtion
        len_data = len(data)
        if time == None:
            self._key = list(range(len_data))
            self._value = data
        else:
            sort_order = np.argsort(np.array(time))
            time = list(np.array(time)[sort_order])
            data = list(np.array(data)[sort_order])
            self._key = time
            self._value = data
        if len(self._value) != len(self._key):
            raise Exception('The length of time input has to be equal to the length of value input')
        #self._time_series = list(zip(self._key, self._value))
  
    def __len__(self):
        '''The function to get the length of the TimeSeries.
           Return: 
             length of the timeseries data.
        '''
        return len(self._value)

    def __getitem__(self,index):
        '''The function to get a time series item
           Param:
             index: int, the position of the item to get.
           Return:  
             the data at the position specified by index. 
        '''
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._value[index],self._key[index])
        elif isinstance(index, numbers.Integral):
            return (self._key[index],self._value[index])
    
    def __setitem__(self, index, val):
        '''Set the data to the input value at the position specified by index.
           Param:
             index: int, the position to set a new value at.
             val:   the new value.
           Return:
             None.
        '''
        #pass in only the value. We can't change the time -- precondition
        self._value[index] = val

    def __repr__(self):
        '''The function to return formal string representation of the timeseries data.
           Return:
             a string representation of the timeseries data.
        '''
        time_series = list(zip(self._key, self._value))
        components = reprlib.repr(time_series)
        components = components[components.find('['):]
        class_name = type(self).__name__+'({})'
        return class_name.format(components)

    def __str__(self):
        '''The function to return a string representation of the timeseries data.
           If the data length exceed the length limit, 
           the function will present part of the time series.
           Return:
             a string representation of the 
        '''
        limit_len = 5
        len_data = len(self._value)
        time_series = list(zip(self._key,self._value))
        if len_data <= limit_len:
            str_part1 = ", ".join(str(item) for item in time_series)
            return "[" + str_part1 + "]" 
            #return str(self._time_series)
        else:
            str_part1 = ", ".join(str(item) for item in time_series[0:limit_len])
            return "[" + str_part1 + " ... " + str(time_series[-1]) + "]" 

    def __iter__(self):
        '''The function that iterates over time series' values.
           Return:
             an iterator of the time series' values.
        '''
        for val in self._value:
            yield val

    def itervalues(self):
        '''The function that iterates over the time series' values.
           Return:
             an iterator of the time series' values.
        '''
        for val in self._value:
            yield val

    def itertimes(self):
        '''The function that iterates over the time series' times.
           Return:
             an iterator of the time series' times.
       '''
        for time in self._key:
            yield time

    def iteritems(self):
        '''The function that iterates over the time series' time-value tuple pairs.
           Return:
             an iterator of the time series' time-value tuple pairs.
        '''
        time_series = zip(self._key, self._value)
        for item in time_series:
            yield item

    def values(self):
        '''The function to get time series' values.
           Return:
              a numpy array of values.
        '''
        return np.array(self._value)

    def times(self):
        '''The function to get time series' times.
           Return:
             a numpy array of times.
        '''
        return np.array(self._key)

    def items(self):
        '''The function to get a list of time-value tuple pairs.
           Return:
            a list of time series' time-value tuple pairs. 
        '''
        return list(zip(self._key, self._value))

    def __contains__(self,val):
        '''The function to check whether a value is in the time series.
           Param:
             val: the value to check
           Return:
             boolean, whether the value is in the time series.
        '''
        return val in self._value


    def interpolate(self, inter_time):
        '''for every new time point passed in, compute a value for the TimeSeries class.
           if a new time point is smaller than the first existing time point, just use the first value; 
           if a new time point is larger than the last existing time point, use the last value;
           else take the nearest two time points, draw a line between them, and pick the value at the new time point.
           Param:
             inter_time: a sequence-like time points.
           Return:
             a TimeSeries object with the input as its time, values as computed by interpolate function. 
        '''
        inter_values = []
        for ti in inter_time:
            if ti < self._key[0]:
                inter_values.append(self._value[0])
            
            elif ti > self._key[-1]:
                inter_values.append(self._value[-1])
            
            else:
                left, right = self._binary_search(self._key, ti)
                if left == right:
                    inter_values.append(self._value[left])
                else:
                    slope = (self._value[right] - self._value[left]) / (self._key[right]- self._key[left])
                    pred_value = (ti- self._key[left])*slope + self._value[left]
                    inter_values.append(pred_value)

        result = TimeSeries(inter_values, inter_time)
        return result

    def _binary_search(self, arr, target):
        '''The private helper function. For a time point, find the nearest two time points.
           If the new coming time point alreay in the time points, return itself as left nearest and right nearest.
           Param:
             arr: the time points that already exist.
             target: the time point to search neighbors for.
           Return: 
             The nearest left and right time points.
        '''
        if len(arr) == 0: 
            return -1 
        lo = 0
        hi = len(arr)-1
        while lo <= hi: 
            mid = lo+(hi-lo)//2
            if target < arr[mid]:
                hi = mid - 1
            elif target > arr[mid]:
                lo = mid + 1
            else: 
                return mid, mid
        return hi, lo


    def __eq__(self, other):
        '''The function to check whether the new TimeSeries object is the same as the current one.
           Param:
             other: the new TimeSeries object to check.
           Return:
             boolean, whether two TimeSeries objects are equal.
        '''
        if type(self) != type(other):
            return False
        if len(self) != len(other):
            return False
        if self._value == other._value and self._key == other._key:
            return True
        else:
            return False

    @property
    def lazy(self):
        '''The function is to change from the lazy decorator on a function 
           to a property of the TimeSeries CLass. 
           Use the property to delay the evaluation of an expression of the TimeSeries until 
           its value is needed.
           Return:
             LaayOperation, which can be used to call an eval() of it in order to calculate.
        '''
        identity = lambda x: x
        return LazyOperation(identity, self)

    def _check_time(function):
        '''The function is a decorator function for checking two TimeSeries objects have the same
           time domain before doing all the arithmetic operations.
           Param:
             function: the function use _check_time on
           Return:
             ValueError if two objects have different time domain.
        '''
        def _check_time_helper(self,rhs):
            if not self._key ==  rhs._key:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
            return function(self,rhs)
        return _check_time_helper
    
    @_check_time
    def __add__(self, rhs):
        '''The arithmetic operation function to add two TimeSeries objects elementwise if two 
           objects have the same time domain, otherwise return a value error
           Param:
             rhs: another TimeSeries object
           Return:
             The new TimeSeries object that has the same time domain as self and the value is 
             the addition of rhs's and self's value.
        '''
        added_value = [self._value[i] + rhs._value[i] for i in range(len(rhs))]
        return TimeSeries(added_value, self._key)

    @_check_time
    def __sub__(self,rhs):
        '''The arithmetic operation function to subtract two TimeSeries objects elementwise 
           if two objects have the same time domain, otherwise return a value error
           Param:
             rhs: another TimeSeries object
           Return:
             The new TimeSeries object that has the same time domain as self and the value is 
             self.value-rhs.value.
        '''
        added_value = [self._value[i] - rhs._value[i] for i in range(len(rhs))]
        return TimeSeries(added_value, self._key)
    
    @_check_time
    def __mul__(self,rhs):
        '''The arithmetic operation function to multiply two TimeSeries objects elementwise 
           if two objects have the same time domain, otherwise return a value error
           Param:
             rhs: another TimeSeries object
           Return:
             The new TimeSeries object that has the same time domain as self and the value 
             is elementwise self.value*rhs.value.
        '''
        added_value = [self._value[i] * rhs._value[i] for i in range(len(rhs))]
        return TimeSeries(added_value, self._key)
    
    def __pos__(self):
        '''The uniary operation function to have a new TimeSeries that have the same time
           domain and value
           Return:
             The new TimeSeries object that has the same time and value domain as self
        '''
        return TimeSeries(self._value, self._key)

    def __neg__(self):
        '''The uniary operation function negative to have a new TimeSeries that have 
           the same time domain and negative of the self.value.
           Return:
             The new TimeSeries object that has the same time and the negative of
             self.value
        '''
        neg_value = [-i for i in self._value]
        return TimeSeries(neg_value, self._key)

    def __abs__(self):
        '''The function that returns the 2-norm of self.value
           Return:
             float, the 2-norm of self.value
        '''
        return math.sqrt(sum([i**2 for i in self._value]))
 
    def __bool__(self):
        '''The function that returns false when the length of self is 0, otherwise true.
           Used in: a = TimeSeries(...)   
                    if a: 
                        ...
                    else:
                        ...
           Return:
             true, if the length of TimeSeries is non-zero
             false, if the length of TimeSeries is zero
        '''
        return bool(len(self))
  
    def mean(self):
        '''The function that returns the mean of the time series.
           Return:
             the mean of the time series data. 
        '''        
        return np.mean(self._value)

    def std(self):
        '''The function that returns the standard deviation of the time series data.
           Return:
             the standard deviation of the time series data.
        '''
        return np.std(self._value)
