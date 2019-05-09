import subprocess


def main():
    args = "ls -lah".split()
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print output


if __name__ == '__main__':
    main()
    