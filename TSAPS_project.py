# Incoming distribution:
# Initial position range comes from 3mm radius source,
# Very soon it hits a tungsten moderator.
# It doesn't matter how soon, the disk of possible impact locations should be 3mm + maxA/omega in radius, for 70 Gauss field.
# maxA here is the radius of the cyclotron beam, which actually max_v_0 = sqrt(2*maxKE/mass)
# Na-22 β decays with:
# 545.5 keV (89.8% abundance/maximum energy)
# 215.5 keV (89.8% abundance/average energy)
# 2842.1 keV (0.6% abundance/maximum energy)
# 834.8 keV (0.6% abundance/average energy)
# According to https://ehs.umich.edu/wp-content/uploads/2016/04/Sodium-22.pdf
# I don't understand the parentheticals.
# 
# The isotope Na-22 decays  (in 99.95% of cases) with half-life of 2.6 years for positron emission or electron capture
# to the first excited state of 22-Ne at 1.274 MeV (which subsequently relaxes with gamma photon emission).
# The positron is emitted with maximum energy of 544KeV
# according to https://physicsopenlab.org/2016/12/25/antimatter/
#
# Maximum (A/omega) values for Na-22 in 70 Gauss = .007 Tesla field
# 544 keV    : 35 cm
# 545.5 keV  : 36 cm
# 215.5 keV  : 22 cm
# 2842.1 keV : 81 cm
# 834.8 keV  : 44 cm

# In any case, these kinds of energies make A much big enough that the entire moderator will probably be hit,
# and then some moderated and unmoderated positrons will exit the window.
#
# Note: omega values (positive for positrons, negative for electrons)
# 70 Gauss = .007 Tesla field: 1.23e9 radians per second
# 100 Gauss = .01 Tesla field: 1.75e9 radians per second
# 40 Gauss = .004 Tesla field: 7.03e8 radians per second
#
# Maximum (A/omega) values, i.e. cyclotron radii, for 2.9 eV in different magnetic field.
# z-direction acceleration should not change this:
# 70 Gauss = .007 Tesla field: 0.820 mm
# 100 Gauss = .01 Tesla field: 0.574 mm
# 40 Gauss = .004 Tesla field: 1.435 mm
#

# 15 eV z-velocity = 2.3e6 m/s (.0077c), which means one full rotation every 8.2 mm in 100 Gauss field,
# So definitly only particles whose center path is A/omega away from the tube walls will pass through the tube,
# without hitting the walls. (Some might go through the walls or be reemitted from them, but I'll ignore those.)
# "center path" in a B-only field is <x, y> = <x_0 + (A/omega)*sin(p), y_0 - (A/omega)*cos(p)>

import numpy as np

POSITRON_C = 1.602176634e-19
ELECTRON_C = -POSITRON_C
ELECTRON_kg = 9.109383701528e-31 # Also positron mass in kg
POSITRON_kg = ELECTRON_kg
eV_J = 1.602176634e-19 # This is a conversion factor: 1 eV = 1.602176634e-19 J
inch_m = .0254

# I'm not certain but I will define the following values as best I can for now:
First_Tube_Radius_m = .005

# Randomness (MonteCarlo) is a bit gratuitous, but for now I'll use it:
# I'll use uniform distribution point of origination on 5 mm disk,
# and hemispherically uniform distribution of velocity directions (part of the unknown moderator behavior)
# and uniform distribution of speeds (part of the unknown moderator behavior)
# and remove particles that would leave the disk due to their A/omega

def getAngle(x, y, N): # I'm making this only work with iterables now.
    # This is just a basic math function, since arctan doesn't map to the whole circle of 2D directions.
    # The returned angle is 0 if pointing in the positive x direction +π/2 if pointing in the positive y direction, etc.
    # For ease of coding, it currently returns an angle in the interval [-π/2, +3π/4)
    for i in range(N):
        if x[i] > 0:
            return np.arctan(y[i]/x[i])
        elif x[i] < 0: # if would do, because of the return statements. I just use elif, which means "else if", for clarity
            return np.pi + np.arctan(y[i]/x[i])
        elif y[i] > 0:
            return  .5*np.pi
        elif y[i] < 0:
            return -.5*np.pi

def initiate_positron_positions(disk_radius, N):
    # polar coordinates
    phis = np.random.uniform(low = 0.0, high = 2*np.pi, size = N)
    rs = np.random.uniform(low = 0.0, high = 1.0, size = N)
    rs = np.sqrt(rs*(disk_radius**2)) # reshaping r from previous line

    # conversion to rectangular coordinates:
    xs = rs*cos(phis)
    ys = rs*sin(phis)
    zs = 0

    return {
        'xs'   : xs
        'ys'   : ys
        'zs'   : zs
        'phis' : phis # used by not_hitting_tube
    }

