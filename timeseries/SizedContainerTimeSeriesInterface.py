import abc
from timeseries.TimeSeriesInterface import TimeSeriesInterface
class SizedContainerTimeSeriesInterface(TimeSeriesInterface):
    '''This is the TimeSeriesInterface.
       SizedContainerTimeSeriesInterface inherits from the TimeSeriesInterface.

       Abstract Methods:
       
         __len__: the length of SizedContainerTimeSeriesInterface.
         __getitem__: get the item from SizedContainerTimeSeriesInterface.
         __setitem__: set the item in SizedContainerTimeSeriesInterface.
         values: get values from SizedContainerTimeSeriesInterface.
         times: get times from SizeContainerTimeSeriesInterface.
         items: get time-values tuple pairs from SizedContainerTimeSeriesInterface.
         __contains__: A test for whether item is in set.
         interpolate: predict the given time value in SizedContainerTimeSeriesInterface.
         __eq__: compare two objects, check if they are equal.
         __add__: add two TimeSeriesInterface.
         __sub__: subtract two TimeSeriesInterface.
         __mul__: multiply two TimeSeriesInterface.
         __pos__: positive value of TimeSeriesInterface.
         __neg__: negative value of TimeSeriesInterface.
         __abs__: 2-norm of TimeSeriesInterface.
         __bool__: bool type of TimeSeries.
         mean: the mean of the SizedContainerTimeSeriesInterface.
         std: the standard devation of the SizedContainerTimeSeriesInterface.

    '''

    @abc.abstractmethod
    def __len__(self):
        "the length of SizedContainerTimeSeriesInterface."

    @abc.abstractmethod
    def __getitem__(self,index):
        "get the item from SizedContainerTimeSeriesInterface."

    @abc.abstractmethod
    def __setitem__(self,index,val):
        "set the item in SizedContainerTimeSeriesInterface."

    @abc.abstractmethod
    def values(self):
        "get values from SizedContainerTimeSeriesInterface."
 
    @abc.abstractmethod
    def times(self):
        "get times from SizeContainerTimeSeriesInterface."

    @abc.abstractmethod
    def items(self):
        "get time-values tuple pairs from SizedContainerTimeSeriesInterface."

    @abc.abstractmethod
    def __contains__(self,val)->bool:
        "A test for whether item is in set"
    
    @abc.abstractmethod
    def interpolate(self,inter_time):
        "predict the given time value in SizedContainerTimeSeriesInterface."

    @abc.abstractmethod
    def __eq__(self,other)->bool:
        "compare two objects, check if they are equal"


    @abc.abstractmethod
    def __add__(self,other:"TimeSeriesInterface"):
        "add two TimeSeriesInterface"

    @abc.abstractmethod
    def __sub__(self,other:"TimeSeriesInterface"):
        "subtract two TimeSeriesInterface"

    @abc.abstractmethod
    def __mul__(self,other:"TimeSeriesInterface"):
        "multiply two TimeSeriesInterface"

    @abc.abstractmethod
    def __pos__(self):
        "positive value of TimeSeriesInterface."

    @abc.abstractmethod
    def __neg__(self):
        "negative value of TimeSeriesInterface"

    @abc.abstractmethod
    def __abs__(self):
        "2-norm of TimeSeriesInterface"

    @abc.abstractmethod
    def __bool__(self):
        "bool type of TimeSeries"
        
    @abc.abstractmethod
    def mean(self):
        "the mean of the SizedContainerTimeSeriesInterface."

    @abc.abstractmethod
    def std(self):
        "the standard devation of the SizedContainerTimeSeriesInterface."


