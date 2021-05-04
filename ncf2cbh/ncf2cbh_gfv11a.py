from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
from netCDF4 import num2date
import datetime
import sys
import numpy as np
import csv

def read(nc_fn):
    nc_fid = Dataset(nc_fn, 'r')
    nc_attrs = nc_fid.ncattrs()
    # print 'attrs', nc_attrs

    nc_dims = [dim for dim in nc_fid.dimensions]
    # print 'dims', nc_dims

    # Figure out the variable names with data in the ncf.
    nc_vars = [var for var in nc_fid.variables]
    remove_list = list(nc_dims)
    remove_list.extend(['hru_lat', 'hru_lon', 'seg_lat', 'seg_lon'])
    var_names = [e for e in nc_vars if e not in remove_list]
    # print 'var_names', var_names

    time = nc_fid.variables['time'][:]
    nts = len(time)
    # print(time, nts)

    time_var = nc_fid.variables['time']
    # print(str(time_var))
    dtime = num2date(time_var[:],time_var.units)
    # print("dtime = " + str(dtime[0]))

    base_date_str = str(dtime[0])
#    print('base_date_str ' + base_date_str)
    tok = base_date_str.split(' ')
    ymd = tok[0]
    tok = ymd.split('-')
    base_date = datetime.date(int(tok[0]), int(tok[1]), int(tok[2]))

    # Read the values into a dictionary.
    vals = {}
    for var in var_names:
        f1 = nc_fid.variables[var][:]
        vals[var] = f1

    nc_fid.close()

    return var_names, base_date, nts, vals

# dir is where to write the CBH files
# full path required for nc_fn
def run(dir, nc_fn):
    var_names, base_date, nts, vals = read(nc_fn)

    # read the mapping
    nhm_id = np.zeros(114958, dtype = np.int)
    ii = 0
    nhm_id_file = dir + 'nhm_id'
    with open(nhm_id_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            nhm_id[ii] = int(row[0])
            ii = ii + 1

    # Write CBH files.
    for name in var_names:
        v = vals[name]
        v2 = np.zeros(114958)
        nfeats = len(v[0])
        fn2 = dir + name + "_t.cbh" # _t to separate unfilled from filled cbh file
        current_date = base_date
        print('writing ' + fn2)
        with open(fn2, 'w') as fp:
            fp.write('Written by ncf2cbh.py\n')
            fp.write(name + ' ' + str(nfeats) + '\n')
            fp.write('########################################\n')

            for ii in range(nts):
                fp.write(str(current_date.year) + ' ' + str(current_date.month) + ' '
                         + str(current_date.day) + ' 0 0 0')
                for jj in range(nfeats):
                    if name == 'prcp':
                        v2[jj] = v[ii, nhm_id[jj]-1] / 25.4
                    elif name == 'tmax':
                        v2[jj] = v[ii, nhm_id[jj]-1] * 9 / 5 + 32
                    elif name == 'tmin':
                        v2[jj] = v[ii, nhm_id[jj]-1] * 9 / 5 + 32
                    else:
                        v2[jj] = v[ii, nhm_id[jj]-1]
                for jj in range(nfeats):
                    if name == 'prcp':
                        fp.write(' ' + '{:.2f}'.format(v2[jj]))
                    elif name == 'tmax':
                        fp.write(' ' + '{:.1f}'.format(v2[jj]))
                    elif name == 'tmin':
                        fp.write(' ' + '{:.1f}'.format(v2[jj]))
                    else:
                        fp.write(' ' + '{:.2f}'.format(v2[jj]))

                fp.write('\n')
                current_date += datetime.timedelta(days=1)


def main(dir, nc_fn):
    run(dir, nc_fn)

if __name__ == '__main__':

    print('setting dir = ' + sys.argv[1])
    dir = sys.argv[1]
    enddate = sys.argv[2]
    prefix = sys.argv[3]
    end_date = datetime.datetime.strptime(enddate, "%Y-%m-%d")

    nc_fn = dir + prefix + end_date.strftime('%Y_%m_%d') +'.nc'

    main(dir, nc_fn)
