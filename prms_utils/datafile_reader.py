import numpy as np
import datetime


def var_name_by_dim(dim_name):
    # This should be more rigorous, but where does this info come from?
    if dim_name == 'nobs':
        return ['runoff']
    elif dim_name == 'nrain':
        return ['precip']
    elif dim_name == 'ntemp':
        return ['tmax', 'tmin']
    else:
        return []

def read(dffn):
    fp = open(dffn, "r")
    description = fp.readline()

# Skip down to station/variable list in the comments
    line = fp.readline()
    while '// ID Type Latitude Longitude Elevation' not in line:
        line = fp.readline()
    line = fp.readline()

# Read the station ID and the variable name.
    id_l = []
    var_name_l = []
    while '///' not in line:
        split = line.split()
        id_l.append(split[1])
        var_name_l.append(split[2])
        line = fp.readline()

# skip over the rest of the comments to get to the variable order and size
    while '//' in line:
        line = fp.readline()

# Get the count of each variable
    idx = 0
    var_positions_l = []
    while '####' not in line:
        split = line.split()
        cnt = int(split[1])
        split.append(str(idx)),
        end = idx + cnt - 1
        split.append(str(end))
        idx = end + 1
        var_positions_l.append(split)
        line = fp.readline()

    line = fp.readline()

# in the data section; count the number of lines to get the number of time steps
    nts = 0
    while len(line) > 0:
        nts = nts + 1
        line = fp.readline()

    fp.close()

# Need two arrays (1) 1-D for date-time stamp; (2) 2-D for values
    dates_l = ["" for x in range(nts)]
    nvals = len(id_l)
    vals_l = np.zeros((nts, nvals))

# Reopen the file, skip to data
    fp = open(dffn, "r")
    while '####' not in line:
        line = fp.readline()
    line = fp.readline()

# Read the data lines
    ii = 0
    while len(line) > 0:
        split = line.split()
        dates_l[ii] = split[0] + '-' + str("%02d" % int(split[1])) + '-' + str("%02d" % int(split[2]))
        for jj in xrange(0, nvals):
            vals_l[ii,jj] = float(split[jj+6])
        ii = ii + 1
        line = fp.readline()

    fp.close()
    return id_l, var_positions_l, dates_l, vals_l


if __name__ == '__main__':
    ids, var_names, dates, vals = read('/work/markstro/intern_demo/ModelInput/skunk.data')
    print ids
    print var_names
    print dates
    print vals
