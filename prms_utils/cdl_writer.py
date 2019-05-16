from prms_utils import get_param_info
# from prms_utils import get_dim_list
import numpy

# Write a CDL format file
#
# cdl_file_name - full path to the cdl file to write
# nc_name - name to call the internal ncdf data structure
# nts - number of time steps
# base_date - integer array (yr, mo, da, hr, mi, se) of time step zero
# ts_code - three or four character string specifying the standard code for the time zone of the base_date
# dims - dictionary of dimensions to write into this cdl. key is name; value is the integer size
# pinfo_file_name - full path to the xml file with the meta data about all parameters, vars, etc.


def cdl_writer(cdl_file_name, nc_name, nts, base_date, tz_code, var_list, dims_list, ps, xml_info_name):
    # print 'writing cdl file ' + cdl_file_name
    cdl_file = open(cdl_file_name, 'w')
    cdl_file.write('netcdf ' + nc_name + ' {' + '\n')

    # Write dimensions block
    cdl_file.write('dimensions:\n')
    cdl_file.write('  time = ' + str(nts) + ';\n')

    for d1 in dims_list:
        cdl_file.write('  ' + d1 + ' = ' + str(ps.get_dim_size(d1)) + ';\n')

    # Write the variables block
    cdl_file.write('variables:\n')

    # time
    cdl_file.write('  int time(time);\n')
    cdl_file.write('    time:long_name = "time";\n')
    cdl_file.write('    time:standard_name = "time";\n')
    print(len(base_date), base_date)
    time_str = str(base_date[0]) + '-' + str(base_date[1] + '-' + str(base_date[2]) + ' 00:00 ' + tz_code)
    cdl_file.write('    time:units = "days since ' + time_str + '";\n')

    # Put in the indexes for the dimensions
    for key in dims_list:
        idname = key + 'id'
        cdl_file.write('  int ' + idname + '(' + key + ');\n')
        cdl_file.write('    ' + idname + ':cf_role = "timeseries_id";\n')
        cdl_file.write('    ' + idname + ':long_name = "local model ' + key + ' id";\n')

    # put in the parameter/var definitions
    for var in var_list:
        var_name = var[1]
        # print 'cdl_writer ', var_name
        long_name, units, standard_name, type_code, dims = get_param_info.get_param_info(var_name, xml_info_name)

        if dims is not None:
            foo_dims = '(' + dims[0]
            for ii in range(1, len(dims)):
                foo_dims += ', ' + dims[ii]
            foo_dims = foo_dims + ');\n'
            # print foo_dims

            # cdl_file.write('  double lat(nhru);\n')
            if type_code == 'I':  # integer
                cdl_file.write('  int ' + var_name + foo_dims)
            elif type_code == 'F':  # float
                cdl_file.write('  float ' + var_name + foo_dims)
            elif type_code == 'S':  # string
                cdl_file.write('  string ' + var_name + foo_dims)
            else:
                print('parameter ' + var_name + ' has unknown type.')

            cdl_file.write('    ' + var_name + ':long_name = "' + str(long_name) + '";\n')
            cdl_file.write('    ' + var_name + ':units = "' + str(units) + '";\n')
            cdl_file.write('    ' + var_name + ':standard_name = "' + str(standard_name) + '";\n')

    # # put in the data file definitions
    # # data_ids, data_var_names, data_dates, data_vals
    # for vl in var_list:
    #     key = vl[0]
    #     print key
    #     fd = get_dim_list.all(key=key)
    #     print fd
    #
    #     foo_dims = '(' + fd[0]
    #     for ii in xrange(1, len(fd)):
    #         foo_dims += ', ' + fd[ii]
    #     foo_dims = foo_dims + ');\n'
    #
    #     cdl_file.write('  float ' + key + foo_dims)
    #
    #     long_name, units, standard_name = get_param_info.get_param_info(key, xml_info_name)
    #     cdl_file.write('    ' + key + ':long_name = "' + str(long_name) + '";\n')
    #     cdl_file.write('    ' + key + ':units = "' + str(units) + '";\n')
    #     cdl_file.write('    ' + key + ':standard_name = "' + str(standard_name) + '";\n')
    #
    # # put in the cbh file definitions
    # # data_ids, data_var_names, data_dates, data_vals
    # for key in csv_data_names:
    #     cdl_file.write('  float ' + key + '(time, nhru);\n')
    #
    #     long_name, units, standard_name = get_param_info.get_param_info(key, xml_info_name)
    #     cdl_file.write('    ' + key + ':long_name = "' + str(long_name) + '";\n')
    #     cdl_file.write('    ' + key + ':units = "' + str(units) + '";\n')
    #     cdl_file.write('    ' + key + ':standard_name = "' + str(standard_name) + '";\n')

    # Put in the coordinate system
    # CRS (coordinate reference system) hardcoded for now, get from the shapefile

    # TODO: fix the coordinate system (crs) so that it's read from the shapefile.

    # This stuff in the bull_creek example, but it causes nc_copy to crash.
    # Comment out for now
    cdl_file.write('  int crs;\n')
    cdl_file.write('    crs:grid_mapping_name = "latitude_longitude";\n')
    cdl_file.write('    crs:longitude_of_prime_meridian = 0.0;\n')
    cdl_file.write('    crs:semi_major_axis = 6378137.0;\n')
    cdl_file.write('    crs:inverse_flattening = 298.257223563;\n')

    # Global attributes
    cdl_file.write('// global attributes:\n')
    cdl_file.write('  :Conventions = "CF-1.8";\n')
    cdl_file.write('  :featureType = "timeSeries";\n')

    # Write data
    cdl_file.write('\ndata:\n\n')

    # Time steps
    cdl_file.write('time =\n  0')
    for ii in range(1, nts + 1):
        cdl_file.write(', ' + str(ii))
    cdl_file.write(';\n\n')

    # IDs for the dimension indexes
    for key in dims_list:
        idname = key + 'id'
        cdl_file.write(idname + ' =\n  1')
        for ii in range(2, ps.get_dim_size(key) + 1):
            cdl_file.write(', ' + str(ii))
        cdl_file.write(';\n\n')

    # # put in the parameter values
    # for key in ps.params:
    #     vals = ps.params[key].vals
    #
    #     cdl_file.write(key + ' =\n  ' + str(vals[0]))
    #     for ii in xrange(1, len(vals)):
    #         cdl_file.write(', ' + str(vals[ii]))
    #     cdl_file.write(';\n\n')

    # put in the data file values
    for var in var_list:
        ext = var[0]
        key = var[1]
        vals = var[2]

        cdl_file.write(key + ' =\n')

        # print var_list
        # print str(len(data_vals))

        # Might need to check for type "list" as well
        if any(isinstance(i, numpy.ndarray) for i in vals):
            flat_list = [item for sublist in vals for item in sublist]
        else:
            flat_list = vals

        cdl_file.write('  ' + str(flat_list[0]))
        for ii in range(1, len(flat_list)):
            cdl_file.write(', ' + str(flat_list[ii]))

        cdl_file.write(';\n\n')

    # Close the cdl file
    cdl_file.write('}\n')
    cdl_file.close()


