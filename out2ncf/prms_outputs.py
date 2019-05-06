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
out_dir = dir + "/output"

cdl_file_name = out_dir + '/nhm_output_example_short.cdl'
#cdl_file_name = in_dir + '/nhm_output_example.cdl'


def main():
# Read the PRMS output
    # soil_moist_vals[nts][nhrus]
    nts, nhrus, base_date, foo = csv_reader.read_output(in_dir + '/' + 'nhru_soil_moist_short.csv')
#    nts, nhrus, base_date, foo = csv_reader.read_output(in_dir + '/' + 'nhru_soil_moist.csv')
    soil_moist_vals = [num * 25.4 for num in foo] # convert inches to mm
    print nts, nhrus, base_date
    print soil_moist_vals[0][nhrus-1], soil_moist_vals[nts-1][0], soil_moist_vals[nts-1][nhrus-1]

    # runoff_vals[nts][nhrus]
    nts1, nhrus1, base_date1, foo = csv_reader.read_output(in_dir + '/' + 'nhru_hru_lateral_flow_short.csv')
#    nts1, nhrus1, base_date1, foo = csv_reader.read_output(in_dir + '/' + 'nhru_hru_lateral_flow.csv')

    if nts != nts1:
        raise ValueError('number of timesteps not the same in nhru_soil_moist.csv and nhru_hru_lateral_flow.csv')

    if nhrus != nhrus1:
        raise ValueError('number of hrus not the same in nhru_soil_moist.csv and nhru_hru_lateral_flow.csv')

    if base_date != base_date1:
        raise ValueError('base date not the same in nhru_soil_moist.csv and nhru_hru_lateral_flow.csv')

    runoff_vals = [num * 25.4 for num in foo] # convert inches to mm
    print nts, nhrus, base_date
    print runoff_vals[0][nhrus-1], runoff_vals[nts-1][0], runoff_vals[nts-1][nhrus-1]

    # seg_outflow_vals[nts][nsegments]
    nts2, nsegments, base_date2, foo = csv_reader.read_output(in_dir + '/' + 'nsegment_seg_outflow_short.csv')
