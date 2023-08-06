'''
Created on Apr 25, 2020

@author: vladislavkargin
'''

class Graph(object):
    '''
    this is a class for a simple graph object
    TODO: This is not yet complete since I don't actually use it 
    '''

    #Creates a graph with v vertices and no edges
    def __init__(self, V = 0):
        self.V = V
        self.E = 0
        self.adj = []; #list of adjacency lists for vertices
    '''
    Returns a string representation of this graph.
    
    return the number of vertices V, followed by the number
    of edges E, followed by the V adjacency lists
    '''
    def __str__(self):
        s = "V = " + str(self.V) + ', E = ' + str(self.E) + '\n'
        for i in range(self.V):
            s = s + str(i) + " -> " + str(self.adj[i]) + '\n'
        return s    
    
    '''
    calculates the degree of vertex v
    '''
    def degree(self, v):
        d = len(self.adj[v])
        return d
    
        # Adds the undirected edge u-v to this graph.    
    def addEdge(self, u, v): 
        self.E = self.E + 1
        self.adj[u].append(v)
        self.adj[v].append(u) 