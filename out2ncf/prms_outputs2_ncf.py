# Markstrom
# Wed Apr 09 09:43:53 MDT 2019

from prms_utils import csv_reader
import numpy as np
import csv
import json
import datetime
import getpass
from netCDF4 import Dataset

dir = "/work/markstro/operat/docker_test/NHM-PRMS_CONUS"
json_file = dir + "/" + "variable_info.json"


def read_feature_georef(cntl, name):
    fn1 = cntl["feature_georef"][name]["file"]
    print fn1

    nfeat = sum(1 for line in open(fn1))
    vals = np.zeros(shape=(nfeat))
    with open(fn1, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        ii = 0
        for row in spamreader:
            vals[ii] = float(row[0])
            ii = ii + 1
    return vals


def write_variable_block(cntl, ncf, name):
    v1 = ncf.createVariable(name, np.float64, (cntl["feature_georef"][name]["dimid"]),
                            fill_value=float(cntl["feature_georef"][name]["fill_value"]))
    v1.long_name = cntl["feature_georef"][name]["long_name"]
    v1.standard_name = cntl["feature_georef"][name]["standard_name"]
    v1.units = cntl["feature_georef"][name]["units"]
    return v1


def write_timeseries_block(cntl, ncf, name):
    v1 = ncf.createVariable(name, np.float64, ("time", cntl["output_variables"][name]["georef"]["dimid"]),
                            fill_value=float(cntl["output_variables"][name]["fill_value"]))
    v1.long_name = cntl["output_variables"][name]["long_name"]
    v1.standard_name = cntl["output_variables"][name]["standard_name"]
    v1.units = cntl["output_variables"][name]["out_units"]
    return v1


def write_timeseries_values(cntl, ncf, name, vals, nc_var):
    for ii in xrange(0, len(vals)):
        nc_var[ii, :] = vals[ii]


def main():
    with open(json_file, "r") as read_file:
        cntl = json.load(read_file)

# Read the PRMS output
    var_names = cntl["output_variables"].keys()
    val_list = []
    dim_list = set()

    for var_name in var_names:
        print "processing " + var_name
        dim_list.add(cntl["output_variables"][var_name]["georef"]["dimid"])

        csv_fn = cntl["output_variables"][var_name]["prms_out_file"]
        nts, nfeats, base_date, vals = csv_reader.read_output(csv_fn)

        conversion_factor = float(cntl["output_variables"][var_name]["conversion_factor"])
        iis = len(vals)
        jjs = len(vals[0])

        for ii in xrange(0, iis):
            for jj in xrange(1, jjs):
                vals[ii,jj] = vals[ii,jj] * conversion_factor

        val_list.append(vals)

    nhrus = -1
    if 'hruid' in dim_list:
        hru_lat_vals = read_feature_georef(cntl, "hru_lat")
        hru_lon_vals = read_feature_georef(cntl, "hru_lon")
        nhrus = len(hru_lat_vals)


    nsegments = -1
    if 'segid' in dim_list:
        seg_lat_vals = read_feature_georef(cntl, "seg_lat")
        seg_lon_vals = read_feature_georef(cntl, "seg_lon")
        nsegments = len(seg_lat_vals)

# write the ncf file
    print 'writing netcdf file ' + cntl['ncf_file_name']
    ncf = Dataset(cntl['ncf_file_name'], 'w', format='NETCDF4_CLASSIC')

    # Write dimensions block
    if nhrus > 0:
        hru_dim = ncf.createDimension('hruid', nhrus)
    if nsegments > 0:
        nsegments_dim = ncf.createDimension('segid', nsegments)
    time_dim = ncf.createDimension('time', None)

    # Put in the indexes for the dimensions
    time_idx = ncf.createVariable("time", np.int32, ("time"), )
    time_idx.long_name = "time"
    time_idx.standard_name = "time"
    time_idx.cf_role = "timeseries_id"
    time_idx.units = "days since " + base_date + " 00:00" + cntl["tz_code"]

    if nhrus > 0:
        hru_idx = ncf.createVariable("hruid", np.int32, ("hruid"), )
        hru_idx.long_name = "local model hru id"

    if nsegments > 0:
        seg_idx = ncf.createVariable("segid", np.int32, ("segid"), )
        seg_idx.long_name = "local model seg id"

    if nhrus > 0:
        hru_lat = write_variable_block(cntl, ncf, "hru_lat")
        hru_lon = write_variable_block(cntl, ncf, "hru_lon")

    if nsegments > 0:
        seg_lat = write_variable_block(cntl, ncf, "seg_lat")
        seg_lon = write_variable_block(cntl, ncf, "seg_lon")

    ncf_vars = []
    for var_name in var_names:
        ncf_vars.append(write_timeseries_block(cntl, ncf, var_name))

    ncf.conventions = "CF-1.8"
    ncf.featureType = "timeSeries"
    ncf.history = str(datetime.datetime.now()) + ',' + str(getpass.getuser()) + ',prms_outputs2_cdl.py'

    # Write data
    time_idx[:] = np.arange(0, nts, 1)
    if nhrus > 0:
        hru_idx[:] = np.arange(1, nhrus+1, 1)
    if nsegments > 0:
        seg_idx[:] = np.arange(1, nsegments + 1, 1)

    if nhrus > 0:
        hru_lat[:] = hru_lat_vals
        hru_lon[:] = hru_lon_vals

    if nsegments > 0:
        seg_lat[:] = seg_lat_vals
        seg_lon[:] = seg_lon_vals

    ii = 0
    for var_name in var_names:
        write_timeseries_values(cntl, ncf, var_name, val_list[ii], ncf_vars[ii])
        ii = ii + 1

    ncf.close()


if __name__ == '__main__':
    main()
