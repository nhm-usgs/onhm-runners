from prms_utils import csv_reader
import numpy as np
import datetime

ppt_rad_adj = 0.02
wd = '/work/markstro/alaska/forcings/'


def precip_day():
    fn = wd + 'CFSR_P_mm_daily_geospatial_fabric_v1.csv'
    nts, nfeat, base_date, end_date, prcp = csv_reader.read_output(fn)
    # print(nts, nfeat, base_date, end_date, prcp)

    prcp_day = np.zeros(shape=prcp.shape, dtype=bool)
    for ii in range(nts):
        for jj in range(nfeat):
            if prcp[ii,jj] > ppt_rad_adj:
                prcp_day[ii,jj] = True
            else:
                prcp_day[ii,jj] = False

    # print(prcp_day)
    return prcp_day


def obs_targets():
    # read the solrad data (monthly means)
    fn = wd + 'non_clear_sky_downward_sw_wm2_monthly_mean_geospatial_fabric_v1.csv'
    nts, nfeat, base_date, end_date, obs_solrad = csv_reader.read_monthly_mean(fn)

    # for jj in range(nts):
    #     print(max(obs_solrad[:, jj]))


    # print(base_date, end_date)
    # print(obs_solrad.shape)

    solrad_targets = np.zeros(shape=(12,nfeat), dtype=float)
    solrad_cnts = np.zeros(shape=(12,nfeat), dtype=float)

    current_date = datetime.datetime.strptime(base_date,"%Y-%m-%d")
    for ii in range(nts):
        idx = current_date.month - 1
        for jj in range(nfeat):
            solrad_targets[idx,jj] = solrad_targets[idx,jj] + obs_solrad[ii,jj]
            solrad_cnts[idx,jj] = solrad_cnts[idx,jj] + 1.0

        current_date += datetime.timedelta(days=30.44)

    # print(solrad_targets)

    for ii in range(12):
        for jj in range(nfeat):
            solrad_targets[ii,jj] = solrad_targets[ii,jj] / solrad_cnts[ii,jj]
            # Langley/day = 0.484583 Watt/m2
            solrad_targets[ii, jj] = solrad_targets[ii, jj] / 0.484583

    return solrad_targets


def main():
# For each HRU, for each day, determine if it is a precip day.
    prcp_day = precip_day()
    prcp_day.tofile(wd + 'prcp_day.txt', sep=",", format="%d")

# For each HRU, for each month (12 values total => monthly means) compute the observed targets.
    solrad_targets = obs_targets()
    solrad_targets.tofile(wd + 'solrad_targets_ly.txt', sep=",", format="%.1f")


if __name__ == '__main__':
    main()