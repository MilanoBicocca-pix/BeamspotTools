import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

import matplotlib

times = [
    'year 2010, month 3, day 1',
    'year 2010, month 4, day 1',
    'year 2010, month 5, day 1',
    'year 2010, month 6, day 1',
    'year 2010, month 7, day 1',
    'year 2010, month 8, day 1',
    'year 2010, month 9, day 1',
    'year 2010, month 10, day 1',
    'year 2011, month 3, day 1',
    'year 2011, month 4, day 1',
    'year 2011, month 5, day 1',
    'year 2011, month 6, day 1',
    'year 2011, month 7, day 1',
    'year 2011, month 8, day 1',
    'year 2011, month 9, day 1',
    'year 2011, month 10, day 1',
    'year 2012, month 4, day 1',
    'year 2012, month 5, day 1',
    'year 2012, month 6, day 1',
    'year 2012, month 7, day 1',
    'year 2012, month 8, day 1',
    'year 2012, month 9, day 1',
    'year 2012, month 10, day 1',
    'year 2012, month 11, day 1',
    'year 2012, month 12, day 1',
    'year 2015, month 7, day 1',
    'year 2015, month 8, day 1',
    'year 2015, month 9, day 1',
    'year 2015, month 10, day 1',
    'year 2015, month 11, day 1',
    'year 2016, month 5, day 1',
    'year 2016, month 6, day 1',
    'year 2016, month 7, day 1',
    'year 2016, month 8, day 1',
    'year 2016, month 9, day 1',
    'year 2016, month 10, day 1',
    'year 2017, month 6, day 1',
    'year 2017, month 7, day 1',
    'year 2017, month 8, day 1',
    'year 2017, month 9, day 1',
    'year 2017, month 10, day 1',
    'year 2017, month 11, day 1',
    'year 2018, month 4, day 1',
    'year 2018, month 5, day 1',
    'year 2018, month 6, day 1',
    'year 2018, month 7, day 1',
    'year 2018, month 8, day 1',
    'year 2018, month 9, day 1',
    'year 2018, month 10, day 1',
    'year 2018, month 11, day 1',
    'year 2021, month 10, day 1',
    'year 2021, month 11, day 1',
    'year 2022, month 5, day 1',
    'year 2022, month 6, day 1',
    'year 2022, month 7, day 1',
    'year 2022, month 8, day 1',
    'year 2022, month 9, day 1',
    'year 2022, month 10, day 1',
    'year 2022, month 11, day 1',
    'year 2023, month 4, day 1',
    'year 2023, month 5, day 1',
    'year 2023, month 6, day 1',
    'year 2023, month 7, day 1',
    'year 2023, month 9, day 1',
    'year 2024, month 3, day 21',
    'year 2024, month 4, day 1',
    'year 2024, month 4, day 5'
]

Time = [datetime.strptime(time,"year 20%y, month %m, day %d") for time in times ]

X = np.array([
    0.094127, 
    0.097010, 
    0.094673, 
    0.095701, 
    0.096137, 
    0.091765, 
    0.094011, 
    0.095973, 
    0.077830, 
    0.073874, 
    0.073432, 
    0.073288, 
    0.070135, 
    0.069991, 
    0.075499, 
    0.075489, 
    0.073277, 
    0.072273, 
    0.071984, 
    0.071005, 
    0.070873, 
    0.069778, 
    0.069772, 
    0.069930, 
    0.069043, 
    0.076854, 
    0.076299, 
    0.076813, 
    0.077053, 
    0.077149, 
    0.064871, 
    0.063223, 
    0.058485, 
    0.058380, 
    0.057529, 
    0.055517, 
    0.085308,
    0.084399,
    0.084372,
    0.083874,
    0.084294,
    0.082513,
    0.096250,
    0.096432,
    0.097094,
    0.095590,
    0.096508,
    0.096190,
    0.096331,
    0.094505,
    0.171753,#2021
    0.172607,
    0.173003,#2022
    0.171824,
    0.173472,
    0.172803,
    0.174092,
    0.174249,
    0.172679,
    0.115344,#2023
    0.116808,
    0.117166,
    0.116243,
    0.112538,
    0.136365, #2024
    0.131317,
    0.095503
])

