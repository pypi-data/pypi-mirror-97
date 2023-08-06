'''
Created on Jan 17, 2021

@author: vladislavkargin
'''

#import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class Ribbon(object):
    '''
    classdocs
    '''


    def __init__(self, x, y, shape):
        '''
        creates a ribbon with root square s_{xy} (south-west corner is at (x, y))
        and a list of 0 and 1 that determines the shape. 
        0 means go right, 1 means go up. This list can be empty which will 
        corresponds to a ribbon tile that consist of a single square. 
        '''
        self.x = x 
        self.y = y 
        self.shape = shape
        
    def __str__(self):
        '''
        Returns a string representation of this ribbon.
        return the graph
        '''
        s = '(' + str(self.x) + ',' + str(self.y) + '), ' + str(self.shape)
        return s       
    
    def draw(self, ax = None, block = False, MaxLength = None, colormap = 'prism'):
        if (ax == None):
            fig, ax = plt.subplots()
        else:
            fig = ax.figure
        
        
        cmap = cm.get_cmap(colormap)
        if MaxLength == None:
            MaxLength = len(self.shape) + 5
        else: 
            MaxLength = max([MaxLength, len(self.shape)])
        
        c = cmap(len(self.shape)/MaxLength)
        
        rectangle = plt.Rectangle((self.x,self.y), 1, 1, fc=c ,ec="black")
        ax.add_patch(rectangle)
        
        sx = self.x
        sy = self.y
        for i in range(len(self.shape)):
            if self.shape[i] == 0:
                rectangle = plt.Rectangle((sx,sy), 2, 1, fc=c,ec="black")
                ax.add_patch(rectangle)
                if i > 0 and self.shape[i - 1] == 0:
                    line = plt.Line2D((sx, sx),(sy, sy + 1), color = c)
                    ax.add_line(line)
                elif i > 0 and  self.shape[i - 1] == 1:
                    line = plt.Line2D((sx, sx + 1),(sy, sy), color = c)
                    ax.add_line(line) 
                sx = sx + 1 
            else:
                rectangle = plt.Rectangle((sx,sy), 1, 2, fc=c,ec="black")
                ax.add_patch(rectangle) 
                if i > 0 and self.shape[i - 1] == 0:
                    line = plt.Line2D((sx, sx),(sy, sy + 1), color = c)
                    ax.add_line(line)
                elif i > 0 and  self.shape[i - 1] == 1:
                    line = plt.Line2D((sx, sx + 1),(sy, sy), color = c)
                    ax.add_line(line) 
                sy = sy + 1
            
            
        if block:            
            plt.show()
        else:
            plt.draw()
        return fig, ax
'''
For testing methods
'''
def main():
    print('Ribbon methods are used')  
    ribbon = Ribbon(0, 0, [0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1]) 
    _, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    print(ribbon)
    ribbon.draw(ax = ax)
    plt.show()
    
if __name__ == "__main__":
    main() 
    
    