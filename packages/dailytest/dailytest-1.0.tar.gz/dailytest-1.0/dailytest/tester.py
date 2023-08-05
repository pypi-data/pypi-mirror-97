import inspect

from dailytest.warpper_class import Decorator
from functools import update_wrapper
import functools
import types

@Decorator()
class Daily(object):

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.is_instance_method = False
        
    def __get__(self, obj, objtype):
        """Support instance methods."""
        self.is_instance_method = True
        return functools.partial(self.__call__, obj)

    def __call__(self,  *args, **kwargs):
        if not self.testing:
            return self.func(*args, **kwargs)
        temp_args = args
        if self.is_instance_method:
            temp_args = args[1:]
        self.validate_params(*temp_args, **kwargs)
        output = self.func(*args, **kwargs)
        # self.validate(*temp_args, **kwargs,funtion_output=output) 
        self.validate(funtion_output=output) 

    
