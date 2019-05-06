def get_dim_list_for_cbh(key):
    if key == 'humidity_hru':
        foo_dim = ['time', 'nhru']
    elif key == 'tmaxf':
        foo_dim = ['time', 'nhru']
    elif key == 'tminf':
        foo_dim = ['time', 'nhru']
    elif key == 'hru_ppt':
        foo_dim = ['time', 'nhru']
    elif key == 'potet':
        foo_dim = ['time', 'nhru']
    elif key == 'swrad':
        foo_dim = ['time', 'nhru']
    elif key == 'transp_on':
        foo_dim = ['time', 'nhru']
    elif key == 'transp_on':
        foo_dim = ['time', 'nhru']
    elif key == 'windspeed_hru':
        foo_dim = ['time', 'nhru']
    else:
        foo_dim = None

    return foo_dim