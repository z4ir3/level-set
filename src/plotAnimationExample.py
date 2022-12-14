### EXAMPLE 1

# import matplotlib.pyplot as plt
# import numpy as np
# x = np.arange(6)
# y = np.arange(5)
# z = x * y[:,np.newaxis]
# for i in range(5):
#     if i==0:
#         p = plt.imshow(z)
#         fig = plt.gcf()
#         plt.clim()   # clamp the color limits
#         plt.title("Boring slide show")
#     else:
#         z = z + 2
#         p.set_data(z)
#     print("step", i)
#     plt.pause(0.5)
# breakpoint()



### EXAMPLE 2

# from pylab import *
# import matplotlib.pyplot as plt
# import numpy as np
# import time
# ion()
# x = linspace(-1,1,51)
# plt.plot(sin(x))
# for i in range(10):
#     plt.plot([sin(i+j) for j in x])
#     draw()      # redraw the canvas
#     pause(1)
# ioff()
# show()   
    

### EXAMPLE 3
    
# from pylab import *
# import time  
# ion()
# tstart = time.time()               # for profiling
# x = arange(0,2*pi,0.01)            # x-array
# line, = plot(x,sin(x))
# for i in arange(1,200):
#     line.set_ydata(sin(x+i/10.0))  # update the data
#     draw()                         # redraw the canvas
#     pause(0.01)
# print('FPS:', 200/(time.time()-tstart))
# ioff()
# show()


### EXAMPLE 4

import matplotlib.pyplot as plt
# import os
plt.ion()
x = []
y = []
# home = os.sep.join((os.path.expanduser('~'),'Desktop'))
for i in range(-100,100):
    x.append(i)
    y.append(i*i)
    plt.plot(x, y, 'g-', linewidth=1.5, markersize=4)
    plt.show()
    plt.pause(0.001)
plt.ioff()
plt.show()