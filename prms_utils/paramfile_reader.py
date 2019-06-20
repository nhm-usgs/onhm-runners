# import numpy as np
# import datetime


class paramfile:
    def __init__(self):
        self.dims = {}
        self.params = {}

    def read(self, pfn):
        fp = open(pfn, "r")
        line1 = fp.readline()
        line2 = fp.readline()

        # read the dimensions part
        fp.readline()
        delim = fp.readline()

        while delim != "** Parameters **":
            dim = fp.readline().strip()
            size = int(fp.readline().strip())
            self.dims[dim] = size
            delim = fp.readline().strip()

        delim = fp.readline().strip()
        while delim:
            param = fp.readline().strip()
            num_dim = int(fp.readline().strip())
            d = []
            for ii in range(num_dim):
                d.append(fp.readline().strip())
            num_vals = int(fp.readline().strip())
            type = int(fp.readline().strip())
            v = []
            for ii in range(num_vals):
                if type == 1:
                    v.append(int(fp.readline().strip()))
                elif type == 2:
                    v.append(float(fp.readline().strip()))
                else:
                    v.append(fp.readline().strip())

            self.params[param] = v

            delim = fp.readline().strip()

    def get_param_vals(self, name):
        return self.params[name]

    def get_dim_size(self, name):
        return self.dims[name]
