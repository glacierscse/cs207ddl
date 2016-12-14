import abc
from timeseries.TimeSeriesInterface import TimeSeriesInterface
class StreamTimeSeriesInterface(TimeSeriesInterface):
    '''
    This is the StreamTimeSeriesInterface.
    StreamTimeSeriesInterface inherits from the TimeSeriesInterface.

    Abstract Methods:
       
         __len__: the length of StreamTimeSeriesInterface.
         produce: produce a chunk sized bunch of new elements into the timeseries whenever it is called.
         online_mean: the mean of the StreamTimeSeriesInterface.
         online_std:  the standard devation of the StreamTimeSeriesInterface.
    Examples:
    --------------------------------
    >>> from timeseries.SimulatedTimeSeries import SimulatedTimeSeries
    >>> def default_generator(value):
    ...     for i in value:
    ...         yield i
    >>> list_value = [10.50, 5.33, 10.15, 8.06, 6.75, 1.01, 7.66, 8.55, 9.68, 8.87]
    >>> gen = default_generator(list_value)
    >>> sts = SimulatedTimeSeries(gen)
    >>> mean = sts.online_mean()
    >>> mean.produce(5)
    [10.5, 7.915, 8.66, 8.51, 8.158]
    >>> mean.produce(5)
    [6.966666666666666, 7.065714285714285, 7.25125, 7.521111111111111, 7.656]

    >>> values = [10.68, 10.18, 4.10, 9.05, 11.68, 12.30, 9.80, 4.44, 11.40, 6.41, 9.15]
    >>> gen2 =  default_generator(values)
    >>> sts = SimulatedTimeSeries(gen2)
    >>> std = sts.online_std()    
    >>> std.produce(5)
    [0, 0.3535533905932738, 3.6631680278141765, 3.0131531103922797, 2.9712993790596056]
    >>> std.produce(5)
    [2.9545338041728337, 2.697590635751695, 3.110504954413121, 3.0150612671129, 2.985171500749813]
    '''
    @abc.abstractmethod
    def __len__(self):
        "the length of StreamTimeSeriesInterface."

    @abc.abstractmethod #xinyi added
    def produce(self, chunk=1):
        "produce a chunk sized bunch of new elements into the timeseries whenever it is called"
    #@abc.abstractmethod
    #def __getitem__(self,index):
    #    "get the item from SizedContainerTimeSeriesInterface."

    #@abc.abstractmethod
    #def __setitem__(self,index,val):
    #    "set the item in SizedContainerTimeSeriesInterface."

    #@abc.abstractmethod
    #def online_values(self):
    #    "get values from StreamTimeSeriesInterface."

    #@abc.abstractmethod
    #def online_times(self):
    #    "get times from StreamTimeSeriesInterface."

    #@abc.abstractmethod
    #def online_items(self):
    #    "get time-values tuple pairs from StreamTimeSeriesInterface."

    #@abc.abstractmethod
    #def __contains__(self,val)->bool:
    #    "A test for whether item is in set"
    
    #@abc.abstractmethod
    #def online_interpolate(self,inter_time):
    #    "predict the given time value in StreamTimeSeriesInterface."
    
    @abc.abstractmethod
    def online_mean(self):
        "the mean of the StreamTimeSeriesInterface."                                                 
    @abc.abstractmethod
    def online_std(self): 
        "the standard devation of the StreamTimeSeriesInterface."
