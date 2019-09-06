# 2019-09-06
# markstro
#
# This is the run time controller for the ONHM.

def main():

    # Determine when the last run was made by finding the last init file
    
    # Determine the last date of the historical CBH

if __name__ == '__main__':
    work_dir = '/var/lib/nhm/NHM-PRMS_CONUS/'

    argc = len(sys.argv) - 1
    # print(argc)

    if argc == 1:
        print('setting dir = ' + sys.argv[1])
        dir = sys.argv[1]
    else:
        dir='/var/lib/nhm/ofp/Output/'