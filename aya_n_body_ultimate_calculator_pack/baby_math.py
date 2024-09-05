# Baby math and other utility functions
import numpy as np
from tqdm import tqdm
def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, np.cos(theta),-np.sin(theta)],
                   [ 0, np.sin(theta), np.cos(theta)]])
def Ry(theta):
  return np.matrix([[ np.cos(theta), 0, np.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-np.sin(theta), 0, np.cos(theta)]])
def Rz(theta):
    return np.matrix([[ np.cos(theta), -np.sin(theta), 0 ],
                    [ np.sin(theta), np.cos(theta) , 0 ],
                    [ 0           , 0            , 1 ]])


def update_gravtational_interaction_matrix(p):
    n = int(p.shape[0]/3) # Get the column number/number of the bodies
    F_dir = np.zeros([3 * n, n]) # empty gravtational_interaction_matrix

    p_i = np.zeros([3,1])
    p_j = np.zeros([3,1])

    for i in range(n):
        for k in range(3):
            p_i[k] = p[i * 3 + k] 
        for j in range(n):
            if i == j: # Diagonal 
                F_dir[i*3+0,j] = 0.0
                F_dir[i*3+1,j] = 0.0
                F_dir[i*3+2,j] = 0.0
            elif j > i: # Upper triangle exculding the diagnal
                for k in range(3):
                    p_j[k] = p[j * 3 + k]
                F_ij = (p_j - p_i) / np.linalg.norm(p_j - p_i)**3
                
                for k in range(3):
                    F_dir[i * 3 + k, j] = F_ij[k].item()
                    F_dir[j * 3 + k, i] = -1. * F_ij[k].item()
            else:
                pass 
    return F_dir



# Euler's method, integration from start till the end, only for referencing
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