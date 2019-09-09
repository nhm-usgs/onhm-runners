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


RESTARTDIR = 'restart/'
INDIR = 'in/'
OUTDIR = 'out/'
IDAHO_PROVISIONAL_DAYS = 59

# Check the restart directory for restart files.
# Return the date of the latest one.
def last_simulation_date(dir):
    foo = glob.glob(dir + RESTARTDIR + '*.restart')

    restart_dates_present = []
    for fn in foo:
        head, tail = os.path.split(fn)
        restart_dates_present.append(datetime.datetime.strptime(tail[0:10], "%Y-%m-%d"))
    
    restart_dates_present.sort(reverse=True)
    f1 = restart_dates_present[0].date()
    return f1


# Check the restart directory for restart files.
# Return the date of the latest one.
def last_date_of_cbh_files(dir):
    # get the list of CBH files
    foo = glob.glob(dir + INDIR + '*.cbh')
    
    # Read the start, end, and number of features for each CBH file.
    sd = None
    ed = None
    nf = -1
    for fn in foo:
        fp = open(fn, "r")
        comment = fp.readline()
        l = fp.readline()
        tok = l.split()
        var_name = tok[0]
        nfeat = int(tok[1])
        l = fp.readline()
        l = fp.readline()
        tok = l.split()
        start_date = datetime.date(int(tok[0]), int(tok[1]), int(tok[2]))

        for line in fp:
            pass 
        last = line

        tok = last.split()
        end_date = datetime.date(int(tok[0]), int(tok[1]), int(tok[2]))
#        delta = end_date - start_date
#        nts = delta.days + 1
        
        fp.close()
        
        # check that the start dates match
        if sd == None:
            sd = start_date
        else:
            if sd != start_date:
                print('log message: start dates in cbh files do not match')
                return None, None, -1
        
        # check that the end dates match
        if ed == None:
            ed = end_date
        else:
            if ed != end_date:
                print('log message: end dates in cbh files do not match')
                return None, None, -1
            
        # check that the number of features match
        if nf == -1:
            nf = nfeat
        else:
            if nf != nfeat:
                print('log message: number of features in cbh files do not match')
                return None, None, -1
    
    return sd, ed, nf


def compute_pull_dates(restart_date, ced):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    pull_date = yesterday - datetime.timedelta(days=IDAHO_PROVISIONAL_DAYS)
    
    # if the restart date is earlier than the pull date, reset the pull date
    if restart_date < pull_date:
        pull_date = restart_date
        print('log message: pull_date reset to restart_date')
    
    # if the end date of the CBH files is earlier than the pull date,
    # reset the pull date. Assume that the last 60 days of the CBH need to be
    # repulled.
    cbh_repull_date = ced - datetime.timedelta(days=IDAHO_PROVISIONAL_DAYS)
    if cbh_repull_date < pull_date:
        pull_date = cbh_repull_date
        print('log message: pull_date reset to CBH repull date')
        
    return pull_date, yesterday


def main(dir):

    # Determine the date for the last simulation by finding the last restart file
    lsd = last_simulation_date(dir)
    restart_date = lsd + datetime.timedelta(days=1)
    print('last simulation date = ' + lsd.strftime('%Y-%m-%d'))
    print('restart date = ' + restart_date.strftime('%Y-%m-%d'))
    
    # Determine the last date of the CBH files
    csd, ced, cfc = last_date_of_cbh_files(dir)
    if csd:
        print('last date in CBH files ', ced.strftime('%Y-%m-%d'))
        print('feature count in CBH files ', cfc)

    else:
        print('log message: last_date_of_cbh failed.')
        
    # Determine the dates for the data pull
    start_pull_date, end_pull_date = compute_pull_dates(restart_date, ced)
    print('pull period start = ', start_pull_date, ' end = ', end_pull_date)
    
    # Run the Fetcher/Parser to pull available data
    # Rich: assume that the start_pull_date = 2019-06-02 and the
    # end_pull_date = 2019-09-08
    
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