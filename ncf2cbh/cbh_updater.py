from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import datetime
from prms_utils import cbh_reader
from prms_utils import ncf_reader

old_cbh_fn = '/work/markstro/operat/docker_test/NHM-PRMS_CONUS/input/prcp.cbh'
new_cbh_fn = '/work/markstro/operat/docker_test/NHM-PRMS_CONUS/input/prcp_new.cbh'

dir = '/work/markstro/operat/docker_test/NHM-PRMS_CONUS/sandbox/'
nc_fn = dir + 'new.nc'

def main():
    cbh_var_name, cbh_nts, cbh_nfeat, cbh_start_date, cbh_end_date, cbh_vals = cbh_reader.read(old_cbh_fn)
    print cbh_var_name, cbh_nts, cbh_nfeat, cbh_start_date, cbh_end_date, cbh_vals

    ncf_var_names, ncf_base_date, ncf_nts, ncf_vals = ncf_reader.read(nc_fn)
    print ncf_var_names, ncf_base_date, ncf_nts, ncf_vals

# TODO this is incomplete because I'm not sure if this is the right approach.

if __name__ == '__main__':
    main()

