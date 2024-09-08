from aya_n_body_ultimate_calculator_pack.baby_math import *
from aya_n_body_ultimate_calculator_pack.n_body_class import *
from aya_n_body_ultimate_calculator_pack.solution_sets import *

simulation_mode = 0 # 0: Manual mode, >1: Load known solution

if __name__ == '__main__':
    ##### Mode 0:  Manual initial conditions 
    if simulation_mode == 0:
        multibody_system = n_body_system(10)
        multibody_system.mass_order_of_magnitude = 30
        multibody_system.distance_order_of_magnitude = 10
        multibody_system.velocity_order_of_magnitude = 5
        multibody_system.body_radius = 0.03
        multibody_system.generate_neat_symmetric_initial_conditions()

    ##### Mode >1: Known solutions from solution_sets.py
    elif simulation_mode == 1:
        multibody_system = solution_1()
    elif simulation_mode == 2:
        multibody_system = solution_2()
    elif simulation_mode == 3:
        multibody_system = solution_3()

    ##### Mode WAT????????
    else:
        print('Invalid simulation mode')
        os._exit(0)

    ###### Simulation settings
    dt = 300 # simulation step size
    max_simulation_count = 300 # max sim count
    endless_simulation = True # go forever?

    ###### Run
    multibody_system.engage_vpython_visualization(dt=dt, endless_simulation=endless_simulation,  max_simulation_count = max_simulation_count)