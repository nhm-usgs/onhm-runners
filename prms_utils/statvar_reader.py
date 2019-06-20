import numpy as np
import datetime


def read(svfn):
    fp = open(svfn, "r")
    var_count = int(fp.readline())
    # print var_count

    # allocate the arrays numpy.ndarray
    var_names = np.empty([var_count], dtype='a80')
    var_indexes = np.empty([var_count], dtype=int)

# read header
    for ii in range(0, var_count):
        line = fp.readline()
        split = line.split()
        var_names[ii] = split[0]
        var_indexes[ii] = int(split[1])

        # print var_names[ii], var_indexes[ii]

# count value lines
    count = 0
    for line in fp:
        count += 1

# rewind the file
    fp.close()
    fp = open(svfn, "r")
    fp.readline()
    for ii in range(0, var_count):
        fp.readline()

# read values
    dates = np.empty([count], dtype=datetime.datetime)

    r = count
    c = var_count
    vals = np.empty(shape=(r,c), dtype=float)

    for ii in range(0, count):
        line = fp.readline().strip()
        # print(repr(line))
        sp = line.split()
        foo = datetime.datetime(int(sp[1]), int(sp[2]), int(sp[3]))
        # dates[ii] = str(sp[1])+ "-" + str(sp[2]).zfill(2) + "-"  + str(sp[3]).zfill(2)
        # print "statvar_reader date = ", foo
        dates[ii] = foo

        for jj in range(0, var_count):
            # Fortran will write "-1.#IND00" into the statvar file and maybe some other
            # string if the model breaks. I don't want these reader to choke if it hits
            # something other than a float value. The user's should get some kind of
            # message if this happens, but don't stop.
            try:
                vals[ii, jj] = float(sp[7 + jj])
            except ValueError:
                vals[ii, jj] = np.NaN
                print("value error in " + svfn)
                print("   " + line)

    fp.close()
    return var_names, var_indexes, dates, vals
