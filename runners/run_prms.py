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
        var_save_file = ' -set prms_save_' + st + '-' + et + '.restart'
    else:
        save_vars_to_file = ' -set save_vars_to_file 0'
        var_save_file = ''

    control_arg = ' -C ' + control_file

    args = prms_path + start_args + end_args + init_vars_from_file + var_save_file + var_init_file +\
           save_vars_to_file + control_arg
    popen = subprocess.Popen(args.split(), stdout=subprocess.PIPE, cwd=work_dir)
    popen.wait()
    output = popen.stdout.read()
    print output

def main():
#     latest test
    work_dir = '/work/markstro/operat/docker_test/NHM-PRMS_CONUS'
    prms_path = '/work/markstro/operat/src/prms/prms/prms'
    control_file = './NHM-PRMS.control'
    start_time = "1980-10-1"
    end_time = "1981-9-30"
    init_flag = False
    save_flag = False
    init_file = 'prms_save_1980-10-1_1981-9-30.restart'

    make_init_file(start_time, end_time, prms_path, work_dir, init_flag, save_flag, control_file, init_file)


if __name__ == '__main__':
    main()
