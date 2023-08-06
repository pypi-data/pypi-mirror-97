'''
Created on Jul 21, 2020

@author: vladislavkargin
'''
import numpy as np
from scipy import linalg as la
import matplotlib.pyplot as plt
import os

import rgs.pmaps.OrderedTree as ot
import rgs.mndrpy.Pairing as pg
import rgs.mndrpy.Meander as mr

    
def randomDyckPath(n, seed = None):
    '''
     * Generates a random Dyck path with 2n steps
     * 
     * @param n half-size of path
     * @return a sequence of -1 and 1 steps.
    '''
    
    if seed != None:
        np.random.seed(seed)
    path = [1] * n + [-1] * (n + 1)   
    #shuffle randomly
    np.random.shuffle(path)
    
    #do a cyclic shift. 
    #Find the first occurrence of the minimum
    S = np.cumsum(np.array([0] + path))
    '''
    fig1, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.plot(S)
    ax1.grid(True)
    '''
    m = np.min(S)
    positions = np.where(S == m)[0]
    pos = positions[0]
    #print(pos)
    path1 = path[pos:] + path[:pos]
    del path1[-1]
    return path1

def plotDyckPath(path, ax = None, method = "upperLatticePath"):
    ''' plots a Dyck path. Path is either list of 1, -1 or numpy array
    of 1, - 1'''
    if isinstance(path, list):
        n = int(len(path)/2)
    else:
        n = int(path.shape[0]/2)
    x = 0
    y = 0
    S = [(x, y)]
    if method == "upperLatticePath":
        for i in range(2 * n):
            if path[i] == 1:
                y += 1
            else:
                x += 1
            S.append((x,y))
    else:         
        for i in range(2 * n):
            if path[i] == 1:
                x += 1
            else:
                y += 1
            S.append((x,y))
    #print(S)
    X, Y = list(zip(*S)) 
    #print(X)
    #print(Y)
    if ax == None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
    major_ticks = np.arange(0, n + 1, 1)
    #minor_ticks = np.arange(0, 101, 5)
    ax.set_xticks(major_ticks)
    #ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    #ax.set_yticks(minor_ticks, minor=True)
    # And a corresponding grid
    ax.grid(which='both')
    ax.plot(X, Y)
    Z = range(n + 1)
    ax.plot(Z)
    return ax  


def areaDyckPath(path):
    ''' calculate the area of the Dyck path, defined as the number
    of unit squares under the path but above the line y = x'''
    if isinstance(path, list):
        n = int(len(path)/2)
    else:
        n = int(path.shape[0]/2)
    x = 0
    y = 0
    S = [(x, y)]
    for i in range(2 * n):
        if path[i] == 1:
            y += 1
        else:
            x += 1
        S.append((x,y))
    area = 0
    y_prev = 0
    for p in S: #every time as y increases, we add y - x - 1 to the area
        if p[1] > y_prev:
            area += p[1] - p[0]- 1
            y_prev = p[1]
    return area

def areaMeander(mndr):
    '''calculates the area of a meander system defined as the area 
    of the polygone that has the Dyck path for the upper pairing
    as its upper boundary and the reflected Dyck path for the lower
    pairing as its lower boundary. The size of the meander is subtracted
    for normalization, so the area of the standard meander system is 0'''
    area = areaDyckPath(pg.prng2path(mndr.uPairing))
    area += areaDyckPath(pg.prng2path(mndr.dPairing))
    #area += mndr.size()
    return area

def genPairings(n):
    '''This is a generator that yields all (non-crossing) Pairings on [2n].
     Not all of them are different. The algorithm simply generates 2^{2n + 1}
     walks on Z, chooses those that sum to -1 (bridges) 
     and rotate each of them to a Dyck path.
     Then it converts the path to a pairing. 
     Of course it will be difficult to exhaust all paths for large n.
     '''
    y = 0
    width = 2 * n + 1
    while y < 2 ** width: 
        walk = [2 * int(x) - 1 for x in '{:0{size}b}'.format(y,size=width)]
        if sum(walk) != -1:
            y = y + 1
            continue 
        else:
            y = y + 1
            #do a cyclic shift. 
            #Find the first occurrence of the minimum
            S = np.cumsum(np.array([0] + walk))
            m = np.min(S)
            positions = np.where(S == m)[0]
            pos = positions[0]
            walk1 = walk[pos:] + walk[:pos]
            del walk1[-1]
            yield pg.Pairing(path = walk1)
            
