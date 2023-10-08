import numpy as np

# Variable Declarations patterned off SimplifiedPositronMotion.m

# Constants and variables named <object>_<unit> with what property of the
# object it is implied by the unit if that is specific enough.
# (Insert list of used units.)

# Physical Constants
POSITRON_C = 1.602176634e-19
ELECTRON_C = -POSITRON_C
ELECTRON_kg = 9.109383701528e-31 # Also positron mass in kg

# Independent Apparatus Constants (All just made-up numbers now.)
# These should be enter

# Potentials: Names patterned after those in Mukherjee et al. 2016 Figure 1.
V_ST_V = 0 # (ST = Source Tube)
V_m_V = 0 # (m o moderator (titanium))
V_AW_V = 1
V_BW_V = 1
V_CW_V = 1
V_CE_V = 1
V_DW_V = V_CE_V
V_DE_V = V_CW_V
V_TOF = 1 # (TOF = Time-Of-Flight Tube)
V_S = 1 # (S = Source)

# Spacial dimensions
# To match diagrams in papers, the coordinate will be as follows:
# The positive z direction points from the sample to the source.
# The positive y direction points from up (opposite gravity).
# The positive x direction points into of the page (down when page on table).
# (The chirality of this coordinate system is as normal in math and physics.)
# Therefore, positrons should move mostly in the negative z direction,
#        and electrons should move mostly in the positive z direction.
SOURCE_TO_ExB_A_m = 0.6 # EparB region

ExB_A_zLENGTH_m = 0.1 # E×B region
ExB_A_yHEIGHT_m = 0.1
ExB_A_xDISTANCE_m = 0.05

ExB_A_TO_ExB_B_m = 0.6 # EparB region

ExB_B_zLENGTH_m = 0.1 # E×B region
ExB_B_yHEIGHT_m = 0.1
ExB_B_xDISTANCE_m = 0.05

ExB_B_TO_ExB_C_m = 0.6

ExB_C_xDISTANCE_m = 0.1
ExB_C_yHEIGHT_m = 0.1
ExB_C_xDISTANCE_m = 0.05

ExB_C_TO_ExB_D_m = 0.6

ExB_D_xDISTANCE_m = 0.1
ExB_D_yHEIGHT_m = 0.1
ExB_D_xDISTANCE_m = 0.05

ExB_D_TO_TARGET_m = 0.6

# Applied Magnetic Fields in z direction
B1_T = .007
B2_T = .01
B3_T = .004
# May need to be based on solenoid currents

# Dependent Apparatus Constants

# Electric Field Strengths in between each set of ExB plates
# (for simplified motion calculation; assumed parallel to x-axis)
# Positive means pointing in positive x direction.
# (This code is slightly unDRY, i.e., repetitive.)
Ex_A_V_per_m = (V_ST_V - V_AW_V)/ExB_A_xDISTANCE_m
Ex_B_V_per_m = (V_BW_V - V_ST_V)/ExB_B_xDISTANCE_m
Ex_C_V_per_m = (V_CE_V - V_CW_V)/ExB_C_xDISTANCE_m
Ex_D_V_per_m = (V_DE_V - V_DW_V)/ExB_D_xDISTANCE_m

R_DISK = 0.005
M_E = 9.1093837e-31 # electron/positron mass
Q_E = 1.60217663e-19 # elementary charge
eV = 1.602176634e-19 # Joules

# functions

# Coordinate system:
# Z-axis points horizontally from source to sample.
# Y-axis points up.
# X-axis points left when facing twards higher z's, with higher y's up.
# Theta (θ) is angle in any direction away from positive Z-axis.
# Phi (φ) is the angle along a circle of constant theta,
#         starting at x>0, y=0 and going first towards y>0.
# (Exception: when theta=0 or n*pi, phi does nothing, x=0, and y=0.) 
#
# 
# Initial velocities: 
# uniform probability-per-unit-solid-angle in forward-facing hemisphere
# (logical if starting at source)
#   v_theta0 in [0, pi/2) : probability density ~ sin(v_theta0)
#   v_phi0 in [0, 2*pi) : uniform distribution
#   KE_pos in (0, 3eV] : ?uniform distribution (I would expect a log-normal distribution.)
#   v = sqrt(2*KE_pos/m_e) ; (classical - no S. Relativity)

def init_velocities(N):
    KE_0s = np.random.uniform(low = 0.0, high = 3*eV, size = N)
    # this distribution needs to be fixed
    
    v_0s = np.sqrt(2*KE_0s/M_E) # magnitude of velocity

    v_theta0s = np.random.uniform(low = 0.0, high = +1.0, size = N)
    v_theta0s = np.arccos(1 - v_theta0s) # reshaping to have pdf = sin(v_theta0)

    v_phi0s = np.random.uniform(low = 0.0, high = 2*np.pi, size = N)

    v_z0s = v_0s * np.cos(v_theta0s)
    v_r0s = v_0s * np.sin(v_theta0s) # to compute sin(v_θ0) once per run instead of twice
    v_x0s = v_r0s * np.cos(v_phi0s)
    v_y0s = v_r0s * np.sin(v_phi0s)

    return {'v_0s' : v_0s,
            'v_theta0s' : v_theta0s,
            'v_phi0s' : v_phi0s,
            'v_z0s' : v_z0s,
            'v_r0s' : v_r0s,
            'v_x0s' : v_x0s,
            'v_y0s' : v_y0s}
    # What is being returned can be changed of course.

