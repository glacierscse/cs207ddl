import abc
class TimeSeriesInterface(abc.ABC):
    '''This is the TimeSeriesInterface.
       The TimeSeriesInterface define a set of common methods that can
       be used both in sized-container based time series as well as 
       the stream based and simulated time seires.

       Abstract Methods:
       
         __repr__: string representation of time series.
         __str__: string representation of time series.
         __iter__: iteration on value.
         itervalues: iteration on value.
         itertimes: iteration on times.
         iteritems: iteration on (time,value) pairs.

    '''

    @abc.abstractmethod
    def __repr__(self)->str:
        "A TimeSeries has repr"

    @abc.abstractmethod
    def __str__(self)->str:
        "A TimeSeries has string"
 
    @abc.abstractmethod
    def __iter__(self):
        "iteration on value. order is not guaranteed"
 
    @abc.abstractmethod
    def itervalues(self):
        "iteration on value. order is not guaranteed"

    @abc.abstractmethod
    def itertimes(self):
        "iteration on times. order is not guaranteed"
 
    @abc.abstractmethod
    def iteritems(self):
        "iteration on (time,value) pairs. order is not guaranteed"

    

