# Testing Code
import SimpleFunctions as SF
import numpy as np
import matplotlib.pyplot as plt
import Colors

N_RUNS = 20 # The number of sets of initial values.

TEST_RUN = SF.init_velocities(N_RUNS)
TEST_RUN['x_0s'] = np.zeros(N_RUNS)
TEST_RUN['y_0s'] = np.zeros(N_RUNS)
TEST_RUN['z_0s'] = np.zeros(N_RUNS)

[v_x0s, v_y0s, v_z0s] = [TEST_RUN['v_x0s'],
                         TEST_RUN['v_y0s'],
                         TEST_RUN['v_z0s']]

fig = plt.figure()

# v_0sSpherePlot = fig.add_subplot(projection = '3d')
# v_0sSpherePlot.scatter(v_x0s, v_y0s, v_z0s)

# ThetaHistogram = fig.add_subplot()
# ThetaHistogram.hist(np.arctan(np.sqrt(v_x0s**2 + v_y0s**2)/v_z0s), bins = int(N_RUNS**0.5))
# print(np.arctan(np.sqrt(v_x0s**2 + v_y0s**2)/v_z0s))

E = 1
B = 1

N_TIMES = 1001
paths = SF.ExB_times(E, B, np.linspace(0,1e-6,N_TIMES), TEST_RUN)
colors = [Colors.numToColor(n) for n in np.linspace(0,1,N_TIMES)]*N_RUNS
#print(colors)
path_plot = fig.add_subplot(projection = '3d')
path_plot.scatter(paths[0],paths[1],paths[2], c=colors)

plt.show()