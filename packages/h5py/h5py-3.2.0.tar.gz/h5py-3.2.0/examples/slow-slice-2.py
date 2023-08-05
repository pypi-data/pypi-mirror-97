import time

import numpy as np
import h5py

# Create a dataset
#a = np.random.random(size=(100000, 1000))
#h5f = h5py.File('/home/takluyver/tmp_test.h5', 'w')
#h5f.create_dataset('dataset_1', data=a, chunks=(1000, 1000))
#h5f.close()

print("Done writing")

# Read the dataset
h5f = h5py.File('/home/takluyver/tmp_test.h5', 'r', rdcc_nbytes=1024 * 1024 * 1024)

# Read every second row with read_direct()
a = None
start = time.time()
ds = h5f["dataset_1"]
a = np.zeros(ds.shape, dtype=ds.dtype)
ds.read_direct(a, np.s_[::2], np.s_[::2])
print(a[:10, :10])
end = time.time()
print("read_direct", end - start)

# Read using [...][::2]
a = None
start = time.time()
a = h5f["dataset_1"][...][::2]
end = time.time()
print("np slicing", end - start) # Prints "5.501309871673584"

# Read using [::2]
a = None
start = time.time()
a = h5f["dataset_1"][::2]
end = time.time()
print("slicing dataset", end - start) # Prints "64.27390313148499"





h5f.close()
