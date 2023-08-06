import onetrick

@onetrick
class funcfilter:
    def __init__(self, filterfunction):
        self.filterfunction = filterfunction
    
    def __call__(self, function):
        from functools import wraps

        @wraps(function)
        def call(*args, **kwargs):
            return self.filterfunction(function, *args, **kwargs)
        
        return call