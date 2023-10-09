# Testing Code
import SimpleModelFunctions as SMF
import numpy as np
import matplotlib.pyplot as plt
import Colors

N_RUNS = 5 # The number of sets of initial values.

TEST_RUN = SMF.point_source(N_RUNS)

[v_x0s, v_y0s, v_z0s] = [TEST_RUN['v_x0s'],
                         TEST_RUN['v_y0s'],
                         TEST_RUN['v_z0s']]

fig = plt.figure()

# v_0sSpherePlot = fig.add_subplot(projection = '3d')
# v_0sSpherePlot.scatter(v_x0s, v_y0s, v_z0s)

# ThetaHistogram = fig.add_subplot()
# ThetaHistogram.hist(np.arctan(np.sqrt(v_x0s**2 + v_y0s**2)/v_z0s), bins = int(N_RUNS**0.5))
# print(np.arctan(np.sqrt(v_x0s**2 + v_y0s**2)/v_z0s))

E = 24000
B = .007

N_TIMES = 10001
paths = SMF.ExB_times(E, B, SMF.POSITRON_C, SMF.POSITRON_kg, np.linspace(0,1,N_TIMES), TEST_RUN)
colors = [Colors.numToColor(n) for n in np.linspace(0,1,N_TIMES)]*N_RUNS
#print(colors)
path_plot = fig.add_subplot(projection = '3d')
#path_plot.set_box_aspect((1/np.ptp(paths[0]), 1/np.ptp(paths[1]), 1/np.ptp(paths[2])))
path_plot.scatter(paths[0],paths[1],paths[2], c=colors)

plt.show()