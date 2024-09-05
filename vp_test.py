import vpython
from vpython import *
import numpy as np


x1,y1,z1,x2,y2,z2,x3,y3,z3 = np.load('./data.npy')
# print(x1,y1,z1,x2,y2,z2,x3,y3,z3)

# canvas(resizable=True, width=600, height=300, background=color.white)
ball1 = vpython.sphere(color = color.green, radius = 0.3, make_trail = True, retain=40)
ball2 = vpython.sphere(color = color.red, radius = 0.3, make_trail = True, retain=40)
ball3 = vpython.sphere(color = color.blue, radius = 0.3, make_trail = True, retain=40)


print('start')
i = 0

while 1:
    rate(60)
    i = i + 1
    i = i % len(x1)
    
    # ball1.pos = vector(x1[i], z1[i], y1[i])
    # ball2.pos = vector(x2[i], z2[i], y2[i])
    # ball3.pos = vector(x3[i], z3[i], y3[i])
    ball1.pos = vector(x1[i],y1[i], z1[i])
    ball2.pos = vector(x2[i],y2[i], z2[i])
    ball3.pos = vector(x3[i],y3[i], z3[i])