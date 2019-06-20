import datetime
import urllib


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def download_nwis_stream_flow(gage_id, fn):
    print ("Going to NWIS web services for gage " + gage_id)

    # get the start and end date of the data
    param = '00060'
    stat = '00003'
    start = '1851-01-01'
    now = datetime.datetime.now()
    end = now.strftime("%Y-%m-%d")
    url = 'http://waterservices.usgs.gov/nwis/dv?site=' + gage_id +\
          '&parameterCd=' + param + '&statCd=' + stat + '&startDt=' + start + '&endDt=' + end

    print(url)
    print(fn)
    urllib.urlretrieve(url, fn)


def parse_stream_flow_xml(wd, gi, quals, ns):
    dt = []
    val = []

    fn = wd + '/download/' + gi + '.xml'
    tree = ET.parse(fn)
    root = tree.getroot()

    foobar = root.findall('*/*/{' + ns + '}value')
    for foo in foobar:
        if foo.get('qualifiers') in quals:
            f1 = foo.get('dateTime').strip()
            dt.append(datetime.datetime(int(f1[0:4]), int(f1[5:7]), int(f1[8:10]), 0, 0, 0, 0))
            val.append(float(foo.text.strip()))

    return dt, val