'''
Created on Jan 20, 2021

@author: vladislavkargin
'''

import numpy as np
import matplotlib.pyplot as plt
import ribbons.Ribbon as rb

class Tiling(object):
    '''
    classdocs
    '''


    def __init__(self, ribbons):
        '''
        Constructor
        ribbons is a list of ribbons
        '''
        self.ribbons = ribbons
        
    def __str__(self):
        ''' Returns a string representation of this tiling
        return the graph'''
        s = ''
        for ribbon in self.ribbons:
            s = s + '\n' + str(ribbon)
        return s 
    
    def draw(self, M, N, ax = None, block = False, MaxLength = None, colormap = 'jet'):
        ''' M is the height and N is the width of the plot'''
        if (ax == None):
            fig, ax = plt.subplots()
        else:
            fig = ax.figure
            
        ax.set_xlim(0, N)
        ax.set_ylim(0, M)
        
        if MaxLength == None:
            MN = 3 * int(np.log2(max([M, N])))
        print(MN)
        for ribbon in self.ribbons:
            ribbon.draw(ax, MaxLength = MN, colormap = colormap)
        
        if block:            
            plt.show()
        else:
            plt.draw()
        return fig, ax

''' 
For testing methods
'''
def main():
    print('Ribbon tiling methods are used')  
    ribbon1 = rb.Ribbon(0, 0, [0, 1])
    ribbon2 = rb.Ribbon(0, 1, [1, 0])
    
    tiling = Tiling([ribbon1, ribbon2]) 
    fig, ax = plt.subplots()
    print(tiling)
    tiling.draw(10, 10, ax = ax)
    plt.show()
    
if __name__ == "__main__":
    main() 