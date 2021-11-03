import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")

times = [
    'year 2010, month 3',
    'year 2010, month 4',
    'year 2010, month 5',
    'year 2010, month 6',
    'year 2010, month 7',
    'year 2010, month 8',
    'year 2010, month 9',
    'year 2010, month 10',
    'year 2011, month 3',
    'year 2011, month 4',
    'year 2011, month 5',
    'year 2011, month 6',
    'year 2011, month 7',
    'year 2011, month 8',
    'year 2011, month 9',
    'year 2011, month 10',
    'year 2012, month 4',
    'year 2012, month 5',
    'year 2012, month 6',
    'year 2012, month 7',
    'year 2012, month 8',
    'year 2012, month 9',
    'year 2012, month 10',
    'year 2012, month 11',
    'year 2012, month 12',
    'year 2015, month 7',
    'year 2015, month 8',
    'year 2015, month 9',
    'year 2015, month 10',
    'year 2015, month 11',
    'year 2016, month 5',
    'year 2016, month 6',
    'year 2016, month 7',
    'year 2016, month 8',
    'year 2016, month 9',
    'year 2016, month 10',
    'year 2017, month 6',
    'year 2017, month 7',
    'year 2017, month 8',
    'year 2017, month 9',
    'year 2017, month 10',
    'year 2017, month 11',
    'year 2018, month 4',
    'year 2018, month 5',
    'year 2018, month 6',
    'year 2018, month 7',
    'year 2018, month 8',
    'year 2018, month 9',
    'year 2018, month 10',
    'year 2018, month 11',
    'year 2021, month 10',
    'year 2021, month 11',
]

Time = [datetime.strptime(time,"year 20%y, month %m") for time in times ]

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
    0.096508,#8
    0.096190,
    0.096331,#10
    0.094505,#10
    0.171753,
    0.173006,
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
    -0.060965, #8
    -0.062271, #9
    -0.061833, #10
    -0.063482, #11
    -0.190651, # 2021
    -0.192189,
])

# convert from cm to micron
X = X*1.e4
Y = Y*1.e4

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()


fig.autofmt_xdate()
plt.plot(Time,X, c='tab:blue')
plt.plot(Time,Y, c='tab:green')
plt.scatter(Time,X, c='b', s=40, lw = 0, label='X')
plt.scatter(Time,Y, c='g', s=40, lw = 0, label='Y')
# plt.legend((X.all(),Y.all()), ('X','Y'), loc=3)
# plt.legend(bbox_to_anchor=(0.8, 1.02, 1., .102), loc=3,
plt.legend(loc=3, scatterpoints=1)
plt.xlabel('Date')
plt.ylabel('position [micron]')
plt.title('CMS beamspot in pp collisions')
# fit with np.polyfit
# m, b = np.polyfit(Time, Y, 1)
# plt.plot(x, m*x + b, '-', c='g')
# plt.show()
plt.show(block=False)
plt.savefig('cms_beamspotXY_vs_time_2021_Nov3.pdf')
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

# year 2021, month 10	X = 0.171753 +/- 2.0963E-05 [cm]	Y = -0.190651 +/- 2.0641E-05 [cm]
# year 2021, month 11	X = 0.173006 +/- 1.7382E-04 [cm]	Y = -0.192189 +/- 1.7061E-04 [cm]



