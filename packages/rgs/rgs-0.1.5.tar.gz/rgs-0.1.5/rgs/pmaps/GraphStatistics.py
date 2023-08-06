'''
Created on May 18, 2020

@author: vladislavkargin

Various methods to calculate statistical properties of various
classes of Graphs, Trees and Maps
'''
#from os.path import dirname, abspath, join
# Find code directory relative to our directory
#THIS_DIR = dirname(__file__)
#CODE_DIR = abspath(join(THIS_DIR, '..', 'code'))

import sys
sys.path.append('..')


import numpy as np
import matplotlib.pyplot as plt
import pmaps.OrderedTree as ot
import pmaps.PlanarGraph as pg
import pmaps.TreeUtility as tu

def probMacroSplit(n, ITER = 100, a = 0.25, SEED = 0, METHOD = "gwTree",
                PARAM = [1, 1, 1]):
    '''
    estimates the probability that a random binary tree on n vertices 
    splits into two pieces of 
    approximately the same size, which means that the size of the smallest 
    piece is > a n
    The probability is conditional on the event that the tree divides at
    the root.
    Arguments
    n - size of the tree
    ITER - number of iterations used to estimate the probability
    a - the threshold used to check if a macro-split occurred. The default
        is 0.25, which means that if the smaller branch is larger than 0.25 n
        the we have a macro-split.  
    SEED - the seed of random generator for replication purposes. If the seed is 
        set to 0 (default) then the results are changing from run to run. 
    METHOD - the method to generate the random tree. If "gwTree" then a random Galton-Watson
        unary-binary tree on n vertices is generated, if "slimTree" then a random slim tree generated
        (a tree with fixed number of vertices and leaves)
    PARAM - the parameter that has to be passed to the generator of the tree
        if METHOD is gwTree, then this is a 3-vector of degree weights (equivalent to 
        offspring probabilities for a critical GW tree). By default
        it is [1, 1, 1]. If METHOD is slimTree then it is the number of leaves in the
        graph.
    '''
    if (SEED != 0):
        np.random.seed(SEED)
        
    #weights = [1, 1, 1]
    counter = 0
    frequency = 0
    while counter < ITER:
        if (METHOD == "qwTree"):
            tree = ot.randomTree(n, PARAM)
        elif (METHOD == "slimTree"):
            tree = ot.randomSlimTree(PARAM, n)
        else:
            print("probMacroSplit says: the METHOD is unknown")
            return
        #print("The degree of root is " + str(len(tree.graph.adj[0])))
        if counter % 10 == 0:
            print("counter = " + str(counter))
        if len(tree.graph.adj[0]) == 2: #the tree is split at the root
            counter = counter + 1
            u = tree.graph.adj[0][0]
            #v = tree.graph.adj[0][1]
            t = tree.sizeVertex(u)/n
            t = np.min([t, 1 - t])
            if t > a:
                frequency = frequency + 1
    return frequency/ITER

def triangulationMaxDegree(n, ITER = 100, SEED = 0):
    '''
    calculate a vector of maximal vertex degrees in random triangulations on n vertices
    The number of replications is given by parameter ITER, which is by default = 100 
    SEED is the seed for the random generator, for replication purposes
    if SEED == 0 (default), then the results change from time to time.
    ''' 
    max_degrees = np.array([0] * ITER)    
    for i in range(ITER):
        if i % 10 == 0:
            print("counter = " + str(i))
        gr = pg.randomTriangulation(n, SEED)
        max_degrees[i] = gr.maxDegree()
    return max_degrees

def plotTriangulationMaxDegrees(start_n = 100, end_n = 1000, step = 100, ITER = 30):
    '''
    creates a plot of average max degrees 
    '''
    max_degrees = [] 
    rng = list(range(start_n, end_n, step))
    print(rng)
    for n in rng:
        print("n = " + str(n))
        mdgr = triangulationMaxDegree(n, ITER)
        max_degrees.append(np.mean(mdgr)/n * np.log(n))
        
    plt.plot(rng, max_degrees, 'ro-', mfc = "blue")
 
    

def main():
    print('Statistics is running')
    
    
    '''
    Here we checking the method probMacroSplit
    '''
    '''
    n = 1000
    a = 0.3
    k = np.int(a * n)
    #prob = probMacroSplit(n, ITER = n)
    prob = probMacroSplit(n, ITER = n, METHOD = "slimTree", PARAM = k)
    print("probability of macro split is " + str(prob))
    exponent = - np.log(prob)/np.log(n)
    print("log(prob)/log(n) = " + str(exponent))
    '''
    
    #plotTriangulationMaxDegrees()
    
    n = 1000
    gr = pg.randomTriangulation(n, method = "decoratedPath")
    

    profile = gr.degreeProfile()
    plt.plot(profile)
    dcut = 21
    plt.xlim(left = 0, right = dcut)
    plt.xlabel("degree (0 corresponds to leafs). cut at d = " + str(dcut))
    plt.ylabel("number of occurrences")
    plt.title("Degree distribution for a triangulation on " + str(n) + " vertices")
    
    
    plt.show()
    
    
    
    print('Statistics has finished')
    

if __name__ == '__main__':
    main()
            
    
    