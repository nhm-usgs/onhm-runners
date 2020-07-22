# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Set the file names. These need to be passed in.

# cbh_in_fn='c:/Users/markstro/work1.1/cbh_gridmet/tmin.cbh'
# cbh_out_fn='c:/Users/markstro/work1.1/cbh_gridmet/tmin_out_from_script.cbh'
# nhm_id_fn='c:/Users/markstro/work1.1/cbh_gridmet/nhm_id.txt'
# miss_to_pres_mapping ='c:/Users/markstro/work1.1/cbh_gridmet/miss_to_pres_mapping.csv'

# var_name = "tmin"
# frmt = "%.1f"


def shift(df, dates, col_name, pos):
    df[col_name] = dates[:,pos]
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]
    return df


def cbh_writer(vals, dates, nhm_id, fn, var_name, f):
    df = pd.DataFrame(vals, columns=nhm_id)
    
    # add the time stamps and move to the front of the DataFrame so they will
    # be on the left of the file
    df = shift(df, dates, "sec", 5)
    df = shift(df, dates, "min", 4)
    df = shift(df, dates, "hr", 3)
    df = shift(df, dates, "day", 2)
    df = shift(df, dates, "mon", 1)
    df = shift(df, dates, "yr", 0)
    
    # Write this out
    # write the header
    fo = open(fn,"w")
    fo.write("Written by cbh_filler\n" + var_name + " " + str(vals.shape[1]) + "\n" + "########################################\n")
    fo.close()

    # write the values
    df.to_csv(fn, sep=' ', float_format=f, header=False, index=False, mode='a')


# Read a cbh file
def read_cbh(cbh_fn):
#    foo = np.loadtxt(cbh_fn, delimiter=' ', skiprows=3,)
    foo = np.loadtxt(cbh_fn, skiprows=3,)
    dates = foo[:,0:6].astype('int')
    vals = foo[:,6:foo.shape[1]]
    return dates, vals


def main(cbh_in_fn, ofile, nhm_id_fn, miss_to_pres_mapping):

    varn = ['tmax', 'tmin', 'prcp', 'humidity']
    for varname in var:
    
# Read the unfilled cbh file
        ifile = Path(cbh_in_fn) / (varname + '_t.cbh') #ncf2cbh now outputs _t.cbh to distinguish between filled and unfilled
        ofile = Path(cbh_out_fn) / (varname + '.cbh')
        dates, vals = read_cbh(ifile)
        nday = vals.shape[0]
        nhru = vals.shape[1]
        
# read the order of the HRUs from a csv version of the parameter file.
        nhm_id = np.loadtxt(nhm_id_fn, dtype='int')

# Read the list of HRUs that have missing values from csv file
        mapping_df = pd.read_csv(miss_to_pres_mapping)
        mapping_df.head()
        nmiss = mapping_df.shape[0]
        
        miss_id = mapping_df["nhru_v11_miss"].values
        pres_id = mapping_df["nhru_v11_pres"].values
        
# Fill the values
        filled_vals = np.zeros(nday * nhru)
        filled_vals.shape = (nday, nhru)

        for iday in range(nday):
            for ii in range(nhru):
                filled_vals[iday,ii] = vals[iday,ii]

        for iday in range(nday):
            for ii in range(nmiss):
                filled_vals[iday,miss_id[ii]-1] = vals[iday,pres_id[ii]-1]
        
# Write out the filled values to a new CBH file
        if var_name == 'prcp':
            fmt = "%.2f"
        else:
            fmt = "%.1f"
        print(f'writing filled cbh file {var_name}')
        cbh_writer(filled_vals, dates, nhm_id, cbh_out_fn, var_name, frmt)


if __name__ == "__main__":
    
# Lots of stuff needs to be passed in.
# cbh_in_fn='c:/Users/markstro/work1.1/cbh_gridmet/tmin.cbh'
# cbh_out_fn='c:/Users/markstro/work1.1/cbh_gridmet/tmin_out_from_script.cbh'
# nhm_id_fn='c:/Users/markstro/work1.1/cbh_gridmet/nhm_id.txt'
# miss_to_pres_mapping ='c:/Users/markstro/work1.1/cbh_gridmet/miss_to_pres_mapping.csv'
# var_name = "tmin"'
# frmt = "%.1f"

    print(sys.argv)
    print(len(sys.argv))
    print(sys.argv[0])
    print(sys.argv[1])
    
    if (len(sys.argv) == 7):     #test whether any arguments have been passed in
        cbh_in_fn = Path(sys.argv[1])
        cbh_out_fn = Path(sys.argv[2])
        nhm_id_fn = Path(sys.argv[3])
        miss_to_pres_mapping = Path(sys.argv[4])
    else:
        print("No name passed in")

    assert cbh_in_fn.exists(), "input directory doesn't exist"
    assert cbh_out_fn.exists(), "output directory doesn't exist"
    assert nhm_id_fn.exists(), "nhm_id file doesn't exist"
    assert miss_to_pres_mapping.exists(), "mapping file doesn't exist"  
    
    main(cbh_in_fn, cbh_out_fn, nhm_id_fn, miss_to_pres_mapping)