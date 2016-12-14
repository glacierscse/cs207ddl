class LazyOperation:
    '''The LazyOperation class to calculate function in a lazy way.

       Attributes:
   
       function: the function that need lazy operation.
       *agrs: the parameters of that function.
       **kwargs: the parameters of that function.

       Methods:

         eval: The function to do the lazy eval on LazyOperation object.

    '''
    def __init__(self, function, *args, **kwargs):
        '''The constructor of LazyOperation.
           Param: 
             function: the function that need lazy operation
             *agrs: the parameters of that function
             **kwargs: the parameters of that function
        '''
        self._function = function
        self._args = args 
        self._kwargs = kwargs

    def eval(self):
        '''The function to do the lazy eval on LazyOperation object
           Return:
            The function result
        '''
        # Recursively eval() lazy args
        new_args = [a.eval() if isinstance(a,LazyOperation) else a for a in self._args]
        new_kwargs = {k:v.eval() if isinstance(v,LazyOperation) else v for k,v in self._kwargs}
        return self._function(*new_args, **new_kwargs)
    
  
