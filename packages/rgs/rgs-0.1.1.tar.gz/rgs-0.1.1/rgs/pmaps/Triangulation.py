'''
Created on Jul 11, 2020

@author: vladislavkargin
'''

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib import cm

import copy
import math
import numpy as np

import rgs.pmaps.OrderedTree as ot
import rgs.pmaps.TreeUtility as tu
import rgs.pmaps.PlanarGraph as pg


class Triangulation(object):
    '''
    An object that represent a triangulation. Its an specialization of the planar graph
    so many of its functionality is provided by the PlanarGraph object.
    '''


    def __init__(self, tree = None):
        '''
        Constructor
        If tree is available buils the triangulation from the tree 
        using a variant of the Poulalhon-Scheffer method, 
        else builds the triangulation that consists of 3 vertices.
        '''
        if tree != None:
            self.graph = pg.buildTriangulation(tree)
            self.realizer = self.calcRealizer()
        else:
            self.graph = pg.PlanarGraph(V = 3, root = 0)
            self.graph.rootArrow = 1
            self.graph.addEdge(0,1)
            self.graph.addEdge(1,2)
            self.graph.addEdge(0,2)
            self.realizer = ([-1, -1, -1], [-1, -1, -1], [-1, -1, -1]) 
    
    def __str__(self):
        return str(self.graph)
    
            
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Triangulation):
            if self.realizer == other.realizer: #realizers are same
                return True
            else: 
                return False
        return False
    
    def __hash__(self):
        return hash(str(self.realizer))
    
    
    def canonLabelling(self):
        '''
        build a canonical labelling for a maximal planar graph (that is, for a triangulation)
        with outer face a, b, c
        That is, outputs a sequence [v0, v1, ..., v_n], where v0 = b, v1 = c, v_n = a, and the 
        sequence satisfies certain requirements useful for building a planar embedding of the
        graph. See Schnyder paper (1990) about realizers and references within. 
        It is assumed that the triangulation has at least 4 vertices 
        TODO: I should enhance this by renaming so that the root was 0, arrowRoot 1 and 
        the remaining vertex on the boundary 2. Perhaps it should be done in a separate 
        method. 
        '''
        gr = copy.deepcopy(self.graph)
        V = gr.V
        seq = [0] * V
          
        boundary = gr.getOuterBoundary(u0 = gr.rootArrow) #this sometimes fails I don't know
                                                        #why
        if boundary == -1:
            return -1                                              
        b = boundary[0]
        c = boundary[1]
        a = boundary[2]
        seq[0] = b 
        seq[1] = c
        seq[-1] = a
        
        for i in range(V- 3): #we are going to remove V - 3 non-boundary vertices
            nbrs = gr.adj[a]
            #print("neighbors are " + str(nbrs))
            #we are looking for a vertex v among neighbors of vertex a, 
            #which is not b or c and which 
            #has exactly 2 common neighbors with vertex a
            #In terminology of Schnyder, av is contractible.
            isContractionFound = False
            for v in nbrs:
                if (v == b) or (v == c):
                    continue
                else:
                    count = 0 
                    for u in gr.adj[v]: 
                        if (u in nbrs):
                            count = count + 1
                    if count == 2: #a contractible edge is found
                        isContractionFound = True
                        #print("Contractible edge is (" + str(a) + ", " + str(v) + ")")
                        break 
            if not isContractionFound:
                print("canonLabelling says: Contractible edge is not found")
                print("drawing current graph:")
                gr.draw(drawLabels = True)
                break
            else:
                seq[gr.V - 2 - i] = v
                #contracting the graph
                for u in gr.adj[v]: #first we add edges to a
                    #print(u)
                    u0 = v #this is to keep track of which new edges were added to a
                        #if no edges are added, this is v
                    if (u not in nbrs) and (u != a):
                        #print("Nontrivial vertex u = " + str(u))
                        gr.addEdgeBeforeAfter(u, a, v, u0)
                        u0 = u
                toRemove = copy.deepcopy(gr.adj[v])
                for u in toRemove: #now we remove all edges from v
                    #print("removing " + str(u))
                    gr.removeEdge(v, u)
                #print("After contraction of (" + str(a) + ", " + str(v) + ")")
                #print("The graph is " + str(gr))
                #gr.draw(drawLabels = True)
        return seq 
    
    def calcRealizer(self):
        '''
        Builds the Schnyder realizer of the triangulation graph. 
        Arguments:
        graph - a triangulation
        seq - a canonical labelling build by canonLabelling function
        Output:
        a triple of arrays, each of them gives a map from a vertex of a triangulation to its parent
        in one of 3 trees.
        if we have b root, c rootarrow, and a the remaining vertex on the outer triangle
        then T1 has its root at a, T2 - at b, and T3 - at c.
        [The array representation of trees loses some info about planar embeddings of these trees]
        '''
        return self.graph.calcRealizer()
        
            
    def draw(self, title = '', drawLabels = False, block = False, root = -1, 
             calculateRepr = "Schnyder", boundary = [], showDual = False,
             palette = "prism"):        
        fig, ax = self.graph.draw(title = title, drawLabels = drawLabels, block = block, root = root, 
             calculateRepr = calculateRepr, boundary = boundary, showDual = showDual,
             palette = palette)   
        return fig, ax
    
    def drawRealizer(self, ax, realizer):
        '''
        draws graph with a Schnyder's realizer (which was computed by calcRealizer)
        '''
        #fig, ax = self.draw(calculateRepr = calculateRepr)
        A = np.array(self.graph.repr)
        x = A[:, 0]
        y = A[:, 1]
        for i in range(3):
            if i == 0:
                c = "red"
            elif i == 1:
                c = "green"
            else:
                c = "purple"
            T = realizer[i]
            for i, v in enumerate(T):
                if v >= 0:
                    line = mlines.Line2D(np.vstack((x[i], x[v])),
                                     np.vstack((y[i], y[v])), marker = ".", color = c);
                    ax.add_line(line)
                    arrow = mpatches.Arrow(x[i], y[i], x[v] - x[i], y[v] - y[i], width = 0.1,
                                            color = c);
                    ax.add_patch(arrow)