Y = np.array([
    0.000908, 
    0.000927, 
    0.006213, 
    0.007750, 
    0.008886, 
    0.018286, 
    0.016824, 
    0.016994, 
    0.028115, 
    0.031726, 
    0.033203, 
    0.035653, 
    0.041351, 
    0.042480, 
    0.040658, 
    0.041007, 
    0.056441, 
    0.061710, 
    0.063612, 
    0.060969, 
    0.063639, 
    0.063423, 
    0.062735, 
    0.062511, 
    0.062314, 
    0.093296, 
    0.094735, 
    0.091153, 
    0.092204, 
    0.094503, 
    0.094045, 
    0.098545, 
    0.101528, 
    0.101729, 
    0.105664, 
    0.107506, 
    -0.034577,
    -0.033694,
    -0.032571,
    -0.031999,
    -0.029872,
    -0.028903,
    -0.069063,
    -0.066068,
    -0.064077,
    -0.064396,
    -0.060965,
    -0.062271,
    -0.061833,
    -0.063482,
    -0.190651,#2021
    -0.192080,
    -0.181755,#2022
    -0.180038,
    -0.181012,
    -0.182373,
    -0.183440,
    -0.183659,
    -0.183023,
    -0.188842,#2023
    -0.186396,
    -0.183765,
    -0.181976,
    -0.186970,
    -0.197122, #2024
    -0.195124,
    -0.195209
])

# convert from cm to micron
#X = X*1.e4
#Y = Y*1.e4

# convert from cm to mm
X = X*1.e1
Y = Y*1.e1

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()

fig.autofmt_xdate()
plt.plot(Time,X, c='tab:blue')
plt.plot(Time,Y, c='tab:green')
plt.scatter(Time,X, c='b', s=40, lw = 0, label='X')
plt.scatter(Time,Y, c='g', s=40, lw = 0, label='Y', marker="s")
# plt.legend((X.all(),Y.all()), ('X','Y'), loc=3)
# plt.legend(bbox_to_anchor=(0.8, 1.02, 1., .102), loc=3,
plt.legend(loc=3, scatterpoints=1)
plt.xlabel('Date')
plt.ylabel('Beam spot centre coordinate [mm]')
plt.title(r'$\bf{CMS}\:\it{Preliminary}$',loc='left',fontname='Nimbus Sans')
plt.xticks(rotation = 0, ha='center')
# fit with np.polyfit
# m, b = np.polyfit(Time, Y, 1)
# plt.plot(x, m*x + b, '-', c='g')
# plt.show()
plt.savefig('cms_beamspotXY_vs_time_2024_April_v2.pdf')
plt.savefig('cms_beamspotXY_vs_time_2024_April_v2.png')
plt.close()


