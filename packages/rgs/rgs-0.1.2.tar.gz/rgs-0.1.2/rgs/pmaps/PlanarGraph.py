'''
Created on Jan 13, 2020

This is a class for the graph object embedded in a plane. 

The graph is a simple graph - no double edges or loops.
It is a rooted graph, so one of the vertices is chosen as a root. By default it is
vertex 0. 
It is desirable that the root is on the outer boundary, and in all cases when we have outer leafs,
it the root should be an outer leaf. This should helps with resetting the root. 
However, the resetting is not yet implemented.

@author: vladislavkargin
'''

try:
    import matplotlib.pyplot as plt
    import matplotlib.lines as mlines
    import matplotlib.patches as mpatches
    from matplotlib import cm
    possibleToDraw = True
except ImportError:
    possibleToDraw = False
    

import copy
import math
import numpy as np
import numdifftools as nd
import scipy.linalg as la
from scipy.optimize import minimize
from copy import deepcopy

import rgs.pmaps.OrderedTree as ot
import rgs.pmaps.TreeUtility as tu
import rgs.pmaps.Triangulation as tr


class PlanarGraph:
    
    
    #Creates a graph with v vertices and no edges
    def __init__(self, V = 0, root = 0, rootArrow = -1):
        self.V = V
        self.E = 0
        self.root = root
        self.rootArrow = rootArrow #if this is defined then the edge (root, rootArrow) is in
                                #the border of outer country
                                #this is used in the construction of dual graph
        self.adj = []; #list of adjacency lists for vertices
        self.repr = []; #list of coordinates of vertices in a planar representation
        self.labels = []; #list of vertex labels. 
        for _ in range(V):
            self.adj.append([])
            self.repr.append([0., 0.])
        self.dlgr = None #This will be the dual graph. it is calculated on demand via dualGraph method.
                        #(at the least, the graph should be connected at this point).
        self.countries = [] #This is also calculated by dualGraph method.
                            #The country 0 is the outerCountry
        self.R = []  #This is radii of circles in Koebe representation of the graph. It is
        #expensive to calculate them so they are stored.            
        #R -vector of radii for vertices. The first V coordinates are 
        #radii of vertices of the original graph. The next F - 1  coordinates are radii of
        #the vertices of the dual graph
    
    def __str__(self):
        '''
        Returns a string representation of this graph.
        return the number of vertices V, followed by the number
        of edges E, followed by the V adjacency lists
        '''
        s = ("V = " + str(self.V) + ', E = ' + str(self.E) + ", root = " + str(self.root) 
                + ", rootArrow = " + str(self.rootArrow) + '\n')
        for i in range(self.V):
            s = s + str(i) + " -> " + str(self.adj[i]) + '\n'
        return s    
    
    '''
    calculates the degree of vertex v
    '''
    def degree(self, v):
        d = len(self.adj[v])
        return d
    
    def leaves(self):
        '''
        return the list of leaves in the graph
        '''
        lvs = []
        for v in range(self.V):
            if self.degree(v) == 1:
                lvs.append(v)
        return lvs 
    
    def singletons(self):
        '''
        returns the list of singletons (i.e., vertices which are not connected to anything else)
        '''
        sngls = []
        for v in range(self.V):
            if self.degree(v) == 0:
                sngls.append(v)
        return sngls
    
    '''
    returns the edge type. If the edge is to/from leaf, then it is called
    external or outer, and the function returns 0. Otherwise the edge is called
    internal or inner, and the function returns 1.
    NOTE: we do not check if (u, v) is indeed an edge. 
    '''    
    def edgeType(self, u, v):
        if (self.degree(u) == 1 or self.degree(v) == 1):
            return 0
        else:
            return 1
    
    def nextEdge(self, u, v):
        '''
        returns x such that (u, x) is the next edge in the adjacency list of u after (u,v)
        In particular, if u is a leaf, then returns back again v
        '''
        if v not in self.adj[u]:
            print("nextEdge says: the edge (" + str(u) + ", " + str(v) + ") is not in graph")
            return -1
        else: 
            d = self.degree(u)
            i = self.adj[u].index(v)
            x = self.adj[u][(i + 1) % d]
            return x
     
    def previousEdge(self, u, v):
        '''
        returns x such that (u, x) is the previous edge in the adjacency list of u with respect 
        to (u,v)
        In particular, if u is a leaf, then returns back again v
        '''
        if v not in self.adj[u]:
            print("nextEdge says: the edge (" + str(u) + ", " + str(v) + ") is not in graph")
            return -1
        else: 
            d = self.degree(u)
            i = self.adj[u].index(v)
            x = self.adj[u][(i - 1) % d]
            return x 
           
    # Adds the undirected edge u-v to this graph.    
    def addEdge(self, u, v): 
        self.E = self.E + 1
        self.adj[u].append(v)
        self.adj[v].append(u) 
    
    # Adds a directed edge from u to v to this graph.   
    # This graph is meant to be undirected, so this is 
    # a convenience tool to take subgraphs and make sure
    # that the order of adjacency lists is not violated
    def addDirectedEdge(self, u, v):
        if ((v not in self.adj[u]) and (u not in self.adj[v])):
            self.E = self.E + 1
        self.adj[u].append(v)
        

    def addEdgeBeforeAfter(self, u, v, a, b):
        '''
        adds an edge (u,v) so that in the adjacency list of u, new vertex v is 
        before a, and in the adjacency list  of v, vertex u is after b 
        if a or b are not in the adjacency list, the function
        simply appends u and v to the relevant lists. (So, then it behaves like the standard
        addEdge. (This last behavior is useful if we just start building the graph.)
        '''
        listU = self.adj[u]
        if a in listU:
            i = listU.index(a)
            self.adj[u].insert(i, v)
        else:
            self.adj[u].append(v)
        listV = self.adj[v]
        if b in listV:
            i = listV.index(b)
            self.adj[v].insert((i + 1)%self.degree(v), u) 
        else:
            self.adj[v].append(u)
        
  
    def removeEdge(self, u, v):
        '''
        removes edge (u, v)
        '''
        self.E = self.E - 1  
        #print("list of u: " + str(self.adj[u]))
        self.adj[u].remove(v)
        #print("list of v: " + str(self.adj[v]))
        self.adj[v].remove(u)
       
    def removeVertex(self, v):
        '''
        returns graph in which vertex v and all edges adjacent to it are removed.
        The assumption is 
        that it is not a root or rootArrow
        '''
        vertices = list(range(v)) + list(range(v + 1, self.V))
        gr = self.subgraph(vertices, self.root, self.rootArrow)
        return gr
    
    def addVertex(self): 
        '''
        adds a vertex to the graph
        '''
        self.V = self.V + 1
        self.adj.append([])
        self.repr.append([0., 0.])
        
                       
    
    # Sets coordinates of vertex v to (x, y)    
    def setCoord(self, v, x, y):
        #print("len(repr) = " + str(len(self.repr)))
        #print("v = " + str(v))
        self.repr[v] = [x, y]
    
    '''
    represent vertices in n-by-1 array vertices
    as points with coordinates in n-by-2 array vrepr
    '''
    def reprVertices(self, vertices, vrepr):
        for i in range(len(vertices)):
            self.setCoord(vertices[i], vrepr[i][0],vrepr[i][1])
            
    '''
    represent selected vertices on the unit circle
    '''        
    def reprOnCircle(self, vertices):
        n = len(vertices)
        for k in range(n):
            self.setCoord(vertices[k], math.cos(2 * math.pi * k/n),
                           math.sin(2 * math.pi * k/n)) 
            
               
    def putSingletonsAway(self):
        '''
        represents singletons by points in the south-west corner
        '''
        sngls = self.singletons()
        n = len(sngls)
        vrepr = [[-1,-1]] * n
        self.reprVertices(sngls, vrepr)

    def calcRubberRepr(self, nailedVs):
        '''
        calculates representation of the graph using the 
        current representation of nailed vertices as fixed and using 
        rubber method that minimizes the energy of edges that connect vertices
        
        Reference: Lovasz "Graphs and Geometry"
        '''
        Alist = [];
        for v in range(self.V):
            equation = []
            for i in range(self.V):
                equation.append(0)
            equation[v] = 1
            if v not in nailedVs: #the equations are non-trivial only for these vertices
                d = len(self.adj[v]) #number of neighbors
                for w in range(d):
                    equation[self.adj[v][w]] = - 1/d
            Alist.append(equation) 
        A = np.array(Alist)
        #print("A is ")
        #print(A) 
        #now we build right hand sides and solve for representation
        b = []
        for v in range(self.V):
            if v not in nailedVs:
                b.append(0)
            else:
                b.append(self.repr[v][0])
        bx = np.array(b)
        #print("bx is ")
        #print(bx)
        x = la.solve(A,bx)
        #print(" x is ")
        #print(x)  
        #now solving for y coordinates      
        b = []
        for v in range(self.V):
            if v not in nailedVs:
                b.append(0)
            else:
                b.append(self.repr[v][1])
        by = np.array(b)
        y = la.solve(A,by)
        #print(" y is ")
        #print(x)
        #adjusting the representation of vertices
        for v in range(self.V):
            self.repr[v][0] = x[v]
            self.repr[v][1] = y[v]  
    
    def calcKoebeRepr(self):
        '''
        calculates representation of the graph as a tangency graph for a system of circles
        reference: Lovascz "Graph and Geometry"
        
        Arguments: 
        '''
        if (self.rootArrow < 0):
            print("calcKoebeRepr says:")
            print("the rootArrow element")
            print("of the graph should be non-negative in order to calculate bounndary")
        fixiki = self.getOuterBoundary(u0 = self.rootArrow)
        self.reprOnCircle(fixiki)
        self.calcRubberRepr(fixiki)
        if self.dlgr == None:
            self.dualGraph()
        self.findRadii()
        #caclculate angles
        angles = self.calcAngles() 
            #Angles - the p-th element contains the list of angles for the vertices of the country
            #p. The angle is the half of the inner angle for the vertex. 
        
        
        #reset all vector positions to 0
        #(I should have represented vertices by numpy vectors from the beginning)
        for v in range(self.V):
            self.repr[v][0] = 0.
            self.repr[v][1] = 0.
        v0 = self.countries[0].border[0] #we place this vertex at 0
        v1 = self.countries[0].border[1] #and this vertex will be on the horizontal line.
                                #all other vertices should be determined automatically
        self.repr[v1][0] = self.R[v0] + self.R[v1]
        markedVertices = [False] * self.V
        markedVertices[v0] = True
        markedVertices[v1] = True
        #we are going to traverse the dual graph and build coordinates for vertices of 
        #each country
        markedCountries = [False] * self.dlgr.V
        markedCountries[0] = [True] #We will not process the outer country
        country = self.getCountry(v1, v0)
        stack = [country]
        counter = 0
        while len(stack) > 0 and counter < 2 * (self.V + self.E):
            counter = counter + 1
            #print("Current repr = " + str(self.repr) )
            country = stack[-1]
            p = self.countries.index(country)
            markedCountries[p] = True
            #print("Country = " + str(country) + "; index = " + str(p))
            #process the country: find the coordinates of all its vertices
            x = 0
            border = country.border
            l = len(border)
            for i in range(l):
                u = border[i - 1]
                v = border[i]
                if markedVertices[u] and markedVertices[v]:
                    x = i
                    break #found a pair of vertices with known coordinates
            for i in range(l - 1):
                u = border[(i + x - 1) % l]
                v = border[(i + x) % l]
                w = border[(i + x + 1) % l]
                if not markedVertices[w]: #need to calculate the representation of vertex w
                    #print("calculating representation for w = " + str(w))
                    #print("index of vertex in the country is (i + x)%l = " + str((i + x) % l))
                    #print("angles for country " + str(p) + " are " + str(angles[p]))
                    a = 2 * angles[p][(i + x) % l]
                    #print("Angle next to v = " + str(v) + " is " + str(180 * a/np.pi))
                    uv = np.array([self.repr[u][0] - self.repr[v][0],
                                   self.repr[u][1] - self.repr[v][1]])
                    vrepr = np.array([self.repr[v][0], self.repr[v][1]])
                    #print(vrepr)
                    wv = np.array([uv[0]*np.cos(a) - uv[1]* np.sin(a), 
                                   + uv[0]*np.sin(a) + uv[1]*np.cos(a)])
                    wv = wv/(np.sqrt(wv @ wv))
                    wv = wv * (self.R[w] + self.R[v])
                    wrepr = vrepr + wv
                    self.repr[w][0] = wrepr[0]
                    self.repr[w][1] = wrepr[1] 
                    #print("calculated position for  w = " + str(w) + " is " + str(wrepr))
                    markedVertices[w] = True
            #look for new countries
            foundNewCountry = False
            for i in range(len(country.border)):
                u = country.border[i - 1]
                v = country.border[i]
                newCountry = self.getCountry(v,u)
                newp = self.countries.index(newCountry)
                if not markedCountries[newp]:
                    foundNewCountry = True
                    stack.append(newCountry)
                    #print("newCountry: " + str(newCountry))
                    break
            if not foundNewCountry:    
                stack.pop()
              
    def calcSchnyderRepr(self):
        '''
        calculated the coordinates of Schnyder's representation for a triangulation graph.
        sets the coordinates of vertices placing the vertices of the external triangle
        as vertices of an equilateral triangle on the unit cirle. 
        
        Returns Shnyder's integer barycentric coordinates as an np.array X
        
        Reference: Schnyder "Embedding planar graphs on a grid"
        '''
        
        #seq = self.canonLabelling()
        tree_arrays = self.calcRealizer()
        #now should convert arrays to trees (the trees may have the planar structure different from 
        #what they have in the original graph
        trees = []
        for t in range(3):
            T = tree_arrays[t]
            trees.append(ot.OrderedTree(V = len(T)))
            for i, v in enumerate(T):
                if v != -1:
                    trees[t].graph.addEdge(i, v)
                    if T[v] == -1:
                        #print("found root v = " + str(v))
                        trees[t].setRoot(v)
        P = [] #heights of vertices in the three trees
        Q = [] #sizes of subtrees rooted on vertices in the three trees               
        for t in range(3):                
            heights, sizes = trees[t].calcHeightsSizes(trees[t].root)
            #print("heights of tree " + str(t) + " is " + str(heights))
            #print("sizes of tree " + str(t) + " is " + str(sizes)) 
            P.append(heights)
            Q.append(sizes)      
            
        #now we are going to calculate the number of vertices in the three regions that 
        # correspond to each vertex. We are going to do using the dfs traversals over the trees
        #initializing
        R = []
        for _ in range(3):
            rrr = [0] * self.V
            R.append(rrr)   
           
        for t in range(3):
            tree = trees[t]
            
            cumsum1 = [0] * self.V
            cumsum2 = [0] * self.V #here we keep cumsums of sizes of subtrees
            #A[x] is the order in which x appears in the dfs path
            A = [-1]* self.V
            
            stack = [tree.root]
            A[tree.root] = 0
            
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
                        cumsum1[w] = cumsum1[v] + Q[t - 1][w]
                        cumsum2[w] = cumsum2[v] + Q[(t + 1) % 3][w]
                        R[t - 1][w] = R[t - 1][w] + cumsum1[w]
                        R[(t + 1) % 3][w] = R[(t + 1) % 3][w] + cumsum2[w]
                        R[t][w] = R[t][w] - Q[t][w]
                        flag = True
                        break #stop searching for an unexplored neighbor
                    else: 
                        continue
                if (not flag): 
                    stack.pop() #no unexplored neighbor around v. Remove it from consideration.
        #print(R) 
        #finally let us calculate the coordinates of the vertices
        X = np.zeros((3, self.V))
        for t in range(3):
            X[t, :] = np.array(R[t]) - np.array(P[t - 1]) + 1
        #adjust the cooordinates of exterior vertices
        for t in range(3):
            X[t, trees[t].root] = self.V - 2
            X[t - 1, trees[t].root] = 0
            X[(t + 1) % 3, trees[t].root] = 1   
        #now we calculate the representation 
        basis = np.transpose(np.array([[1, 0], [-1/2, np.sqrt(3)/2], [-1/2, - np.sqrt(3)/2]]))
        #print(basis)
        Y = basis @ X
        #print(Y)
        for i in range(self.V):
            self.repr[i][0] = Y[0,i]
            self.repr[i][1] = Y[1,i]
        return X    
  
    def canonLabelling(self):
        '''
        build a canonical labelling for a maximal planar graph (that is, for a triangulation)
        with outer face a, b, c
        That is, outputs a sequence [v0, v1, ..., v_n], where v0 = b, v1 = c, v_n = a, and the 
        sequence satisfies certain requirements useful for building a planar embedding of the
        graph. See Schnyder paper (1990) about realizers and refernces within. 
        It is assumed that the triangulation has at least 4 vertices 
        '''
        gr = copy.deepcopy(self)
        V = self.V
        seq = [0] * V
          
        boundary = gr.getOuterBoundary(u0 = gr.rootArrow)
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
        Builds a Schnyder realizer of the triangulation graph. 
        Arguments:
        graph - a triangulation
        seq - a canonical labelling build by canonLabelling function
        Output:
        a triple of arrays, each of them gives a map from a vertex of a triangulation to its parent
        in one of 3 trees.
        if we have b root, c rootarrow, and a the remaining vertex on the outer triangle
        then T1 has its root at a, T2 - at b, and T3 - at c.
        [The array representation of trees loses the info about planar embeddings of these trees]
        (TODO: may be it would be useful to find a way to output a triple of ordered trees)
        '''
        seq = self.canonLabelling()
        gr = copy.deepcopy(self)
        V = gr.V
        T1 = [-1] * V
        T2 = [-1] * V
        T3 = [-1] * V
        processed = seq[:2]
        for s in range(2, V - 1):
            x = seq[s]
            wheel = gr.adj[x]
            #print("wheel = " + str(wheel))
            deg = len(wheel)
            for i in range(deg): #we need to find such a point v in the wheel of x that v is in 
                #processed list but the vertex preceding v is not
                if (wheel[i - 1] not in processed) and (wheel[i] in processed):
                    wheel = wheel[i:] + wheel[:i]
                    break
            #print("wheel = " + str(wheel))
            T1[x] = seq[-1] #connect current vertex to a in T1 tree
            T2[x] = wheel[0] 
            for i in range(1, deg - 1):
                if (wheel[i] in processed) and (wheel[i + 1] in processed):
                    T1[wheel[i]] = x
                elif (wheel[i] in processed) and (wheel[i + 1] not in processed):
                    T3[x] = wheel[i]
                else:
                    break
            processed.append(x)
        return [T1, T2, T3]   
    
    def degreeProfile(self):
        '''
        Calculates an array with the numbers of vertices that have a given degree.
        Leaves here have degree 1. Singletons are not allowed.
        So [10, 3, 4, 1] means that 10 vertices are leaves, 3 vertices have degree 2, and so on
        The maximum degree is 4
        The array truncated, so that any trailing 0 are removed. 
        '''
        profile = [0] * (self.V - 1)
        maxdegree = 0; 
        for v in range(self.V):
            d = len(self.adj[v])
            if d > maxdegree:
                maxdegree = d
            profile[d-1] = profile[d-1] + 1
        profile = profile[:maxdegree]
        return profile    
    
    def maxDegree(self):
        '''
        calculates the max degree of the graph. 
        '''
        md = 0
        for v in range(self.V):
            d = len(self.adj[v])
            if d > md:
                md = d 
        return md
                
    def subgraph(self, vertices, root, rootArrow):
        '''
        return the graph which is the subraph of this graph based on a list of vertices
        The vertices are renamed to 0, 1, 2, 3, ....
        '''   
        newV = len(vertices)
        sgr = PlanarGraph(newV, root = vertices.index(root), 
                          rootArrow = vertices.index(rootArrow))
        for i in range(newV):
            v = vertices[i]
            sgr.repr[i] = self.repr[v]
            for u in self.adj[v]:
                if u in vertices:
                    sgr.addDirectedEdge(i, vertices.index(u))
        return sgr    
    

    def dualGraph(self):
        '''
        builds the dual graph
        '''
        F = self.E + 2 - self.V #this includes the outer country
        self.dlgr = PlanarGraph(F)
        #we start the list of all countries with the outer country
        outerCountry = Country(self.getOuterBoundary(u0 = self.rootArrow))
        self.countries = [outerCountry]
        #next we should do something like depth first exploration 
        #of the countries, however, we need to check if we have already visited a country
        stack=[outerCountry]
        while (len(stack) > 0):
            currentC = stack[-1] #last element in the stack
            #now we are going over vertices in the current country and 
            #see if we can add any of the neighbor countries
            #print("Current country = " + str(currentC))
            foundNewCountry = False
            for i in range(len(currentC.border)): 
                #get 2 consequitive points 
                u = currentC.border[i - 1]
                v = currentC.border[i]
                neighbor = self.getCountry(v, u)
                #print("The country next to [" + str(v) + ", " + str(u) + "] edge is " 
                #      + str(neighbor))
                if neighbor not in self.countries: #new country is found.
                    foundNewCountry = True
                    self.countries.append(neighbor)
                    stack.append(neighbor)
                    break #stop searching for neighbors of currentC
            if not foundNewCountry:
                stack.pop() #remove current country from the stack
        #print("Countries = " + str(self.countries))
        #add edges to the dual graph
        for x in range(len(self.countries)):
            country = self.countries[x]
            for i in range(len(country.border)):
                u = country.border[i - 1]
                v = country.border[i]
                neighbor = self.getCountry(v, u)
                y = self.countries.index(neighbor) 
                self.dlgr.addDirectedEdge(x, y)
                #print("Neighbor of country " + str(x) + " is " + str(y))
        #print(" Dual Graph is " + str(self.dlgr))
        # assign vector representations to vertices of the dual graph
        for x in range(len(self.countries)):
            country = self.countries[x]
            for v in country.border:
                self.dlgr.repr[x][0] = self.dlgr.repr[x][0] + self.repr[v][0]
                self.dlgr.repr[x][1] = self.dlgr.repr[x][1] + self.repr[v][1]
            self.dlgr.repr[x][0] = self.dlgr.repr[x][0] / len(country.border)
            self.dlgr.repr[x][1] = self.dlgr.repr[x][1] / len(country.border)
                   
    def calcInitAngles(self):
        '''
        calculate original angles: B_{ip} is half of the angle of country p at 
        its vertex i. 
        We exclude the outer country p
        The assumption is that the rubber representation is already computed.
        '''
        #initialize
        V = self.V
        F = self.dlgr.V
        B = [] 
        for _ in range(V):
            B.append([0.0] * (F - 1))
        B = np.array(B)
        #going along countries (except outer Counter)
        for p in range(1, F):
            country = self.countries[p]
            #print(self.countries[p])
            L = len(country.border)
            for i in range(L):
                u = np.array(self.repr[country.border[i - 1]])
                v = np.array(self.repr[country.border[i]])
                w = np.array(self.repr[country.border[(i + 1) % L]])
                x = w - v
                y = u - v
                angle = np.arccos(x @ y /np.sqrt(x @ x * y @ y))/2
                B[country.border[i]][p - 1] = angle
            
        #print(str(B))
        #do a couple of checks
        #Sum over row should give pi or pi/6
        #print(str(np.sum(B, axis = 1)))
        return B
        
    def targetFunction(self, x, B):
        '''
        calculates target function, which will be optimize in order to 
        find the radii of the circles in the circle representation of the planar graph.
        For reference, see Lovasz "Graphs and Geometry" section 5.1.3.
        Arguments:
        x is the list of radii. The first V elements of the list are radii of the circles 
        around vertices, and the next (F - 1) elements are radii of the circles around
        the centers of the countries.
        B is the matrix of the angles calculated by calcInitAngles
        '''
        #let us normalize x so that its maximal element is not greater than 1
        m = np.max(x)
        x = x - m
        V = self.V
        F = self.dlgr.V
        xV = x[:V]
        xP = x[V:]
        phi = 0.0
        for i in range(V):
            for p in range(F - 1):
                if i in self.countries[p + 1].border: #if country and vertex are incident
                    phi = phi + tu.verdiereFunction(- xV[i] + xP[p]) - B[i][p]*(- xV[i] + xP[p])
        return phi
    
    def tfGrad(self, x, B):
        '''
        calculates the gradient of the target function
        '''
        m = np.max(x)
        x = x - m
        V = self.V
        F = self.dlgr.V
        xV = x[:V]
        xP = x[V:]
        grad = [0.0] * len(x)
        for i in range(V):
            for p in range(F - 1):
                if i in self.countries[p + 1].border: #if country and vertex are incident
                    grad[i] = grad[i] - np.arctan(np.exp(- xV[i] + xP[p])) + B[i][p]
                    grad[V + p] = grad[V + p] + np.arctan(np.exp( - xV[i] + xP[p])) - B[i][p] 
        return np.array(grad)
    
    def tfGradient(self, B):
        '''
        this is for checking. It calculates the gradient of the target function in numerical
        fashion -- namely using automatic differentiation
        '''
        fun = lambda x: self.targetFunction(x, B)
        dfun = nd.Gradient(fun)
        return dfun
        
     
    def findRadii(self, useGrad = True, disp = False):   
        '''
        finds the radii of the circles in the representation of the graph
        as the tangency graph for a collection of circles (Koebe's representation).
        This is done by minimization of the targetFunction
        The radii are stored to self.R variable
        
        [see Lovasz "Graphs and Geometry" section 5.1.3.]
        
        If useGrad = True, uses the analytical gradient in tfGrad, otherwise uses
        numerical gradient for optimization
        
        If disp = True, shows the messages generated by optimization routine
        
        '''
        x0 = np.array([1.] * (self.V + self.dlgr.V - 1)) 
        B = self.calcInitAngles();
        if useGrad:
            logR = minimize(self.targetFunction, x0, args = B, method='BFGS', jac=self.tfGrad,
                       options={'disp': disp, 'gtol': 1e-08, 'maxiter': 800})
        else:
            logR = minimize(self.targetFunction, x0, args = B, method='BFGS',
                       options={'disp': disp, 'gtol': 1e-06, 'maxiter': 800})
        print("findRadii says: Target function after optimization = " + str(logR['fun']))
        #print("logR = " + str(logR['x']))
        x = logR['x']
        x = x - np.max(x)
        self.R = np.exp(x)
        
    
    def calcAngles(self):
        '''
        calculate the angles in the circles representation of the graph
        based on the radii computed in findRadii
        The output is an array of list for each country, it 
        corresponds to the ordering of vertices in self.country structure
        '''
        if len(self.R) == 0:
            self.findRadii()
        countryAngles = []
        for p in range(len(self.countries)):
            if p == 0:
                countryAngles.append([0.0] * len(self.countries[0].border))
            else:
                country = self.countries[p].border
                x = [0.0] * len(country)
                for i in range(len(country)):
                    x[i] = np.arctan(self.R[self.V + p - 1]/self.R[country[i]])
                countryAngles.append(x)
        return countryAngles
            
    def calcVertexAngles(self, countryAngles):   
        '''
        calculates the angles for every vertex
        Arguments: the list of angles for countries
        Returns: an array of lists, each least contain angles for a vertex
        The angle for the infinite country is not listed.
        '''     
        vertexAngles = []
        for v in range(self.V):
            anglesV = []
            for w in self.adj[v]:
                p = self.countries.index(self.getCountry(w, v))
                #print("a country for vertex " + str(v) + " is " + str(p))
                if p != 0:
                    i = self.countries[p].border.index(v)
                    anglesV.append(countryAngles[p][i])
            vertexAngles.append(anglesV)
            #print("current vertexAngles: " + str(vertexAngles))
        return vertexAngles      
    
    def drawNiceDualGraph(self):  
        '''
        this simply gives a nice picture of the dual graph. 
        The original graph should be a planar triangulation
        '''
        if self.dlgr == None:
            self.dualGRaph()
        dual = deepcopy(self.dlgr)
        a = self.dlgr.adj[0][0]
        b = self.dlgr.adj[a][0]
        dual.root = b
        dual.rootArrow = a
        dlgr2 = dual.removeVertex(0)
        fig, ax = dlgr2.draw(drawLabels = False, calculateRepr = "drawCircles")
                

    def draw(self, title = '', drawLabels = False, block = False, root = -1, 
             calculateRepr = "Boundary", boundary = [], showDual = False,
             palette = "prism", ax = None):
        '''
        draws the graph.
        Arguments 
        - title = string in the title of the plot
        - drawlabels = if true show labels of vertices next to them. If no Labels are provided
            just show the order number of vertices
        - block: if block is true, then calling 
            the draw function will stop execution of further commands. 
            if block is false (default), then the execution continues but the calling function
            should have plt.show() at the end. 
        - root: if root>0 show this vertex as root. 
        - calculateRepr: If "No" the function will use 
            existing vector representation of vertices;
                if calculateRepr = "Leaves", calculates the vector representation of vertices
            by putting leaves on the unit circle and using rubber edges algorithm
                if calculateRepr = "Boundary" (default), then calculates the vector representation of vertices
            by putting the boundary vertices on the circle. If the boundary argument is non-empty, 
            then it is used as the boundary. Otherwise, the boundary is computed, and 
            then it required that the graph should have positive rootArrow. The assumption 
            is that the edge (root, rootArrow) starts a walk on the boundary. 
                if drawCircles, draws the circles representation.
                [TODO] if calculateRepr = "Schnyder", calculates the Schnyder representation of 
                the graph. This is currently restricted only to triangulations. 
        - boundary: If available then vertices in the boundary are put on the unit circle.
        - showDual: If true, shows the dual graph in red.
                - drawCircles: If true, draws the circles associated with vertices. In this case, 
                 the attribute R should be already computed for the graph (by findRadii function). 
        - palette: the palette used to draw circles, default = "prism"
        
        returns fig and ax handles
         '''
        if (calculateRepr == "Leaves"):  
            boundary = self.getOuterBoundary(typ = "Leaves")
            fixiki = []
            for v in boundary:
                if self.degree(v) == 1:
                    fixiki.append(v)
            #fixiki = self.leaves()
            self.reprOnCircle(fixiki)
            self.calcRubberRepr(fixiki)
            self.putSingletonsAway() 
        elif (calculateRepr == "Boundary"):
            if len(boundary) == 0:
                if (self.rootArrow < 0):
                    print("Draw says: if calculateRepr option is Boundary, ")
                    print("then either the boundary should be supplied or rootArrow element")
                    print("of the graph should be non-negative")
                    return
                else:
                    boundary = self.getOuterBoundary(u0 = self.rootArrow)
                    print("Draw says: Calculated Boundary = " + str(boundary))
            fixiki = boundary.copy()
            self.reprOnCircle(fixiki)
            self.calcRubberRepr(fixiki)
            self.putSingletonsAway()
        elif calculateRepr == "drawCircles":
            print("calculating Koebe's representation")
            self.calcKoebeRepr()
            #print(self.R)
        elif calculateRepr == "Schnyder":
            X = self.calcSchnyderRepr()
            
        
        if (ax == None):
            fig, ax = plt.subplots()
        else:
            fig = ax.figure
            
        ax.set_title(title)
        #TODO choice of plot limits can be improved
        A = np.array(self.repr)
        x = A[:, 0]
        y = A[:, 1]
        ax.set_xlim(np.amin(x), np.amax(x))
        ax.set_ylim(np.amin(y), np.amax(y))
        ax.set_xticks([])
        ax.set_yticks([])

        for v in range(self.V):
            for w in self.adj[v]:
                if w > v: #to avoid double-drawing of the same edge
                    line = mlines.Line2D(np.vstack((x[v], x[w])),
                                         np.vstack((y[v], y[w])), marker = ".");
                    ax.add_line(line)
                    
        if root >= 0:
            circle = plt.Circle((x[root], y[root]), 0.01, color='g', clip_on=False)
            ax.add_artist(circle)
            ax.scatter(x[root], y[root], marker = "X", color = 'g')
        else:
            circle = plt.Circle((x[self.root], y[self.root]), 0.01, color='g', clip_on=False)
            ax.add_artist(circle)
            
        if drawLabels:
            if len(self.labels) == 0: #use index of the vertex instead of label
                for v in range(self.V):
                    ax.text(x[v],y[v], str(v))
            else:
                for v in range(self.V):
                    ax.text(x[v],y[v], str(self.labels[v]))
                    
        if showDual:
            A = np.array(self.dlgr.repr)
            x = A[:, 0]
            y = A[:, 1]
            for v in range(1, self.dlgr.V):
                if drawLabels:
                    ax.text(x[v],y[v], str(v))
                for w in self.dlgr.adj[v]:
                    if w > v:
                        line = mlines.Line2D(np.vstack((x[v], x[w])),
                            np.vstack((y[v], y[w])), marker = ".", color = "r");
                    ax.add_line(line)
                    
        if calculateRepr == "drawCircles":
            colormap = cm.get_cmap(palette, 128)
            #print(self.R)
            maxLogR = np.max(-np.log(self.R))
            for v in range(self.V):
                c = colormap(-np.log(self.R[v])/maxLogR)
                circle = plt.Circle((self.repr[v][0], self.repr[v][1]),
                    self.R[v], color=c, clip_on=False)
                ax.add_artist(circle)
        
        if block:            
            plt.show()
        else:
            plt.draw()
        return fig, ax
    
    def drawPath(self, ax, path):
        '''
        draws a path that connects vertices in path argument in the axes given by ax
        The axes should be created by draw function
        '''    
        A = np.array(self.repr)
        x = A[:, 0]
        y = A[:, 1]       
        for i in range(len(path) - 1):
            v = path[i]
            w = path[i + 1]
            line = mlines.Line2D(np.vstack((x[v], x[w])),
                                         np.vstack((y[v], y[w])), color = 'r', 
                                         linestyle = '-');
            ax.add_line(line)
    
    #def drawRealizer(self, ax, realizer):
        '''
        draws graph with a Schnyder's realizer (which was computed by calcRealizer)
        '''
    '''
        A = np.array(self.repr)
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
    '''


    
       
    def outerFaceClosure(self):
        '''
        goes along the edges in the outer face starting from the root and 
        in the counterclockwise direction. Adds a triangular face if possible.
        This function will only work if certain assumptions are satisfied 
     
        Returns 1 if a face was added or 0 if it was not added
        '''  
        #first three edges from the root along the boundary of the outer space.
        x = self.root   #note that we almost always use (or should use)
                        #the dfs names for vertices
                        #and in this convention the root is always named 0.
        y = self.adj[x][0]
        z = self.nextEdge(y, x)
        t = self.nextEdge(z, y)
        #print("(x, y, z, t) = (" + str([x,y,z,t]) + ")")
        counter = 0
        while ((t == y or x == z or (self.degree(x) == 1 and self.degree(t) == 1) 
               or (self.degree(x) > 1 and self.degree(t) > 1))
               and counter < 2 * self.V): #go along the boundary until find a suitable sequence 
                                    #of edges or until the number of observed edge sequences >= 2 V
            counter = counter + 1
            #print("x = " + str(x) + "; counter = " + str(counter))
            x = y
            y = z
            z = t 
            t = self.nextEdge(z, y)
        #print("degree of " + str(x) + " = " + str(self.degree(x)))
        #print("degree of " + str(t) + " = " + str(self.degree(t)))
        #print("[x, y, z, t] = "    + str([x,y,z,t]) + ")")
        
        #Now we need to check and if one vertex on the boundary of the sequence is a leaf
        #and  the other is not a leaf, and there is no other leaf in between) then we need to remove the leaf and connect 
        #the parent of the leaf with the other end-point. This connection should be done
        #accurately, so that planarity of the graph would not suffer.
        if (self.degree(x) == 1 and self.degree(t) > 1 and self.degree(z) > 1):
            self.removeEdge(y, x)
            self.addEdgeBeforeAfter(y, t, z, z)
            return 1
        elif (self.degree(x) > 1 and self.degree(y) > 1 and self.degree(t) == 1):
            self.removeEdge(z, t)
            self.addEdgeBeforeAfter(x, z, y, y)
            return 1
        else: 
            return 0
    
    def getCountry(self, u0, v0):
        '''
        gets a country with an edge (u0, v0) on its border so that if we go
        along (u0, v0) the country is on the right. (And so we go in the clockwise direction
        for inner countries.)
        '''
        border = [u0]
        u = u0 #current vertex
        v = v0 #next vertex
        while (v != u0):
            border.append(v)
            w = u #new previous vertex
            u = v #new current vertex
            v = self.nextEdge(u, w)
        country = Country(border)
        if country in self.countries: #this strange thing ensures, that if the country is already
                            #in the list of countries, then its border is exactly as its
                            # in the listed country 
            p = self.countries.index(country)
            return(self.countries[p])
        else: 
            return country   
    
    def getOuterBoundary(self, typ = "root", u0 = -1):
        '''
        gets a sequence of vertices that are on the border of the outer face
        if typ = "root" assumes that root is on the boundary and uses (root, u0) 
        as the first edge in the walk around the boundary.
        Otherwise tries to start from a leaf. 
        It is assumed that all leaves look into the outer face.
        '''
        boundary = []
        if typ == "root": #use the supplied arguments
            if u0 < 0:
                print("getOuterBoundaryWarning: A positive u0 must be supplied")
                return
            else: 
                v0 = self.root
                v = v0 #current vertex
                u = u0 #next vertex
        else: #try to start boundary at a leaf
            lvs = self.leaves()
            if (len(lvs) == 0): #there are no leaves, cannot start
                return boundary
            v0 = lvs[0] #initial vertex
            v = v0 #current vertex on the boundary
            u = self.adj[v0][0] #next vertex in on the boundary
        
        boundary = [v0]
        while (u != v0):
            boundary.append(u)
            w = v #new previous vertex
            v = u #new current vertex
            u = self.nextEdge(v, w)
            if u == -1:
                print("getOuterBoundary says: was not able to continue building boundary")
                print("current boundary is " + str(boundary))
                print("the graph is " + str(self))
                boundary = -1
                return boundary
        return boundary    

class Country(object):
    '''
    An object that represents a country in a planar graph
    '''


    def __init__(self, border):
        '''
        Constructor:
        boundary is the list of vertices that surrounds the country in counterclockwise order
        '''
        self.border = border   
        
    def __str__(self):
        '''
        returns the string representation of the country_names
        '''
        return str(self.border)
    def __repr__(self):
        '''
        returns the string representation of the country_names
        '''
        return str(self.border)
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Country):
            if self.border == other.border: #borders are same
                return True
            else: #check if borders would coincide after a cyclic shift
                b = self.border.copy()      
                for _ in range(len(self.border) - 1):
                    b = b[1:] + b[:1]
                    #print(b)
                    if b == other.border:
                        return True
        return False
    
def getFromTree(tree):
    '''
    returns a copy of the tree's graph
    '''
    gr = deepcopy(tree.graph)
    fixiki = gr.leaves() 
    gr.reprOnCircle(fixiki)
    gr.calcRubberRepr(fixiki)
    return gr
        
def buildTriangulation(tree):
    '''
    builds a triangulation from the supplied tree
    the tree should be B - tree (every inner vertex has 2 leaves)
    '''
    gr = getFromTree(tree)
    flag = 1
    counter = 0;
    while (flag == 1 and counter < 2 * gr.V):
        #print(counter)
        counter = counter + 1
        flag = gr.outerFaceClosure() 
        #gr.draw(drawLabels = True, block = False)
    if counter == 2 * gr.V :
        print ("buildTriangulation warning: there was too many face closures.")
        
    '''
    In the second step we add two additional vertices and glue leaves to these vertices
    '''
    boundary = gr.getOuterBoundary(typ = "Leaves")
    #print("Boundary = " + str(boundary))

    if (len(boundary) == 0): #this condition is satisfied only if there is no leaves in the 
                            #boundary. In this case the graph must already be a triangulation
        return gr
    extrema =[] #points that occur 3 times in the boundary sequence, and so adjacent to 2 leaves
    for v in range(gr.V):
        if (boundary.count(v) == 3):
            extrema.append(v)
    #print("Extrema = " + str(extrema))
    ind_extrema0 = [i for i in range(len(boundary)) if boundary[i] == extrema[0]]
    #print(ind_extrema0)
    
    #let us rotate the boundary so that that it starts with the first extreme
    #and this extreme is between two leaves
    #We well do it by checking three possibilities for indices of extrema[0]
    flag = False
    for s in range(3):
        boundary_rot = boundary[ind_extrema0[s]:] + boundary[:ind_extrema0[s]]
        #print("Rotated boundary = " + str(boundary_rot))
        j = boundary_rot.index(extrema[1])
        #print(j)
        lvs1 = []
        for k in range(1, j + 2):
            v = boundary_rot[k]
            if gr.degree(v) == 1:
                lvs1.append(v)
                lvs2 = []
        for k in range(j + 3, len(boundary_rot)):
            v = boundary_rot[k]
            if gr.degree(v) == 1:
                lvs2.append(v)
        #check that this lvs1 has only one leaf connected to extrema0
        count = 0
        for leaf in lvs1:
            if gr.adj[leaf][0] == extrema[0]:
                count = count + 1
        if count == 1: #found a suitable sequence of leaves
            flag = True
            break 
    if not flag:
        print("buildTriangulation says: is not able to find a valid lvs1 sequence of leaves")
        print("Graph before gluing leaves to additional vertices: " + str(gr))
        print("lvs1 = " + str(lvs1))
        print("lvs2 = " + str(lvs2))
        gr.draw(drawLabels = True,
            calculateRepr = "Leaves",
            title = "Graph before gluing leaves to additional vertices: ") 
    #print("Graph before gluing leaves to additional vertices: " + str(gr))
    #print("lvs1 = " + str(lvs1))
    #print("lvs2 = " + str(lvs2))
              
    #gr.draw(drawLabels = True,
    #        calculateRepr = "Leaves",
    #        title = "Graph before gluing leaves to additional vertices: ")
    #plt.show()

    
    #now we introduce two new vertices - v1 and v2 and glue leaves from lvs1 and lvs2 to them
    gr.V = gr.V + 2
    gr.adj.append([])
    gr.adj.append([])
    gr.repr.append([0., 0.])
    gr.repr.append([0., 0.])
    v1 = gr.V - 2
    v2 = gr.V - 1
    
    for u in lvs1:
        w = gr.adj[u][0]
        if len(gr.adj[v1]) == 0:
            gr.addEdgeBeforeAfter(v1,w, -1, u)
        else:
            gr.addEdgeBeforeAfter(v1,w, gr.adj[v1][0], u)
        gr.removeEdge(w,u)
    #print("Extrema:" + str(extrema))
    gr.root = extrema[0]    
    gr.rootArrow = v1
    #gr.draw(drawLabels = True, block = False,
    #        calculateRepr = "Boundary", title = "Graph after gluing lvs1: " + str(lvs1))
    #print("Graph after gluing lvs1: " + str(gr))
    
    for u in lvs2:
        w = gr.adj[u][0]
        if len(gr.adj[v2]) == 0:
            gr.addEdgeBeforeAfter(v2, w, -1, u)
        else:
            gr.addEdgeBeforeAfter(v2, w, gr.adj[v2][0], u)
        gr.removeEdge(w,u)
        #print("graph after gluing " + str(v2) + " instead of  " + str(u)  + ": " + str(gr))
    #gr.draw(drawLabels = True, block = False,
    #        calculateRepr = "Boundary", title = "Graph after gluing lvs2: " + str(lvs2))
    #print("Graph after gluing lvs2: " + str(gr))
    
    #connect two additional vertices 
    gr.addEdge(v1, v2)
    #gr.root = extrema[0]
    #gr.rootArrow = v2
    #gr.draw(drawLabels = True, block = False,
    #        calculateRepr = "Boundary", title = "Graph before renaming vertices")
    #gr.draw(drawLabels = True, title = "Graph before renaming vertices")
    
    #remove all singletons and rename the remaining vertices
    vvv = []
    for v in range(gr.V):
        if gr.degree(v) > 0:
            vvv.append(v)
    sgr = gr.subgraph(vvv, gr.root, gr.rootArrow)
    return sgr
    

'''
For testing methods
'''
def main():
    print('Graph.main() started')
    '''
    V = 4
    my_graph = PlanarGraph(V)     
    my_graph.addEdge(0,1)
    my_graph.addEdge(1,3)
    my_graph.addEdge(3,0)
    my_graph.addEdge(3,2)
    my_graph.addEdge(2,0)
    my_graph.addEdge(1,2)
    my_graph.root = 1
    vertices = [0, 1, 2, 3]
    vrepr = np.array(([[0, 0, 1, 1], [0, 1, 1, 0]]))
    vrepr = np.transpose(vrepr)
    my_graph.reprVertices(vertices,vrepr)
    print(my_graph.repr)
    print(my_graph)
    nailedVs = [0, 1, 2]
    my_graph.reprOnCircle(nailedVs)
    my_graph.calcRubberRepr(nailedVs)
    my_graph.draw("Graph 1",  block = False, drawLabels = True)
    '''
    
    '''
    some nice pictures
    '''
    '''
    n = 50
    #seed = 123
    seed = 0 #random, that is, changes from time to time  
    gr = randomTriangulation(n, seed)
    print("Triangulation graph = " + str(gr))
    gr.draw(drawLabels = False, block = False, 
           calculateRepr = "Boundary")
    
    gr.dualGraph()   
    gr.draw(drawLabels = False, block = False, 
            calculateRepr = "Boundary", showDual = True)
   '''
    
    '''
    drawing a tangency circle graphs (the dual graph is very pretty)
    '''  
    n = 50
    #seed = 123
    seed = 0 #random, that is, changes from time to time  
    trngl, _ = tr.randomTriangulation(n, seed)
    _, ax = trngl.graph.draw(drawLabels = False, calculateRepr = "drawCircles")
    trngl.graph.dualGraph()  
    trngl.graph.drawNiceDualGraph()
    
    plt.show()

    
    print('Graph.main() finished')  

    '''  
    (It seems that there is a memory leak somewhere. If the program is left 
    for a long time with plots open, then
    it eats all the computer memory. It may be a problem of matplotlib.)
    '''
    
if __name__ == "__main__":
    main()

