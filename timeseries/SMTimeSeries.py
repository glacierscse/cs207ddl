import os, sys
curr_dir = os.getcwd().split('/')
sys.path.append('/'.join(curr_dir[:-1]))
ts_dir = curr_dir[:-1]
ts_dir.append('timeseries')
sys.path.append('/'.join(ts_dir))
from timeseries.FileStorageManager import *
import numbers
import reprlib
#fileSM = FileStorageManager("timeseriesDB")
from timeseries.lazy import LazyOperation


class SMTimeSeries(SizedContainerTimeSeriesInterface):
    '''This is the SMTimeSeries class implemented using Python.
       The SMTimeSeries class can store time series data.
       
       Implements:
       
          SizedContainerTimeSeriesInterface.
       

       Attributes:

          id: the file id.


       Methods:

         from_db: The class function that gets the timeseries from database according to the id.
         __len__: The function to get the length of the SMTimeSeries.
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
         interpolate: for every new time point passed in, compute a value for the SMTimeSeries class.
         __eq__: The function to check whether the new SMTimeSeries object is the same as the current one.
         __add__: The arithmetic operation function to add two SMTimeSeries objects.
         __sub__: The arithmetic operation function to get the difference of two SMTimeSeries objects.
         __mul__: The arithmetic operation function to multiply two SMTimeSeries objects elementwise.
         __pos__: The uniary operation function to have a new SMTimeSeries that have the same time
           domain and value
         __neg__: The uniary operation function negative to have a new SMTimeSeries that have 
           the same time domain and negative of the self.value.
         __abs__: returns the 2-norm of self.value
         __bool__: The function that returns false when the length of self is 0, otherwise true.
         mean: The function that returns the mean of the time series.
         std: The function that returns the standard deviation of the time series data.

      Example:
      -----------------
      >>> data = [1,2,3]
      >>> time = [4,5,6]
      >>> ts = SMTimeSeries(time, data)
      >>> SMTimeSeries.from_db(ts.f_id)
      SMTimeSeries([(4.0, 1.0), (5.0, 2.0), (6.0, 3.0)])
      >>> len(ts)
      3
      >>> ts[2]
      (6.0, 3.0)
      >>> l = iter(ts)
      >>> next(l)
      1.0
      >>> l = ts.itertimes()
      >>> next(l)
      4.0
      >>> l = ts.iteritems()
      >>> next(l)
      (4.0, 1.0)
      >>> ts.values()
      array([ 1.,  2.,  3.])
      >>> ts.times()
      array([ 4.,  5.,  6.])
      >>> ts.items()
      [(4.0, 1.0), (5.0, 2.0), (6.0, 3.0)]
      >>> 5 in ts
      False
      >>> ts.interpolate([4.5])
      SMTimeSeries([(4.5, 1.5)])
      >>> (SMTimeSeries([1, 2, 3], [4, 5, 6]) == SMTimeSeries([1, 2, 3], [4, 5, 6]))
      True
      >>> SMTimeSeries([1, 2, 3], [4, 5, 6]) + SMTimeSeries([1, 2, 3], [6, 5, 4])
      SMTimeSeries([(1.0, 10.0), (2.0, 10.0), (3.0, 10.0)])
      >>> SMTimeSeries([1, 2, 3], [4, 5, 6]) - SMTimeSeries([1, 2, 3], [6, 5, 4])
      SMTimeSeries([(1.0, -2.0), (2.0, 0.0), (3.0, 2.0)])
      >>> SMTimeSeries([1, 2, 3], [4, 5, 6]) * SMTimeSeries([1, 2, 3], [6, 5, 4])
      SMTimeSeries([(1.0, 24.0), (2.0, 25.0), (3.0, 24.0)])
      >>> +ts
      SMTimeSeries([(4.0, 1.0), (5.0, 2.0), (6.0, 3.0)])
      >>> -ts
      SMTimeSeries([(4.0, -1.0), (5.0, -2.0), (6.0, -3.0)])
      >>> abs(ts)
      3.7416573867739413
      >>> bool(ts)
      True
      >>> ts.mean()
      2.0
      >>> ts.std()
      0.81649658092772603
      >>> ts[0] = 0
      >>> ts
      SMTimeSeries([(4.0, 0.0), (5.0, 2.0), (6.0, 3.0)])


    '''
    
    def __init__(self, time, data, fileSM, id = None):
        '''The constructor to initialize a SMTimeSeries object.
           Param: 
             data: the initial sequence-like data to fill the time series. Data can have length 0, but must be given.
             time: the initial time to fill the time series.
             id: the id of the time series. This is an optional argument.
        '''
        # No id is provided, we need to generate an id
        self.f_id = None
        self.fileSM = fileSM
        if id is None:
            while self.fileSM.id_generator in self.fileSM.dictionary:
                self.fileSM.id_generator += 1
            self.f_id = self.fileSM.id_generator
            self.fileSM.dictionary[self.f_id] = 1      
        # id is provided          
        else:
            # if the id is already in the dictionary, raise an exception.
            if id in self.fileSM.dictionary:
                raise Exception('This id has already been used, please choose another one.')
            # if the id is NOT in the dictionary, use this one.
            else:
                self.f_id = id
                self.fileSM.dictionary[self.f_id] = 1 
             
        arrayTS = ArrayTimeSeries(time, data)
        self.fileSM.store(self.f_id, arrayTS)


    @classmethod
    def from_db(cls, id):
        '''The class function that gets the timeseries from database according to the id.
           Param:
              id: the file id to get data from.
           Return:
              SMTimeSeries read from file.
        '''
        #exception throw in fileSM
        arrayTS = self.fileSM.get(id)
        return SMTimeSeries(arrayTS.times(), arrayTS.values())


    def __len__(self):
        '''The function to get the length of the SMTimeSeries.
           Return: 
             length of the timeseries data.
        '''
        return len(self.fileSM.get(self.f_id))

    def __getitem__(self, index):
        '''The function to get a time series item
           Param:
             index: int, the position of the item to get.
           Return:  
             the data at the position specified by index. 
        '''
        cls = type(self)
        if isinstance(index, slice):
            arrayTS = self.fileSM.get(self.f_id)[index]
            return cls(arrayTS.times(), arrayTS.values())
        elif isinstance(index, numbers.Integral):
            return self.fileSM.get(self.f_id)[index]
    
    def __setitem__(self, index, val):
        '''Set the data to the input value at the position specified by index.
           Param:
             index: int, the position to set a new value at.
             val:   the new value.
           Return:
             None.
        '''
        #pass in only the value. We can't change the time -- precondition
        arrayTS = self.fileSM.get(self.f_id)
        arrayTS[index] = val
        self.fileSM.store(self.f_id, arrayTS)


    def __repr__(self):
        '''The function to return formal string representation of the timeseries data.
           Return:
             a string representation of the timeseries data.
        '''
        smTS = self.fileSM.get(self.f_id)
        time_series = list(zip(smTS._key, smTS._value))
        components = reprlib.repr(time_series)
        components = components[components.find('['):]
        class_name = type(self).__name__+'({})'
        return class_name.format(components)


    def __str__(self):
        '''The function to return a string representation of the timeseries data.
           If the data length exceed the length limit, 
           the function will present part of the time series.
           Return:
             a string representation of the SMTimeSeries.
        '''

        return self.fileSM.get(self.f_id).__str__()


    def __iter__(self):
        '''The function that iterates over time series' values.
           Return:
             an iterator of the time series' values.
        '''

        return self.fileSM.get(self.f_id).__iter__()


    def itervalues(self):
        '''The function that iterates over the time series' values.
           Return:
             an iterator of the time series' values.
        '''
        return self.fileSM.get(self.f_id).itervalues()


    def itertimes(self):
        '''The function that iterates over the time series' times.
           Return:
             an iterator of the time series' times.
        '''
        return self.fileSM.get(self.f_id).itertimes()


    def iteritems(self):
        '''The function that iterates over the time series' time-value tuple pairs.
           Return:
             an iterator of the time series' time-value tuple pairs.
        '''
        return self.fileSM.get(self.f_id).iteritems()


    def values(self):
        '''The function to get time series' values.
           Return:
              a numpy array of values.
        '''
        return self.fileSM.get(self.f_id).values()

    def times(self):
        '''The function to get time series' times.
           Return:
             a numpy array of times.
        '''
        return self.fileSM.get(self.f_id).times()

    def items(self):
        '''The function to get a list of time-value tuple pairs.
           Return:
            a list of time series' time-value tuple pairs. 
        '''
        return self.fileSM.get(self.f_id).items()

    def __contains__(self,val):
        '''The function to check whether a value is in the time series.
           Param:
             val: the value to check
           Return:
             boolean, whether the value is in the time series.
        '''

        return val in self.fileSM.get(self.f_id)


    def interpolate(self, inter_time):
        '''for every new time point passed in, compute a value for the SMTimeSeries class.
           if a new time point is smaller than the first existing time point, just use the first value; 
           if a new time point is larger than the last existing time point, use the last value;
           else take the nearest two time points, draw a line between them, and pick the value at the new time point.
           Param:
             inter_time: a sequence-like time points.
           Return:
             a SMTimeSeries object with the input as its time, values as computed by interpolate function. 
        '''
        arrayTS = self.fileSM.get(self.f_id).interpolate(inter_time)
        return SMTimeSeries(arrayTS.times(), arrayTS.values())

    def __eq__(self, other):
        '''The function to check whether the new SMTimeSeries object is the same as the current one.
           Param:
             other: the new SMTimeSeries object to check.
           Return:
             boolean, whether two SMTimeSeries objects are equal.
        '''
        if type(self) != type(other):
            return False
        return self.fileSM.get(self.f_id) == self.fileSM.get(other.f_id)
 

    def __add__(self, rhs):
        '''The arithmetic operation function to add two SMTimeSeries objects elementwise if two 
           objects have the same time domain, otherwise return a value error
           Param:
             rhs: another SMTimeSeries object
           Return:
             The new SMTimeSeries object that has the same time domain as self and the value is 
             the addition of rhs's and self's value.
        '''
        arrayTS = self.fileSM.get(self.f_id) + self.fileSM.get(rhs.f_id)
        return SMTimeSeries(arrayTS.times(), arrayTS.values())

    def __sub__(self,rhs):
        '''The arithmetic operation function to subtract two SMTimeSeries objects elementwise 
           if two objects have the same time domain, otherwise return a value error
           Param:
             rhs: another SMTimeSeries object
           Return:
             The new SMTimeSeries object that has the same time domain as self and the value is 
             self.value-rhs.value.
        '''
        arrayTS = self.fileSM.get(self.f_id) - self.fileSM.get(rhs.f_id)
        return SMTimeSeries(arrayTS.times(), arrayTS.values())
    
    def __mul__(self,rhs):
        '''The arithmetic operation function to multiply two SMTimeSeries objects elementwise 
           if two objects have the same time domain, otherwise return a value error
           Param:
             rhs: another SMTimeSeries object
           Return:
             The new SMTimeSeries object that has the same time domain as self and the value 
             is elementwise self.value*rhs.value.
        '''
        arrayTS = self.fileSM.get(self.f_id) * self.fileSM.get(rhs.f_id)
        return SMTimeSeries(arrayTS.times(), arrayTS.values())
    
    def __pos__(self):
        '''The uniary operation function to have a new SMTimeSeries that have the same time
           domain and value
           Return:
             The new SMTimeSeries object that has the same time and value domain as self
        '''
        arrayTS = self.fileSM.get(self.f_id)
        return SMTimeSeries(arrayTS.times(), arrayTS.values())


    def __neg__(self):
        '''The uniary operation function negative to have a new SMTimeSeries that have 
           the same time domain and negative of the self.value.
           Return:
             The new SMTimeSeries object that has the same time and the negative of
             self.value
        '''
        arrayTS = -self.fileSM.get(self.f_id)
        return SMTimeSeries(arrayTS.times(), arrayTS.values())

    def __abs__(self):
        '''The function that returns the 2-norm of self.value
           Return:
             float, the 2-norm of self.value
        '''
        return abs(self.fileSM.get(self.f_id))
 
    def __bool__(self):
        '''The function that returns false when the length of self is 0, otherwise true.
           Used in: a = SMTimeSeries(...)   
                    if a: 
                        ...
                    else:
                        ...
           Return:
             true, if the length of SMTimeSeries is non-zero
             false, if the length of SMTimeSeries is zero
        '''
        return bool(self.fileSM.get(self.f_id))
  
    def mean(self):
        '''The function that returns the mean of the time series.
           Return:
             the mean of the time series data. 
        '''        
        return self.fileSM.get(self.f_id).mean()

    def std(self):
        '''The function that returns the standard deviation of the time series data.
           Return:
             the standard deviation of the time series data.
        '''
        return self.fileSM.get(self.f_id).std()





