# Function calls for cbh fillers ( for reference)

``` bash 
srun python /caldera/projects/usgs/water/wbeep/filled_cbh/src/cbh_filler.py /caldera/projects/usgs/water/wbeep/bandit/jobs/2020-04-09_conus_gm/prcp.cbh /caldera/projects/usgs/water/wbeep/filled_cbh/prcp.cbh /caldera/projects/usgs/water/wbeep/filled_cbh/nhm_id.txt /caldera/projects/usgs/water/wbeep/filled_cbh/miss_to_pres_mapping.csv prcp "%.2f" 

srun python /caldera/projects/usgs/water/wbeep/filled_cbh/src/cbh_filler.py /caldera/projects/usgs/water/wbeep/bandit/jobs/2020-04-09_conus_gm/tmax.cbh /caldera/projects/usgs/water/wbeep/filled_cbh/tmax.cbh /caldera/projects/usgs/water/wbeep/filled_cbh/nhm_id.txt /caldera/projects/usgs/water/wbeep/filled_cbh/miss_to_pres_mapping.csv tmax "%.1f"
cbh_filler_prcp.slurm

srun python /caldera/projects/usgs/water/wbeep/filled_cbh/src/cbh_filler.py /caldera/projects/usgs/water/wbeep/bandit/jobs/2020-04-09_conus_gm/tmin.cbh /caldera/projects/usgs/water/wbeep/filled_cbh/tmin.cbh /caldera/projects/usgs/water/wbeep/filled_cbh/nhm_id.txt /caldera/projects/usgs/water/wbeep/filled_cbh/miss_to_pres_mapping.csv tmin "%.1f"

srun python /caldera/projects/usgs/water/wbeep/filled_cbh/src/cbh_humidity_filler.py /caldera/projects/usgs/water/wbeep/bandit/jobs/2020-04-09_conus_gm/humidity.cbh /caldera/projects/usgs/water/wbeep/filled_cbh/humidity.cbh /caldera/projects/usgs/water/wbeep/filled_cbh/nhm_id.txt /caldera/projects/usgs/water/wbeep/filled_cbh/miss_to_pres_mapping.csv humidity "%.1f"
```
