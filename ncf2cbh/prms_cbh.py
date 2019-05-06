# Markstrom
# Wed Mar 13 09:43:53 MDT 2019

#import os
from prms_utils import csv_reader
import numpy as np
import csv

#from prms_utils import paramfile
#from prms_utils import datafile_reader
# from prms_utils import get_dim_list
from prms_utils import cdl_writer
# import fiona
# from netCDF4 import Dataset
#
# # This stuff located at
# # moto:/work/markstro/intern_demo/simple-geom/netCDF-CF-simple-geometry/src/python
# from ncgeom.convert.netcdf.nc_names import NcNames
#
# import ncf_writer_utils
#import prms_inputs_noglob

# Time zone code for the timestamps. Skunk River is in Iowa (central time zone)
# Not sure where this should come from
tz_code = '-05:00'
nc_name = 'nhm_conus'

# define the shapefile that goes with each dimension
#shape_dir = "/work/markstro/intern_demo/GIS_Data"

# Names of shapefile can only be in a dictionary once so the same map cannot be used for more than one dimension. Make
# copy(ies) of the shapefile, with different names, for each duplicate dimension.
# shapes = {'/hrus_all_conus_geo.shp': ('Polygon', 'nhru', 'nhm_id'),
#           #'/segs_all_conus_geo.shp': ('LineString', 'nsegment', 'nhm_seg')
#           }

# Input modeling files
dir = "/work/markstro/operat/samples/nhm_animation_ncdf"
in_dir = dir + "/prms_files"

# Output nc file
out_dir = dir + "/input"

cdl_file_name = out_dir + '/nhm_cbh_example_short.cdl'
#cdl_file_name = in_dir + '/nhm_output_example.cdl'


