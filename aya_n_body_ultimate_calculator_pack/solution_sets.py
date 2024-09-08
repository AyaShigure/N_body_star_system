from .baby_math import *
from .n_body_class import *

def solution_1():
    '''
        A 6-body solution
    '''
    multibody_system = n_body_system(6)
    multibody_system.mass_order_of_magnitude = 30
    multibody_system.distance_order_of_magnitude = 9
    multibody_system.velocity_order_of_magnitude = 5.5
    multibody_system.generate_neat_symmetric_initial_conditions()

    return multibody_system

def solution_2():
    '''
        Like solution 1 but 3-body
    '''
    multibody_system = n_body_system(3)
    multibody_system.mass_order_of_magnitude = 30
    multibody_system.distance_order_of_magnitude = 9
    multibody_system.velocity_order_of_magnitude = 5.3
    multibody_system.generate_neat_symmetric_initial_conditions()

    return multibody_system

def solution_3():
    '''
        Like solution 1 & 2 but 10-body
    '''
    multibody_system = n_body_system(10)
    multibody_system.mass_order_of_magnitude = 30
    multibody_system.distance_order_of_magnitude = 10
    multibody_system.velocity_order_of_magnitude = 5
    multibody_system.body_radius = 0.03
    multibody_system.generate_neat_symmetric_initial_conditions()
    return multibody_system

def solution_4():
    multibody_system = n_body_system(3)

    return multibody_system

def solution_5():
    multibody_system = n_body_system(3)

    return multibody_system

def solution_6():
    multibody_system = n_body_system(3)

    return multibody_system

def solution_7():
    multibody_system = n_body_system(3)

    return multibody_system

def solution_8():
    multibody_system = n_body_system(3)

    return multibody_system

def solution9():
    multibody_system = n_body_system(3)

    return multibody_system

def solution_10():
    multibody_system = n_body_system(3)

    return multibody_system


