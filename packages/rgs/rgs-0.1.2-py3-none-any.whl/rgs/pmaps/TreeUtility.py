'''
Created on Jan 24, 2020

@author: vladislavkargin

Various tools needed for manipulating Trees and Maps

'''
import copy
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

import rgs.pmaps.OrderedTree as ot
#import pmaps.PlanarGraph as pg
import rgs.pmaps.Triangulation as trngl

 
def reweight(w, rho):
    '''
    Reweights a weight sequence by \rho. 
    For an array w, sends w_k to w_k*rho^k and divides the resulting sequence 
    by its sum, so the result is a probability sequence. Returns 
    the reweighted sequence.
    returns a reweighted sequence and its mean. 
    
    The argument w should be a numpy 1-dim array
    '''  
    rw = w
    for i in range(len(w)):
        rw[i] = w[i] * rho ** i         
    #normalizing sum
    s = np.sum(rw)
    rw = rw / s
    mu = 0.
    for i in range(len(rw)):
        mu = mu + i * rw[i]
    return rw, mu


def rescale(w):
    '''
    Obtains a probability weights with expectation 1 from 
    an arbitrary sequence of (non-negative) weights.
    Returns the rescaled sequence
    The argument should be an object convertible to a numpy 1dim array
    '''
    pp, mu = reweight(np.array(w), 1.)
    #initializing search window [a b] for the re-weight parameter.
    b = 1.;
    delta = 0.05;
    while (abs(mu - 1.) > 10 ** (-10)):
        if (mu < 1.):
            b = 1 + delta;
            pp, mu = reweight(pp, b)
            while (mu < 1.):
                pp, mu = reweight(pp, b)
        else:
            b = 1 - delta;
            pp, mu = reweight(pp, b)
            while (mu > 1.):
                pp, mu = reweight(pp, b)
        delta = delta/2;
    return pp

def alphaShift(alpha, w):
    '''
    using a parameter alpha and a weight sequence w
    uses an exponential rescaling on w1, w2, ...  and 
    finds a new sequence wn such that wn[0] = alpha and 
    w1 a probability sequence with mean 1
    '''
    w1 = np.concatenate(([0],w[1:])) #the sequence w with 0 instead of w_0
    #print("w1 = ", w1)
    pp, mu = reweight(w1, 1.)
    pp = pp * (1 - alpha)
    #print("alpha = ", alpha)
    #print("pp = ", pp)
    mu = mu *  (1 - alpha)
    #initializing search window [a b] for the re-weight parameter.
    b = 1.;
    delta = 0.05;
    while (abs(mu - 1.) > 10 ** (-10)):
        if (mu < 1.):
            b = 1 + delta;
            pp, mu = reweight(pp, b)
            pp = pp * (1 - alpha)
            mu = mu *  (1 - alpha)
            while (mu < 1.):
                pp, mu = reweight(pp, b)
                pp = pp * (1 - alpha)
                mu = mu *  (1 - alpha)
        else:
            b = 1 - delta;
            pp, mu = reweight(pp, b)
            pp = pp * (1 - alpha)
            mu = mu *  (1 - alpha)
            while (mu > 1.):
                pp, mu = reweight(pp, b)
                pp = pp * (1 - alpha)
                mu = mu *  (1 - alpha)
        delta = delta/2;
    pp[0] = alpha    
    return pp

def treeToDyckPath(tree):
    '''converts a planar rooted tree to a Dyck path'''
    A = [-1]* tree.graph.V 
    dyckPath = []
    v = tree.graph.root
    stack = [v]
    A[v] = 0 
    #dfsTimes = [0]  #the list of times when a new vertex was discovered.
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
                #dfsTimes.append[len(dyckPath)]
                flag = True
                break #stop searching for an uexplored neighbor
            else: 
                continue
        if (not flag): 
            stack.pop() #no unexplored neighbor around v. Remove it from consideration.
            dyckPath.append(-1)
    del dyckPath[-1]
    return  dyckPath   