def positive_z_hemispherically_uniform_velocities(initial_positions, vs, N): # vs = array of magnitudes of velocities
    #N = len(vs)

    v_theta0s = np.random.uniform(low = 0.0, high = +1.0, size = N)
    v_theta0s = np.arccos(1 - v_theta0s) # reshaping to have pdf = sin(v_theta0)

    v_phi0s = np.random.uniform(low = 0.0, high = 2*np.pi, size = N)

    v_z0s = v_0s * np.cos(v_theta0s)
    v_r0s = v_0s * np.sin(v_theta0s) # to compute sin(v_θ0) once per run instead of twice
    v_x0s = v_r0s * np.cos(v_phi0s)
    v_y0s = v_r0s * np.sin(v_phi0s)

    initiated_states = initial_positions
    initiated_states['v_xs'] = v_x0s
    initiated_states['v_ys'] = v_y0s
    initiated_states['v_zs'] = v_z0s

    return initiated_states

def moderate_with_tungsten(entering_positions, N):
    # N = len(entering_positions)
    # This is supposed to model particles being moderated with a thin tungsten sheet.
    # A uniform distribution is used because the actual distribution is unknown.
    KE_0s = np.random.uniform(low = 0.0, high = 2.9*eV_J, size = N)
    v_0s = np.sqrt(2*KE_0s/ELECTRON_kg) # magnitude of velocity
    exiting_states = hemispherically_uniform_velocities(v_0s)
    exiting_states['xs'] = entering_positions['xs']
    exiting_states['ys'] = entering_positions['ys']
    exiting_states['zs'] = entering_positions['zs']

    return exiting_states

def z_accelerate(entering_states, potential_difference, charge, mass): # mass = ELECTRON_kg
    # This function only gives the states after acceleration, not during, and not the time the acceleration took.
    added_energy = charge*potential_difference
    added_velocity = np.sqrt(2*added_energy/mass)
    exiting_states = entering_states
    exiting_states['v_zs'] += added_velocity # This does work in numpy.

# Ex = (V_west_V - V_east_V)/d_plates_m
def ExB_end(Ex, B, charge, mass, L, inits, N):
    # Returns dictionary of numpy arrays giving the ending positions and velocities of particles
    # after passing through a distance L of given Ex and B,
    # given a similar dictionary of their positions and velocities entering the region (inits)

    # B is a scalar in teslas
    # arguments ending in s accept vectors of scalars
    # all except ts must be of the same length
    # ts is in seconds
    # a dictionary of initials
    # x_0s, y_0s, z_0s are in meters
    # v_x0s, v_y0s, v_z0s are in m/s

    omega = charge*B/mass # angular frequency of cyclotron motion

    v_x0s = inits['v_xs']
    v_y0s = inits['v_ys']
    v_z0s = inits['v_zs']

    x_0s = inits['xs']
    y_0s = inits['ys']
    z_0s = inits['zs']

    As = np.sqrt(v_x0s**2 + (v_y0s + Ex/B)**2) # v0s in the v' = v + (E/B)j frame
    ps = getAngle(v_x0s, v_y0s + Ex/B, N) # vφ0s in the v' = v + (E/B)j reference frame

    t_finals = L/v_z0

    # I see now that the fact that I've been using 0s this whole time is a bit unfortunate, but has some uses.
    xs = (As/omega)*np.sin(omega*t_finals - ps)                   + (As/omega)*np.sin(ps) + x_0s
    ys = (As/omega)*np.cos(omega*t_finals - ps) - (Ex/B)*t_finals - (As/omega)*np.cos(ps) + y_0s
    zs = np.array(L*len(x_0s))

    v_xs =  As*cos(omega*t_finals - ps)
    v_ys = -As*sin(omega*t_finals - ps) - Ex/B
    v_zs = v_z0s # sort of unnecessary line

    # vs = np.sqrt(v_xs**2 + v_ys**2 + v_zs**2)
    # v_rs = np.sqrt(v_xs**2 + v_ys**2)
    # v_thetas = getAngle(v_zs, v_rs)
    # v_phis = getAngle(v_xs, v_ys)

    return {
        'xs' : xs
        'ys' : ys
        'zs' : zs
        'v_xs' : v_xs
        'v_ys' : v_ys
        'v_zs' : v_zs
        'As' : As # used by not_hitting_tube
        'ps' : ps # used by not_hitting_tube
    }

def not_hitting_tube(inits, tube_radius, N): # removes paths that would hit a wall before getting to the ExB plate
    # inits should be a dictionary of 1D arrays
    indices_to_delete = []
    for i in range(N):
        worst_case_x = inits['xs'][i] + sin(inits['ps'][i]) + inits['As'][i]*cos(inits['phis'][i])
        worst_case_y = inits['ys'][i] - cos(inits['ps'][i]) + inits['As'][i]*sin(inits['phis'][i])
        if worst_case_x**2 + worst_case_y**2 < tube_radius**2:
            indices_to_delete += [i]
    return np.delete(inits, indices_to_delete)

