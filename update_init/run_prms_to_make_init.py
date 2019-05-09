import subprocess

working_dir = '/work/markstro/operat/docker_test/NHM-PRMS_CONUS'
prms_path = '/work/markstro/operat/src/prms/prms/prms'
control_file = ' -C ./NHM-PRMS.control'


def main():
    # a1 = 'cd ' + working_dir + ';' + prms_path
    a1 = prms_path + control_file

    args = a1.split()
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=working_dir)

    popen.wait()
    output = popen.stdout.read()
    print output


if __name__ == '__main__':
    main()
    