def allPairings(n):   
    '''returns a list of all pairings of length 2n'''     
    A = set([])
    for pairing in genPairings(n):
        A.add(pairing)
    return list(A)

def allMeanders(n):
    ''' returns all meander systems of length 2n. '''
    B = []
    A = allPairings(n)
    for p in A:
        for q in A:
            mndr = mr.Meander(p, q)
            B.append(mndr)
    return B

def dot(p, q):
    ''' calculates the dot product of two pairings, which is 
    the number of cycles in the resulting meander.
    Parameters: p and q - pairings'''
    mndr = mr.Meander(p, q)
    cycles, _ = mndr.findCycles()
    c = len(cycles)
    return c

def dotMatrix(n):
    ''' calculate the matrix of all dot products among non-crossing pairings of 
    length 2n.'''
    A = allPairings(n)
    N = len(A)
    M = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            M[i,j] = dot(A[i], A[j])
    return M

def randomTree(n, w, seed = None):
    '''
    creates a random planar tree with weight sequence w
    '''
    if seed == None:
        seed = 0 #OrderedTree uses different convention 
                # about the seed of Random Generator
    tree = ot.randomTree(n, w, SEED = seed)
    return tree

def randomCrossMeander(n, seed = None):
    '''generate a random crossing meander'''
    if seed != None:
        np.random.seed(seed)
    uP = pg.randomCrossPairing(n)
    dP = pg.randomCrossPairing(n)
    mndr = mr.Meander(uP, dP)
    return mndr


def treeToDyckPath(tree):
    '''converts a planar rooted tree to a Dyck path'''
    A = [-1]* tree.graph.V 
    dyckPath = []
    v = tree.graph.root
    stack = [v]
    A[v] = 0
    #dfsPath = []
    n = 1
    while (len(stack) > 0):
        #print("stack = " + str(stack));
        v = stack[-1]; #peaking at the top of the stack
        #print("processing v = " + str(v))
        flag = False #can we find unprocessed neighbors?
        d = tree.graph.degree(v)
        for i in range(d):
            w = tree.graph.adj[v][i]
            if (A[w] < 0): #this neighbor has not been explored previously
                A[w] = n
                n = n + 1
                stack.append(w)
                #print(dfsPath)
                dyckPath.append(1)
                flag = True
                break #stop searching for an uexplored neighbor
            else: 
                continue
        if (not flag): 
            stack.pop() #no unexplored neighbor around v. Remove it from consideration.
            dyckPath.append(-1)
    del dyckPath[-1]
    return  dyckPath    

def findQuasiClusters(mndr, max_gap_size = 3):
    ''' finds all quasi-cluster cycle in a meander 
    parameter: meander
    returns: list of cluster cycles'''
    cycles, _ = mndr.findCycles()
    clusters = []
    for cycle in cycles:
        support = cycle.copy()
        support.sort()
        isQuasiCluster = True
        for i, x in enumerate(support):
            if i != len(support) - 1:
                gap = support[i + 1] - x
                if gap > max_gap_size:
                    isQuasiCluster = False
                    break
        if isQuasiCluster:
            clusters.append(cycle)
    return clusters

def largestCluster(mndr, max_gap_size = 3):
    ''' finds the largest quasi-cluster cycle in a meander. If there are several, 
    finds and returns one of them'''
    clusters = findQuasiClusters(mndr, max_gap_size = max_gap_size)
    if clusters == []:
        return []
    lengths = [len(cycle) for cycle in clusters]
    i = lengths.index(max(lengths))
    largest = clusters[i]
    return largest        

def largestClusterLength(mndr, max_gap_size = 3):
    largestCycle = largestCluster(mndr, max_gap_size = max_gap_size)
    return len(largestCycle)

def plotRandomProperMeander(n):
    '''gets a random proper meander and plots it'''
    max_iter = 100000 #maximum number of attempts to get a meander 
    counter = 0
    while counter < max_iter:
        mndr = mr.randomMeander(n)
        if mndr.isProper():
            mndr.draw()
            return mndr
        else:
            counter = counter + 1
    print("Max number of attempts: ", max_iter, " exceeded.")
    print("Proper meander is not found")
    return None


