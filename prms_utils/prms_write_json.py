# Markstrom
# Wed Mar 13 09:43:53 MDT 2019

import json

# PRMS output files
# dir = "/work/markstro/operat/docker_test/NHM-PRMS_CONUS"
dir = "./"
hru_dir = '/work/markstro/intern_demo/GIS_Data/hrus_all_conus_geo.shp'
#seg_dir = '/work/markstro/intern_demo/GIS_Data/segs_all_conus_geo.shp'
#outdir = dir + "/output/"
#indir = dir + "/input/"
#sandbox = dir + "/output/"
outdir = dir + "/out/"
indir = dir + "/in/"
sandbox = dir + "/out/"
#fn = "/work/markstro/operat/setup/stage/stage_1/NHM-PRMS_CONUS/variable_info.json"
fn = "//ssd/markstro/conusStreamTemp/work_lev3/variable_info.json"

data = {
    "tz_code":'-05:00',
    "nc_name":'nhm_conus',
    "cdl_file_name":sandbox + 'nhm_output_example.cdl',
    "ncf_file_name":sandbox + 'nhm_output_example.ncf',

    "output_variables": {
        "soil_moist": {
            "long_name": "Soil moisture content",
            "standard_name": "lwe_thickness_of_moisture_content_of_soil_layer",
            "source": outdir + "nhru_soil_moist_tot.csv",
            "fill_value": "9.969209968386869e+36",
            "format": "%.1f",
            "in_units": "inch",
            "out_units": "mm",
            "conversion_factor": "25.4",
            "prms_out_file": outdir + "nhru_soil_moist_tot.csv",
            "georef": {
                "map": hru_dir,
                "type": 'Polygon',
                "dimid":"hruid",
                "attribute": 'nhm_id'
            }
        },
        "lateral_flow": {
            "long_name": "Lateral flow from HRU into the corresponding stream segment",
            "standard_name": "lateral_flow",
            "source": outdir + "nhru_hru_lateral_flow.csv",
            "fill_value": "9.969209968386869e+36",
            "format": "%.1f",
            "in_units": "inch/day",
            "out_units": "mm/day",
            "conversion_factor": "25.4",
            "prms_out_file": outdir + "nhru_hru_lateral_flow.csv",
            "georef": {
                "map": hru_dir,
                "type": 'Polygon',
                "dimid":"hruid",
                "attribute": 'nhm_id'
            }
        },
#        "streamflow": {
#            "long_name": "Streamflow in channel",
#            "standard_name": "water_volume_transport_in_river_channel",
#            "source": outdir + "nsegment_seg_outflow.csv",
#            "fill_value": "9.969209968386869e+36",
#            "format": "%.1f",
#            "in_units": "ft3/s",
#            "out_units": "m3/s",
#            "conversion_factor": "0.0283168",
#            "prms_out_file": outdir + "nsegment_seg_outflow.csv",
#            "georef": {
#                "map": seg_dir,
#                "type": 'LineString',
#                "dimid":"segid",
#                "attribute": 'nhm_seg'
#            }
#        },
        "pkwater_equiv": {
            "long_name": "Snowpack water equivalent",
            "standard_name": "liquid_water_content_of_surface_snow",
            "source": outdir + "pkwater_equiv.csv",
            "fill_value": "9.969209968386869e+36",
            "format": "%.1f",
            "in_units": "in",
            "out_units": "mm",
            "conversion_factor": "25.4",
            "prms_out_file": outdir + "pkwater_equiv.csv",
            "georef": {
                "map": hru_dir,
                "type": 'Polygon',
                "dimid":"hruid",
                "attribute": 'nhm_id'
            }
        },
        "soil_moist_tot": {
            "long_name": "Total soil-zone water storage (soil_moist + ssres_stor)",
            "standard_name": "lwe_thickness_of_soil_moisture_content",
            "source": outdir + "soil_moist_tot.csv",
            "fill_value": "9.969209968386869e+36",
            "format": "%.1f",
            "in_units": "in",
            "out_units": "mm",
            "conversion_factor": "25.4",
            "prms_out_file": outdir + "soil_moist_tot.csv",
            "georef": {
                "map": hru_dir,
                "type": 'Polygon',
                "dimid":"hruid",
                "attribute": 'nhm_id'
            }
        },
        "hru_intcpstor": {
            "long_name": "HRU area-weighted average Interception storage in the canopy for each HRU",
            "standard_name": "lwe_thickness_of_canopy_water_amount",
            "source": outdir + "hru_intcpstor.csv",
            "fill_value": "9.969209968386869e+36",
            "format": "%.1f",
            "in_units": "in",
            "out_units": "mm",
            "conversion_factor": "25.4",
            "prms_out_file": outdir + "hru_intcpstor.csv",
            "georef": {
                "map": hru_dir,
                "type": 'Polygon',
                "dimid":"hruid",
                "attribute": 'nhm_id'
            }
        },
        "hru_impervstor": {
            "long_name": "HRU area-weighted average storage on impervious area for each HRU",
            "standard_name": "lwe_thickness_of_impervious_area_water_amount",
            "source": outdir + "hru_impervstor.csv",
            "fill_value": "9.969209968386869e+36",
            "format": "%.1f",
            "in_units": "in",
            "out_units": "mm",
            "conversion_factor": "25.4",
            "prms_out_file": outdir + "hru_impervstor.csv",
            "georef": {
                "map": hru_dir,
                "type": 'Polygon',
                "dimid":"hruid",
                "attribute": 'nhm_id'
            }
        },
        "gwres_stor": {
            "long_name": "Storage in each GWR",
            "standard_name": "lwe_thickness_of_groundwater_amount",
            "source": outdir + "gwres_stor.csv",
            "fill_value": "9.969209968386869e+36",
            "format": "%.1f",
            "in_units": "in",
            "out_units": "mm",
            "conversion_factor": "25.4",
            "prms_out_file": outdir + "gwres_stor.csv",
            "georef": {
                "map": hru_dir,
                "type": 'Polygon',
                "dimid":"hruid",
                "attribute": 'nhm_id'
            }
        },
        "dprst_stor_hru": {
            "long_name": "Surface-depression storage for each HRU",
            "standard_name": "lwe_thickness_of_surface-depression_water_amount",
            "source": outdir + "dprst_stor_hru.csv",
            "fill_value": "9.969209968386869e+36",
            "format": "%.1f",
            "in_units": "in",
            "out_units": "mm",
            "conversion_factor": "25.4",
            "prms_out_file": outdir + "dprst_stor_hru.csv",
            "georef": {
                "map": hru_dir,
                "type": 'Polygon',
                "dimid":"hruid",
                "attribute": 'nhm_id'
            }
        },
    },
    "feature_georef": {
        "hru_lat":{
            "file": indir + "hru_lat.txt",
            "dimid":"hruid",
            "long_name": "Latitude of HRU centroid",
            "units":"degrees_north",
            "standard_name": "hru_latitude",
            "fill_value": "9.969209968386869e+36"
        },
        "hru_lon":{
            "file": indir + "hru_lon.txt",
            "dimid":"hruid",
            "long_name": "Longitude of HRU centroid",
            "units":"degrees_east",
            "standard_name": "hru_longitude",
            "fill_value": "9.969209968386869e+36"
        },
#        "seg_lat":{
#            "file": indir + "lat_seg.txt",
#            "dimid":"segid",
#            "long_name": "Latitude of stream segment centroid",
#            "units":"degrees_north",
#            "standard_name": "segment_latitude",
#            "fill_value": "9.969209968386869e+36"
#        },
#        "seg_lon":{
#            "file": indir + "lon_seg.txt",
#            "dimid":"segid",
#            "long_name": "Longitude of stream segment centroid",
#            "units":"degrees_east",
#            "standard_name": "segment_longitude",
#            "fill_value": "9.969209968386869e+36"
#        }
    }
}


def main():
    with open(fn, "w") as write_file:
        json.dump(data, write_file)


if __name__ == '__main__':
    main()
