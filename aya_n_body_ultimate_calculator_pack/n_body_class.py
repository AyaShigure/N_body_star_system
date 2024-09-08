from .baby_math import *
import os
import random as rand
import vpython
from vpython import *
import time
## Todo notes:

# 1. non complete random initial conditions (DONE)
# 2. randomized body color(DONE)
# 3. body mass not all at the same order of magnitude (so they dont sling shot that easily)
# 4.1 initial positions on a plane, evenly spaced (DONE)
# 4. initial velocities pointing towards to (0,0,0) (initial velocity)
# 5. 0 initial velocities but put the bodies closer?

# 6. Known solutions(initial conditions) to n=3 problems

def generate_random_color_vector():
    return vector(rand.random(), rand.random(), rand.random())

class n_body_system():
    def __init__(self, n):
        self.n = n          
        self.G = 6.6743e-11 # [m^3/(kg^1*s^2)]

        ##### Initial conditions
        self.mass_order_of_magnitude = 30
        self.distance_order_of_magnitude = 9
        self.velocity_order_of_magnitude = 5.4
        self.p_0 = None
        self.dpdt_0 = None
        self.mass_vector = None
        self.initial_condition_is_set_flag = False
        ##### Vpython settings
        self.body_radius = 0.3 # Default

    def kill_the_kernel_countdown(self):
        self.kill_counter +=1
        if self.kill_counter > self.max_simulation_count:
            print('max_simulation_count is reached, exiting...')
            os._exit(0)
        else:
            print(f'Current simulation step: [{self.kill_counter}/{self.max_simulation_count}]')

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
            initialize_body = vpython.sphere(color = generate_random_color_vector(), radius = self.body_radius, make_trail = True, retain=800)
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
            else:
                self.kill_counter += 1
                print(f'Current simulation step: [{self.kill_counter}/inf]')
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


    def generate_neat_symmetric_initial_conditions(self):
        '''
            1) same mass
            2) xy plane initial position, Rz rotated, with no z direction conponents
            3) xy plane initial velocities, Rz rotated, with some z direction noise
        '''
        ##### Random mass vector with different mass magnitudes
        self.mass_vector = np.zeros([self.n,1])
        for i in range(self.n):
            # self.mass_vector[i] = rand.randint(1,9) * 10 ** self.mass_order_of_magnitude 
            self.mass_vector[i] = 1. * 10 ** self.mass_order_of_magnitude 

        ##### Random initial position with different order of magnitude
        self.p_0 = np.zeros([3 * self.n,1])
        Rz_rotation_angle = 2 * np.pi/self.n
        for i in range(self.n):
            body_initial_position = Rz(Rz_rotation_angle * i).dot(np.array([1 * 10 ** self.distance_order_of_magnitude, 0.0, 0.0]))
            self.p_0[3*i + 0] = body_initial_position.T[0].item()
            self.p_0[3*i + 1] = body_initial_position.T[1].item()
        ##### Random initial velocity 1)pointing roughly to the spacial [0,0,0] 2)different order of magnitude
        self.dpdt_0 = np.zeros([3 * self.n,1])
        for i in range(self.n):
            body_initial_velocity = Rz(Rz_rotation_angle * i).dot(np.array([0.0, 1 * 10 ** self.velocity_order_of_magnitude, 0.0]))
            self.dpdt_0[3*i + 0] = body_initial_velocity.T[0].item()
            self.dpdt_0[3*i + 1] = body_initial_velocity.T[1].item()
            self.dpdt_0[3*i + 2] = (2 * rand.random() - 1.0) * 10 ** 1
        self.initial_condition_is_set_flag = True    


    def generate_better_initial_conditions_0_velocities(self):
        ##### Random mass vector with different mass magnitudes
        self.mass_vector = np.zeros([self.n,1])
        for i in range(self.n):
            self.mass_vector[i] = rand.randint(1,9) * 10 ** self.mass_order_of_magnitude
        ##### Random initial position with different order of magnitude
        self.p_0 = np.zeros([3 * self.n,1])
        for i in range(self.n):
            for k in range(3):
                self.p_0[3*i + k] = (2 * rand.random() - 1.0) * 10 ** self.distance_order_of_magnitude
        ##### Random initial velocity 1)pointing roughly to the spacial [0,0,0] 2)different order of magnitude
        self.dpdt_0 = np.zeros([3 * self.n,1])
        # for i in range(self.n):
        #     for k in range(3):
        #         self.dpdt_0[3*i + k] = sign_array[3*i + k] * rand.random() * 10 ** rand.randint(self.velocity_order_of_magnitude-3, self.velocity_order_of_magnitude)
        self.initial_condition_is_set_flag = True    


    def generate_better_initial_conditions(self):
        
        ##### Random mass vector with different mass magnitudes
        self.mass_vector = np.zeros([self.n,1])
        for i in range(self.n):
            self.mass_vector[i] = rand.randint(1,9) * 10 ** rand.randint(self.mass_order_of_magnitude - 3, self.mass_order_of_magnitude)
        ##### Random initial position with different order of magnitude
        self.p_0 = np.zeros([3 * self.n,1])
        for i in range(self.n):
            for k in range(3):
                self.p_0[3*i + k] = (2 * rand.random() - 1.0) * 10 **  rand.randint(self.distance_order_of_magnitude - 6, self.distance_order_of_magnitude)
        ##### Random initial velocity 1)pointing roughly to the spacial [0,0,0] 2)different order of magnitude
        self.dpdt_0 = np.zeros([3 * self.n,1])
        sign_array = -1 * np.sign(self.p_0)
        for i in range(self.n):
            for k in range(3):
                self.dpdt_0[3*i + k] = sign_array[3*i + k] * rand.random() * 10 ** rand.randint(self.velocity_order_of_magnitude-3, self.velocity_order_of_magnitude)
        self.initial_condition_is_set_flag = True                

    def generate_random_initial_conditions(self):
        '''
            Completely random initial position and velocities
        '''
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