# year 2010, month 3	X = 0.094127 +/- 1.6812E-05 [cm]	Y = 0.000908 +/- 1.6740E-05 [cm]
# year 2010, month 4	X = 0.097010 +/- 1.4807E-06 [cm]	Y = 0.000927 +/- 1.4767E-06 [cm]
# year 2010, month 5	X = 0.094673 +/- 7.4104E-07 [cm]	Y = 0.006213 +/- 7.4049E-07 [cm]
# year 2010, month 6	X = 0.095701 +/- 2.4302E-06 [cm]	Y = 0.007750 +/- 2.4570E-06 [cm]
# year 2010, month 7	X = 0.096137 +/- 1.4521E-06 [cm]	Y = 0.008886 +/- 1.4675E-06 [cm]
# year 2010, month 8	X = 0.091765 +/- 8.1333E-07 [cm]	Y = 0.018286 +/- 8.2139E-07 [cm]
# year 2010, month 9	X = 0.094011 +/- 1.8261E-06 [cm]	Y = 0.016824 +/- 1.8576E-06 [cm]
# year 2010, month 10	X = 0.095973 +/- 1.4924E-06 [cm]	Y = 0.016994 +/- 1.5119E-06 [cm]
# year 2011, month 3	X = 0.077830 +/- 9.9305E-07 [cm]	Y = 0.028115 +/- 9.9116E-07 [cm]
# year 2011, month 4	X = 0.073874 +/- 7.7686E-07 [cm]	Y = 0.031726 +/- 7.7852E-07 [cm]
# year 2011, month 5	X = 0.073432 +/- 6.9384E-07 [cm]	Y = 0.033203 +/- 6.9257E-07 [cm]
# year 2011, month 6	X = 0.073288 +/- 4.6439E-07 [cm]	Y = 0.035653 +/- 4.6361E-07 [cm]
# year 2011, month 7	X = 0.070135 +/- 8.7669E-07 [cm]	Y = 0.041351 +/- 8.7235E-07 [cm]
# year 2011, month 8	X = 0.069991 +/- 1.2090E-06 [cm]	Y = 0.042480 +/- 1.2034E-06 [cm]
# year 2011, month 9	X = 0.075499 +/- 4.9409E-07 [cm]	Y = 0.040658 +/- 4.9167E-07 [cm]
# year 2011, month 10	X = 0.075489 +/- 4.4468E-07 [cm]	Y = 0.041007 +/- 4.4240E-07 [cm]
# year 2012, month 4	X = 0.073277 +/- 4.1297E-07 [cm]	Y = 0.056441 +/- 4.1600E-07 [cm]
# year 2012, month 5	X = 0.072273 +/- 4.4371E-07 [cm]	Y = 0.061710 +/- 4.4601E-07 [cm]
# year 2012, month 6	X = 0.071984 +/- 4.7545E-07 [cm]	Y = 0.063612 +/- 4.7791E-07 [cm]
# year 2012, month 7	X = 0.071005 +/- 4.5817E-07 [cm]	Y = 0.060969 +/- 4.6010E-07 [cm]
# year 2012, month 8	X = 0.070873 +/- 4.4563E-07 [cm]	Y = 0.063639 +/- 4.4742E-07 [cm]
# year 2012, month 9	X = 0.069778 +/- 5.6908E-07 [cm]	Y = 0.063423 +/- 5.7218E-07 [cm]
# year 2012, month 10	X = 0.069772 +/- 4.1637E-07 [cm]	Y = 0.062735 +/- 4.1755E-07 [cm]
# year 2012, month 11	X = 0.069930 +/- 4.2480E-07 [cm]	Y = 0.062511 +/- 4.2626E-07 [cm]
# year 2012, month 12	X = 0.069043 +/- 9.4942E-07 [cm]	Y = 0.062314 +/- 9.5232E-07 [cm]
# year 2015, month 7	X = 0.076854 +/- 6.3099E-07 [cm]	Y = 0.093296 +/- 6.2963E-07 [cm]
# year 2015, month 8	X = 0.076299 +/- 1.3169E-06 [cm]	Y = 0.094735 +/- 1.3130E-06 [cm]
# year 2015, month 9	X = 0.076813 +/- 2.3779E-07 [cm]	Y = 0.091153 +/- 2.3620E-07 [cm]
# year 2015, month 10	X = 0.077053 +/- 2.2095E-07 [cm]	Y = 0.092204 +/- 2.1972E-07 [cm]
# year 2015, month 11	X = 0.077149 +/- 1.1199E-06 [cm]	Y = 0.094503 +/- 1.1146E-06 [cm]
# year 2016, month 5	X = 0.064871 +/- 4.0766E-07 [cm]	Y = 0.094045 +/- 4.0545E-07 [cm]
# year 2016, month 6	X = 0.063223 +/- 2.3448E-07 [cm]	Y = 0.098545 +/- 2.3346E-07 [cm]
# year 2016, month 7	X = 0.058485 +/- 2.9540E-07 [cm]	Y = 0.101528 +/- 2.9448E-07 [cm]
# year 2016, month 8	X = 0.058380 +/- 3.1998E-07 [cm]	Y = 0.101729 +/- 3.1790E-07 [cm]
# year 2016, month 9	X = 0.057529 +/- 3.8561E-07 [cm]	Y = 0.105664 +/- 3.8219E-07 [cm]
# year 2016, month 10	X = 0.055517 +/- 2.9459E-07 [cm]	Y = 0.107506 +/- 2.9170E-07 [cm]