def treeToLukasPath(tree):
    '''converts a planar rooted tree to the corresponding Lukasiewicz path
    Assumes that the vertices are already named in the DFS order'''
    path = []
    for v in range(tree.graph.V):
        path.append(tree.outDegree(v) - 1)
    return path    

def treeToHeightPath(tree):
    '''converts a planar rooted tree to the corresponding height path
    Assumes that the vertices are already named in the DFS order'''
    path = []
    for v in range(tree.graph.V):
        path.append(tree.heightVertex(v))
    return path 
        
def cyclicShift(path):
    '''cyclic shift of the path: it finds the first minimum of the path and rotate 
    the sequence of steps so that it starts from this minimum. It is useful for 
    creating Dyck and Lucasiewicz paths. 
    arguments: path (in fact, it is a sequence of steps)
    returns: the shifted path
    '''
    m = 0
    pos = 0
    S = 0
    n = len(path)
    for i in range(n):
        S = S + path[i]
        if (S < m):
            m = S
            pos = i + 1
    if (pos == n):
        return path
    else:
        path = np.concatenate([path[pos:n], path[0:pos]])
        return path.astype(np.int64)   

def randomBridge(n, w, ITER = 10000, SEED = 0):
    ''' creates a random walk bridge that starts at 0, ends at -1 and have
    the distribution of steps w. (w_0 corresponds to step -1)
    returns: the path of the bridge as a sequence of steps. 
    '''
    K = len(w);
    pp = rescale(w)
    #get a sample from multinomial distribution
    count = 0
    mu = 0
    if (SEED != 0):
        np.random.seed(SEED)
    else:
        np.random.seed()
    while (mu != -1 and count < ITER):
        #repeat until the required property of the path is 
        #ensured or too many iteration are used. 
        X = np.random.multinomial(n, pp)
        mu = 0
        for i in range(K):
            mu = mu + (i - 1) * X[i]
        count = count + 1

    if (count == ITER and mu != -1):
        print("RandomLukasiewicz says: Could not find a path that would "
                    + "end in -1 after " + str(ITER) + "iterations")

    #convert multinomial array X to a path
    path = np.array([]);
    for i in range(K): 
        path = np.concatenate([path, np.array([i - 1] * X[i])])
    #print(path)    
    np.random.shuffle(path)
    return path

    '''
     * generate a random L􏰀ukasiewicz path that have n steps, starts at
      (0,0)  and never goes below the horizontal line except at the 
      last step and stops at (n,-1).
     * 
     * A L􏰀ukasiewicz path is a path of a random walk that can steps of 
     size in the set {-1, 0, 1, 2, 3, ...} and that do not go below 
     the horizontal line except at the last step. 
     * 
     * The weights of steps are given in the array w. So w0 is the 
     * probability of the -1 step, w1 probability of 0, w2 probability of 1
     * and so on. 
     * 
     * The generator works in 3 steps
     * 0) from the given sequence of weights generate a sequence of probabilities
     * such that the expectation is close to 1.
     * 1) generate a multinomial partition of n according do the 
     * distribution pp. So we will get N0, N1, N2, ... which will sum
     * to n and have probabilities p0, p1, p2 and so on. 
     * The number Nj represent the number of times the step j-1 occurs in 
     * the path. 
       2) repeat until \sum (j - 1)Nj hits -1 
     * 2) then we create a array of n steps and randomly permute it. 
     * 3) then we do a Vervaat transform to make sure that the path
     * stays above the horizontal line. 
     * 4) repeat until we hit -1
     * 
     * 
     * @param n length of the path
     * @param w weights of the steps. 
     * @param ITER maximum number of attempts to generate the path 
     * @param SEED if seed not 0 then uses provided seed to generate random sequence
     * @return
    '''
def randomLukasiewicz(n, w, ITER = 10000, SEED = 0):
    #generate a random L􏰀ukasiewicz path that have n steps, starts at
    #(0,0)  and never goes below the horizontal line except at the 
    #last step and stops at (n,-1).
    
    path = randomBridge(n, w, ITER = ITER, SEED = SEED)
    shifted_path = cyclicShift(path)
    return shifted_path
        
