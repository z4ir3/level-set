# import time
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab
# from pylab import *
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
# from mpl_toolkits.mplot3d import axes3d, Axes3D


def get_data(nx = 100,
            x1 = -1,
            x2 = 1,
            y1 = -1,
            y2 = 1,
            t1 = 0,
            t2 = 0.005):
    '''
    '''

    Data = dict()
    
    # Input data
    Data["nx"] = nx                                                 # number of 1-dim spatial nodes
    Data["x1"] = x1                                                 # left xlim
    Data["x2"] = x2                                                 # right xlim
    Data["y1"] = y1                                                 # left ylim
    Data["y2"] = y2                                                 # right ylim        
    Data["t1"] = t1                                                 # initial time        
    Data["t2"] = t2                                                 # final time

    Data["x"] = np.linspace(Data["x1"],Data["x2"],Data["nx"])       # 1-dim x grid
    Data["y"] = np.linspace(Data["y1"],Data["y2"],Data["nx"])       # 1-dim y grid
    Data["h"] = abs(Data["x"][1] - Data["x"][0])                    # 1-dim step
    Data["X"] = np.meshgrid(Data["x"], Data["y"])[0]                # 2-dim X meshgrid
    Data["Y"] = np.meshgrid(Data["x"], Data["y"])[1]                # 2-dim Y meshgrid
    
    # Data["dt"] = 0.2 * Data["h"]**2                                 # temporal step
    Data["dt"] = 0.55 * Data["h"]**2                                 # temporal step
    Data["t"]  = np.arange(Data["t1"],Data["t2"],Data["dt"])        # time grid
    Data["nt"] = len(Data["t"])                                     # number of temporal nodes 

    return Data



def init_quatrefoil(Data,
                    ll = -0.8,
                    fontsize = 14): # altura del quatrefoil
    '''
    '''

    # Generate the Quatrefoil
    qfoil = [ [0 for i in range(Data["nx"])] for i in range(Data["nx"]) ]
    for i in range(0,Data["nx"]):
        for j in range(0,Data["nx"]):
            rr = 0.6 + 0.4 * np.sin(4.0 * math.atan(Data["y"][j] / Data["x"][i]))
            qfoil[i][j] = ll + np.sqrt(Data["x"][i]**2 + Data["y"][j]**2) / rr
    Data["U0"] = np.array(qfoil)

    # Plot
    fig = plt.figure(figsize=(16,6))
    fig.subplots_adjust(left = 0.01,
                        right = 0.98,
                        top = 0.92,
                        bottom = 0.1,
                        wspace = 0.01)

    ### Quatrefoil contour plot
    ax = fig.add_subplot(121)
    cs = ax.contour(Data["X"], Data["Y"], Data["U0"]) 
    ax.set_title("Initial Quatrefoil (contour plot)", fontsize=fontsize)
    ax.set_xlabel("x", fontsize=fontsize)
    ax.set_ylabel("y", fontsize=fontsize)
    ax.axis("square")
    # Plot isolines and level
    fmt = dict()
    for l, s in zip(cs.levels,cs.levels):
        fmt[l] = np.round(s,2)
    plt.clabel(cs, cs.levels, inline=True, fmt=fmt, fontsize=9)


    ### Quatrefoil 3D plot  
    ax = fig.add_subplot(122, projection = "3d")
    surf = ax.plot_surface(Data["X"], 
                        Data["Y"],
                        Data["U0"],
                        cmap = cm.viridis)
    ax.set_title("Initial Quatrefoil (3D plot)", fontsize=fontsize)
    ax.set_xlabel("x", fontsize=fontsize)
    ax.set_ylabel("y", fontsize=fontsize)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    plt.colorbar(surf, ax=ax, shrink=0.5, location="right", aspect=12, pad = 0.1)

    plt.show()        

    return Data



def motion_under_curvature(Data,
                            setpause = 0.00001): 
    '''
    '''
    # Initial U0
    U0 = Data["U0"].copy()
    Utemp = U0 

    # Derivatives index 
    ip = [n for n in range(1,Data["nx"])] + [0]
    im = [Data["nx"]-1] + [n for n in range(Data["nx"]-1)]

    # Setup figure
    fig = plt.figure(figsize=(16,6))
    fig.subplots_adjust(left = 0.06,
                        right = 0.97,
                        top = 0.85,
                        bottom = 0.1,
                        wspace = 0.06)
    ax1 = fig.add_subplot(131)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax2 = fig.add_subplot(132)
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    
    # On
    pylab.ion()

    # Main loop over time
    for n in range(0,Data["nt"]):
        
        # Spatial loop for updating the mesh
        for i in range(0,Data["nx"]):
            for j in range(0,Data["nx"]):

                # First-order derivatives
                px = ( U0[ip[i]][j] - U0[im[i]][j] ) / (2*Data["h"])
                py = ( U0[i][ip[j]] - U0[i][im[j]] ) / (2*Data["h"])

                # Second-order derivatives
                pxx = ( U0[ip[i]][j] - 2*U0[i][j] + U0[im[i]][j] ) / (Data["h"]**2)
                pyy = ( U0[i][ip[j]] - 2*U0[i][j] + U0[i][im[j]] ) / (Data["h"]**2)
                pxy = ( U0[ip[i]][ip[j]] + U0[im[i]][im[j]] - U0[im[i]][ip[j]] - U0[ip[i]][im[j]]) / (4*Data["h"]**2)
        
                # Curvature gradient 
                agrad2 = px**2 + py**2 + 0.001
                curvegrad = (pxx * py**2 - 2.0*px*py*pxy + pyy*px**2) / agrad2

                # New mesh
                Utemp[i][j] = U0[i][j] + curvegrad * Data["dt"]

        fig.suptitle("Motion under the curvature (t={:.5f}/{:.5f})".format(Data["t"][n],Data["t"][-1]))

        # Plot all level sets 
        ax1.contour(Data["X"],Data["Y"],Utemp)
        ax1.set_title("Quatrefoil's level sets")
        ax1.axis("square")
        ax1.set_xlabel("x")
        ax1.set_ylabel("y")
    
        # Plot the level set 0
        ax2.contour(Data["X"],Data["Y"],Utemp,0) 
        ax2.set_title("Quatrefoil's level set 0")
        ax2.axis("square")
        ax2.set_xlabel("x")
        # ax2.set_ylabel("y")
        ax2.set_yticks([])
        
        # Plot the surface 
        ax3.plot_surface(Data["X"],
                        Data["Y"], 
                        Utemp, 
                        cmap = cm.viridis)
        ax3.set_title("Quatrefoil's 3D plot")
        ax3.set_xlabel("x")
        ax3.set_ylabel("y")
        ax3.zaxis.set_major_locator(LinearLocator(10))
        ax3.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))

        # Draw current figure and pause image
        plt.draw()
        plt.pause(setpause)

        if n < Data["nt"]-1:
            ax1.clear()
            ax2.clear()
            ax3.clear()
                
        # Update current function for next plot             
        U0 = Utemp
    
    # Off
    pylab.ioff()

    # Dejar el plot.show si la window con los plots se cierra
    plt.show()