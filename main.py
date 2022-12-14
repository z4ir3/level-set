# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
from src import levelset as ls


def get_inputs():

    # Input data
    nx = 70
    x1 = -1
    x2 = 1
    y1 = -1
    y2 = 1
    t1 = 0
    t2 = 0.05

    Data = ls.get_data(nx = nx, x1 = x1, x2 = x2, y1 = y1, y2 = y2, t1 = t1, t2 = t2)    
    return Data




if __name__ == "__main__":    
    # Collect inputs
    Data = get_inputs()

    # Initialize quatrefoil
    Data = ls.init_quatrefoil(Data)

    # Call the main engine
    _ = ls.motion_under_curvature(Data)