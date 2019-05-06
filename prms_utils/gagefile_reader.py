import numpy as np
import csv
import datetime

def read(fn):
    num_lines = sum(1 for line in open(fn)) - 1

    # allocate the arrays numpy.ndarray
    dates = np.empty([num_lines], dtype=datetime.datetime)
    data = np.empty([num_lines], dtype=float)

    ii = 0
    with open(fn, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # skip header row
        for row in reader:
            # print row[0][0:4], "|", row[0][5:7], "|", row[0][8:10], "\n"
            foo = datetime.datetime(int(row[0][0:4]), int(row[0][5:7]), int(row[0][8:10]))
            # print foo
            if foo is not None:
                dates[ii] = foo
                data[ii] = float(row[1])
                ii += 1

    return data, dates
