__version__ = "0.1.0"

from .signal import Signal

signal = Signal

def true_every(number):
    """ Return True every 'number' of iterations"""
    return (i==(number-1) for _ in iter(int,1) for i in range(number))