# Variable Declarations patterned off SimplifiedPositronMotion.m

# Constants and variables named <object>_<unit> with what property of the
# object it is implied by the unit if that is specific enough.
# (Insert list of used units.)

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
# The positive x direction points out of the page (up when page on table), if source is on right, as in Mukherjee et al 2016.
# (Previously I wrongly said into the page, since I was imagining the source on the left.)
# (The chirality of this coordinate system is as normal in math and physics.)
# Therefore, positrons should move mostly in the negative z direction,
#        and electrons should move mostly in the positive z direction.
SOURCE_TO_MODERATOR_m = 0.3 # EparB region

#MODERATOR_zTHICKNESS_m = 0 # I haven't actually used this.
#My currentSMF.moderate_with_tungsten function doesn't make sense unless the moderator is a thin sheet.

MODERATOR_to_BARRIER_B_m = 0.3# EparB region This "Barrier B" (Tungsten Barrier B in Mukherjee et al) is actually where the 70 Gauss region becomes 100 Gauss.

BARRIER_B_to_ExB_A_m = 0.6 # EparB region

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

import SimpleModelFunctions as SMF
#import numpy

def positron_path_times(N_RUNS):
    # N_RUNS is the number of sets of initial values.
    # We're currently treating v_z as constant for now (all plates have equal net charge.)

    states_initial = SMF.point_source(N_RUNS)

    # Reminder: Using ExB_end(Ex, B, charge, mass, L, inits)

    states_entering_moderator = SMF.ExB_end(0,            B1_T, POSITRON_C, POSITRON_kg, SOURCE_TO_MODERATOR_m,    states_initial)
    states_leaving_moderator = SMF.moderate_with_tungsten(states_entering_moderator)
    states_at_barrier_B =       SMF.ExB_end(0,            B1_T, POSITRON_C, POSITRON_kg, MODERATOR_to_BARRIER_B_m, states_leaving_moderator)

    states_enteringExB_A =      SMF.ExB_end(0,            B2_T, POSITRON_C, POSITRON_kg, BARRIER_B_to_ExB_A_m,     states_at_barrier_B)
    states_leavingExB_A =       SMF.ExB_end(Ex_A_V_per_m, B2_T, POSITRON_C, POSITRON_kg, ExB_A_zLENGTH_m,          states_enteringExB_A)

    states_enteringExB_B =      SMF.ExB_end(0,            B2_T, POSITRON_C, POSITRON_kg, ExB_A_TO_ExB_B_m,         states_leavingExB_A)
    states_leavingExB_B =       SMF.ExB_end(Ex_B_V_per_m, B2_T, POSITRON_C, POSITRON_kg, ExB_B_zLENGTH_m,          states_enteringExB_B)

    # I think there is no magnetic field between ExB_B
    Ez_ExB_B_TO_ExB_C = 
    states_enteringExB_C =      SMF.Ez_only_mid_dipole_end(Ez_ExB_B_TO_ExB_C,       POSITRON_C, POSITRON_kg, ExB_A_TO_ExB_B_m,         states_leavingExB_B)
    states_leavingExB_C =       SMF.ExB_end(Ex_B_V_per_m, B2_T, POSITRON_C, POSITRON_kg, ExB_B_zLENGTH_m,          states_enteringExB_B)




def electron_path_times():
    pass