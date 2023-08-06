'''
Created on Jul 21, 2020

@author: vladislavkargin
'''
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#import matplotlib.lines as mlines


import rgs.mndrpy.Utility as ut
#import mndrpy.ElementTL as tl


class Pairing(object):
    '''
    classdocs
    
    Non-crossing pairing on 2n point. Represented by a tuple prng,
    which is something like (3, 2, 1, 0) meaning that 0 is connected to 3
    and 1 is connected to 2. The tuple (1, 0, 3, 2) means that 0 connected to 1
    and 2 connected to 3. 
    
    Can also handle pairings with crossings. In this case a crossing matrix can be 
    calculated. 
    '''


    def __init__(self, path = None, prngArray = None):
        '''
        Constructor
        creates a pairing from a Dyck path (which is a sequence of 1 and -1), 
        or from an external pairing -- which is an array of numbers. 
        For example [3 2 1 0] pairs  0 with 3 and 1 with 2 
        '''
        if prngArray != None:
            self.prng = tuple(prngArray)
            return
        
        self.prng = []
        if path != None:
            stack = []
            self.prng = [0] * len(path)
            for i in range(len(path)):
                if path[i] == 1:
                    stack.append(i)
                else:
                    j = stack.pop(-1);
                    self.prng[i] = j;
                    self.prng[j] = i;    
        self.prng = tuple(self.prng)
        self.crossM = None #if the matrix is crossing this should be calculated
        #separately
        
    def __str__(self):
        return str(self.prng)
    
    def __eq__(self, other):
        '''Overrides the default implementation'''
        if isinstance(other, Pairing):
            if self.prng == other.prng: 
                return True
            else: 
                return False
        return False
    
    def __hash__(self):
        return hash(tuple(self.prng))
    
    def size(self):
        '''return n for a pairing on 2n objects '''
        return len(self.prng)//2
    
    def draw(self, ax = None, up = True, asPath = False):
        ''' draws the pairing. 
        If up is False, then draws it in the lower half-plane.
        If asPath is true, draws it as the corresponding Dyck path.
        '''
        
        if ax == None:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
        
        if not asPath:
            width = len(self.prng)
            ax.set_xlim(0, width)
            ax.set_ylim(-width/2, width/2)
            
            if up:
                theta1 = 0.0
                theta2 = 180.0
            else:
                theta1 = 180.0
                theta2 = 360.0
            for i in range(width):
                j = self.prng[i]
                xy = (i + (j - i)/2, 0)
                w = np.abs((j - i)/2)
                #print("i = " + str(i) + " j = " + str(j) + " xy = " + str(xy) 
                #      + " w = " + str(w))
                arc = mpatches.Arc(xy, 2*w, 2*w, 0, theta1, theta2)
                ax.add_patch(arc)
            #ax.grid(True)
            ax.xaxis.set_ticks(np.arange(0,width))
            ax.yaxis.set_ticks(np.arange(-width/2 + 1,width/2 , width/2 - 1))
        else: 
            path = prng2path(self)
            if up:
                ut.plotDyckPath(path, ax)
            else:
                ut.plotDyckPath(path, ax, method = "lowerLatticePath")
        pass

def randomPairing(n, w = None, seed = None):
    '''generates a (uniformly) random non-crossing pairing of length 2n
    If w != None, then generates a pairing from a Galton-Watson tree
    with weight sequence w'''
    if w == None:
        path = ut.randomDyckPath(n, seed = seed)
    else:
        tree = ut.randomTree(n + 1, w, seed = seed)
        path = ut.treeToDyckPath(tree)
    prng = Pairing(path)
    return prng

def randomCrossPairing(n, seed = None):
    ''' generate a random pairing of length 2n,
     which is allowed to have crossings.'''
    if seed != None:
        np.random.seed(seed)
    elements = list(range(2*n))
    prngArray = [0] * (2 * n)
    for k in range(0, 2*n, 2):
        ind1 = np.random.randint(2 * n - k)
        a = elements.pop(ind1)
        ind2 = np.random.randint(2 * n - k - 1)
        #print("ind2 = ",ind2)
        #print("elements = ", elements)
        b = elements.pop(ind2)
        prngArray[a] = b
        prngArray[b] = a
    return Pairing(prngArray = prngArray)

