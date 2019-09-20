from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import datetime
from prms_utils import ncf_reader
import sys


def main(dir, nc_fn):
    var_names, base_date, nts, vals = ncf_reader.read(nc_fn)

    # Write CBH files.
    for name in var_names:
        v = vals[name]
        nfeats = len(v[0])
        fn2 = dir + name + ".cbh"
        current_date = base_date
        print("base_date", str(base_date))
        print('writing ' + fn2)
        with open(fn2, 'w') as fp:
            fp.write('Written by yeti_ncf_2_cbh.py\n')
            fp.write(name + ' ' + str(nfeats) + '\n')
            fp.write('########################################\n')

            for ii in range(nts):
                fp.write(str(current_date.year) + ' ' + str(current_date.month) + ' '
                         + str(current_date.day) + ' 0 0 0')
                for jj in range(nfeats):
                    # if name == 'prcp':
                    #     v[ii, jj] = v[ii, jj] / 25.4
                    # elif name == 'tmax':
                    #     v[ii, jj] = v[ii, jj] * 9 / 5 + 32
                    # elif name == 'tmin':
                    #     v[ii, jj] = v[ii, jj] * 9 / 5 + 32
                    # else:
                    #     "don't know how to convert units"
                    fp.write(' ' + str(v[ii,jj]))
                fp.write('\n')
                current_date += datetime.timedelta(days=1)


if __name__ == '__main__':
    dir = '/work/markstro/operat/setup/test/cbh_update/gridMet/'
    nc_fn = dir + '2019_climate_2019_09_13.nc'

    argc = len(sys.argv) - 1
    # print(argc)

    if argc == 1:
        print('setting dir = ' + sys.argv[1])
        dir = sys.argv[1]

    main(dir, nc_fn)
