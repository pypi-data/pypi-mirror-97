"""
Utility functions
"""
# To define wrappers to enhance existing classes
from functools import wraps
from gwosc.datasets import find_datasets
from gwosc.datasets import event_gps, run_segment 
from gwpy.time import to_gps

def _add_property(cls):
    """
    Decorator to add properties to already existing classes.
    Partially based on the work of M. Garod:
    https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
    
    Example
    -------
    To add theproperty `func` to the class Class:
    @_add_property(Class)
    def func(self):
        pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs): 
            return func(self,*args, **kwargs)
        setattr(cls, func.__name__, property(wrapper))
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator


def _add_method(cls):
    """
    Decorator to add methds to already existing classes.
    Partially based on the work of M. Garod:
    https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
    
    Example
    -------
    To add theproperty `func` to the class Class:
    @_add_method(Class)
    def func(self):
        pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs): 
            return func(self,*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator

# def name_changer(obj, kay):
#     if not os.path.exists(outdir):
#         os.makedirs(outdir)
#     else:
#         expand = 0
#         while True:
#             expand += 1
#             new_event = event_id +'_'+ str(expand)
#             if os.path.exists(args.directory.rstrip('/')+'/'+new_event):
#                 continue
#             else:
#                 event_id = new_event
#                 break
#         outdir = args.directory.rstrip('/')+'/'+event_id
#         os.makedirs(outdir)	

def find_run(start, end, host='https://www.gw-openscience.org'):
    """
    Given GPS ``start`` and GPS ``stop``, it returns the run the data belongs to,
    otherwise it rises an error: data not belonging to gwosc
    
    Parameters
    ----------
    start : LIGOTimeGPS, float, str
        GPS start time of required data; any input parseable by to_gps is fine
    end : LIGOTimeGPS, float, str
        GPS end time of required data; any input parseable by to_gps is fine
    host : str, optional
        The URL of the GWOSC host to query, defaults to ``'https://www.gw-openscience.org'``
    
    """
    if type(start) != type(to_gps('now')):
        start = to_gps(start)
    if type(end) != type(to_gps('now')):
        end = to_gps(end)

    # O3a
    start_a = to_gps('2019-04-01')
    end_a = to_gps('2019-10-02')
    # O3b
    start_b = to_gps('2019-10-31')
    end_b = to_gps('2020-03-28')
    
    if (start>=start_a) and (end<=end_a):
        run = 'O3A'
    elif (start>=start_b) and (end<=end_b):
        run = 'O3B'        
    
    else:
        all_runs = find_datasets(type='run',segment=(start.gpsSeconds, end.gpsSeconds),host=host)
        
        if all_runs:
            # Remove this not to mess up with things
            try:
                all_runs.remove('BKGW170608_16KHZ_R1')
            except:
                pass

            run = all_runs[0]
            for r in all_runs:
                if r[:2] in run:
                    pass
                else:
                    raise Exception('Data spanning multiple runs! Try to reduce the gps time interval.') 
            run = run[:2]
        else:
            raise Exception('GPS time interval not corresponding to any known run. Please, double-check ``start`` and ``stop``.')
    return run
    