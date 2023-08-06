'''
Created on Jan 24, 2020

@author: vladislavkargin
'''
import numpy as np
import matplotlib.pyplot as plt
import rgs.pmaps.TreeUtility as tu
from rgs.pmaps.PlanarGraph import PlanarGraph



class OrderedTree(object):
    '''
    This is an object that represent a planar rooted tree.

    It is essentially a tree graph with additional structure
    and some convention on what the order of adjacency lists means
    In particular, 
    (0) Usually the root is 0. 
    (1) we will use the convention that the first element in the
    list of adjacent vertices represent the parent with exception 
    of the root vertex. Howeve, if the root is set with setRoot to something != 0,
     then this convention is not ensured. If one wants to change the root and ensure this convention
      then one should run the dfsRename method
    (2) the order of the elements in the adjacency list should correspond to the order in the 
    planar embedding of the tree, in counterclockwise order starting from the edge to
     the parent vertex. 
    '''


    def __init__(self, V = 1, root = 0):
        self.graph = PlanarGraph(V, root)
        self.root = root #this is the root 
                        #[it looks redundant to me. the info about the 
                        #root is already in the graph structure.
        #self.edgeLabels = np.array([])  #This is only used for some labeled trees 
                                        #[so far never used]
        #self.graph.labels = [] #[I think it is never used]
        

    def __str__(self):
        '''
        Returns a string representation of this tree.
        return the graph
        '''
        s = 'Graph of Tree: \n' + str(self.graph) + '\n'
        return s   
    
    def __repr__(self):
        '''
        Returns a string representation of this tree.
        return the graph
        '''
        s = str(self.graph)
        return s     
    
    def setRoot(self, root):
        '''
        changes root of the tree
        the deficiency of this method is that it does not ensure the 
        assumption that the first element in the adjacency list of each vertex 
        except root
        is the parent of the vertex
        '''
        self.root = root
        self.graph.root = root
    
    
    def outDegree(self, v):
        d = len(self.graph.adj[v])
        if v == self.root:
            outdegree = d
        else:
            outdegree = d - 1
        return outdegree
    

    def leaves(self):
        '''
    Returns all the leaves 
        '''
        lvs = []
        for v in range(self.graph.V):
            if self.outDegree(v) == 0:
                lvs.append(v)
        return lvs 
    
    
    def height(self):
        '''
        returns the height of the tree
        '''
        leaves = self.leaves()
        H = 0
        V = 0
        for v in leaves:
            h = self.heightVertex(v)
            if h > H:
                H = h
                V = v
        return H, V
    
    def heightVertex(self, v):
        '''
        measures the distance of vertex v from the root
        '''
        if v == self.graph.root:
            return 0
        dist = 0
        while v != self.graph.root:
            dist = dist + 1
            v = self.graph.adj[v][0] 
        return dist    
    
    def sizeVertex(self, v):
        '''
        calculate the size of the tree below the vertex (this vertex should 
        be different from the root)
        '''
        stack = [v]
        A = [-1]* self.graph.V
        A[v] = 0
        n = 1
        while (len(stack) > 0):
            #print("stack = " + str(stack));
            v = stack[-1]; #peaking at the top of the stack
            #print("processing v = " + str(v))
            flag = False #can we find unprocessed neighbors?
            d = self.graph.degree(v) - 1 #(outdegree)
            for i in range(d):
                w = self.graph.adj[v][i + 1]
                if (A[w] < 0): #this neighbor has not been explored previously
                    A[w] = n
                    n = n + 1
                    stack.append(w)
                    flag = True
                    break #stop searching for an uexplored neighbor
                else: 
                    continue
            if (not flag): 
                stack.pop() #no unexplored neighbor around v. Remove it from consideration.
        return  n  

    
    
        
    def calcHeightsSizes(self, v):    
        '''
    Traverses the tree using dfs starting with v and 
    returns two arrays. The first has the height of each vertex x, which is its distance from
    the root, the second is the size of each vertex x, which is the number of vertices in the 
    subtree rooted at x ( x itself is counted).
        '''
        
        #A[x] is the order in which x appears in the dfs path
        A = [-1]* self.graph.V
        heights = [-1]* self.graph.V 
        sizes = [-1] * self.graph.V
        stack = [v]
        A[v] = 0
        
        heights[v] = 0
        #sizes[v] = self.graph.V - 1 #in principle, this is redundant

        n = 1
        while (len(stack) > 0):
            #print("stack = " + str(stack));
            v = stack[-1]; #peaking at the top of the stack
            #print("processing v = " + str(v))
            flag = False #can we find unprocessed neighbors?
            d = self.graph.degree(v)
            for i in range(d):
                w = self.graph.adj[v][i]
                if (A[w] < 0): #this neighbor has not been explored previously
                    A[w] = n
                    n = n + 1
                    stack.append(w)
                    heights[w] = heights[v] + 1
                    flag = True
                    break #stop searching for an uexplored neighbor
                else: 
                    continue
            if (not flag): 
                stack.pop() #no unexplored neighbor around v. Remove it from consideration.
                sizes[v] = n - A[v]
                
        return  [heights, sizes]  
    '''
    TODO This is not yet implemented
    We need to to some re-ordering of vertices in the adjacency list of the 
    graph
    '''
    '''
    def setRoot(self, root = 0):
        self.root = root
        self.graph.setRoot(root)
    '''
    

    def dfsGeneral(self, v):    
        '''
    A general variant of dfs suitable for unrooted graph. It is starts with v and 
    returns the pair A, dfsPath:
    A[x] is the order in which x appears in the dfs path 
    dfsPath is a sequence of edges in the order in which they were
    first traversed (does not include returns through these edges)
        '''
        A = [-1]* self.graph.V #may be I do not need this 
        stack = [v]
        A[v] = 0
        dfsPath = []
        n = 1
        while (len(stack) > 0):
            #print("stack = " + str(stack));
            v = stack[-1]; #peaking at the top of the stack
            #print("processing v = " + str(v))
            flag = False #can we find unprocessed neighbors?
            d = self.graph.degree(v)
            for i in range(d):
                w = self.graph.adj[v][i]
                if (A[w] < 0): #this neighbor has not been explored previously
                    A[w] = n
                    n = n + 1
                    stack.append(w)
                    #print(dfsPath)
                    dfsPath.append([v, w])
                    flag = True
                    break #stop searching for an uexplored neighbor
                else: 
                    continue
            if (not flag): 
                stack.pop() #no unexplored neighbor around v. Remove it from consideration.
        return  [A, dfsPath]      
    

    def dfsRename(self, v):
        '''
    Rename all vertices of the tree in dfs order starting with vertex v.
    We will do it by creating a new graph
        '''
        [A, dfsPath] = self.dfsGeneral(v)
        V = self.graph.V
        gr = PlanarGraph(V)
        for i in range(V - 1):
            edge = dfsPath[i]
            gr.addEdge(A[edge[0]],A[edge[1]])
        self.root = 0
        self.graph = gr
        self.graph.root = 0
            
    

    def draw(self, drawLabels = False, rootInCenter = False, block = False, 
             calculateRepr = "No", ax = None):
        '''
        Draws the tree
            - block: if block is true, then calling 
            the draw function will stop execution of further commands. 
            if block is false (default), then the execution continues but the calling function
            should have plt.show() at the end. 
        '''
        fixiki = self.leaves() #if we want a correct graphical representation
                            #the leaves should be arranged in a correct order
                            #the easiest way to do it is to 
                            #rename vertices in DFS order (dfsRename method)
        if (rootInCenter): #put root in center: can violate planarity (non self-intersection)
            self.graph.reprOnCircle(fixiki)
            fixiki.append(self.root)
            self.graph.reprVertices([self.root],[[0, 0]])
        else: #treat root as a usual leaf:
            fixiki.append(self.root)
            self.graph.reprOnCircle(fixiki)
        self.graph.calcRubberRepr(fixiki)
        fig1, ax1 = self.graph.draw(root = 0, calculateRepr = calculateRepr,
                drawLabels = drawLabels, block = block, ax = ax)
        return fig1, ax1
    
    def drawPathToVertex(self, ax, v):
        '''
        draws a path that connects a vertex v to the root in the axes given by the argument ax
        The axes should be created by the draw() function
        ''' 
        path = [v];
        if v == self.graph.root:
            print("drawPathToVertex says: the vertex should be different from the root")
            return 
        else:
            while v != self.graph.root:
                v = self.graph.adj[v][0]
                path.append(v)
            self.graph.drawPath(ax, path)
         
    
    #def setLabels(self, labels):
        '''
        set the labels of vertices
        '''
    #    self.graph.labels = labels
        
