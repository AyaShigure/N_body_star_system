from baby_math import *
import os
import random
import vpython
from vpython import *

class n_body_system():
    def __init__(self, n):
        self.n = n          
        self.G = 6.6743e-11 # [m^3/(kg^1*s^2)]

        ##### Initial conditions
        self.mass_order_of_magnitude = 10
        self.distance_order_of_magnitude = 30
        self.velocity_order_of_magnitude = 4
        self.p_0 = None
        self.dpdt_0 = None
        self.mass_vecter = None

        ##### Sky box size
        self.sky_box_size = 10 * self.distance_order_of_magnitude

    def generate_initial_conditions(self):
        ##### Random mass vector
        self.mass_vecter = np.array([self.n,1])
        for i in range(len(self.n)):
            self.mass_vecter[i] = random.ranint() * self.mass_order_of_magnitude
        ##### Random initial position
        self.p_0 = np.array([3 * self.n,1])
        for i in range(len(self.n)):
            self.p_0[i] = (2 * random.random() - 1.0) * self.distance_order_of_magnitude
        ##### Random initial velocity
        self.dpdt_0 = np.array([3 * self.n,1])
        for i in range(len(self.n)):
            self.dpdt_0[i] = (2 * random.random() - 1.0) * self.velocity_order_of_magnitude

    def engage_vpython_visualization(self, dt=10, simulation_steps=200):
        ##### Break condition
        if self.p_0 == None:
            print('Initial conditions are not defined, exiting')
            os._exit(0)

        ##### Log the solutions to last_xxxx
        self.last_p_0 = None
        self.last_dpdt_0 = None
        self.last_mass_vecter = None

        ###### Initialize vpython bodies
        self.vpython_body_list = []
        for i in range(self.n):
            initialize_body = vpython.sphere(color = color.green, radius = 0.3, make_trail = True, retain=40)
            self.vpython_body_list.append(initialize_body)

        # Simulation and visualization
        while(1):
            # 1. Calculate 1~100 step
            # 1.5 Handle the solution p_i = [x_i, y_i, z_i], dpdt_i = [dxdt_i, dydt_i, dzdt_i]
            # 2. Update the visualization
            # 3. Check if all the body is out of bound, teleportations
            # 4. Log the solutions as initial conditions
            pass

def euler_s_method_one_step(dt, initial_p, initial_dpdt, G, mass_vector):
    pass

def boundary_teleportation(p, sky_box_size):
    ### If the body left the preset region, teleport it to the other side of the boundary without changing the velocity vector
    revized_p = None # Check if p is out of the bound, return p if not, return revized_p if does
    return revized_p














# Euler's method
def i_will_return_the_rough_n_body_problem_solution_for_im_using_the_eulers_method(dt, simulation_steps, initial_p, initial_dpdt, mass_vector):
    # Log the initial conditions
    time_stamp = np.ndarray(1)
    time_stamp[0] = 0.0
    p_solution = initial_p
    dpdt_solution = initial_dpdt
    
    # Initial conditions & start calculating
    p_k = initial_p
    dpdt_k = initial_dpdt
    for step in tqdm(range(simulation_steps)):
        F_dir_matrix_k = update_gravtational_interaction_matrix(p_k) 
        
        # Euler's method 
        p_k_plus_1 = p_k + dt * dpdt_k
        dpdt_k_plus_1 = dpdt_k + dt * G * F_dir_matrix_k.dot(mass_vector)
        # print(F_dir_matrix_k.dot(mass_vector))
        # Log the results
        time_stamp = np.c_[time_stamp, (step+1) * dt]
        p_solution = np.c_[p_solution, p_k_plus_1]
        dpdt_solution = np.c_[dpdt_solution, dpdt_k_plus_1]
        
        # Update p_[k] and dpdt_[k]
        p_k = p_k_plus_1
        dpdt_k = dpdt_k_plus_1
        
    solution = [time_stamp, p_solution, dpdt_solution]
    return solution
