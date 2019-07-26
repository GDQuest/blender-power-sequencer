import numpy as np


def cross_correlation(mfcc1, mfcc2, nframes):
    n1, mdim1 = mfcc1.shape
    # n2, mdim2 = mfcc2.shape

    n = n1 - nframes + 1

    if n < 0:
        return None

    c = np.zeros(n)
    for k in range(n):
        cc = np.sum(np.multiply(mfcc1[k : k + nframes], mfcc2[:nframes]), axis=0)
        c[k] = np.linalg.norm(cc)
    return c
