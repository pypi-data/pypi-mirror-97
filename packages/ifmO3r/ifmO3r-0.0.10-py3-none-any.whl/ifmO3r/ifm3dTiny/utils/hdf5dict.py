# -*- coding: utf-8 -*-
"""
@author: ifm

This is sample code. Use at your own risk.
"""

import h5py
import numpy as np
import os


def loadDictFromHdf5(h5filename):
    with h5py.File(h5filename, 'r') as h5file:
        return loadDictFromGroup(h5file, '/')


def saveDictToHdf5(dic, h5filename):
    with h5py.File(h5filename, 'w') as h5file:
        saveDict2Group(h5file, '/', dic)


def saveDict2Group(h5file, path, dic):
    # argument type checking
    if not isinstance(dic, dict):
        raise ValueError(f"Argument dic must be a dictionary, not {type(dic)}.")
    if not isinstance(path, str):
        raise ValueError(f"Argument path must be a string, not {type(path)}")
    if not isinstance(h5file, h5py._hl.files.File):
        raise ValueError(f"Argument h5file must be an open h5py file, not {type(h5file)}")
    # save items to the hdf5 file
    for key, item in dic.items():
        key = str(key)
        # save
        if isinstance(item,
                      (np.int64, np.int32, np.float64, str, np.float, float, np.float32, int, list, np.ndarray, tuple)):
            h5file[path + key] = item
            if not np.all(h5file[path + key][()] == item):
                raise ValueError('The data representation in the HDF5 file does not match the original one.')
        # save dictionaries
        elif isinstance(item, dict):
            saveDict2Group(h5file, f"{path}{key}/", item)
        # other types cannot be saved and will result in an error
        else:
            raise ValueError('Cannot save %s type.' % type(item))


def loadDictFromGroup(h5file, path):
    ans = {}
    for key, item in h5file[path].items():
        if isinstance(item, h5py._hl.dataset.Dataset):
            ans[key] = item[()]
        elif isinstance(item, h5py._hl.group.Group):
            ans[key] = loadDictFromGroup(h5file, f"{path}{key}/")
    return ans


def loadItemFromHdf5(h5filename, key, path="/"):
    with h5py.File(h5filename, 'r') as h5file:
        item = h5file[path][key]
        if isinstance(item, h5py._hl.dataset.Dataset):
            return item[()]
        elif isinstance(item, h5py._hl.group.Group):
            return loadDictFromGroup(h5file, f"{path}{key}/")


def loadDictsToPandas(path, *args):
    import pandas as pd
    idx = 0
    dum = str(*args)
    for file in os.listdir(path):
        if file.endswith(".hdf5") and dum in file:
            print(os.path.join(path, file))
            data = loadDictFromHdf5(os.path.join(path, file))
            if idx == 0:
                dat = pd.DataFrame.from_dict(data, orient='index', columns=[str(idx)])
            else:
                df2 = pd.DataFrame.from_dict(data, orient='index', columns=[str(idx)])
                dat = pd.concat([dat, df2], axis=1)
            idx += 1
    datuse = dat.T
    return datuse