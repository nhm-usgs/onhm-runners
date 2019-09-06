###############################################################################
# 2019-09-06
# markstro
#
# This is the run time controller for the ONHM. This can be run everyday or
# whenever it is needed to update to the "current state".
###############################################################################

import os
import sys
import glob
import datetime


# Check the restart directory for restart files.
# Return the date of the latest one.
def last_simulation_date(dir):
    foo = glob.glob(dir + 'restart/*.restart')

    restart_dates_present = []
    for fn in foo:
        head, tail = os.path.split(fn)
        restart_dates_present.append(datetime.datetime.strptime(tail[0:10], "%Y-%m-%d"))
    
    restart_dates_present.sort(reverse=True)
    return restart_dates_present[0]


def main(dir):

    # Determine the date for the last simulation by finding the last restart file
    lsd = last_simulation_date(dir)
    print('last simulation date = ' + lsd.strftime('%Y-%m-%d'))
    
    # Determine the last date of the historical CBH data
    
    # Run the Fetcher/Parser to pull available data
    
    # If the Fetcher/Parser pull has new data, map it onto the HRUs
    
    # Add/overwrite the CBH files with the new Fetcher/Parser data
    
    # Figure out the run period for PRMS. It should usually be the previous 60
    # days, but it could be more if the ONHM has been down for some time
    
    # Run PRMS for the prescribed period.
    
    # Verify that PRMS ran correctly.
    
    # Create ncf files from the output csv files (one for each output variable).
    
    # Rename the ncf output files according to the last day of the simulation,
    # like this YYYY-MM-DD_variable_name_out.nc
    
    # Copy these nc files (made in the previous step) to the s3 area.
    
    # Run PRMS to update the init files to reflect the run that was just made
    # so as to be ready for the next run (usually tomorrow).


if __name__ == '__main__':
    argc = len(sys.argv) - 1
    # print(argc)

    if argc == 1:
        print('setting dir = ' + sys.argv[1])
        dir = sys.argv[1]
    else:
        dir='/var/lib/nhm/NHM-PRMS_CONUS/'
        
    dir = '/ssd/markstro/conusStreamTemp/work_lev3/'
    main(dir)