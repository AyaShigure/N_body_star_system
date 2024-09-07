from aya_n_body_ultimate_calculator_pack.baby_math import *
# from aya_n_body_ultimate_calculator_pack.matplotlib_mp4_generator import *
from aya_n_body_ultimate_calculator_pack.n_body_class import *
# from aya_n_body_ultimate_calculator_pack.vpython_script_generator import *


three_body_system = n_body_system(6)

three_body_system.generate_initial_conditions()
three_body_system.engage_vpython_visualization(dt=1000)