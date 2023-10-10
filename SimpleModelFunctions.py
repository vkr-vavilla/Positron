import numpy as np

# This code is very unDRY, i.e., repetitive.

# Constants and variables named <object>_<unit> with what property of the
# object it is implied by the unit if that is specific enough.
# (C = Coulombs, kg = kilograms, J = Joules)

# Physical Constants
POSITRON_C = 1.602176634e-19
ELECTRON_C = -POSITRON_C
ELECTRON_kg = 9.109383701528e-31 # Also positron mass in kg
POSITRON_kg = ELECTRON_kg
eV_J = 1.602176634e-19 # This is a conversion factor: 1 eV = 1.602176634e-19 J

R_DISK = 0.005

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

def getAngle(x, y): # I'm making this only work with iterables now.
    # This is just a basic math function, since arctan doesn't map to the whole circle of 2D directions.
    # The returned angle is 0 if pointing in the positive x direction +π/2 if pointing in the positive y direction, etc.
    # For ease of coding, it currently returns an angle in the interval [-π/2, +3π/4)
    for i in range(len(x)):
        if x[i] > 0:
            return np.arctan(y[i]/x[i])
        elif x[i] < 0: # if would do, because of the return statements. I just use elif, which means "else if", for clarity
            return np.pi + np.arctan(y[i]/x[i])
        elif y[i] > 0:
            return  .5*np.pi
        elif y[i] < 0:
            return -.5*np.pi

def hemispherically_uniform_velocities(N, v_0s):

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

def point_source(N_particles):
    KE_0s = np.random.uniform(low = 0.0, high = 3*eV_J, size = N_particles)
    # this distribution needs to be fixed
    
    v_0s = np.sqrt(2*KE_0s/ELECTRON_kg) # magnitude of velocity

    inits = hemispherically_uniform_velocities(N_particles, v_0s)
    inits['x_0s'] = np.zeros(N_particles)
    inits['y_0s'] = np.zeros(N_particles)
    inits['z_0s'] = np.zeros(N_particles)

    return inits

def moderate_with_tungsten(entering_states):
    # This is supposed to model particles being moderated with a thin tungsten sheet, but I really don't know how that works so I'm making stuff up.
    KEs = 2.9*eV_J
    v_0s = np.sqrt(2*KE_0s/ELECTRON_kg) # magnitude of velocity
    exiting_states = hemispherically_uniform_velocities(N, v_0s)
    exiting_states['x_0s'] = entering_states['x_0s']
    exiting_states['y_0s'] = entering_states['y_0s']
    exiting_states['z_0s'] = entering_states['z_0s']

    return exiting_states

def getE(q_lowxPlate, q_highxPlate, d_plates): # I don't actually use this.
    # calculates Ez in a region between to 
    # Ex = f(q_highxPlate - lowxPlate)/d_plates # Recall/derive equation
    Ez = 0.5 * (q_lowxPlate + q_highxPlate)
    return [Ex, 0, Ez]

def ExB_times(Ex, B, charge, mass, ts, inits):
    # Returns position at each time t for each initial position and velocity
    # B is a scalar in teslas
    # arguments ending in s accept vectors of scalars
    # all except ts must be of the same length
    # ts is in seconds
    # a dictionary of initials
    # x_0s, y_0s, z_0s are in meters
    # v_x0s, v_y0s, v_z0s are in m/s

    omega = charge*B/mass # angular frequency of cyclotron motion

    v_x0s = inits['v_x0s']
    v_y0s = inits['v_y0s']
    v_z0s = inits['v_z0s']

    x_0s = inits['x_0s']
    y_0s = inits['y_0s']
    z_0s = inits['z_0s']

    As = np.sqrt(v_x0s**2 + (v_y0s + Ex/B)**2) # v0s in the v' = v + (E/B)j frame
    ps = getAngle(v_x0s, v_y0s + Ex/B) # v_φ0s in the v' = v + (E/B)j reference frame

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