def randomLukasSlim(k, n, w, ITER = 10000, SEED = 0):
    '''
    This is a slight generalization of randomLukasiewicz function that we need to 
    generate slim trees. The generalization is that we 
    1) build a sequence of n i.i.d variables that sum to -1 
    using the alpha shifted distribution and making sure that there are k steps of size - 1
    2) proceeding as usual in random Lukasiewicz
    arguments: k - number of -1 
    n - length of the sequence 
    w - weight of increments.  
    ITER number of attempts to find the sequence
    SEED - for replication purposes. 
    '''
    weights_len = len(w);
    alpha = k/n
    pp = rescale(w)
    #print('pp = ', pp)
    wn = alphaShift(alpha, pp)
    #get a sample from multinomial distribution
    count = 0
    mu = 0
    if (SEED != 0):
        np.random.seed(SEED)
    while (mu != -1 or count < ITER):
        #print(count)
        #repeat until the required property of the path is 
        #ensured or too many iteration are used. 
        #print('wn = ', wn)
        X = np.random.multinomial(n, wn)
        #print('X = ', X)
        if X[0] != k:
            count = count + 1
            continue
        mu = 0
        for i in range(weights_len):
            mu = mu + (i - 1) * X[i]
        #print("mu =" + str(mu))
        count = count + 1

    if (count == ITER and mu != -1):
        print("Random LukasSlim says: Could not find a path that would "
                + "end in -1 after " + ITER + "iterations")
            #convert multinomial array X to a path
    path = np.array([]);
    for i in range(weights_len): 
        path = np.concatenate([path, np.array([i - 1] * X[i])])
    #print(path)    
    np.random.shuffle(path)        
    #find the minimum 
    m = 0
    pos = 0
    S = 0
    for i in range(n):
        S = S + path[i]
        if (S < m):
            m = S
            pos = i + 1
    if (pos == n):
        return path
    else:
        path = np.concatenate([path[pos:n], path[0:pos]])
        return path.astype(np.int64)  


        
def randomLukas31(n, ITER = 10000, SEED = 0):  
    '''
 * This is a variant of the method that generate Lukasiewicz paths 
 * that will be used to generate random tiangulations according to 
 * Poulalhon - Schaeffer method 
 * We need a path that consists of steps 3 and -1 such that it has 4n - 2 elements 
 * and total weight (sum of steps) -2.  The path should be always above -2 except at
 * the last step.  
 *  
    '''    
    #length of the path 
    N = 4 * n - 2
    pp = [0.75, 0., 0., 0., 0.25]
    K = len(pp) #K = 5
    #get a sample from multinomial distribution
    count = 0 #number of iterations
    mu = 0    #value at the end of the path
    if (SEED != 0):
        np.random.seed(SEED)
    while (mu != -2 or count < ITER):
        #repeat trials until the required property of the path is 
        #ensured or too many iteration are used. 
        X = np.random.multinomial(N, pp)
        mu = 0
        for i in range(K):
            mu = mu + (i - 1) * X[i]
        count = count + 1
    if (count == ITER and mu != -2):
            print("Could not find a path that would "
                    + "end in -2 after " + ITER + "iterations")
    #convert multinomial array X to a path
    path = np.array([]);
    for i in range(K): 
        path = np.concatenate([path, np.array([i - 1] * X[i])])
        #print(path)    
    np.random.shuffle(path)
    #plt.plot(np.cumsum(path))
    #find the minimum 
    m = 0
    pos = 0
    S = 0
    for i in range(N):
        S = S + path[i]
        if (S < m):
            m = S
            pos = i + 1
    #print("pos = " + str(pos))
    if (pos == N):
        return path
    else:
        path = np.concatenate([path[pos:N], path[0:pos]])
        return path.astype(np.int64)
    
              