# Initial positions:
# uniform probability-per-unit-area in r=5mm disk
# (as if source were a flat disk of radioactive material)
#   r_0 in [0, 5mm) : probability density ~ r_0
#   theta_0 in [0, 2*pi) : uniform distribution
#   x_0 = r_0 * cos(theta_0)
#   y_0 = r_0 * sin(theta_0)
#   z_0 = 0
#
# If source were hole in the sample chamber wall subtending a circle of angle
# from the perspective of a point sample,
# and the sample chamber had no internal EM field,
# then v_theta0 could be in [0, sin(r_h/d_e) )
# where r_h is the radius of the circular hole
# and d_e is the distance from the source to the edge of the circular hole.
# You could also use tan(r_h/d_c),
# where d_c is the distance to the center of the circular hole.
#
# If the sample chamber had the same magnetic field, cyclotron motion might make
# this radioactive disk model match the hole, but then why not just model
# the sample chamber? With the analytic solving methods, extra distance
# doesn't reduce speed, and precision is proportional to log_2 of number size.

# First I'm going to use a point source in a magnetic field only:

def getEz(q_lowxPlate, q_highxPlate, d_plates):
    # Ex = f(q_highxPlate - lowxPlate)/d_plates # Recall/derive equation
    Ez = 0.5 * (q_lowxPlate + q_highxPlate)
    return [Ex, 0, Ez]

def Ez(start_V, end_V):
    # calculates Ez in a region between to 
    pass

def ExB_times(Ex, B, ts, inits):
    # Returns position at each time t for each initial position and velocity
    # B is a scalar in teslas
    # arguments ending in s accept vectors of scalars
    # all except ts must be of the same length
    # ts is in seconds
    # a dictionary of initials
    # x_0s, y_0s, z_0s are in meters
    # v_x0s, v_y0s, v_z0s are in m/s

    omega = Q_E*B/M_E # angular frequency of cyclotron motion

    v_0s = inits['v_0s']
    v_theta0s = inits['v_theta0s']
    v_phi0s = inits['v_phi0s']

    v_x0s = inits['v_x0s']
    v_y0s = inits['v_y0s']
    v_z0s = inits['v_z0s']

    x_0s = inits['x_0s']
    y_0s = inits['y_0s']
    z_0s = inits['z_0s']

    As = np.sqrt(v_x0s**2 + (v_y0s + Ex/B)**2) # v0s in the v' = v + (E/B)j frame
    ps = np.arctan(v_x0s/(v_y0s + Ex/B)) # vφ0s in the v' = v + (E/B)j reference frame

    num_ts = len(ts)
    num_runs = len(v_x0s) # I could have used any variable rather than v_x0s

    # initializing return variable to be filled in following for loop
    xs_ts = np.empty((num_ts, num_runs))
    ys_ts = np.empty((num_ts, num_runs))
    zs_ts = np.empty((num_ts, num_runs))

    i = 0 # I want both the index and the value of t for the following loop,
          # and incrementing the index myself is faster than getting the value of t myself every loop
          # IF Python is smart about travesing linked lists for for loops.
    for t in ts:
        xs_t = As*np.sin(omega*t - ps)           + As*np.sin(ps) + x_0s
        ys_t = As*np.cos(omega*t - ps) - (Ex/B)*t - As*np.cos(ps) + y_0s
        zs_t =                           v_z0s*t # Edit to include Ek component for ExBparE.

        # Here, I am making ndarrays, where each row is a numpy array of x, y, or z coordinates at a particular time.
        # This means all the points at a particular timee are stored together in memory (rows), while particular runs are columns.
        xs_ts[i] = xs_t
        ys_ts[i] = ys_t
        zs_ts[i] = zs_t

        i += 1

    # I now want rows to be whole runs, with columns being times, i.e., whole runs are blocks in memory.
    xs_ts = np.transpose(xs_ts)
    ys_ts = np.transpose(ys_ts)
    zs_ts = np.transpose(zs_ts)

    return [xs_ts, ys_ts, zs_ts]

def ExBparE_times(Ex, Ez_func, B, ts, inits):
    # BECAUSE ABOVE REQUIRES ADDITION OF Z COMPONENT ACCELERATION
    # CAN ALSO BE RUN WITH Ez = 0 AND 
    # Ez_func
    pass

def ExB_end(E, B, L, x_0s, y_0s, z_0s, v_x0s, v_y0s, v_z0s):
    pass

def total_path_times():
    pass