def makeMeanderFromCycle(cycle):
    ''' creates a (crossing) meander from a cycle. 
    For example, given a cycle (0, 5, 3, 2, 1, 4), which corresponds to upper arcs
    (0, 5), (3, 2) and (1, 4) and lower arcs (5, 3) (2, 1) and (4, 0)
    creates pairings 
    [5 4 3 2 1 0] and [4 2 1 5 0 3] and the (crossing) meander based on these pairings.
    parameter: cycle, a list of permuted numbers from 0 to 2n - 1 that starts from 0
    returns: a meander
    '''
    if len(cycle)%2 != 0:
        print("Error: the length of the cycle must be even.")
        return 
    n = int(len(cycle)/2)
    uprng = [0] * 2 * n
    dprng = [0] * 2 * n
    for i in range(n):
        uprng[cycle[2 * i]] = cycle[2 * i + 1]
        uprng[cycle[2 * i + 1]] = cycle[2 * i]
        dprng[cycle[2 * i + 1]] = cycle[(2 * i + 2)%(2 * n)]
        dprng[cycle[(2 * i + 2)%(2 * n)]] = cycle[2 * i + 1]
    mndr = mr.Meander(None, None, uprngArray = uprng, dprngArray = dprng)  
    return mndr  
        
'''
For testing methods
'''
def main():
    
    '''
    #Generate and prints a random tree (weighted)
    n = 100
    w = [1, 1, 1]
    tree = randomTree(n, w)
    print(tree)
    tree.draw(drawLabels = True)
    
    
    #Creates a random Dyck path and plot it 
    #path = randomDyckPath(n)
    path = treeToDyckPath(tree)
    #print(path)
    S = np.cumsum([0] + path)
    fig1, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.plot(S)
    ax1.grid(True)
    ax1.xaxis.set_ticks(np.arange(0,S.shape[0]))
    ax1.yaxis.set_ticks(np.arange(0, np.max(S) + 1))
    
    
    #Generates a random meander, finds a random cluster cycle (all 
    #point in the cycle are near each other and prints them. 
    n = 100    
    mndr = mr.randomMeander(n)  
    fig, ax = mndr.draw()
    clusters = findQuasiClusters(mndr)  
    print("clusters = \n", clusters)
    
    #here it looks for the largest quasi cluster cycle -- some gaps are allowed. 
    mgs = 9
    cycle = largestCluster(mndr, max_gap_size = mgs)
    print("Largest quasi cluster cycle is ", cycle)
    print("Its length is ", largestClusterLength(mndr, max_gap_size= mgs))
    
    mndr.drawCycle(cycle, ax = ax)
    '''    
    
    #let us generate all non-crossing pairings of length n  
    n = 6
    A = allPairings(n)
    print(len(A))

    
    '''
    p = [3, 2, 1, 0, 5, 4]
    q = [1, 0, 3, 2, 5, 4]
    mndr = mr.Meander(p, q)
    mndr.draw()
    x = dot(p, q)
    print(x)
    '''
    
    M = dotMatrix(n)
    print(type(M))
    print(M)
    path = "/Users/vladislavkargin/Dropbox/Programs/forPapers/Meanders/"
    print(os.path.isdir(path))
    np.savetxt(path + "Matrix" + str(n) + ".csv",
               M.astype(int), delimiter = ',')
    w = la.eigvalsh(M)
    print(w)
    
    
    q = 0.5
    #q = 7/8
    Mq = q ** (n - M) 
    print(Mq)
    w = la.eigvalsh(Mq)
    print("Eigenvalues: ", w)
    print("Maximum eigenvalue: ", max(w))
    print("Minimal Eigenvalue: ", min(w))
    print("Minimal Eigenvalue * C_n^2: ", min(w) * (Mq.shape[0]**2))
    print("Number of Negative Eigenvalues: ", (w[w < 0]).shape[0])
    print("Index: ", (w[w > 0]).shape[0] - (w[w < 0]).shape[0])
    plt.plot(w)
    plt.grid()
    
    ''' I used this for an example in my Math 447 class.
    plotRandomProperMeander(5)
    plt.grid(True)        
    '''
    
    '''This is for paper. It is now available as a notebook in Colab'''
    '''
    seed = 3
    n = 5
    path1 = randomDyckPath(n, seed = seed)
    plotDyckPath(path1)
    prng1 = pg.Pairing(path = path1)
    prng1.draw()
    
    area = areaDyckPath(path1)
    print("Area of path1 is ", area)   
     
    path2 = randomDyckPath(n, seed = seed + 2)
    #plotDyckPath(path2, method = "lowerLatticePath")
    area = areaDyckPath(path2)
    print("Area of path2 is ", area)  
    
    prng2 = pg.Pairing(path = path2)
    mndr = mr.Meander(prng1, prng2)
    mndr.draw(drawCycles=True)
    mr.drawAsPolygon(mndr)
   '''
    
    plt.show()
    
    

if __name__ == '__main__':
    main()