def fromGraph(gr):
    '''
    builds the tree from the graph gr (which should be a tree topologically). 
    The vertices are renamed in dfs order.  
    '''      
    tr = OrderedTree(V = gr.V, root = gr.root)
    tr.graph = gr
    tr.dfsRename(gr.root)
    return tr
    

def fromLukasiewicz(path):
    '''
    Returns a rooted planar tree created from a Lukasiewicz path
    '''
    V = len(path)
    #print(path)
    tr = OrderedTree(V);
    stack = [0] #put root on the stack
    x = 1 #current available vertex
    for i in range(V):
        v = stack.pop()
        #print("working on " + str(v))
        k = int(path[i] + 1)
        if (k > 0):
            #print("k =" + str(k));
            for _ in range(k):
                tr.graph.addEdge(x, v)
                stack.append(x)
                x = x + 1
        #print(stack)
    tr.dfsRename(0)
    return tr

'''
returns a random simply generated tree on n vertices using the weights in w
The algorithm works by building a random Lukasiewicz path and converting it to tree
'''

def randomTree(n, w, SEED = 0):
    path = tu.randomLukasiewicz(n, w, SEED = SEED)
    tr = fromLukasiewicz(path) 
    return tr  


def randomBTree(n, SEED = 0):
    '''
    returns a random B tree with n inner nodes each of which has 2 leaves
    This is used for building a triangulation
    '''
    path = tu.randomLukas31(n, SEED = SEED)
    tr= tu.decodeToPSTree(path)  
    return tr

