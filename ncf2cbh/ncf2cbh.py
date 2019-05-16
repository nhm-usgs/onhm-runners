from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import datetime
from prms_utils import ncf_reader

dir = '/work/markstro/operat/docker_test/NHM-PRMS_CONUS/sandbox/'
nc_fn = dir + 'new.nc'

if __name__ == '__main__':
    var_names, base_date, nts, vals = ncf_reader.read(nc_fn)

    # Write CBH files.
    for name in var_names:
        v = vals[name]
        nfeats = len(v[0])
        fn2 = dir + name + ".cbh"
        current_date = base_date
        with open(fn2, 'w') as fp:
            fp.write('Written by ncf2cbh.py\n')
            fp.write(name + ' ' + str(nfeats) + '\n')
            fp.write('########################################\n')

            for ii in range(nts):
                fp.write(str(current_date.year) + ' ' + str(current_date.month) + ' '
                         + str(current_date.day) + ' 0 0 0')
                for jj in range(nfeats):
                    if name == 'prcp':
                        v[ii, jj] = v[ii, jj] / 25.4
                    elif name == 'tmax':
                        v[ii, jj] = v[ii, jj] * 9 / 5 + 32
                    elif name == 'tmin':
                        v[ii, jj] = v[ii, jj] * 9 / 5 + 32
                    else:
                        "don't know how to convert units"
                    fp.write(' ' + str(v[ii,jj]))
                fp.write('\n')
                current_date += datetime.timedelta(days=1)