def decodeToPSTree(path):
    ''' 
    This will take a path with steps 3 and - 1
    (typically generated by randomLukas31) and convert it to 
    a tree where each inner node has only 2 leafs. 
    arguments: path
    returns: the tree
    '''  
    n = (len(path) + 2) /4
    #print("n = " + str(n))
    tree = ot.OrderedTree(3 * int(n))
    #in a sense we trying to do dfs. I believe the path will always start with 3
    # which means we go down from an inner node.
    x = 0 #name of the currently available vertex in the tree
    stack = [x]
    leafMap = {x : 0} #this will be used to check how many leaves vertex x already has
    x = x + 1 #the next available step
    i = 0 #currently processed step in the path
    
    while (i < len(path) and len(stack) > 0):
        #print("stack = " + str(stack))
        #print("i = " + str(i) + "; path[i] = " + str(path[i]))
        v = stack[-1]; #peaking at the top of the stack
        #print("processing vertex v = " + str(v))
        #print("leafMap[v] = " + str(leafMap[v]))
        if (path[i] == 3): #the step is 3 meaning just go down the tree
            tree.graph.addEdge(v, x)
            #print("Adding edge (" + str(v) + ", " + str(x) + ")")
            stack.append(x)
            leafMap[x] = 0
            x = x + 1
            i = i + 1
        else: #the step is - 1
            if (leafMap[v] < 2): #we can add another edge
                tree.graph.addEdge(v, x)
                #print("Adding edge (" + str(v) + ", " + str(x) + ")")
                leafMap[v] = leafMap[v] + 1
                x = x + 1
                i = i + 1 
            else:  #this vertex is done. 
                i  = i + 1
                stack.pop()
                continue
    #print(tree)        
    return tree        

def randomLukasBinary(k, n, ITER = 10000, SEED = 0):
    '''
    generates a random Lukasiewicz path that consist of k steps of size -1, 
    k-1 steps of size 1 and n-2k+1 steps of size 0 
    '''
    #print("seed = " + str(SEED))
    if (SEED != 0):
        np.random.seed(SEED)
    if n < 2 * k + 1:
        print("randomLukasBinary says: n = " + str(n) + " is too small for k = " + str(k))
        return []
    path = [-1] * k + [0] * (n - 2*k + 1) + [1] * (k - 1)
    np.random.shuffle(path)
    m = 0
    pos = 0
    S = 0
    for i in range(n):
        S = S + path[i]
        if (S < m):
            m = S
            pos = i + 1
    #print("pos = " + str(pos))
    if (pos == n):
        return path
    else:
        path = np.concatenate([path[pos:n], path[0:pos]])
        return path.astype(np.int64)
    return path

def decoratedPathTree(n, SEED = 0):
    '''
    builds a (planar) tree that consists of a path of n inner vertices with each inner
    vertex connected to two leaves. It is going to be used in experiments on triangulations
    '''
    if (SEED != 0):
        np.random.seed(SEED)
    tree = ot.OrderedTree(V = 3 * int(n))
    inner = 0
    for i in range(n - 1):
        tree.graph.addEdge(inner, 3 * i + 1)
        tree.graph.addEdge(inner, 3 * i + 2)
        tree.graph.addEdge(inner, 3 * i + 3)
        r = np.random.randint(1,4)
        inner = 3 * i + r
    tree.graph.addEdge(inner, 3 * (n - 1) + 1)
    tree.graph.addEdge(inner, 3 * (n - 1) + 2)
    tree.dfsRename(0)
    return tree
    


def verdiereFunction(x):
    '''
    calculates the integral of atan(e^t) from -\infty to x
    '''
    [v, _] = quad(lambda t: np.arctan(np.exp(t)), -np.inf, x)
    return v



