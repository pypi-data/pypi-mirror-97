from time import time
import sys


class Profiler:
    def __init__(self, enabled=True, out=sys.stdout):
        """Initializes the profiler.
        Args:
        enabled (bool, optional): Indicates if the profiler is active. Defaults to True.
        out ([TextIO], optional): A text stream for writing the logs. Defaults to sys.stdout.
        """
        self.profile = {}
        self.enabled = enabled
        self.out = out

    def start(self, fname):
        """Indicates the starting line of a block of codes for profiling

        Args:
            fname (string): A name represnting this block of code. This name will be used for
            stopping and also reporting this block of code.
        """
        if fname not in self.profile:
            self.profile[fname] = {
                'current': None,
                'total': 0,
                'calls': 0
            }
        self.profile[fname]['current'] = time()
        self.profile[fname]['calls'] += 1

    def finish(self, fname):
        """Indicates the end of the profiled block of code

        Args:
            fname (string): The same name that used in the start method.
        """
        self.profile[fname]['total'] += time() - self.profile[fname]['current']

    def print_profile(self):
        """Prints the summary report of the profiled codes.
        """
        self.out.write("=" * 85 + "\n")
        self.out.write("=" + " " * 35 +
                       "Time Profiles" + " " * 35 + "=\n")
        self.out.write("=" * 85 + "\n")
        self.out.write(
            f"{'Function name':40s} {'# of calls':15s} {'time per call':15s} {'total time':15s}\n")
        self.out.write("-" * 85 + "\n")
        for k in self.profile:
            self.out.write(f"{k:40s} {self.profile[k]['calls']:<15d} ")
            self.out.write(
                f"{self.profile[k]['total']/self.profile[k]['calls']:<15.2f} ")
            self.out.write(f"{self.profile[k]['total']:<15.2f}\n")
        self.out.write("=" * 85 + "\n")


default_profiler = Profiler()


def profile(func, profiler=default_profiler):
    """Wraps specified functions of an object with start and finish.

    Example:
        >>> @profile
        >>> def method(a, b):
        >>>   return a + b
    """
    if not profiler.enabled:
        return func if callable(func) else lambda f: f
        
    name = func.__name__ if callable(func) else func

    def decorator(f):
        def wrap(*args, **kwargs):
            profiler.start(name)
            result = f(*args, **kwargs)
            profiler.finish(name)
            return result
        wrap.__name__ = f.__name__
        return wrap
    # if callable return the wrapper. If name, return the decorator to create a wrapper...
    return decorator(func) if callable(func) else decorator
