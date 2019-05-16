import numpy as np
# import csv
import datetime
import os

def read(cbhfn):
    fp = open(cbhfn, "r")
    comment = fp.readline()
    l = fp.readline()
    tok = l.split()
    var_name = tok[0]
    nfeat = int(tok[1])

    l = fp.readline()

    l = fp.readline()
    tok = l.split()
    start_date = datetime.date(int(tok[0]), int(tok[1]), int(tok[2]))

    fp.seek(-2, os.SEEK_END)     # Jump to the second last byte.
    while fp.read(1) != b"\n":   # Until EOL is found...
        fp.seek(-2, os.SEEK_CUR) # ...jump back the read byte plus one more.
    last = fp.readline()

    tok = last.split()
    end_date = datetime.date(int(tok[0]), int(tok[1]), int(tok[2]))
    delta = end_date - start_date
    nts = delta.days + 1
    fp.close()

    vals = np.zeros(shape=(nts,nfeat))
    fp = open(cbhfn, "r")
    l = fp.readline()
    l = fp.readline()
    l = fp.readline()

    ii = 0
    l = fp.readline()
    while l:
        tok = l.split()
        for jj in range(nfeat):
            vals[ii,jj] = float(tok[jj + 6])
        ii = ii + 1
        l = fp.readline()
    fp.close()

    return var_name, nts, nfeat, start_date, end_date, vals