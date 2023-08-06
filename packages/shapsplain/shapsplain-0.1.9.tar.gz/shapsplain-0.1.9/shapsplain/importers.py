"""Namespace just for importing other namespaces to avoid spamming of
various messages on import.

"""
import os
import sys
import logging
import warnings

logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('matplotlib').setLevel(logging.ERROR)
logging.getLogger('numba').setLevel(logging.WARNING)
warnings.filterwarnings('ignore', message='.*binary incompatibility.*')

from contextlib import contextmanager

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', message='.*binary incompatibility.*')
    import numpy

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', message='.*as a synonym of type.*')
    import tensorflow
    import tensorflow.keras.layers

import sklearn.ensemble
import sklearn.cluster

def import_tensorflow():
    return tensorflow

def import_keras_layers():
    return tensorflow.keras.layers

def import_numpy():
    return numpy

def import_sklearn_ensembles():
    return sklearn.ensemble

def import_sklearn_cluster():
    return sklearn.cluster

@contextmanager
def suppress_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

with suppress_stderr():
    try:
        import keras
    except:
        pass