def fromTriangulation(trntn):
    '''
    builds a tree from a triangulation trntn. It is supposed to be the inverse of the 
    map buildTriangulation in PlanarGraph module
    Reference: Poulalhon and Schaeffer "Optimal Coding and Sampling of Triangulations"
    
    Arguments: trntn - a triangulation
    Returns: trFinal - a BT tree (that is a tree where each inner node have two leaves attached.
    '''
    V = trntn.graph.V
    v1 = trntn.graph.root
    v2 = trntn.graph.rootArrow
    boundary = trntn.graph.getOuterBoundary(u0 = v2)
    v0 = boundary[2] 
    T0, T1, T2 = trntn.calcRealizer()
    
    #print("T0 = " + str(T0))
    #print("T1 = " + str(T1))
    #print("T2 = " + str(T2))
      
    tr = copy.deepcopy(trntn)   
    tr.graph.removeEdge(v0, v1)
    tr.graph.removeEdge(v0, v2)
    
    #initialization of the stack
    stack = trntn.graph.adj[v0]
    stack.remove(v1)
    stack.remove(v2)
    #print("Stack = " + str(stack))
    
    #now we need to add two new vertices (and leaves leading to them)
    tr.graph.addVertex()
    tr.graph.addVertex()
    tr.graph.addEdge(v0, V)
    tr.graph.addEdgeBeforeAfter(v0, V + 1, tr.graph.adj[v0][0],0)
    
    #change root and rootArrow
    tr.graph.root = V + 1
    tr.graph.rootArrow = v0
    
    nvertices = V + 2 #current number of vertices in graph tr.  
    marked = [] #processed edges   
    #counter = 0 #this is for debugging purposes
     
    while len(stack) > 0:
        v = stack[-1]
        
        #we are going around the vertex [in the original graph in the clockwise direction]
        # from an edge on the directed path to v2 
        # to an edge on the directed path to v1
        # and do some operations:
        # if we encounter an edge directed to current v, and this edge is not marked (not processed),
        # we mark this endpoint and add it to the stack and proceed 
        # with this new stack element,
        # if we encounter an edge not directed to v, (it must be on a directed path to v2 or v1)
        # and it is not marked, we mark it, remove it in the new graph, add a new leaf in the new graph and 
        #  continue going around v. 
        # when we are finished exploring edges from v between v1 and v2, we remove the vertex from the stack
        # and proceed with a new element on the stack
        
        start = T2[v]
        finish = T1[v]
        spisok = [] #the edges that go from start to finish edges from v in clockwise direction
        #constructing the list spisok
        ind = trntn.graph.adj[v].index(start) 
        x = trntn.graph.adj[v][ind]
        spisok.append(x)
        while x != finish:      
            ind = (ind - 1) % len(trntn.graph.adj[v])
            x = trntn.graph.adj[v][ind]
            spisok.append(x)
        #print("spisok = " + str(spisok))
        #processing edges in spisok
        isNewEdgeFound = False
        for u in spisok:
            if [v, u] in marked:
                continue
            else:
                isNewEdgeFound = True
                marked.append([v, u]) 
                #TODO: edges should be added in clockwise direction - this is different
                #then simply addEdge below
            if u == start or u == finish: 
                tr.graph.removeEdge(v,u)
                tr.graph.addVertex()
                if u == start:
                    tr.graph.addEdge(v, nvertices)
                else:
                    tr.graph.addEdgeBeforeAfter(v, nvertices, tr.graph.adj[v][1], 0) #this behavior is not 
                        #totally in agreement with Poulalhon - Shaeffer paper, but I cannot quite 
                        #understand how the leaves can be at any place but on the ends of the list
                        #of children.
                nvertices = nvertices + 1
            else:
                stack.append(u)
                break
        if not isNewEdgeFound:
            stack.remove(v)
            #counter = counter + 1
            #print("Vertex " + str(v) + "has been processed")
            #print("After vertex " + str(v) + "is processed, the graph is \nç")
            #print(tr)
            #tr.draw(drawLabels = True, calculateRepr = "Leaves", title = "After v = " + str(v) + "is processed")
            #tr.draw(drawLabels = True, title = "After v = " + str(v) + "is processed")
            
        #finally we should remove the edge between v1 and v2 and both vertices themselves
    tr.graph.removeEdge(v1, v2)
    #tr.draw(drawLabels = True, calculateRepr = "Leaves")
    
    #removing v1 and v2 and renaming vertices in dfs order.
    vertices = list(range(tr.graph.V))
    vertices.remove(v1)
    vertices.remove(v2)  
    trFinal = ot.fromGraph(tr.graph.subgraph(vertices, tr.graph.root, tr.graph.rootArrow))    
    return trFinal
    

