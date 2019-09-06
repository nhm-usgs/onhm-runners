# 2019-09-06
# markstro
#
# This is the run time controller for the ONHM. This can be run everyday or
# whenever it is needed to update to the "current state".

def main():

    # Determine when the last run was made by finding the last init file
    
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
    # so as to be ready for the next run (usuall tomorrow).


if __name__ == '__main__':
    work_dir = '/var/lib/nhm/NHM-PRMS_CONUS/'

    argc = len(sys.argv) - 1
    # print(argc)

    if argc == 1:
        print('setting dir = ' + sys.argv[1])
        dir = sys.argv[1]
    else:
        dir='/var/lib/nhm/ofp/Output/'
        
    main()