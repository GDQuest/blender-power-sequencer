import numpy as np

def ensure_non_zero(signal):
    """
    Adds a little bit of static to avoid
    'divide by zero encountered in log' during MFCC computation.
    """

    signal += np.random.random(len(signal)) * 10**-10

    return signal