# year 2021, month 10   X Pos = 0.171753 - Width = 1.3734E-02 [cm]   Y Pos = -0.190651 - Width = 1.5133E-02 [cm]   Z Pos = 0.050984 - Width = 6.8873E+00 [cm]
# year 2021, month 11   X Pos = 0.172607 - Width = 1.4820E-02 [cm]   Y Pos = -0.192080 - Width = 1.6455E-02 [cm]   Z Pos = 0.045097 - Width = 7.1213E+00 [cm]
# year 2022, month 5    X Pos = 0.173003 - Width = 1.3459E-02 [cm]   Y Pos = -0.181755 - Width = 1.4755E-02 [cm]   Z Pos = -0.107226 - Width = 6.1230E+00 [cm]
# year 2022, month 6    X Pos = 0.171824 - Width = 1.3523E-02 [cm]   Y Pos = -0.180038 - Width = 1.4674E-02 [cm]   Z Pos = 0.283074 - Width = 6.3571E+00 [cm]
# year 2022, month 7    X Pos = 0.173472 - Width = 7.6120E-04 [cm]   Y Pos = -0.181012 - Width = 9.1500E-04 [cm]   Z Pos = 1.441225 - Width = 3.2385E+00 [cm]
# year 2022, month 8    X Pos = 0.172803 - Width = 7.6612E-04 [cm]   Y Pos = -0.182373 - Width = 9.0643E-04 [cm]   Z Pos = 0.026420 - Width = 3.1990E+00 [cm]
# year 2022, month 9    X Pos = 0.174092 - Width = 8.0332E-04 [cm]   Y Pos = -0.183440 - Width = 8.4724E-04 [cm]   Z Pos = -0.052570 - Width = 3.2982E+00 [cm]
# year 2022, month 10   X Pos = 0.174249 - Width = 8.2544E-04 [cm]   Y Pos = -0.183659 - Width = 9.4380E-04 [cm]   Z Pos = -0.561499 - Width = 3.3948E+00 [cm]
# year 2022, month 11   X Pos = 0.172679 - Width = 9.1814E-04 [cm]   Y Pos = -0.183023 - Width = 1.0329E-03 [cm]   Z Pos = -1.721754 - Width = 3.5523E+00 [cm]
# year 2023, month 4    X Pos = 0.115345 - Width = 7.0596E-04 [cm]   Y Pos = -0.188842 - Width = 7.7293E-04 [cm]   Z Pos = -0.246330 - Width = 3.6249E+00 [cm]
# year 2023, month 5    X Pos = 0.116808 - Width = 7.8006E-04 [cm]   Y Pos = -0.186396 - Width = 8.5948E-04 [cm]   Z Pos = -0.600535 - Width = 7.8904E-01 [cm]
# year 2023, month 6    X Pos = 0.117145 - Width = 8.4810E-04 [cm]   Y Pos = -0.183745 - Width = 9.4802E-04 [cm]   Z Pos = -0.430677 - Width = 3.7080E+00 [cm]
# year 2023, month 7    X Pos = 0.116243 - Width = 7.7234E-04 [cm]   Y Pos = -0.181976 - Width = 8.3111E-04 [cm]   Z Pos = -0.519375 - Width = 3.6933E+00 [cm]
# year 2023, month 9    X Pos = 0.112538 - Width = 6.5062E-03 [cm]   Y Pos = -0.186970 - Width = 6.5946E-03 [cm]   Z Pos = -0.278197 - Width = 4.5345E+00 [cm]
# year 2024, month 3, day 21    X Pos = 0.136365 - Y Pos = -0.197122   --> from run 378238 workflow PCL_HP_byRun
# year 2024, month 4, day 1     X Pos = 0.131317 - Y Pos = -0.195124   --> from run 378750 workflow PCL_HP_byRun
# year 2024, month 4, day 5     X Pos = 0.095503 - Y Pos = -0.195209   --> from run 378985 workflow PCL_HP_byRun
