import numbers
import reprlib
import numpy as np
import sys
import math
from timeseries.TimeSeriesInterface import TimeSeriesInterface
from timeseries.StreamTimeSeriesInterface import StreamTimeSeriesInterface
#from TimeSeriesInterface import TimeSeriesInterface
#from StreamTimeSeriesInterface import StreamTimeSeriesInterface
from random import normalvariate, random

class SimulatedTimeSeries(StreamTimeSeriesInterface):
    '''This is the imulatedTimeSeries class implemented using Python.
       The imulatedTimeSeries class can store time series data.

       Implements:

         StreamTimeSeriesInterface.


       Attributes:

         gen: a generator to return an iterator whose element can be number or tuple.
         length: length of the time series.
         mu: the mean by the nth element in generator.
         std: the standard deviation by the nth element in generator.
         n: the number keeping track of at what position the generator is at.
         mu_std: the helper variable for calculating the standard deviation.
         n_std: the nth standard deviation.



       Methods:

         __len__: The function to get the length of the SimulatedTimeSeries.
         __repr__: The function to return formal string representation of SimulatedTimeSeries.
         __str__: The function to return a string representation of SimulatedTimeSeries.
         __iter__: The function that iterates over time series' data.
         produce: The function that produce a list of outcome from SimulatedTimeSeries' generator.
         itervalues: The function that iterates over the time series' data.
         itertimes: The function that iterates over the time series' times.
         iteritems: The function that iterates over the time series' time-value tuple pairs.

         online_mean: The function that convert a generator of mean to a SimulatedTimeSeries of mean.
         _online_mean_helper: The function to return a online mean of SimulatedTimeSeries.
         online_std: The function that convert a generator of standard deviation to a SimulatedTimeSeries of mean.
         _online_std_helper: The function to return a online standard deviation of SimulatedTimeSeries.

    '''
    def __init__(self, gen):
        '''The constructor to initialize a TimeSeries object.
           Param: 
             gen: a generator to return an iterator whose element can be number or tuple.
        '''
        ##the time has to be in order when pass in -- precondtion
        ##if each element in the generator is a tuple, then the first one must be time,
        ##the second one must be data
        self._gen = gen
        self._length = 0
        self._mu = 0
        self._n = 0
        self._mu_std = 0
        self._n_std = 0
  
    def __len__(self):
        '''The function to get the length of the SimulatedTimeSeries.
           Return: 
             length of the timeseries data.
        '''
        l = 0
        for v in self._gen:
            l += 1
        self._length = l
        return self._length

    def __repr__(self):
        '''The function to return formal string representation of SimulatedTimeSeries.
           Return:
             a string indicating this is a generator.
        '''
        return "this is a generator: <SimulatedTimeSeries>"

    def __str__(self):
        '''The function to return a string representation of SimulatedTimeSeries.
           Return:
             a string indicating this is a generator.
        '''
        return "this is a generator: <SimulatedTimeSeries>"

    def __iter__(self):
        '''The function that iterates over time series' data.
           Return:
             an iterator of the time series' data.
        '''
        for i in self._gen:
            if isinstance(i,tuple):
                yield i[1]
            elif isinstance(i, numbers.Integral):
                yield i
    
    def produce(self, chunk=1):
        '''The function that produce a list of outcome from SimulatedTimeSeries' generator.
           Param:
             chunk: the size of the list to return.
           Return:
             a list of outcome from a generator.
        '''         
        result = []
        for i in range(chunk):
            result.append(next(self._gen))
        return result 


    def itervalues(self):
        '''The function that iterates over the time series' data.
           Return:
             an iterator of the time series' data.
        '''
        for i in self._gen:
            if isinstance(i,tuple):
                yield i[1]
            elif isinstance(i, numbers.Integral):
                yield i

    def itertimes(self):
        '''The function that iterates over the time series' times.
           If the input generator's element is time-data tuple, then return the corresponding times;
           if the imput generator's element is data only, then time is the order of generating data.
           Return:
             an iterator of the time series' times.
       '''
        count = 0
        for i in self._gen:
            if isinstance(i,tuple):
                yield i[0]
            elif isinstance(i, numbers.Integral):
                yield count 
            count += 1

    def iteritems(self):
        '''The function that iterates over the time series' time-value tuple pairs.
           If the input generator' element is only data, return the (order, data) pair;
           If the input generator' element is (time, data) pair, return this pair.
           Return:
             an iterator of the time series' (time, data) pairs.
        '''
        count = 0
        for i in self._gen:
            if isinstance(i,tuple):
                yield i
            elif isinstance(i, numbers.Integral):
                yield (count,i) 
            count += 1


    def online_mean(self):
        '''The function that convert a generator of mean to a SimulatedTimeSeries of mean.
           Return:
             a SimulatedTimeSeries object.
        '''
        return SimulatedTimeSeries(self._online_mean_helper())

    def _online_mean_helper(self):
        '''The function to return a online mean of SimulatedTimeSeries.
           Return:
             a generator of online mean. 
        '''
        for value in self._gen:
            self._n += 1
            delta = value - self._mu
            self._mu += delta / self._n
            yield self._mu

    def online_std(self):
        '''The function that convert a generator of standard deviation to a SimulatedTimeSeries of mean.
           Return:
             a SimulatedTimeSeries object.
        '''
        return SimulatedTimeSeries(self._online_std_helper())

    def _online_std_helper(self):
        '''The function to return a online standard deviation of SimulatedTimeSeries.
           Return:
             a generator of online standard deviation. 
        '''
        dev_accum = 0
        for value in self._gen:#_value:# according to the formulae in my remarks 
            self._n_std += 1
            mu_new = (value - self._mu_std) / self._n_std + self._mu_std   #every time comes a new element, calculate a new mu
            dev_accum = dev_accum + (value - self._mu_std) * (value - mu_new) 
            self._mu_std = mu_new     # update new mu
            if self._n_std > 1:
                stddev = math.sqrt(dev_accum/(self._n_std-1))  
            else:
                stddev = 0
            yield stddev
