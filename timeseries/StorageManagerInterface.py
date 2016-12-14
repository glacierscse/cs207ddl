import abc
from timeseries.SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from timeseries.TimeSeriesInterface import TimeSeriesInterface
class StorageManagerInterface:
    '''This is the StorageManagerInterface.

       Abstract Methods:
       
         store: Store the SizedContainerTimeSeriesInterface object into database.
         size: The size of the SizedContainerTimeSeriesInterface object given id.
         get: Get the SizedContainerTimeSeriesInterface object according to id.

    '''
    
    @abc.abstractmethod
    def store(id:int, t:SizedContainerTimeSeriesInterface)->SizedContainerTimeSeriesInterface:
         "Store the SizedContainerTimeSeriesInterface object into database."

    @abc.abstractmethod
    def size(id:int)->int:
        "The size of the SizedContainerTimeSeriesInterface object given id"

    @abc.abstractmethod
    def get(id:int)->SizedContainerTimeSeriesInterface:
        "Get the SizedContainerTimeSeriesInterface object according to id."
