'''
Created on Aug 29, 2020

@author: vladislavkargin
'''

''' Various function for SlimTree paper '''

import numpy as np
import matplotlib.pyplot as plt

import rgs.pmaps.OrderedTree as ot
import rgs.pmaps.TreeUtility as tutil

def slimTree():
    pass



'''
For testing methods
'''
def main():
    
    '''
    We plot several processes for a given tree: contour, Lukasiewisz and height
    
    '''
    n = 8
    w = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #w = [1, 0, 1]
    seed = 123
    _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    
    tree = ot.randomTree(n, w, SEED = seed)
    tree.draw(drawLabels = True, ax = ax1)
    print(tree)
    path = tutil.treeToDyckPath(tree)
    DyckPath = np.concatenate(([0], np.cumsum(path)))
    ax2.plot(DyckPath)
    for i in range(len(path)):
        if path[i] == 1:
            ax2.plot(i + 1, DyckPath[i + 1],'ro')
    ax2.grid(True)
    ax2.set_title("Contour")
    ax2.set_xticks(list(range(2*n-1)))
    ax2.set_yticks(list(range(max(DyckPath))))
    
    path = tutil.treeToLukasPath(tree)
    LukasPath = np.concatenate(([0], np.cumsum(path)))
    ax3.plot(LukasPath)
    ax3.grid(True)
    ax3.set_title("Lukasiewics")
    ax3.set_xticks(list(range(n + 1)))
    ax3.set_yticks(list(range(-1, max(LukasPath))))
    
    HeightPath = tutil.treeToHeightPath(tree)
    ax4.plot(HeightPath)
    ax4.grid(True)
    ax4.set_title("Height")
    ax4.set_xticks(list(range(n + 1)))
    ax4.set_yticks(list(range(0, max(HeightPath))))
    
    
    
    
    n = 21
    w = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    seed = 74
    path1 = tutil.randomBridge(n, w, SEED = seed)
    print(path1)
    walk1 = np.concatenate(([0],np.cumsum(path1)))
    print(walk1)
    walk2 = np.concatenate(([0],np.cumsum(tutil.cyclicShift(path1))))
    print(walk2)
    
    
    _, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    ax1.plot(walk1)
    ax2.plot(walk2)
    ax1.grid(True)
    ax1.set_xticks(list(range(0,n + 1,2)))
    ax2.grid(True)
    ax2.set_xticks(list(range(0,n + 1,2)))
    ax2.set_yticks(list(range(-1, max(walk2))))
    
    plt.show()
    pass

if __name__ == '__main__':
    main()