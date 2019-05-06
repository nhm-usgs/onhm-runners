import numpy
import re
from parameter import Parameter


class ParamFile:
    def __init__(self):
        # dims is a dictionary where the name is the key and the value is the integer size
        self.dims = {}
        # params is a dictionary where the name is the key and the value is a Parameter() object
        self.params = {}
        # line1 is the first line of the parameter file
        self.line1 = ""
        # line2 is the second line of the parameter file
        self.line2 = ""
        self.file_name = ""

    def read(self, pfn):
        fp = open(pfn, "r")
        self.file_name = pfn
        self.line1 = fp.readline()
        self.line2 = fp.readline()

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
            p = Parameter()
            name = fp.readline().strip()
            p.name = name

            num_dim = int(fp.readline().strip())
            d = []
            for ii in xrange(num_dim):
                d.append(fp.readline().strip())
            p.dims = d

            num_vals = int(fp.readline().strip())
            type_t = int(fp.readline().strip())
            p.type_code = type_t

            v = []
            for ii in xrange(num_vals):
                if type_t == 1:
                    v.append(int(fp.readline().strip()))
                elif type_t == 2:
                    v.append(float(fp.readline().strip()))
                else:
                    v.append(fp.readline().strip())
            p.vals = v

            self.params[name] = p

            delim = fp.readline().strip()

    def write(self, pfn):
        fp = open(pfn, "w")
        fp.write(self.line1)
        fp.write(self.line2)

        # write the dimensions part
        fp.write("** Dimensions **\n")
        for key in self.dims:
            fp.write("####\n")
            fp.write(key + '\n')
            fp.write(str(self.dims[key]) + '\n')

        # write the parameters part
        fp.write("** Parameters **\n")
        for key in self.params:
            param = self.params[key]

            fp.write("####\n")
            fp.write(key + '\n')
            fp.write(str(len(param.dims)) + '\n')
            for dim in param.dims:
                fp.write(dim + '\n')
            fp.write(str(len(param.vals)) + '\n')
            fp.write(str(param.type_code) + '\n')

            # print "paramfile " + key + " type_code " + str(param.type_code)

            if param.type_code == 1:
                # write int
                for val in param.vals:
                    fp.write(str(int(val)) + '\n')
                    # print str(int(val))

            elif param.type_code == 2:
                # write float
                for val in param.vals:
                    fp.write(str(val) + '\n')

            elif param.type_code == 3:
                # write double?
                for val in param.vals:
                    fp.write(str(val) + '\n')

            elif param.type_code == 4:
                # write string?
                for val in param.vals:
                    fp.write(str(val) + '\n')

        fp.close()

    def get_param_vals(self, name):
        return self.params[name]

    def get_dim_size(self, name):
        if name in self.dims:
            return self.dims[name]
        else:
            return -1

    def update_param_value(self, param_name, new_mean, lo, hi):
        # if parameter name ends in _## then this is an index optimization
        result = re.search(r'_\d+$', param_name)

        # if the string ends in digits m will be a Match object, or None otherwise.
        if result is not None:
            # get the index
            m = re.search(r'\d+$', param_name)
            ii = int(m.group())
            # print str(ii)

            # get the parameter base name without index
            base = re.sub(result.group(), '', param_name)
            # print base


            # get the list of param values from file
            p = self.get_param_vals(base)
            params = p.vals

            if new_mean > hi:
                params[ii-1] = hi
            elif new_mean < lo:
                params[ii - 1] = lo
            else:
                params[ii - 1] = new_mean

            p.vals = params

        else:
            # This will set all of the values of array to single value
            # get the list of param values from file
            p = self.get_param_vals(param_name)
            params = p.vals

            # mean of parameter values across all dimensions
            mean = numpy.mean(params)

            # list of parameter values as their difference from the overall mean
            dev_from_mean = params - mean

            # normalize the parameter values based on the range from the mean to the max
            # and from the mean to the min depending on whether the individual value is
            # above or below the mean.
            proportion = []
            for ii in xrange(len(params)):
                if dev_from_mean[ii] > 0.0:
                    proportion.append(dev_from_mean[ii] / (hi - mean))
                else:
                    proportion.append(-1.0 * dev_from_mean[ii] / (lo - mean))

            # redistribute the values based on proportion and the "new" parameter value
            new_params = []
            print len(proportion)
            for ii in xrange(len(proportion)):
                if proportion[ii] > 0.0:
                    new_params.append(proportion[ii] * (hi - new_mean) + new_mean)
                else:
                    new_params.append(-1.0 * proportion[ii] * (lo - new_mean) + new_mean)

            # print params
            # print new_params
            p.vals = new_params


if __name__ == '__main__':
    ps = ParamFile()
    ps.read("D:/backedUp/applications/skunk_river_model_for_paper/runs/skunk_prms_foobar/input/skunk.params")

# args are name of parameter, new value, minimum, maximum
#     ps.update_param_value("lat_temp_adj_1", 0.1, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_2", 0.2, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_3", 0.3, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_4", 0.4, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_5", 0.5, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_6", 0.6, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_7", 0.7, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_8", 0.8, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_9", 0.9, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_10", 1.0, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_11", 1.1, -4.0, 4.0)
#     ps.update_param_value("lat_temp_adj_12", 1.2, -4.0, 4.0)

    ps.update_param_value("lat_temp_adj", 2.5, -4.0, 4.0)

    ps.write("D:/backedUp/applications/skunk_river_model_for_paper/runs/skunk_prms_foobar/input/foobar.params")