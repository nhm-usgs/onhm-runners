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
import subprocess

# These are onhm modules
import run_prms
import prms_verifier
import prms_outputs2_ncf
import ncf2cbh

RESTARTDIR = 'restart/'
INDIR = 'input/'
OUTDIR = 'output/'
GRIDMET_PROVISIONAL_DAYS = 59
PRMSPATH = '/work/markstro/operat/repos/prms/prms/prms'
WORKDIR = '/work/markstro/operat/setup/test/NHM-PRMS_CONUS/'
CONTROLPATH = './NHM-PRMS.control'
PRMSLOGPATH = './prms.log'
MAKERSPACE = ['dprst_stor_hru','gwres_stor','hru_impervstor','hru_intcpstor',
            'pkwater_equiv','soil_moist_tot']

# This one will probably need to change
FPWRITEDIR = WORKDIR

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
    pull_date = yesterday - datetime.timedelta(days=GRIDMET_PROVISIONAL_DAYS)
    
    # if the restart date is earlier than the pull date, reset the pull date
    if restart_date < pull_date:
        pull_date = restart_date
        print('log message: pull_date reset to restart_date')
    
    # if the end date of the CBH files is earlier than the pull date,
    # reset the pull date. Assume that the last 60 days of the CBH need to be
    # repulled.
    if ced:
        cbh_repull_date = ced - datetime.timedelta(days=GRIDMET_PROVISIONAL_DAYS)
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
    print('foo', restart_date, ced)
    start_pull_date, end_pull_date = compute_pull_dates(restart_date, ced)
    print('pull period start = ', start_pull_date, ' end = ', end_pull_date)
    
    # Run the Fetcher/Parser to pull available data
    # RMCD: Note sure this works, I imagine this would be the call to make over-riding
    # the START_DATE and END_DATE ENV variables setup in the nhmusgs-ofp Dockerfile
    sformat = "%Y-%m-%d"
    str_start_pull_date = start_pull_date.strftime(sformat)
    str_end_pull_date = end_pull_date.strftime(sformat)
    # START_DATE and END_DATE are ENV variables in nhmusgs-ofp Docker file we over-ride with -e option
    ofp_docker_cmd = f"docker run ofp -e START_DATE={str_start_pull_date} END_DATE={str_end_pull_date}"
    with open("ofp_log.log", "a") as output:
        subprocess.call(ofp_docker_cmd, stdout=output, stderr=output)

    
    # Add/overwrite the CBH files with the new Fetcher/Parser data
    #
    # Note that "_" are used instead of "-" in the date name.
    # end_pull_date.strftime('%Y_%m_%d')
    nc_fn = FPWRITEDIR + 'climate_' + end_pull_date.strftime('%Y_%m_%d') + '.nc'
    ncf2cbh.run(dir + INDIR, nc_fn)
    
    # Figure out the run period for PRMS. It should usually be from one day
    # past the date of the restart file through yesterday.
    # This is a hack until FP code is in here and CBH files are updated
    start_prms_date = datetime.date(2019, 6, 2)
    end_prms_date = datetime.date(2019, 7, 31)
    print(start_prms_date.strftime('%Y-%m-%d'), end_prms_date.strftime('%Y-%m-%d'))

    # Remove the verification file before running PRMS.
    foo = glob.glob(dir + 'PRMS_VERIFIED_*')
    for f in foo:
        print(f)
        os.remove(f)
    
    # Run PRMS for the prescribed period.
    # st, et, prms_path, work_dir, init_flag, save_flag, control_file, init_file, save_file
    init_file = RESTARTDIR + lsd.strftime('%Y-%m-%d') + '.restart'
    save_file = RESTARTDIR + end_prms_date.strftime('%Y-%m-%d') + '.restart'
    
    run_prms.run(start_prms_date.strftime('%Y-%m-%d'),
                 end_prms_date.strftime('%Y-%m-%d'), PRMSPATH, dir, True, True,
                 CONTROLPATH, init_file, save_file, PRMSLOGPATH)
    
    # Verify that PRMS ran correctly.
    # args: work_dir, fname, min_time
    ret_code = prms_verifier.main(dir, "prms.out", 1)
    if ret_code == 0:
        print('PRMS run verified')
    else:
        print('PRMS run failed')
    
    # Create ncf files from the output csv files (one for each output variable).
    if !ret_code:
        prms_outputs2_ncf.write_ncf(dir, MAKERSPACE)
    
    # Copy these nc files (made in the previous step) to the s3 area.
    
    # TODO: The previous step wrote 6 .nc files in dir + OUTDIR  These files
    # need to be moved to the S3 storage for the Makerspace visualization.


if __name__ == '__main__':
    argc = len(sys.argv) - 1
    # print(argc)

    if argc == 1:
        print('setting dir = ' + sys.argv[1])
        dir = sys.argv[1]
    else:
        dir='/var/lib/nhm/NHM-PRMS_CONUS/'
        
    dir = WORKDIR
    main(dir)