def randomTriangulation(n, SEED = 0, method = "Lukas31"):
    '''
    builds a random triangulation on n vertices
    arguments:
    n - number of vertices in the triangulation
    SEED is the seed of the random generator for replication;
        if SEED = 0 (default) then the results will change from time to time.
    method - if "Lukas31" (default) uses the Poulalhon - Schaeffer method
        to build a uniformly random triangulation based on building a Lukasiewisz path
        with steps 3 and -1 and then decoding it to a tree, in which each internal vertex
        is connected to two leaves.
        -if "decoratedPath" then modifies the Poulalhon Schaeffer method and builds 
        a tree in which an internal vertex is connected to two leaves and exactly one next
        internal vertex, so it is a path decorated with leaves (or some kind of asymmetric
        caterpillar. 
    returns the triangulation and the tree from which it was constructed
    '''
    if method == "Lukas31":
        tree = ot.randomBTree(n - 2, SEED = SEED)
        #tree.draw(drawLabels = True)
    elif method == "decoratedPath":
        tree = tu.decoratedPathTree(n, SEED = SEED)
    else:
        print("randomTriangulation says: the method should be either Lukas31 or decoratedPath")
    trngl = Triangulation(tree)
    return trngl, tree 


'''
For testing methods
'''
def main():
    print('Triangulation.main() started')
    
    

    
    #n = 8
    #seed = 23167
    '''
    n = 5
    seed = 0
    trngl, _ = randomTriangulation(n, SEED = seed)
    #trngl = randomTriangulation(n, SEED = seed, method = 'decoratedPath')
    print(trngl.graph)
    _, ax = trngl.draw(drawLabels = True)
    

    profile = trngl.graph.degreeProfile()
    print("Degree profile is " + str(profile))
    print("Max degree = " + str(trngl.graph.maxDegree()))
    boundary = trngl.graph.getOuterBoundary(u0 = trngl.graph.rootArrow)
    print("Calculated Boundary = " + str(boundary))
    seq = trngl.graph.canonLabelling()
    print("Canonical Labeling = " + str(seq))
    
   # realizer = trngl.graph.calcRealizer()
    #print(trngl.realizer) 
    
    X = trngl.graph.calcSchnyderRepr()
    print("barycentric coordinates are: \n" + str(X))   
    
    #_, ax = trngl.draw(drawLabels = True)
    #trngl.drawRealizer(ax, trngl.realizer)
    '''
    
    
    n = 5
    seed = 0
    hashTrngl = {}
    ITER = 100
    for count in range(ITER):
        if count % 10 == 0:
            print(count)
        trngl, _ = randomTriangulation(n, SEED = seed)
        #print(str(trngl))
        seq = trngl.canonLabelling()
        if seq == -1:
            break
        if trngl in hashTrngl.keys():
            hashTrngl[trngl] = hashTrngl[trngl] + 1
        else:
            hashTrngl[trngl] = 1
    print(len(hashTrngl))
    for i in range(len(hashTrngl)):
        trngl = list(hashTrngl.keys())[i]
        _, ax = trngl.draw(drawLabels = True)
        trngl.drawRealizer(ax, trngl.realizer)
        

    
    plt.show()  
    
    print('Triangulation.main() finished')  

    
if __name__ == "__main__":
    main()