def cdl_no_map_writer(cdl_file_name, nc_name, missing_val_set, all_values_dict, dims_set, ps, info_file_name):
    # print 'writing cdl file ' + cdl_file_name
    cdl_file = open(cdl_file_name, 'w')
    cdl_file.write('netcdf ' + nc_name + ' {' + '\n')

    # Write dimensions block
    cdl_file.write('dimensions:\n')

    for d1 in dims_set:
        cdl_file.write('  ' + d1 + ' = ' + str(ps.get_dim_size(d1)) + ';\n')

    # Write the variables block
    cdl_file.write('variables:\n')

    # Put in the indexes for the dimensions
    for key in dims_set:
        idname = key + 'id'
        cdl_file.write('  int ' + idname + '(' + key + ');\n')
        cdl_file.write('    ' + idname + ':cf_role = "id";\n')
        cdl_file.write('    ' + idname + ':long_name = "local model ' + key + ' id";\n')

    # put in the parameter/var definitions
    for var in missing_val_set:
        # print 'cdl_writer ', var_name
        foo = get_dim_list.all(var, ps)

        if foo is not None:
            foo_dims = '(' + foo[0]
            for ii in range(1, len(foo)):
                foo_dims += ', ' + foo[ii]
            foo_dims = foo_dims + ');\n'
            # print foo_dims

            long_name, units, standard_name, type_code = get_param_info.get_param_info(var, info_file_name)

            # cdl_file.write('  double lat(nhru);\n')
            if type_code == 'I':  # integer
                cdl_file.write('  int ' + var + foo_dims)
            elif type_code == 'F':  # float
                cdl_file.write('  float ' + var + foo_dims)
            elif type_code == 'S':  # string
                cdl_file.write('  string ' + var + foo_dims)
            else:
                print('parameter ' + var + ' has unknown type.')

            cdl_file.write('    ' + var + ':long_name = "' + str(long_name) + '";\n')
            cdl_file.write('    ' + var + ':units = "' + str(units) + '";\n')
            cdl_file.write('    ' + var + ':standard_name = "' + str(standard_name) + '";\n')

    # Global attributes
    cdl_file.write('// global attributes:\n')
    cdl_file.write('  :Conventions = "CF-1.8";\n')

    # Write data
    cdl_file.write('\ndata:\n\n')

    # IDs for the dimension indexes
    for key in dims_set:
        idname = key + 'id'
        cdl_file.write(idname + ' =\n  1')
        for ii in range(2, ps.get_dim_size(key) + 1):
            cdl_file.write(', ' + str(ii))
        cdl_file.write(';\n\n')

    # put in the data file values
    for var in missing_val_set:
        foo = all_values_dict[var]
        ext = foo[0]
        key = foo[1]
        vals = foo[2]

        cdl_file.write(key + ' =\n')

        # print var_list
        # print str(len(data_vals))

        # Might need to check for type "list" as well
        if any(isinstance(i, numpy.ndarray) for i in vals):
            flat_list = [item for sublist in vals for item in sublist]
        else:
            flat_list = vals

        cdl_file.write('  ' + str(flat_list[0]))
        for ii in range(1, len(flat_list)):
            cdl_file.write(', ' + str(flat_list[ii]))

        cdl_file.write(';\n\n')

    # Close the cdl file
    cdl_file.write('}\n')
    cdl_file.close()