def main():
# Read the PRMS CBH
    nts, nhrus, base_date, foo = csv_reader.read_cbh(in_dir + '/' + 'prcp_short.csv')
    prcp_vals = [num * 25.4 for num in foo] # convert inches to mm
    print nts, nhrus, base_date
    print prcp_vals[0][nhrus-1], prcp_vals[nts-1][0], prcp_vals[nts-1][nhrus-1]

    nts1, nhrus1, base_date1, foo = csv_reader.read_cbh(in_dir + '/' + 'tmax_short.csv')
    tmax_vals = [(num -32.0) * 5.0/9.0 for num in foo] # convert F to C
    print nts, nhrus, base_date
    print tmax_vals[0][nhrus-1], tmax_vals[nts-1][0], tmax_vals[nts-1][nhrus-1]

    if nts != nts1:
        raise ValueError('number of timesteps not the same in prcp_short.csv and tmax_short.csv')

    if nhrus != nhrus1:
        raise ValueError('number of hrus not the same in prcp_short.csv and tmax_short.csv')

    if base_date != base_date1:
        raise ValueError('base date not the same in prcp_short.csv and tmax_short.csv')

    nts2, nhrus2, base_date2, foo = csv_reader.read_cbh(in_dir + '/' + 'tmin_short.csv')
    tmin_vals = [(num - 32.0) * 5.0 / 9.0 for num in foo]  # convert F to C
    print nts2, nhrus2, base_date2
    print tmin_vals[0][nhrus - 1], tmin_vals[nts - 1][0], tmin_vals[nts - 1][nhrus - 1]
    if nts != nts2:
        raise ValueError('number of timesteps not the same in prcp_short.csv and tmin_short.csv')

    if nhrus != nhrus2:
        raise ValueError('number of hrus not the same in prcp_short.csv and tmin_short.csv')

    if base_date != base_date2:
        raise ValueError('base date not the same in prcp_short.csv and tmin_short.csv')

    # hru_lat
    hru_lat_vals = np.zeros(shape=(nhrus))
    with open(in_dir + '/' + 'hru_lat.txt', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        ii = 0
        for row in spamreader:
            hru_lat_vals[ii] = float(row[0])
            ii = ii + 1

    # hru_lon
    hru_lon_vals = np.zeros(shape=(nhrus))
    with open(in_dir + '/' + 'hru_lon.txt', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        ii = 0
        for row in spamreader:
            hru_lon_vals[ii] = float(row[0])
            ii = ii + 1

# write the cdl file
    print 'writing cdl file ' + cdl_file_name
    cdl_file = open(cdl_file_name, 'w')
    cdl_file.write('netcdf ' + nc_name + ' {' + '\n')

    # Write dimensions block
    cdl_file.write('dimensions:\n')
    cdl_file.write('  ' + 'time' + ' = ' + str(nts) + ';\n')
    cdl_file.write('  ' + 'hruid' + ' = ' + str(nhrus) + ';\n')

    # Write the variables block
    cdl_file.write('variables:\n')

    # Put in the indexes for the dimensions
    key = 'time'
    idname = key + 'id'
    cdl_file.write('  int time(time);\n')
    cdl_file.write('    time:long_name = "time";\n')
    cdl_file.write('    time:standard_name = "time";\n')
    cdl_file.write('    time:units = "days since ' + base_date +' 00:00' + tz_code + '";\n')

    key = 'hru'
    idname = key + 'id'
    cdl_file.write('  int ' + idname + '(' + idname + ');\n')
    cdl_file.write('    ' + idname + ':cf_role = "timeseries_id";\n')
    cdl_file.write('    ' + idname + ':long_name = "local model ' + key + ' id";\n')

    cdl_file.write('  float hru_lat(hruid);\n')
    cdl_file.write('    hru_lat:long_name = "Latitude of HRU centroid";\n')
    cdl_file.write('    hru_lat:units = "degrees_north";\n')
    cdl_file.write('    hru_lat:standard_name = "hru_latitude";\n')

    cdl_file.write('  float hru_lon(hruid);\n')
    cdl_file.write('    hru_lon:long_name = "Longitude of HRU centroid";\n')
    cdl_file.write('    hru_lon:units = "degrees_east";\n')
    cdl_file.write('    hru_lon:standard_name = "hru_longitude";\n')

    cdl_file.write('  float prcp(time, hruid);\n')
    cdl_file.write('    prcp:long_name = "Daily precipitation rate";\n')
    cdl_file.write('    prcp:units = "mm/day";\n')
    cdl_file.write('    prcp:standard_name = "lwe_precipitation_rate";\n')

    cdl_file.write('  float tmax(time, hruid);\n')
    cdl_file.write('    tmax:long_name = "Maximum daily air temperature";\n')
    cdl_file.write('    tmax:units = "degree_Celsius";\n')
    cdl_file.write('    tmax:standard_name = "maximum_daily_air_temperature";\n')

    cdl_file.write('  float tmin(time, hruid);\n')
    cdl_file.write('    tmin:long_name = "Minimum daily air temperature";\n')
    cdl_file.write('    tmin:units = "degree_Celsius";\n')
    cdl_file.write('    tmin:standard_name = "minimum_daily_air_temperature";\n')

    cdl_file.write('  // global attributes:\n')
    cdl_file.write('  :Conventions = "CF-1.8";\n')
    cdl_file.write('  :featureType = "timeSeries";\n')
    cdl_file.write('  :history = "Thu Mar 21 11:22:48 MDT 2019,markstro,prms_cbh.py,\\n";\n')

    # Write data
    cdl_file.write('\ndata:\n\n')

# time
    cdl_file.write('time =\n')
    cdl_file.write('  0')
    for ii in xrange(1, nts):
        cdl_file.write(', ' + str(ii))
    cdl_file.write(';\n\n')

# hruid
    cdl_file.write('hruid =\n')
    cdl_file.write('  1')
    for ii in xrange(2, nhrus):
        cdl_file.write(', ' + str(ii))
    cdl_file.write(';\n\n')

# latitude
    cdl_file.write('hru_lat =\n')
    cdl_file.write('  ' + str('%.6f' % hru_lat_vals[0]))
    for ii in xrange(1, nhrus):
        cdl_file.write(', ' + str('%.6f' % hru_lat_vals[ii]))
    cdl_file.write(';\n\n')

# longitude
    cdl_file.write('hru_lon =\n')
    cdl_file.write('  ' + str('%.6f' % hru_lon_vals[0]))
    for ii in xrange(1, nhrus):
        cdl_file.write(', ' + str('%.6f' % hru_lon_vals[ii]))
    cdl_file.write(';\n\n')

# soil_moist
    cdl_file.write('prcp =\n')
    for ii in xrange(0, nts):
        cdl_file.write('  ' + str('%.1f' % prcp_vals[ii][0]))
        for jj in xrange(1, nhrus):
            cdl_file.write(', ' + str('%.1f' % prcp_vals[ii][jj]))
        if ii == nts-1:
            cdl_file.write('\n')
        else:
            cdl_file.write(',\n')
    cdl_file.write(';\n\n')

# runoff
    cdl_file.write('tmax =\n')
    for ii in xrange(0, nts):
        cdl_file.write('  ' + str('%.1f' % tmax_vals[ii][0]))
        for jj in xrange(1, nhrus):
            cdl_file.write(', ' + str('%.1f' % tmax_vals[ii][jj]))
        if ii == nts - 1:
            cdl_file.write('\n')
        else:
            cdl_file.write(',\n')
    cdl_file.write(';\n\n')

# stream_flow
    cdl_file.write('tmin =\n')
    for ii in xrange(0, nts):
        cdl_file.write('  ' + str('%.1f' % tmin_vals[ii][0]))
        for jj in xrange(1, nhrus):
            cdl_file.write(', ' + str('%.1f' % tmin_vals[ii][jj]))
        if ii == nts - 1:
            cdl_file.write('\n')
        else:
            cdl_file.write(',\n')
    cdl_file.write(';\n\n')

    # Close the cdl file
    cdl_file.write('}\n')
    cdl_file.close()

# at this point, missing_val_set contains the names of all values because nothing has been removed yet.
#     print '1', missing_val_set


# This writes the netcdf files.
#     for map_name, f1, in shapes.items():
#         print map_name, f1
#         prms_inputs_noglob.prms_inputs_noglob(map_name, f1, model_output_file_names, in_dir,
#                                               parameter_file_name_for_dim_size, out_dir, nc_name, tz_code,
#                                               info_file_name, shape_dir, missing_val_set, all_values_dict, nts,
#                                               base_date)


if __name__ == '__main__':
    main()