def Ez_only_uniform_end(Ez, charge, mass, L, inits):
    acceleration = charg*Ez/mass

    v_x0s = inits['v_x0s']
    v_y0s = inits['v_y0s']
    v_z0s = inits['v_z0s']

    x_0s = inits['x_0s']
    y_0s = inits['y_0s']
    z_0s = inits['z_0s']

    t_finals = np.sqrt(2*L/v_z0) # ?speed
    

    xs = 0.5*acceleration*(t_finals**2) + v_x0s*t_finals + x_0s
    ys = 0.5*acceleration*(t_finals**2) + v_y0s*t_finals + y_0s
    zs = 0.5*acceleration*(t_finals**2) + v_z0s*t_finals + z_0s

    v_xs = acceleration*t_finals + v_x0s
    v_ys = acceleration*t_finals + v_y0s
    v_zs = acceleration*t_finals + v_z0s

    vs = np.sqrt(v_xs**2 + v_ys**2 + v_zs**2)
    v_rs = np.sqrt(v_xs**2 + v_ys**2)
    v_thetas = getAngle(v_zs, v_rs)
    v_phis = getAngle(v_xs, v_ys)

    return {'v_0s' : vs,
            'v_theta0s' : v_thetas,
            'v_phi0s' : v_phis,
            'v_z0s' : v_zs,
            'v_r0s' : v_rs,
            'v_x0s' : v_xs,
            'v_y0s' : v_ys}

def Ez_only_mid_dipole_end(Ez, charge, mass, L, inits):
    acceleration = charg*Ez/mass

    v_x0s = inits['v_x0s']
    v_y0s = inits['v_y0s']
    v_z0s = inits['v_z0s']

    x_0s = inits['x_0s']
    y_0s = inits['y_0s']
    z_0s = inits['z_0s']

    t_finals = np.sqrt(2*L/v_z0) # ?speed
    
    # xs = 
    # ys = 
    # zs = 

    # v_xs = 
    # v_ys =
    # v_zs =

    # vs = np.sqrt(v_xs**2 + v_ys**2 + v_zs**2)
    # v_rs = np.sqrt(v_xs**2 + v_ys**2)
    # v_thetas = getAngle(v_zs, v_rs)
    # v_phis = getAngle(v_xs, v_ys)

    # return {'v_0s' : vs,
    #         'v_theta0s' : v_thetas,
    #         'v_phi0s' : v_phis,
    #         'v_z0s' : v_zs,
    #         'v_r0s' : v_rs,
    #         'v_x0s' : v_xs,
    #         'v_y0s' : v_ys}

def ExB_end(Ex, B, charge, mass, L, inits):
    # Returns dictionary of numpy arrays giving the ending positions and velocities of particles after passing through a distance L of given Ex and B,
    # given a similar dictionary of their positions and velocities entering the region (inits)

    # B is a scalar in teslas
    # arguments ending in s accept vectors of scalars
    # all except ts must be of the same length
    # ts is in seconds
    # a dictionary of initials
    # x_0s, y_0s, z_0s are in meters
    # v_x0s, v_y0s, v_z0s are in m/s

    omega = charge*B/mass # angular frequency of cyclotron motion

    v_x0s = inits['v_x0s']
    v_y0s = inits['v_y0s']
    v_z0s = inits['v_z0s']

    x_0s = inits['x_0s']
    y_0s = inits['y_0s']
    z_0s = inits['z_0s']

    As = np.sqrt(v_x0s**2 + (v_y0s + Ex/B)**2) # v0s in the v' = v + (E/B)j frame
    ps = getAngle(v_x0s, v_y0s + Ex/B) # vφ0s in the v' = v + (E/B)j reference frame

    t_finals = L/v_z0

    # I see now that the fact that I've been using 0s this whole time is a bit unfortunate, but has some uses.
    xs = As*np.sin(omega*t_finals - ps)                   + As*np.sin(ps) + x_0s
    ys = As*np.cos(omega*t_finals - ps) - (Ex/B)*t_finals - As*np.cos(ps) + y_0s
    zs = np.array(L*len(x_0s))

    v_xs =  As*cos(omega*t_finals - ps)
    v_ys = -As*sin(omega*t_finals - ps) - Ex/B
    v_zs = v_z0s # sort of unnecessary line

    vs = np.sqrt(v_xs**2 + v_ys**2 + v_zs**2)
    v_rs = np.sqrt(v_xs**2 + v_ys**2)
    v_thetas = getAngle(v_zs, v_rs)
    v_phis = getAngle(v_xs, v_ys)

    return {'v_0s' : vs,
            'v_theta0s' : v_thetas,
            'v_phi0s' : v_phis,
            'v_z0s' : v_zs,
            'v_r0s' : v_rs,
            'v_x0s' : v_xs,
            'v_y0s' : v_ys}