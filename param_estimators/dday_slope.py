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

# def compute_soltab(Obliquity, Solar_declination, Slope, Aspect, Latitude, Cossl, Soltab, Sunhrs, Hru_type, Id):
#     sl = ATAN(Slope)
#     Cossl = COS(sl)
#     a = Aspect*RADIANS
#
# # x0 latitude of HRU
#     x0 = Latitude*RADIANS
#
# # x1 latitude of equivalent slope
# # This is equation 13 from Lee, 1963
#     x1 = ASIN(Cossl*SIN(x0)+SIN(sl)*COS(x0)*COS(a))
#
# # d1 is the denominator of equation 12, Lee, 1963
#     d1 = Cossl*COS(x0) - SIN(sl)*SIN(x0)*COS(a)
#     IF ( ABS(d1)<DNEARZERO ) d1 = DNEARZERO
#
# # x2 is the difference in longitude between the location of
# # the HRU and the equivalent horizontal surface expressed in angle hour
# # This is equation 12 from Lee, 1963
#     x2 = ATAN(SIN(sl)*SIN(a)/d1)
#     IF ( d1<0.0D0 ) x2 = x2 + PI
#
# # r0 is the minute solar constant cal/cm2/min
#     r0 = 2.0D0
# # r0 could be 1.95 (Drummond, et al 1968)
#     DO jd = 1, 366
#         d = Solar_declination(jd)
#
# # This is adjusted to express the variability of available insolation as
# # a function of the earth-sun distance.  Lee, 1963, p 16.
# # r1 is the hour solar constant cal/cm2/hour
# # r0 is the minute solar constant cal/cm2/min
# # 60.0D0 is minutes in an hour
# # Obliquity is the obliquity of the ellipse of the earth's orbit around the sun. E
# # is also called the radius vector of the sun (or earth) and is the ratio of
# # the earth-sun distance on a day to the mean earth-sun distance.
# # obliquity = ~23.439 (obliquity of sun)
#         r1 = 60.0D0*r0/(Obliquity(jd)*Obliquity(jd))
# #  compute_t is the sunrise equation.
# #  t7 is the hour angle of sunset on the equivalent slope
# #  t6 is the hour angle of sunrise on the equivalent slope
#         CALL compute_t(x1, d, t)
#         t7 = t - x2
#         t6 = -t - x2
#
# #  compute_t is the sunrise equation.
# #  t1 is the hour angle of sunset on a hroizontal surface at the HRU
# #  t0 is the hour angle of sunrise on a hroizontal surface at the HRU
#         CALL compute_t(x0, d, t)
#         t1 = t
#         t0 = -t
#
# # For HRUs that have an east or west direction component to their aspect, the
# # longitude adjustment (moving the effective slope east or west) will cause either:
# # (1) sunrise to be earlier than at the horizontal plane at the HRU
# # (2) sunset to be later than at the horizontal plane at the HRU
# # This is not possible. The if statements below check for this and adjust the
# # sunrise/sunset angle hours on the equivalent slopes as necessary.
# #
# # t3 is the hour angle of sunrise on the slope at the HRU
# # t2 is the hour angle of sunset on the slope at the HRU
#         IF ( t7>t1 ) THEN
#           t3 = t1
#         ELSE
#           t3 = t7
#         ENDIF
#         IF ( t6<t0 ) THEN
#           t2 = t0
#         ELSE
#           t2 = t6
#         ENDIF
#
#         IF ( ABS(sl)<DNEARZERO ) THEN
# #  solt is Swift's R4 (potential solar radiation on a sloping surface cal/cm2/day)
# #  Swift, 1976, equation 6
#           solt = func3(0.0D0, x0, t1, t0, r1, d)
# #  sunh is the number of hours of direct sunlight (sunset minus sunrise) converted
# #  from angle hours in radians to hours (24 hours in a day divided by 2 pi radians
# #  in a day).
#           sunh = (t1-t0)*PI_12
#         ELSE
#           IF ( t3<t2 ) THEN
#             t2 = 0.0D0
#             t3 = 0.0D0
#           ENDIF
#           t6 = t6 + TWOPI
#           IF ( t6<t1 ) THEN
#             solt = func3(x2, x1, t3, t2, r1, d) + func3(x2, x1, t1, t6, r1, d)
#             sunh = (t3-t2+t1-t6)*PI_12
#           ELSE
#             t7 = t7 - TWOPI
#             IF ( t7>t0 ) THEN
#               solt = func3(x2, x1, t3, t2, r1, d) + func3(x2, x1, t7, t0, r1, d)
#               sunh = (t3-t2+t7-t0)*PI_12
# ELSE
#             t7 = t7 - TWOPI
#             IF ( t7>t0 ) THEN
#               solt = func3(x2, x1, t3, t2, r1, d) + func3(x2, x1, t7, t0, r1, d)
#               sunh = (t3-t2+t7-t0)*PI_12
#             ELSE
#               solt = func3(x2, x1, t3, t2, r1, d)
#               sunh = (t3-t2)*PI_12
#             ENDIF
#           ENDIF
#         ENDIF
#         IF ( solt<0.0D0 ) THEN
#           PRINT *, 'WARNING: solar table value for day:', jd, &
#      &             ' computed as:', solt, ' set to', 0.0, &
#      &             ' for HRU:', Id, ' hru_type:', Hru_type
#           PRINT *, 'slope, aspect, latitude, cossl', Slope, Aspect, Latitude, Cossl
#           solt = 0.0D0
#           PRINT *, Slope, Aspect, Latitude, Cossl, sunh
#           PRINT *, t0, t1, t2, t3, t6, t7, d
#         ENDIF

def main():
# For each HRU, for each day, determine if it is a precip day.
    prcp_day = precip_day()
    prcp_day.tofile(wd + 'prcp_day.txt', sep=",", format="%d")

# For each HRU, for each month (12 values total => monthly means) compute the observed targets.
    solrad_targets = obs_targets()
    solrad_targets.tofile(wd + 'solrad_targets_ly.txt', sep=",", format="%.1f")

    # compute_soltab(obliquity, Solar_declination, Hru_slope(n), Hru_aspect(n),
    #      &                      Hru_lat(n), Hru_cossl(n), Soltab_potsw(1, n),
    #      &                      Soltab_sunhrs(1, n), Hru_type(n), n)

if __name__ == '__main__':
    main()