def calcCrossM(self):
    ''' calculate crossing matrix '''
    #TODO
    N = len(self.prng)
    self.crossM = np.zeros((N,N))

def addCrossing(prng, i, j):
    '''
    Add a crossing: if we have pairs (i l) (j k) then changes this to (i k) (j l)
    [if i and j are paired, does nothing]
    retunrs a prng with the crossing
    '''
    if prng.prng[i] == j:
        return prng
    else: 
        l = prng.prng[i]
        k = prng.prng[j]
        prngArray = list(prng.prng)
        prngArray[i] = k 
        prngArray[k] = i
        prngArray[j] = l
        prngArray[l] = j 
        return Pairing(prngArray = prngArray)
        
def standardPairing(n):
    '''
    creates the pairing of half-length n 
    that connects 0 to 1, 2 to 3, 4 to 5 and so on 
    '''
    p = Pairing()
    p.prng = [-1] * 2 * n
    for i in range(n):
        p.prng[2 * i] =  2 * i + 1
        p.prng[2 * i + 1] = 2 * i
    return p

def rainbowPairing(n):
    '''
    creates the rainbow that pairs 0 to 2n - 1, 1 to 2n-2 and so on
    '''
    p = Pairing()
    p.prng = [-1] * 2 * n
    for i in range(n):
        p.prng[i] = 2 * n - 1 - i
        p.prng[2 * n - 1 - i] = i
    return p


    

def rainbows(widths):
    '''
     * Creates a NC pairing on 2*n points that consists of rainbows.
     * The half-widths of rainbows are contained in widths array.
     * 
     * For example the array [n] should correspond to the identity pairing
     * and the array [1, 1, ..., 1] - to the standard pairing. 
     * 
     * @param widths array of half-widths of rainbows
     * @return a pairing
     '''
    N = sum(widths)
    prng = [0] * (2*N)
    pos = 0
    for j in range(len(widths)):
        w = widths[j];
        for i in range(w):
            prng[pos + i] = pos + (2 * w - 1 - i)
            prng[pos + (2 * w - 1 - i)] = pos + i
        pos = pos + 2 * w;
    return Pairing(prngArray = prng)

def smallRainbows(amounts, sizes):
    '''
    creates a random pairing whose arks are small rainbows of two types
    parameters:
    amounts: number of rainbows of every type 
    sizes: half-lengths of the types
    for example amounts = [3, 4] sizes = [2, 3]
    means that we will rhave 3 rainbows of half size 2 and 4 rainbows of 
    half-size 3
    '''
    widths = ([sizes[0]] * amounts[0]) + ([sizes[1]] * amounts[1])
    random.shuffle(widths)
    prng = rainbows(widths)
    return prng

def prng2path(prng):
    '''
     * Calculates a Dyck path from a NC pairing
     * 
     * 
     * @param pairing an NC pairing 
     * @return corresponding Dyck path [0 are up, 1 are down] [1 - up, -1 down]
     '''
    N = len(prng.prng)
    path = np.ones(N)

    for i in range(N):
        if prng.prng[i] < i :
            path[i] = -1
    return path;

     

'''
For testing methods
'''
def main():
    
    n = 4
    seed = None    
    prng = randomPairing(n, seed)
    #prng = standardPairing(n)
    #prng = rainbowPairing(n)
    #prng = randomPairing(n, w = [1, 1, 1])
    #prng = randomCrossPairing(n)
    #prng = smallRainbows([2,3],[1,4])
    print(prng.prng)
    print("Size is ", prng.size())
    prng.draw()
    
    path = prng2path(prng)
    print(path)
    ut.plotDyckPath(path)
    
   
    #newPrng = addCrossing(prng, 0, 1)
    #newPrng.draw()
    '''
    prng = Pairing(path = None, prngArray = [2, 3, 0, 1])
    prng.draw(up = False)
    prng2 = Pairing(path = None, prngArray = [1, 0, 3, 2])
    print(prng == prng2)
    print(hash(prng))
    '''
    

    
    plt.show()

if __name__ == '__main__':
    main()    
    