# Main?

# # Potentials: Names patterned after those in Mukherjee et al. 2016 Figure 1.
# # These are the potentials in that paper, but I need to rederive them.
# V_ST_V = -15.8 # (ST = Source Tube)

# V_m_V_1eV = -0.8 # (m = moderator (tungsten))
# V_m_V_2eV = -0.38

# V_AW_V = 5.5
# V_AE_V = V_ST_V

# V_BW_V = -15.8
# V_BE_V = V_ST_V

# V_CW_V = -2.79
# V_CE_V =  2.71

# V_DW_V = V_CE_V
# V_DE_V = V_CW_V

# V_TOF = ? # (TOF = Time-Of-Flight Tube)
# V_S = ? # (S = Source)



# I want to get the ExB plate potential differences as a function of positron energy
# (which is also controlled by the average/net potentials) 

#The above probably have wrong heights.
ExB_A_zLENGTH_m = 10.5*inch_m # E×B region
ExB_A_yHEIGHT_m = 3.5*inch_m
ExB_A_xDISTANCE_m = inch_m

ExB_B_zLENGTH_m = 10.5*inch_m # E×B region
ExB_B_yHEIGHT_m = 3.5*inch_m
ExB_B_xDISTANCE_m = inch_m

# The below are true.
ExB_C_zLENGTH_m = 10.5*inch_m
ExB_C_yHEIGHT_m = 3.5*inch_m
ExB_C_xDISTANCE_m = inch_m

ExB_D_zLENGTH_m = 10.5*inch_m
ExB_D_yHEIGHT_m = 3.5*inch_m
ExB_D_xDISTANCE_m = inch_m

# Ex_A_V_per_m = (V_ST_V - V_AW_V)/ExB_A_xDISTANCE_m
# Ex_B_V_per_m = (V_BW_V - V_ST_V)/ExB_B_xDISTANCE_m
# Ex_C_V_per_m = (V_CE_V - V_CW_V)/ExB_C_xDISTANCE_m
# Ex_D_V_per_m = (V_DE_V - V_DW_V)/ExB_D_xDISTANCE_m

# First I want a function that will take input velocities and a desired verticle distance and give the ...
# One can simply calculate the vertical transport given by a given ExB plate within A...

# Actually, what I want is SimpleModelPaths but for only the x-y plane.

# Points of interest:
# Entering ExB A
# Entering ExB 

def positron_ExB_A_B(potentials, N):
    # N_RUNS is the number of sets of initial values.
    # We're currently treating v_z as constant for now (all plates have equal net charge.)

    initial_positions = initiate_positron_positions(First_Tube_Radius_m, N)
    initial_states = moderate_with_tungsten(initial_positions, N)
    initial_states = not_hitting_tube(initial_states, First_Tube_Radius_m, N)

    # Reminder: Using ExB_end(Ex, B, charge, mass, L, inits)

    V_m_V = potentials['V_m_V']
    V_avg_A_V = potentials['V_avg_A_V']

    # Because the cyclotron motion is a distribution, I can just model the space between
    # E×B plates and z-only acceleration, and the inaccuracy will be averaged out.
    states_enteringExB_A =     z_accelerate(initial_states, V_avg_A_V - V_m_V, POSITRON_C, POSITRON_kg)
    states_leavingExB_A =      ExB_end(Ex_A_V_per_m, B2_T, POSITRON_C, POSITRON_kg, ExB_A_zLENGTH_m, states_enteringExB_A)

    V_avg_B_V = potentials['V_avg_B_V']

    states_enteringExB_B =     z_accelerate(initial_states, V_avg_A_V - V_m_V, POSITRON_C, POSITRON_kg)
    states_leavingExB_B =      ExB_end(Ex_B_V_per_m, B2_T, POSITRON_C, POSITRON_kg, ExB_B_zLENGTH_m, states_enteringExB_B)

    return states_leavingExB_B

def positron_ExB_C_D(states_enteringExB_C, potentials, N):
    
    V_avg_B_V = potentials['V_avg_B_V']
    states_leavingExB_C =      ExB_end(Ex_C_V_per_m, B3_T, POSITRON_C, POSITRON_kg, ExB_B_zLENGTH_m, states_enteringExB_B)

    V_avg_C_V = potentials[]
    states_enteringExB_B =     ExB_end(0,            B2_T, POSITRON_C, POSITRON_kg, ExB_A_TO_ExB_B_m, states_leavingExB_A)
    states_leavingExB_B =      ExB_end(Ex_B_V_per_m, B2_T, POSITRON_C, POSITRON_kg, ExB_B_zLENGTH_m, states_enteringExB_B)




def electron_paths():
    pass