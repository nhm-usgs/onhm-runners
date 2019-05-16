# Markstrom
# Wed Apr 09 09:43:53 MDT 2019

from prms_utils import csv_reader
import numpy as np
import csv
import json
import datetime
import getpass

dir = "/work/markstro/operat/docker_test/NHM-PRMS_CONUS"
json_file = dir + "/" + "variable_info.json"


def read_feature_georef(cntl, name):
    fn1 = cntl["feature_georef"][name]["file"]
    print(fn1)

    nfeat = sum(1 for line in open(fn1))
    vals = np.zeros(shape=(nfeat))
    with open(fn1, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        ii = 0
        for row in spamreader:
            vals[ii] = float(row[0])
            ii = ii + 1
    return vals


def write_variable_block(cntl, cdl_file, name):
    cdl_file.write('  float ' + name + '(' + cntl["feature_georef"][name]["dimid"] + ');\n')
    cdl_file.write('    ' + name + ':long_name = "' + cntl["feature_georef"][name]["long_name"] + '";\n')
    cdl_file.write('    ' + name + ':units = "' + cntl["feature_georef"][name]["units"] + '";\n')
    cdl_file.write('    ' + name + ':standard_name = "' + cntl["feature_georef"][name]["standard_name"] + '";\n')
    cdl_file.write('    ' + name + ':_FillValue = ' + cntl["feature_georef"][name]["fill_value"] + ';\n')


def write_timeseries_block(cntl, cdl_file, name):
    cdl_file.write('  float ' + name + '(time, ' + cntl["output_variables"][name]["georef"]["dimid"] + ');\n')
    cdl_file.write('    ' + name + ':long_name = "' + cntl["output_variables"][name]["long_name"] + '";\n')
    cdl_file.write('    ' + name + ':units = "' + cntl["output_variables"][name]["out_units"] + '";\n')
    cdl_file.write('    ' + name + ':standard_name = "' + cntl["output_variables"][name]["standard_name"] + '";\n')
    cdl_file.write('    ' + name + ':_FillValue = ' + cntl["output_variables"][name]["fill_value"] + ';\n')


def write_timeseries_values(cntl, cdl_file, name, vals):
    cdl_file.write(name + ' =\n')
    fmt = cntl["output_variables"][name]['format']

    nts = len(vals)
    nhrus = len(vals[0])

    for ii in range(0, nts):
        cdl_file.write('  ' + str(fmt % vals[ii][0]))
        for jj in range(1, nhrus):
            cdl_file.write(', ' + str(fmt % vals[ii][jj]))
        if ii == nts-1:
            cdl_file.write('\n')
        else:
            cdl_file.write(',\n')
    cdl_file.write(';\n\n')


def main():
    with open(json_file, "r") as read_file:
        cntl = json.load(read_file)

# Read the PRMS output
    var_names = cntl["output_variables"].keys()
    val_list = []
    dim_list = set()

    for var_name in var_names:
        print("processing " + var_name)
        dim_list.add(cntl["output_variables"][var_name]["georef"]["dimid"])

        csv_fn = cntl["output_variables"][var_name]["prms_out_file"]
        nts, nfeats, base_date, foo = csv_reader.read_output(csv_fn)

        conversion_factor = float(cntl["output_variables"][var_name]["conversion_factor"])
        vals = [num * conversion_factor for num in foo]
        val_list.append(vals)

#     if nts != nts1:
#         raise ValueError('number of timesteps not the same in nhru_soil_moist.csv and nhru_hru_lateral_flow.csv')
#
#     if nhrus != nhrus1:
#         raise ValueError('number of hrus not the same in nhru_soil_moist.csv and nhru_hru_lateral_flow.csv')
#
#     if base_date != base_date1:
#         raise ValueError('base date not the same in nhru_soil_moist.csv and nhru_hru_lateral_flow.csv')
#
#     if nts != nts2:
#         raise ValueError('number of timesteps not the same in nhru_soil_moist.csv and nsegment_seg_outflow.csv')
#
#     if base_date != base_date2:
#         raise ValueError('base date not the same in nhru_soil_moist.csv and nsegment_seg_outflow.csv')

    print(dim_list)

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

# write the cdl file
    print('writing cdl file ' + cntl['cdl_file_name'])
    cdl_file = open(cntl['cdl_file_name'], 'w')
    cdl_file.write('netcdf ' + cntl["nc_name"] + ' {' + '\n')

    # Write dimensions block
    cdl_file.write('dimensions:\n')
    cdl_file.write('  ' + 'time' + ' = ' + str(nts) + ';\n')

    if nhrus > 0:
        cdl_file.write('  ' + 'hruid' + ' = ' + str(nhrus) + ';\n')

    if nsegments > 0:
        cdl_file.write('  ' + 'segid' + ' = ' + str(nsegments) + ';\n')

    # Write the variables block
    cdl_file.write('variables:\n')

    # Put in the indexes for the dimensions
    key = 'time'
    idname = key + 'id'
    cdl_file.write('  int time(time);\n')
    cdl_file.write('    time:long_name = "time";\n')
    cdl_file.write('    time:standard_name = "time";\n')
    cdl_file.write('    time:cf_role = "timeseries_id";\n')
    cdl_file.write('    time:units = "days since ' + base_date +' 00:00' + cntl["tz_code"] + '";\n')

    if nhrus > 0:
        key = 'hru'
        idname = key + 'id'
        cdl_file.write('  int ' + idname + '(' + idname + ');\n')
        cdl_file.write('    ' + idname + ':long_name = "local model ' + key + ' id";\n')

    if nsegments > 0:
        key = 'seg'
        idname = key + 'id'
        cdl_file.write('  int ' + idname + '(' + idname + ');\n')
        cdl_file.write('    ' + idname + ':long_name = "local model ' + key + ' id";\n')

    if nhrus > 0:
        write_variable_block(cntl, cdl_file, "hru_lat")
        write_variable_block(cntl, cdl_file, "hru_lon")

    if nsegments > 0:
        write_variable_block(cntl, cdl_file, "seg_lat")
        write_variable_block(cntl, cdl_file, "seg_lon")

    for var_name in var_names:
        write_timeseries_block(cntl, cdl_file, var_name)

    cdl_file.write('  // global attributes:\n')
    cdl_file.write('  :Conventions = "CF-1.8";\n')
    cdl_file.write('  :featureType = "timeSeries";\n')
    cdl_file.write('  :history = "' + str(datetime.datetime.now()) + ',' + str(getpass.getuser()) + ',prms_outputs2_cdl.py";\n')

    # Write data
    cdl_file.write('\ndata:\n\n')

# time
    cdl_file.write('time =\n')
    cdl_file.write('  0')
    for ii in range(1, nts):
        cdl_file.write(', ' + str(ii))
    cdl_file.write(';\n\n')

    if nhrus > 0:
# hruid
        cdl_file.write('hruid =\n')
        cdl_file.write('  1')
        for ii in range(2, nhrus):
            cdl_file.write(', ' + str(ii))
        cdl_file.write(';\n\n')

    if nsegments > 0:
# segid
        cdl_file.write('segid =\n')
        cdl_file.write('  1')
        for ii in range(2, nsegments):
            cdl_file.write(', ' + str(ii))
        cdl_file.write(';\n\n')

    if nhrus > 0:
# latitude
        cdl_file.write('hru_lat =\n')
        cdl_file.write('  ' + str('%.6f' % hru_lat_vals[0]))
        for ii in range(1, nhrus):
            cdl_file.write(', ' + str('%.6f' % hru_lat_vals[ii]))
        cdl_file.write(';\n\n')

# longitude
        cdl_file.write('hru_lon =\n')
        cdl_file.write('  ' + str('%.6f' % hru_lon_vals[0]))
        for ii in range(1, nhrus):
            cdl_file.write(', ' + str('%.6f' % hru_lon_vals[ii]))
        cdl_file.write(';\n\n')

    if nsegments > 0:
# latitude
        cdl_file.write('seg_lat =\n')
        cdl_file.write('  ' + str('%.6f' % seg_lat_vals[0]))
        for ii in range(1, nsegments):
            cdl_file.write(', ' + str('%.6f' % seg_lat_vals[ii]))
        cdl_file.write(';\n\n')

# longitude
        cdl_file.write('seg_lon =\n')
        cdl_file.write('  ' + str('%.6f' % seg_lon_vals[0]))
        for ii in range(1, nsegments):
            cdl_file.write(', ' + str('%.6f' % seg_lon_vals[ii]))
        cdl_file.write(';\n\n')

    ii = 0
    for var_name in var_names:
        vals = val_list[ii]
        write_timeseries_values(cntl, cdl_file, var_name, vals)
        ii = ii + 1

    # Close the cdl file
    cdl_file.write('}\n')
    cdl_file.close()


if __name__ == '__main__':
    main()