#    nts2, nsegments, base_date2, foo = csv_reader.read_output(in_dir + '/' + 'nsegment_seg_outflow.csv')

    if nts != nts2:
        raise ValueError('number of timesteps not the same in nhru_soil_moist.csv and nsegment_seg_outflow.csv')

    if base_date != base_date2:
        raise ValueError('base date not the same in nhru_soil_moist.csv and nsegment_seg_outflow.csv')

    seg_outflow_vals = [num * 0.0283168 for num in foo] # convert cfs to cms
    print nts, nsegments, base_date
    print seg_outflow_vals[0][nsegments - 1], seg_outflow_vals[nts - 1][0], seg_outflow_vals[nts - 1][nsegments - 1]

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

    # seg_lat
    seg_lat_vals = np.zeros(shape=(nsegments))
    with open(in_dir + '/' + 'lat_seg.txt', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        ii = 0
        for row in spamreader:
            seg_lat_vals[ii] = float(row[0])
            ii = ii + 1

    # seg_lon
    seg_lon_vals = np.zeros(shape=(nsegments))
    with open(in_dir + '/' + 'lon_seg.txt', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        ii = 0
        for row in spamreader:
            seg_lon_vals[ii] = float(row[0])
            ii = ii + 1

# write the cdl file
    print 'writing cdl file ' + cdl_file_name
    cdl_file = open(cdl_file_name, 'w')
    cdl_file.write('netcdf ' + nc_name + ' {' + '\n')

    # Write dimensions block
    cdl_file.write('dimensions:\n')
    cdl_file.write('  ' + 'time' + ' = ' + str(nts) + ';\n')
    cdl_file.write('  ' + 'hruid' + ' = ' + str(nhrus) + ';\n')
    cdl_file.write('  ' + 'segid' + ' = ' + str(nsegments) + ';\n')

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

    key = 'seg'
    idname = key + 'id'
    cdl_file.write('  int ' + idname + '(' + idname + ');\n')
    cdl_file.write('    ' + idname + ':cf_role = "timeseries_id";\n')
    cdl_file.write('    ' + idname + ':long_name = "local model ' + key + ' id";\n')

    cdl_file.write('  float hru_lat(hruid);\n')
    cdl_file.write('    hru_lat:long_name = "Latitude of HRU centroid";\n')
    cdl_file.write('    hru_lat:units = "degrees_north";\n')
    cdl_file.write('    hru_lat:standard_name = "hru_latitude";\n')
    cdl_file.write('    hru_lat:_FillValue = "9.969209968386869e+36";\n')

    cdl_file.write('  float hru_lon(hruid);\n')
    cdl_file.write('    hru_lon:long_name = "Longitude of HRU centroid";\n')
    cdl_file.write('    hru_lon:units = "degrees_east";\n')
    cdl_file.write('    hru_lon:standard_name = "hru_longitude";\n')
    cdl_file.write('    hru_lon:_FillValue = "9.969209968386869e+36";\n')

    cdl_file.write('  float seg_lat(segid);\n')
    cdl_file.write('    seg_lat:long_name = "Latitude of stream segment centroid";\n')
    cdl_file.write('    seg_lat:units = "degrees_north";\n')
    cdl_file.write('    seg_lat:standard_name = "segment_latitude";\n')
    cdl_file.write('    seg_lat:_FillValue = "9.969209968386869e+36";\n')

    cdl_file.write('  float seg_lon(segid);\n')
    cdl_file.write('    seg_lon:long_name = "Longitude of stream segment centroid";\n')
    cdl_file.write('    seg_lon:units = "degrees_east";\n')
    cdl_file.write('    seg_lon:standard_name = "segment_longitude";\n')
    cdl_file.write('    seg_lon:_FillValue = "9.969209968386869e+36";\n')

    cdl_file.write('  float soil_moist(time, hruid);\n')
    cdl_file.write('    soil_moist:long_name = "Soil moisture content";\n')
    cdl_file.write('    soil_moist:units = "mm";\n')
    cdl_file.write('    soil_moist:standard_name = "lwe_thickness_of_moisture_content_of_soil_layer";\n')
    cdl_file.write('    soil_moist:_FillValue = "9.969209968386869e+36";\n')

    cdl_file.write('  float lateral_flow(time, hruid);\n')
    cdl_file.write('    lateral_flow:long_name = "Lateral flow from HRU into the corresponding stream segment";\n')
    cdl_file.write('    lateral_flow:units = "mm/day";\n')
    cdl_file.write('    lateral_flow:standard_name = "lateral_flow";\n')
    cdl_file.write('    lateral_flow:_FillValue = "9.969209968386869e+36";\n')

    cdl_file.write('  float streamflow(time, hruid);\n')
    cdl_file.write('    streamflow:long_name = "Streamflow in channel";\n')
    cdl_file.write('    streamflow:units = "m3/s";\n')
    cdl_file.write('    streamflow:standard_name = "water_volume_transport_in_river_channel";\n')
    cdl_file.write('    streamflow:_FillValue = "9.969209968386869e+36";\n')

    cdl_file.write('  // global attributes:\n')
    cdl_file.write('  :Conventions = "CF-1.8";\n')
    cdl_file.write('  :featureType = "timeSeries";\n')
    cdl_file.write('  :history = "Thu Mar 14 17:25:14 MDT 2019,markstro,prms_outputs.py,\\nThu Mar 21 09:33:58 MDT 2019,markstro,prms_outputs.py,\\n";\n')

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

# segid
    cdl_file.write('segid =\n')
    cdl_file.write('  1')
    for ii in xrange(2, nsegments):
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

# latitude
    cdl_file.write('seg_lat =\n')
    cdl_file.write('  ' + str('%.6f' % seg_lat_vals[0]))
    for ii in xrange(1, nsegments):
        cdl_file.write(', ' + str('%.6f' % seg_lat_vals[ii]))
    cdl_file.write(';\n\n')

# longitude
    cdl_file.write('seg_lon =\n')
    cdl_file.write('  ' + str('%.6f' % seg_lon_vals[0]))
    for ii in xrange(1, nsegments):
        cdl_file.write(', ' + str('%.6f' % seg_lon_vals[ii]))
    cdl_file.write(';\n\n')

# soil_moist
    cdl_file.write('soil_moist =\n')
    for ii in xrange(0, nts):
        cdl_file.write('  ' + str('%.1f' % soil_moist_vals[ii][0]))
        for jj in xrange(1, nhrus):
            cdl_file.write(', ' + str('%.1f' % soil_moist_vals[ii][jj]))
        if ii == nts-1:
            cdl_file.write('\n')
        else:
            cdl_file.write(',\n')
    cdl_file.write(';\n\n')

# runoff
    cdl_file.write('lateral_flow =\n')
    for ii in xrange(0, nts):
        cdl_file.write('  ' + str('%.1f' % runoff_vals[ii][0]))
        for jj in xrange(1, nhrus):
            cdl_file.write(', ' + str('%.1f' % runoff_vals[ii][jj]))
        if ii == nts - 1:
            cdl_file.write('\n')
        else:
            cdl_file.write(',\n')
    cdl_file.write(';\n\n')

# stream_flow
    cdl_file.write('stream_flow =\n')
    for ii in xrange(0, nts):
        cdl_file.write('  ' + str('%.1f' % seg_outflow_vals[ii][0]))
        for jj in xrange(1, nsegments):
            cdl_file.write(', ' + str('%.1f' % seg_outflow_vals[ii][jj]))
        if ii == nts - 1:
            cdl_file.write('\n')
        else:
            cdl_file.write(',\n')
    cdl_file.write(';\n\n')

    # Close the cdl file
    cdl_file.write('}\n')
    cdl_file.close()


if __name__ == '__main__':
    main()
