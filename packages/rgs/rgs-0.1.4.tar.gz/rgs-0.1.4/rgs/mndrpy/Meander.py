'''
Created on Jul 23, 2020

@author: vladislavkargin
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm

import rgs.mndrpy.Pairing as pr
import rgs.mndrpy.Utility as ut


class Meander(object):
    '''
    classdocs
    '''


    def __init__(self, uPairing, dPairing, uprngArray = None,
                    dprngArray = None):
        '''
        Constructor
        Makes the meander from upper and lower pairings
        arguments:
        uPairing, dPairing -- upper and lower parings (as objects or lists)
        
        The other pair of arguments is obsolete (poor design),
        kept only for compatibility with some other functions. 
        uprgnArray, dprngArray -- upper and lower pairings (as lists)
        '''
        if type(uPairing) is list:
            self.uPairing = pr.Pairing(prngArray = uPairing)
        elif uPairing == None:
            self.uPairing = pr.Pairing(prngArray = uprngArray)
        else: 
            self.uPairing = uPairing
            
        if type(dPairing) is list:
            self.dPairing = pr.Pairing(prngArray = dPairing)
        elif uPairing == None:
            self.dPairing = pr.Pairing(prngArray = dprngArray)
        else: 
            self.dPairing = dPairing
        
        
    def __str__(self):
        return str(self.uPairing) + ", " + str(self.dPairing)
    
    def __eq__(self, other):
        '''Overrides the default implementation'''
        if isinstance(other, Meander):
            if self.uPairing == other.uPairing and self.dPairing == other.dPairing: 
                return True
            else: 
                return False
        return False
    
    def __hash__(self):
        return hash(self.uPairing) + 17 * hash(self.dPairing)
    
    def draw(self, ax = None, drawCycles = False, palette = "jet"):
        if ax == None:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
        fig = ax.figure
        self.uPairing.draw(ax = ax)
        self.dPairing.draw(ax = ax, up = False)
        if drawCycles == True:
            colormap = cm.get_cmap(palette, 128)
            cycles, _ = self.findCycles()
            for i in range(len(cycles)):
                col = colormap(i/len(cycles))
                #print(i, col)
                self.drawCycle(cycles[i], ax, color = col) 
        return fig, ax
    
    def drawCycle(self, cycle, ax = None, color = "red"):
        if ax == None:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            width = len(self.uPairing.prng)
            ax.set_xlim(0, width)
            ax.set_ylim(-width/2, width/2)
        for c, i in enumerate(cycle):
            j = cycle[(c + 1) % len(cycle)]
            xy = (i + (j - i)/2, 0)
            w = np.abs((j - i)/2)
            if c % 2 == 0:
                theta1 = 0.0
                theta2 = 180.0
            else:
                theta1 = 180.0
                theta2 = 360.0
            arc = mpatches.Arc(xy, 2*w, 2*w, 0, theta1, theta2, color = color)
            ax.add_patch(arc)
    
    def isProper(self):
        '''checks if this system has only one cycle'''  
        N = len(self.uPairing.prng)
        #print(N)
        next_v = self.uPairing.prng[0]
        up = False 
        counter = 0    
        while next_v != 0 and counter <= 2*N:
            counter = counter + 1
            if up == True:
                next_v = self.uPairing.prng[next_v]
                up = False
            else:
                next_v = self.dPairing.prng[next_v]
                up = True
        if counter == N - 1:
            return True
        else:
            return False
        
    def  isIrreducible(self):
        '''checks if the meander is irreducible. (It is somewhat different
        then irreducible meanders in the sense of Zvonkin-Lando.)'''
        if self.isProper():
            return True   
        cycles, _ = self.findCycles()
        for cycle in cycles:
            if len(cycle) == max(cycle) - min(cycle) + 1:
                return False
        return True
    
        
    def findCycles(self):
        ''' finds all cycles in the meander and stores them in two structures
        cycles - which is an array of arrays that represent cycles
        cyclesInd - which is an 2n-array with each element marked by 
        the number of the cycle that it belongs to.
        '''
        N = len(self.uPairing.prng)
        c = 0
        up = True #shows which pairing we are going to use in tracking 
        cycles = []
        cyclesInd = [-1] * N
        
        for i in range(N):
            if cyclesInd[i] == -1:
                c = c + 1
                cyclesInd[i] = c
                cycle = [i]
                if up:
                    next_v =  self.uPairing.prng[i]
                    up = False
                else:
                    next_v =  self.dPairing.prng[i]
                    up = True
                #the following cycle can go in infinite loop if one of the
                #pairing is invalid for this reason we break it 
                # if it go for more than N iterations.
                # The result is invalid and likely to break the following programs
                counter = 0
                while (next_v != i and counter <= 2 * N):
                    cyclesInd[next_v] = c
                    cycle.append(next_v)
                    if up:
                        next_v =  self.uPairing.prng[next_v]
                        up = False
                    else:
                        next_v =  self.dPairing.prng[next_v]
                        up = True
                    counter = counter + 1
                cycles.append(cycle)
                if counter > 2 * N:
                    print( "findCycles Warning:")
                    print(" An infinite loop in find components was broken")
                    print(" A likely problem with validity of one of the pairings")
        return cycles, cyclesInd
     
    def calcCycleLengths(self):
        ''' caclulate the lengths of all cycles in the meander'''
        (cycles, _) = self.findCycles()
        lengths = []
        for cycle in cycles:
            lengths.append(len(cycle))
        return lengths
        
         
def randomMeander(n, w = None, seed = None):
    ''' generates a uniformly random meander on half-length n.
    If 2-tuple w != None, generates a meander with pairings distributed 
    according to weights w1 and w2'''
    if seed != None:
        np.random.seed(seed)
    if w == None:
        uP = pr.randomPairing(n)
        dP = pr.randomPairing(n)
    else:
        uP = pr.randomPairing(n, w[0])
        dP = pr.randomPairing(n, w[1])
    mndr = Meander(uP, dP)
    return mndr

def randomCrossSemiMeander(n, seed = None):
    '''generate a random crossing semi-meander'''
    if seed != None:
        np.random.seed(seed)
    uP = pr.randomCrossPairing(n)
    dP = pr.rainbowPairing(n)
    mndr = Meander(uP, dP)
    return mndr
    

def randomComb(n, seed = None):
    ''' generates a random comb meander of half-length n'''
    if seed != None:
        np.random.seed(seed)
    uP = pr.randomPairing(n)
    dP = pr.standardPairing(n)
    mndr = Meander(uP, dP)
    return mndr

def randomSemiMeander(n, seed = None):
    ''' generates a random meander of half-length n that have a random pairing
    on top and the rainbow pairing in the bottom'''
    
    if seed != None:
        np.random.seed(seed)
    uP = pr.randomPairing(n)
    dP = pr.rainbowPairing(n)
    mndr = Meander(uP, dP)
    return mndr

def rainbowMeander(uWidths, dWidths):
    '''
    generates a rainbow meander.
    Parameters:
    uWidths, dWidths -- sizes of the meanders on the top and on the bottom.
    returns a meander
    '''  
    N = sum(uWidths)
    M = sum(dWidths)
    if M != N:
        print("Rainbow meander says: the total sizes of upper and lower meanders")
        print("should be the same. N = ", N, " and M = ", M)
        return 
    uP = pr.rainbows(uWidths)
    dP = pr.rainbows(dWidths)
    return Meander(uP, dP)

def smallRainbowsMeander(amounts, sizes):
    '''
    creates a random meander whose pairings are collections of small rainbows
    '''
    uP = pr.smallRainbows(amounts, sizes)
    dP = pr.smallRainbows(amounts, sizes)
    return Meander(uP, dP)

def drawAsPolygon(mndr):
    ''' draws meander as polygon. The upper pairing is represented
    by a Dyck path above the diagonal y = x, and the lower pairing
    is represented by a Dyck path below the main diagonal. 
    '''
    upath = pr.prng2path(mndr.uPairing)
    ax = ut.plotDyckPath(upath)
    dpath = pr.prng2path(mndr.dPairing)
    ax = ut.plotDyckPath(dpath, ax = ax, method = "lowerLatticePath")
    return ax    
    
'''
For testing methods
'''
def main():
    
    #n = 100
    #seed = None    
    #mndr = randomMeander(n, seed = seed)
    #mndr = randomComb(n, seed = seed)
    #mndr = randomSemiMeander(n, seed = seed)
    #mndr = randomMeander(n, w = ([1,1,1],[1,1,1]), seed = seed)
    #mndr = randomCrossSemiMeander(n)
    amounts = [20, 20]
    sizes = [1, 5]
    mndr = smallRainbowsMeander(amounts, sizes)
    
    print(str(mndr))
    _, ax = mndr.draw(drawCycles = True)
    
    (cycles, cyclesInd) = mndr.findCycles()
    print("Cycles = " + str(cycles))
    print("CyclesInd = " + str(cyclesInd))
    
    lengths = mndr.calcCycleLengths()
    print("Cycle lengths = " + str(lengths))
    
    maxL = max(lengths)
    i = lengths.index(maxL)
    
    print("The length of the largest cycle is " + str(maxL))
    
    mndr.drawCycle(cycles[i], ax = ax)
    
    print("Hash = ", hash(mndr))
    print("Meander? ", mndr.isProper())
    print("Irreducible? ", mndr.isIrreducible())
    
    
    
    ''' Picture for the paper about meanders'''
    
    uWidths = [15, 5, 11]
    dWidths = [18, 13]
    mndr = rainbowMeander(uWidths, dWidths)
    _, ax = mndr.draw(drawCycles = True)  
    (cycles, cyclesInd) = mndr.findCycles()
    print("Cycles = " + str(cycles))
    print("CyclesInd = " + str(cyclesInd))
    lengths = mndr.calcCycleLengths()
    print("Cycle lengths = " + str(lengths))
    maxL = max(lengths)
    i = lengths.index(maxL)
    print("The length of the largest cycle is " + str(maxL))
    mndr.drawCycle(cycles[i], ax = ax)
    
    drawAsPolygon(mndr)
    
    plt.show()


if __name__ == '__main__':
    main()          
        
        