'''
For testing methods
'''
def main():
    print('Tree Utility is running')
    '''
    Here we check that random Lukasiewicz method works
    '''
    '''
    w = np.array([1, 2, 3])
    rho = 3
    rw, mu = reweight(w, rho)
    print(rw)
    print(mu)
    rw = rescale(w)
    print(rw)
    n = 100
    path = randomLukasiewicz(n, w)
    print(path)
    plt.plot(np.cumsum(path))
    plt.show()
    '''
    
    '''
    Another tree based on Lukasiewicz paths and used to create triangulations
    '''
    '''
    n = 10
    path = randomLukas31(n)
    decodeToPSTree(path)
    plt.plot(np.cumsum(path))
    tree = decodeToPSTree(path)
    print(tree)
    tree.draw(drawLabels = True)
    plt.show()
    '''
    '''
    Test that Verdiere function is working
    '''
    '''
    x = -5
    v = verdiereFunction(x)
    print(v)
    '''
    
    '''
    A binary-unary tree based on Lukasiewicz method.
    '''
    '''
    n = 1000
    k = 300
    path = randomLukasBinary(k, n)
    #print(path)
    plt.plot(np.cumsum(path))
    tree = ot.fromLukasiewicz(path)
    tree.draw()
    '''
    
    '''
    a decorated path tree (path with 2 leaves attached to each vertex)
    '''
    '''
    n = 30
    seed = 123
    tree = decoratedPathTree(n, SEED = seed)
    print(tree)
    tree.draw(drawLabels = False)
    '''
 
    #n = 8
    #seed = 23167
    n = 5
    seed = 0
    #path = [3, -1, -1, -1, 3, -1, -1, -1, -1, -1]
    #btTree = decodeToPSTree(path)
    #trntn = pg.buildTriangulation(btTree)
    trntn, btTree = trngl.randomTriangulation(n, SEED = seed)
    print("btTree is " + str(btTree))
    btTree.draw(drawLabels = True)
    #trntn = pg.randomTriangulation(n, SEED = seed, method = 'decoratedPath')
    _, ax = trntn.draw(drawLabels = True, calculateRepr = "Schnyder")
    realizer = trntn.calcRealizer()
    trntn.drawRealizer(ax, realizer)
    
    
    '''
    tree that we got back from the realizer
    '''
    tr = fromTriangulation(trntn)
    print(tr)
    tr.draw(drawLabels = True, calculateRepr = "Leaves")
    #plt.show()
    
    '''
    TODO something not OK below
    
    newTrntn = pg.buildTriangulation(tr)
    _, ax = newTrntn.draw(drawLabels = True, calculateRepr = "Schnyder")
    realizer = newTrntn.calcRealizer()
    newTrntn.drawRealizer(ax, realizer)
    '''


    '''
    This checks the the generation of the Lukasiewicz path for the slim trees
    
    '''
    w = [1, 1, 1, 1]
    wn = alphaShift(0.3, w)
    print("Shifted weights = " + str(wn) + "\n have sum = " + str(wn.sum()) )
    _, mu = reweight(wn, 1.)
    print(" and expectation " + str(mu))
    
    n = 99
    alpha = 1/3
    k = np.floor(alpha * n)
    print(k)
    
    path1 = randomLukasiewicz(n, w)
    path2 = randomLukasSlim(k, n, w)
    print(path2)
    print(np.sum(path2 == -1))
    
    fig1, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    ax1.plot(np.cumsum(path1))
    ax2.plot(np.cumsum(path2))
    ax1.grid(True)
    ax2.grid(True)
    plt.show()
    
    
    
    print('Tree Utility has finished')
    
if __name__ == '__main__':
    main()