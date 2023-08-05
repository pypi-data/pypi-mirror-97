from subprocess import check_call
from tempfile import NamedTemporaryFile
from threading import Thread
from time import sleep

import faulthandler
faulthandler.enable()

import h5py
import numpy as np

# build a dummy array w/ vlen strs
N = 1000
strs = np.array([ f'row {i}' for i in range(N) ])
ints = np.array([ i**2 for i in range(N) ])
arr = np.rec.fromarrays(
    [ strs, ints ],
    dtype={
        'names': [ 'strs', 'ints' ],
        'formats': [ h5py.special_dtype(vlen=str), '<i4' ],
    },
)

with NamedTemporaryFile(delete=False) as tmp:
    # write it to an HDF5 file
    path = tmp.name
    print("path=", path)
    key = 'df'
    with h5py.File(path, 'w') as f:
        f[key] = arr

    # peek at some records
    with h5py.File(path,'r') as f:
        dataset = f[key]
        print(dataset[:10])

    # thread worker fn: read a range from the HDF5 file
    def read_ranges(path, key, ranges):
        f = h5py.File(path,'r')
        if True:
            dataset = f[key]
            for r in ranges:
                print(r)
                print(dataset[r].shape)

    attempt = 1
    while True:
        print(f'Attempt {attempt}:')
        thread1 = Thread(target=read_ranges, args=(path, key, [slice(i,i+100) for i in range(  0,1000,200)]))
        thread2 = Thread(target=read_ranges, args=(path, key, [slice(i,i+100) for i in range(100,1000,200)]))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        attempt += 1
        print('')
        sleep(1)
