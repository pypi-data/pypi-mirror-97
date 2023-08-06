"""
    CONTENT DECODERS

    Handle Decoding of Content in to appropriate format from request.

    e.g. 
        list of lists -> dataframe or array. Expect flask server to handle the 
"""
"""This module contains utilities to encode and decode different content types."""
# from __future__ import absolute_import

import csv
import io
import json

import numpy as np
from scipy.sparse import issparse
from six import BytesIO, StringIO

from mldock.platform_helpers.mldock.inference import content_types

def npy_to_numpy(npy_array):
    """Convert an NPY array into numpy.
    Args:
        npy_array (npy array): NPY array to be converted.
    Returns:
        (np.array): Converted numpy array.
    """
    stream = BytesIO(npy_array)
    return np.load(stream, allow_pickle=True)

def json_to_numpy(string_like, dtype=None):
    """Convert a JSON object to a numpy array.
        Args:
            string_like (str): JSON string.
            dtype (dtype, optional):  Data type of the resulting array. If None,
                                      the dtypes will be determined by the
                                      contents of each column, individually.
                                      This argument can only be used to
                                      'upcast' the array.  For downcasting,
                                      use the .astype(t) method.
        Returns:
            (np.array): Numpy array.
        """
    data = json.loads(string_like)
    return np.array(data, dtype=dtype)

def csv_to_numpy(string_like, dtype=None):
    """Convert a CSV object to a numpy array.
    Args:
        string_like (str): CSV string.
        dtype (dtype, optional):  Data type of the resulting array. If None, the
                                  dtypes will be determined by the contents of
                                  each column, individually. This argument can
                                  only be used to 'upcast' the array.  For
                                  downcasting, use the .astype(t) method.
    Returns:
        (np.array): Numpy array.
    """
    try:
        stream = StringIO(string_like)
        reader = csv.reader(stream, delimiter=",", quotechar='"', doublequote=True, strict=True)
        array = np.array([row for row in reader]).squeeze()
        array = array.astype(dtype)
    except ValueError as e:
        if dtype is not None:
            raise Exception(
                "Error while writing numpy array: {}. dtype is: {}".format(e, dtype)
            )
    except Exception as e:
        raise Exception("Error while decoding csv: {}".format(e))
    return array

_decoders_map = {
    content_types.NPY: npy_to_numpy,
    content_types.CSV: csv_to_numpy,
    content_types.JSON: json_to_numpy,
}

def decode(obj, content_type):
    """Decode an object of one of the default content types to a numpy array.
    Args:
        obj (object): Object to be decoded.
        content_type (str): Content type to be used.
    Returns:
        np.array: Decoded object.
    """
    try:
        decoder = _decoders_map[content_type]
        return decoder(obj)
    except KeyError:
        raise TypeError("{} is not supported".format(content_type))
