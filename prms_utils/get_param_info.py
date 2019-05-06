import xml.etree.ElementTree
from prms_utils import paramfile
# from prms_utils import get_dim_list

# Global vars
e = None


def get_param_info(pname, pfn):
    global e
    if e is None:
        e = xml.etree.ElementTree.parse(pfn).getroot()

    found = False
    for pa in e.findall('parameter'):
        name = pa.get('name')
        if name == pname:
            units = pa.get('units')
            long_name = pa.get('desc')
            standard_name = pa.get('cf_name')
            type_code = pa.get('type')
            d = pa.get('dims')
            dims =d.split(',')

            found = True
            break

    if not found:
        print 'did not find ', pname

    return long_name, units, standard_name, type_code, dims


def add_attribute_to_all_nodes(pfn):
    # read the parameter file to get dimensions
    ps = paramfile.ParamFile()
    ps.read('/work/markstro/intern_demo/ModelInput/skunk.params')

    tree = xml.etree.ElementTree.parse(pfn)
    e_loc = tree.getroot()

    for pa in e_loc.findall('parameter'):
        name = pa.get('name')

        dim_list = []


        if name in ps.params:
            dim_list = ps.params[name].dims
        elif get_dim_list.input_data(name) is not None:
            dim_list = get_dim_list.input_data(name)
        elif get_dim_list.cbh(name) is not None:
            dim_list = get_dim_list.cbh(name)
        elif get_dim_list.output_var(name) is not None:
            dim_list = get_dim_list.output_var(name)
        else:
            dim_list = None

        if dim_list is not None:
            print name, dim_list
            dim_str = dim_list[0]
            for ii in xrange(1, len(dim_list)):
                dim_str += ',' + dim_list[ii]

            pa.set('dims', dim_str)
        else:
            pa.set('dims', '')

    tree.write(pfn)


if __name__ == '__main__':
    add_attribute_to_all_nodes("/work/markstro/intern_demo/ModelInput/parameters.xml")