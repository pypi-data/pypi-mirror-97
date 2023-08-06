'''
Created on Aug 14, 2020

@author: vladislavkargin
'''
import rgs.mndrpy.Meander as Meander
import rgs.mndrpy.Utility as ut
import rgs.mndrpy.Pairing as pg


import numpy as np
import itertools 
import matplotlib.pyplot as plt
#from progress.bar import Bar

def enumPropMeanders(n):
    ''' enumerates proper Meanders on [2n]. (Obviously, n cannot be too large.)
    '''
    meanders = set([])
    for uPrng in ut.genPairings(n):
        for dPrng in ut.genPairings(n):
            mndr = Meander.Meander(uPrng, dPrng)
            if mndr.isProper():
                meanders.add(mndr)
    return meanders       

def enumIrrMeanders(n):
    ''' enumerates irreducible Meanders on [2n]. (Obviously, n cannot be too large.)
    '''
    meanders = set([])
    for uPrng in ut.genPairings(n):
        for dPrng in ut.genPairings(n):
            mndr = Meander.Meander(uPrng, dPrng)
            if mndr.isIrreducible():
                meanders.add(mndr)
    return meanders     

def rotationNumber(cycle):
    '''calculate the rotation number for a cycle
    The input is a permuted list of numbers from 0 to 2n - 1 that starts with 0.
    It represents a cycle in the plane (a meander with self-intersections allowed)
    For example (0 2 1 3) represents a cycle formed by arcs (0 2) and (1 3) in 
    the upper-halfplane and arcs (2 1) (3 0) in the lower half-plane
    The function returns the rotation number for this cycle. For example, for this
    cycle the rotation number is 2. For non-crossing meanders the rotation number
    is always 0. '''
    if len(cycle)%2 != 0:
        print("Rotation Number says: The length of the cycle must be even!")
        return
    n = int(len(cycle)/2)
    #print(n)
    rn = 0
    for i in range(2*n):
        if cycle[(i + 1)%(2*n)] > cycle[i]:
            rn = rn + (-1)**(i%2)
        else:
            rn = rn - (-1)**(i%2)
    return int(rn/2) 
    
def rnDistribution(n):
    ''' Calculates the distribution of rotation numbers for all cycles of length 
    2n '''
    counts = {}
    for cycle in itertools.permutations(range(1,2 * n)):
        cycle2 = [0] + list(cycle)
        #print(cycle2)
        rn = rotationNumber(cycle2)
        if rn in counts:
            counts[rn] = counts[rn] + 1
        else:
            counts[rn] = 1
    return counts

def cycleLenDistr(n):
    ''' calculates the distribution of meander systems over cycle lengths 
    (exactly). Returns smth like [8 12 5] which means 8 meander systems with 
    only one cycle (proper meanders), 12 - with two cycles and 5 with 3 cycles'''
    
    D = [0] * n
    for mndr in ut.allMeanders(n):
        cycles, _ = mndr.findCycles()
        c = len(cycles)
        D[c - 1] = D[c - 1] + 1
    return D
    
def areaDyckPathDistr(n):
    ''' calculate the distribution of all Dyck Paths by area (Carlitz'
    variant of q-Catalan numbers)'''
    
    D = [0] * (n*(n-1)//2 + 1) #this is possible values for area
    for prng in ut.allPairings(n):
        path = pg.prng2path(prng)
        area = ut.areaDyckPath(path)
        D[area] += 1
    return D
        
   
   
'''
For testing methods
'''
def main():
    #n = 7
    n = 4
    meanders = enumPropMeanders(n)
    print(len(meanders))
    #print(list(map(str,meanders)))
    
    meanders = enumIrrMeanders(n)
    print(len(meanders))
    #print(list(map(str,meanders)))
    
    print(list(itertools.permutations(range(1,n))))
    cycle = [0, 1, 5, 2, 4, 3]
    mndr = ut.makeMeanderFromCycle(cycle)
    print(mndr)
    mndr.draw()
    rn = rotationNumber(cycle)
    print("Rotation number = ", rn) 
    
    cycle = [0, 5, 1, 4, 2, 3]
    mndr = ut.makeMeanderFromCycle(cycle)
    print(mndr)
    mndr.draw()
    rn = rotationNumber(cycle)
    print("Rotation number = ", rn) 
    
    
    n = 5
    counts = rnDistribution(n) #6 is max that it can do in reasonable time
    print(counts)
    
    '''calculate cycle length distribution for meander systems
    and study its properties ''' 
    n = 5 #n = 9 takes a rather long although reasonable time. 
    D = cycleLenDistr(n)
    print(D)
    
        
    rts = np.roots(D)
    print(rts)
    X = [z.real for z in rts]
    Y = [z.imag for z in rts]
    plt.figure()
    plt.scatter(X, Y, color = "red")
    
    print("Value of cycle distribution polynomial at -1 is ", 
          np.polyval(np.flip(D),-1))   
    
    '''now let us study the properties of the distribution 
    of Dyck paths by area'''
    
    n = 5
    D = areaDyckPathDistr(n)
    print("Distribution by area: ", D)
    rts = np.roots(D)
    print(rts)
    X = [z.real for z in rts]
    Y = [z.imag for z in rts]
    plt.figure()
    plt.scatter(X, Y, color = "red")
     
    plt.show()

if __name__ == '__main__':
    main()