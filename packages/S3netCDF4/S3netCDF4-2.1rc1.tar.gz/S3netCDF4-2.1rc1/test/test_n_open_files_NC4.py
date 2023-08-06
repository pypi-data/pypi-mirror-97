import netCDF4._netCDF4 as netCDF4
import os
import numpy as np

loc = '/Users/dhk63261/Test/nc4test/'

dim_len_t = 256
dim_len_a = 50
nc = []

for i in range(0,1000):
    filename = 'nc4_test{}.nc'.format(i)
    # create file
    nc.append(netCDF4.Dataset(loc+filename, 'w'))
    # create dims
    nc[-1].createDimension('dim0', dim_len_t)
    nc[-1].createDimension('dim1', dim_len_a)
    nc[-1].createDimension('dim2', dim_len_a)
    nc[-1].createDimension('dim3', dim_len_a)

    nc[-1].createVariable('dim0', 'f4', ('dim0',))
    nc[-1].createVariable('dim1', 'f4', ('dim1',))
    nc[-1].createVariable('dim2', 'f4', ('dim2',))
    nc[-1].createVariable('dim3', 'f4', ('dim3',))

    var = nc[-1].createVariable(
        'var','f8', ('dim0','dim1','dim2','dim3'),
    )

    # for i in range(dim_len_t):
    #     for j in range(dim_len_a):
    #         #var[i,j,:,:] = np.random.random([dim_len_a,dim_len_a])
    #         var[i,j,:,:] = i
    #nc[-1].close()
