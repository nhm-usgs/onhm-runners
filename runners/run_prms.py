import subprocess


def make_init_file(st, et, prms_path, work_dir, init_flag, save_flag, control_file, init_file):
    tok = st.split('-')
    start_args = ' -set start_time ' + str(tok[0]) + ',' + str(tok[1]) + ',' + str(tok[2]) + ',0,0,0'
    tok = et.split('-')
    end_args = ' -set end_time ' + str(tok[0]) + ',' + str(tok[1]) + ',' + str(tok[2]) + ',0,0,0'

    if init_flag:
        init_vars_from_file = ' -set init_vars_from_file 1'
        var_init_file = ' -set var_init_file ' + init_file
    else:
        init_vars_from_file = ' -set init_vars_from_file 0'
        var_init_file = ''

    if save_flag:
        save_vars_to_file = ' -set save_vars_to_file 1'
        var_save_file = ' -set var_save_file prms_save_' + st + '_' + et + '.restart'
    else:
        save_vars_to_file = ' -set save_vars_to_file 0'
        var_save_file = ''

    control_arg = ' -C ' + control_file

    args = prms_path + start_args + end_args + init_vars_from_file + var_save_file + var_init_file +\
           save_vars_to_file + control_arg

    print(args)

    popen = subprocess.Popen(args.split(), stdout=subprocess.PIPE, cwd=work_dir)
    popen.wait()
    output = popen.stdout.read()
    print(output)


def main():
    work_dir = '/work/markstro/operat/docker_test/NHM-PRMS_CONUS'
    prms_path = '/work/markstro/operat/src/prms/prms/prms'
    control_file = './NHM-PRMS.control'

    # Test 1 - run straight through with no init or save
    # start_time = "1980-10-1"
    # end_time = "1981-9-30"
    # init_flag = False
    # save_flag = False
    # init_file = None
    # make_init_file(start_time, end_time, prms_path, work_dir, init_flag, save_flag, control_file, init_file)

    # Test 2 - run through and save
    # start_time = "1980-10-1"
    # end_time = "1981-9-30"
    # init_flag = False
    # save_flag = True
    # init_file = None
    # make_init_file(start_time, end_time, prms_path, work_dir, init_flag, save_flag, control_file, init_file)

    # Test 3 - init with the file made in Test 2 and run through and save. Compare the output from this to
    # the output of test 1 and they should be different (and they are).
    # start_time = "1980-10-1"
    # end_time = "1981-9-30"
    # init_flag = True
    # save_flag = False
    # init_file = 'prms_save_1980-10-1_1981-9-30.restart'
    # make_init_file(start_time, end_time, prms_path, work_dir, init_flag, save_flag, control_file, init_file)

    # Test 4 - run for the first half and save. Initialize a run of the second half with the save file created
    # by the first half and compare to the output from Test 1. Don't just run a diff on the output files because
    # the dates don't match line by line. In other words, make sure that only lines with the same dates are compared.
    start_time = "1980-10-1"
    end_time = "1981-4-1"
    init_flag = False
    save_flag = True
    init_file = None
    make_init_file(start_time, end_time, prms_path, work_dir, init_flag, save_flag, control_file, init_file)

    start_time = "1981-4-2"
    end_time = "1981-9-30"
    init_flag = True
    save_flag = False
    init_file = 'prms_save_1980-10-1_1981-4-1cd cd.restart'
    make_init_file(start_time, end_time, prms_path, work_dir, init_flag, save_flag, control_file, init_file)


if __name__ == '__main__':
    main()
