from .baby_math import *
import os
import random as rand
import vpython
from vpython import *
import time
## Todo notes:

# 1. non complete random initial conditions
# 2. randomized body color


class n_body_system():
    def __init__(self, n):
        self.n = n          
        self.G = 6.6743e-11 # [m^3/(kg^1*s^2)]

        ##### Initial conditions
        self.mass_order_of_magnitude = 30
        self.distance_order_of_magnitude = 10
        self.velocity_order_of_magnitude = 5
        self.p_0 = None
        self.dpdt_0 = None
        self.mass_vector = None
        self.initial_condition_is_set_flag = False
        ##### Sky box size
        self.sky_box_size = 10 * self.distance_order_of_magnitude

    def kill_the_kernel_countdown(self):
        self.kill_counter +=1
        if self.kill_counter > self.max_simulation_count:
            print('max_simulation_count is reached, exiting...')
            os._exit(0)
        else:
            print(f'Current simulation step: [{self.kill_counter}/{self.max_simulation_count}]')

    def generate_initial_conditions(self):
        ##### Random mass vector
        self.mass_vector = np.zeros([self.n,1])
        for i in range(self.n):
            self.mass_vector[i] = rand.randint(1,9) * 10 ** self.mass_order_of_magnitude
        ##### Random initial position
        self.p_0 = np.zeros([3 * self.n,1])
        for i in range(self.n):
            for k in range(3):
                self.p_0[3*i + k] = (2 * rand.random() - 1.0) * 10 **  self.distance_order_of_magnitude
        ##### Random initial velocity
        self.dpdt_0 = np.zeros([3 * self.n,1])
        for i in range(self.n):
            for k in range(3):
                self.dpdt_0[3*i + k] = (2 * rand.random() - 1.0) * 10 ** self.velocity_order_of_magnitude
        self.initial_condition_is_set_flag = True

    def engage_vpython_visualization(self,  dt=100, endless_simulation=False, max_simulation_count=100):
        ##### Break condition
        self.kill_counter = 0
        self.max_simulation_count = max_simulation_count  # Default 100
        if self.initial_condition_is_set_flag == False:
            print('Initial conditions are not defined, exiting')
            os._exit(0)

        ##### Log the solutions to last_xxxx
        self.time_stamp = 0.0
        p_k = None
        dpdt_k = None

        ###### Initialize vpython bodies
        self.vpython_body_list = []
        for i in range(self.n):
            initialize_body = vpython.sphere(color = generate_random_color_vector(), radius = 0.03, make_trail = True, retain=40)
            self.vpython_body_list.append(initialize_body)
        ###### Vpython settings
        scene.autoscale = True
        scene.center = vector(0,0,0)

        ###### Starting the simulation
        p_k = self.p_0 
        dpdt_k = self.dpdt_0 
        print(f'Starting the simulation, dt = {dt}')
        while(1):
            # time.sleep(0.1)
            if endless_simulation == False:
                self.kill_the_kernel_countdown()
            ###### 1. Calculate 1~100 step
            for i in range(1):
                # print(p_k)
                p_k_plus_1, dpdt_k_plus_1 = euler_s_method_one_step(dt, p_k, dpdt_k, self.G, self.mass_vector)
                p_k = p_k_plus_1
                dpdt_k = dpdt_k_plus_1
            ###### 1.5 Handle the solution p_i = [x_i, y_i, z_i], dpdt_i = [dxdt_i, dydt_i, dzdt_i]
            p_solution_list_k_plus_1 = [] # p_solution_list = [p_1, p_2, ... , p_n]
            dpdt_solution_list_k_plus_1 = []
            for i in range(self.n):
                p_i = np.zeros([3,1])
                dpdt_i = np.zeros([3,1])
                for k in range(3):
                    p_i[k] = p_k[3*i + k]
                    dpdt_i[k] = dpdt_k[3*i + k]
                p_solution_list_k_plus_1.append(p_i / (10**self.distance_order_of_magnitude))
                # dpdt_solution_list_k_plus_1.append(dpdt_i / self.velocity_order_of_magnitude)
            ###### 2. Update the visualization
            rate(30)
            # print(p_solution_list_k_plus_1)
            for i in range(self.n):
                self.vpython_body_list[i].pos = vector(p_solution_list_k_plus_1[i][0], p_solution_list_k_plus_1[i][1], p_solution_list_k_plus_1[i][2])
            ###### 3. Check if all the body is out of bound, teleportations
            # p_k = boundary_teleportation(p_k, sky_box_size = 10**self.distance_order_of_magnitude)
            ###### 4. Log the solutions as initial conditions

def euler_s_method_one_step(dt, initial_p, initial_dpdt, G, mass_vector):
    ##### p_k
    p_k = initial_p
    dpdt_k = initial_dpdt
    ##### F_dir at time k
    F_dir_matrix_k = update_gravtational_interaction_matrix(p_k) 
    ##### Euler's method for k+1
    p_k_plus_1 = p_k + dt * dpdt_k
    dpdt_k_plus_1 = dpdt_k + dt * G * F_dir_matrix_k.dot(mass_vector)
    return p_k_plus_1, dpdt_k_plus_1

def boundary_teleportation(p, dpdt,  sky_box_size=2e10):
    teleportation_distance = 1e9
    revized_p = p
    # sign_array = np.sign(revized_p)
    magnitude_array = np.fabs(revized_p)
    print(f'bef: {revized_p}')

    ### If the body left the preset region, teleport it to the other side of the boundary(with some distance off set) without changing the velocity vector
    for i in range(len(revized_p)):
        if magnitude_array[i] > sky_box_size:
            # revized_p[i] = 1. * (magnitude_array[i] - teleportation_distance)
            revized_p[i] = 1. * sky_box_size
    print(f'aft: {revized_p}')

    # print('eeping')
    # time.sleep(1)
    return revized_p


def generate_random_color_vector():
    return vector(rand.random(), rand.random(), rand.random())