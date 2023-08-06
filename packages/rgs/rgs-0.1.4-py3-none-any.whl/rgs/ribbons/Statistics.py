'''
Created on Jan 30, 2021

@author: vladislavkargin
'''
import numpy as np
import matplotlib.pyplot as plt

import ribbons.Ribbon as rb
import ribbons.Tiling as tl
import ribbons.Utility as ut


'''
For testing methods
'''
def main():
    
    M = 10
    N = 100
    tiling = ut.randomStanleyTiling(M, N)
    tiling.draw(M, N, colormap = 'prism')

    
    plt.show()

if __name__ == '__main__':
    main()

