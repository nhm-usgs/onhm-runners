import numpy as np
import os

fn = '/ssd/markstro/conusStreamTemp/work_lev3/out/stream_temp.out.nsegment'


def sizes():
    num_lines = sum(1 for line in open(fn))
    print(num_lines)

    ii = 0
    with open(fn) as fp:
        line = fp.readline()
        ii = ii + 1

        while line.startswith('#'):
            line = fp.readline()
            ii = ii + 1

        col_names = line.split()
        line = fp.readline()
        ii = ii + 1
        line = fp.readline()
        ii = ii + 1
    toks = line.split()
    first_date = toks[0]

    header_len = ii

    with open(fn, "rb") as f:
        first = f.readline()        # Read the first line.
        f.seek(-2, os.SEEK_END)     # Jump to the second last byte.
        while f.read(1) != b"\n":   # Until EOL is found...
            f.seek(-2, os.SEEK_CUR) # ...jump back the read byte plus one more.
        last = f.readline()         # Read last line.

    toks = last.split()
    last_date = toks[0]
    nfeats = int(toks[1])
    nts = ((num_lines - header_len) / nfeats) + 1

    return first_date, last_date, nfeats, nts, col_names


def read_vals(first_date, last_date, nfeats, nts, col_names):
# allocate the arrays
    dates = np.chararray(int(nts))
    val_list =[]
    for ii in range(len(col_names) - 2):
        val_list.append(np.zeros([int(nts), int(nfeats)]))

    with open(fn) as fp:
        line = fp.readline()

        while line.startswith('#'):
            line = fp.readline()

        line = fp.readline()
        line = fp.readline()

        ii = -1
        date_string = None
        while line:
            # print("Line {}: {}".format(cnt, line.strip()))
            toks = line.split()
            # print("    toks " , toks)

# Check to see if the date stamp has incremented
            if date_string != toks[0]:
                ii += 1
                print(date_string, str(ii))
                dates[ii] = toks[0]
                date_string = toks[0]

            jj = int(toks[1]) - 1
            for kk in range(len(col_names) - 2):
                vals = val_list[kk]
# ii is the time step, jj is the feature index, kk is the variable
                vals[ii,jj] = float(toks[2+kk])

            line = fp.readline()

    return val_list


if __name__ == '__main__':
    first_date, last_date, nfeats, nts, col_names = sizes()
    print(first_date, last_date, nfeats, nts, col_names)
    val_list = read_vals(first_date, last_date, nfeats, nts, col_names)

    dir = '/ssd/markstro/conusStreamTemp/work_lev3/out/'
    for kk in range(len(col_names) - 2):
        vals = val_list[kk]
        fn1 = dir + col_names[kk+2] + ".txt"
        np.savetxt(fn1, vals, delimiter=',',fmt='%.4e')

        print(vals)