def randomSlimTree(k, n, W = [], SEED = 0):
    '''
    generates a random Galton-Watson tree that has k leaves and n vertices
    Arguments:
    k - number of leaves
    n - number of vertices 
    W - if it is empty then the function assumes that the tree is binary/unary,
        if not we will use it as the weight sequence for the original Galton-Watson tree
    returns the random tree 
    
    TODO - improve to be able to work for any distribution of weights
    '''
    if len(W) == 0:
        path = tu.randomLukasBinary(k, n, SEED = SEED)
        tree = fromLukasiewicz(path)
    else:
        w1 = tu.rescale(W)
        #print(w1)
        path = tu.randomLukasSlim(k, n, w1, SEED = SEED)
        #print("path = ", path)
        tree = fromLukasiewicz(path)
        #print(tree)
    return tree




'''
creates a random embedding of the tree by 
assigning labels from {-1, 0, 1} to edges
'''
'''
def randomEdgeLabel(self):
    self.edgeLabels=np.random.randint(-1, 2, self.V - 1)
'''

'''  
visits every vertex by DFS and calculates the vertex labels
'''    
'''    
def calcVertexLabels(self):
    stack = [self.root]
    path = []
    self.vertexLabels[self.root] = 1;
    edge = 0;
    while (len(stack) > 0):
        x = stack[-1] #current element on top of the stack
        path.append(x)
        if (self.outdegree(x) == 0): #this is a leaf, do not go deeper
            stack.pop()
        else:
            children = self.graph.adj[x].remove(0)
            for child in children:
                self.vertexLabels[child] = self.vertexLabels[x] + self.edgeLabels[edge]
                edge = edge + 1
                stack.append(child)                
    pass
'''    
    

'''
For testing methods
'''
def main():
    print('OrderedTree methods are used')  
    w = np.array([1] * 3)
    #rw = tu.rescale(w) #This rescaling is done in function that generates Lukasiewicz path
    #print(rw)
    
    n = 10
    seed = 12345
    #seed = 0 #(random - changing from one execution to another)

    tr = randomTree(n, w, SEED = seed)
    #tr = randomBTree(n, SEED = seed) 
    print(tr)
    tr.draw(drawLabels=True)

    heights, sizes = tr.calcHeightsSizes(0)
    print("heights = " + str(heights))
    print("sizes = " + str(sizes))
    
    
    '''
    These are some drawings and calculations associated with Slim Trees
    '''
    
    n = 400
    #n = 20
    seed = 12345
    seed = 0
    k = 10
    tr = randomSlimTree(k, n, SEED = seed)
    #print(tr)
    #fig, ax = tr.draw(drawLabels = True, block = False)
    #fig, ax = tr.draw(drawLabels = False, block = False)  
    #fig1, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    _, ax = tr.draw(drawLabels = False, block = False)  
    H, v = tr.height()
    dist = tr.heightVertex(v);
    print("Height of vertex " + str(v) + " is " + str(dist))
    tr.drawPathToVertex(ax, v)
    print("Height of the tree is " + str(H))  
    v = 1
    S = tr.sizeVertex(v)
    print("size of vertex " + str(v) + " is " + str(S))
    
    
    
    
    plt.show() 
    
    
   
    
    
    
if __name__ == "__main__":
    main()
    