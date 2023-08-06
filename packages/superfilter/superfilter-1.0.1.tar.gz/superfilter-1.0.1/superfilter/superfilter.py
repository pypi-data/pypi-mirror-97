from argskwargs import argskwargs as awk
from functools import wraps
import onetrick
from typing import Sequence as seq

@onetrick
class superfilter:
    def __init__(self, filterfunction):
        self.filterfunction = filterfunction
    
    # This will decorate the specified function
    def __call__(self, function):
        @wraps(function)
        def call(*args, **kwargs):
            params = self.filterfunction(*args, **kwargs)

            if isinstance(params, awk): #0
                args = params.args
                kwargs = params.kwargs
            elif isinstance(params, dict): #1
                args = list()
                kwargs = params
            elif isinstance(params, seq): #3
                if isinstance(params, str): #2
                    args = [params]
                else:
                    args = params
                
                kwargs = dict()
            else:
                args = [params]
                kwargs = dict()

            return function(*args, **kwargs)
        
        return call