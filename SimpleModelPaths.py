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

import SimpleModelFunctions as SMF
#import numpy

def positron_path_times():
    pass

def electron_path_times():
    pass