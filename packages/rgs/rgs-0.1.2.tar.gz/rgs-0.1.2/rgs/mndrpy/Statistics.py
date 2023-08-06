'''
Created on Jul 25, 2020

@author: vladislavkargin
'''
import rgs.mndrpy.Meander as Meander
import rgs.mndrpy.Utility as ut

import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import skew


def statsLargestCycle(n, ITER = 1000, method = "Uniform", w = None, seed = None):
    '''
    calculate the mean and the variances 
    of the largest cycle in a sample of ITER random meanders
    '''   
    if seed != None:
        np.random.seed(seed) 
    listL = []
    for count in range(ITER):
        if count > 0 and count % 10000 == 0:
            print("statsLargeCycle : iteration " + str(count))
        if method == "Uniform":
            mndr = Meander.randomMeander(n)
        elif method == "Semi":
            mndr = Meander.randomSemiMeander(n)
        elif method == "Weighted":
            mndr = Meander.randomMeander(n, w)
        elif method == "Comb":
            mndr = Meander.randomComb(n)
        elif method == "CrossSemi":
            mndr = Meander.randomCrossSemiMeander(n)
        else: 
            print("StatsLargestCycle says: Unknown type of a random meander")
            return
        lengths = mndr.calcCycleLengths()
        L = max(lengths)
        listL.append(L)
    listL = np.array(listL)
    M = np.mean(listL)
    S = np.std(listL)
    skewness = skew(listL)
    return M, S, skewness, listL

def statsLargestClusterCycle(n, max_gap_size = 3, ITER = 1000):
    '''calculate the mean of the largest cluster cycle'''
    listL = []
    for _ in range(ITER):
        '''
        if count % 1000 == 0:
            print("statsLargestClusterCycle : iteration " + str(count))
        '''
        mndr = Meander.randomMeander(n)
        listL.append(ut.largestClusterLength(mndr,
                            max_gap_size = max_gap_size))
    M = np.mean(listL)
    return M


def statsCycleSpectrum(n, ITER = 10000, method = "Uniform", w = None, seed = None):
    '''calculate the distribution of cycles over cycles lengths
    parameters:
    n = half-length of the meander system, 
    ITER = number of elements in the sample, 
    method = methods for meander generation
    w - pair of weight sequence needed if the method = "Weighted"
    seed - for replication purposes
    returns:
    listL - array of cycle lengths combined for all iterations
    counts - counts of cycle lengths in all iterations 
    '''
    if seed != None:
        np.random.seed(seed) 
    listL = []
    for count in range(ITER):
        if count % 10 == 0:
            print(count)
        if method == "Uniform":
            mndr = Meander.randomMeander(n)
        elif method == "Semi":
            mndr = Meander.randomSemiMeander(n)
        elif method == "Weighted":
            mndr = Meander.randomMeander(n, w)
        elif method == "Comb":
            mndr = Meander.randomComb(n)
        else: 
            print("StatsLargestCycle says: Unknown type of a random meander")
            return
        lengths = mndr.calcCycleLengths()
        listL = listL + lengths
    listL = np.array(listL)
    counts = []
    for i in range(2, np.max(listL) + 2, 2):
        counts.append(np.count_nonzero(listL == i))
    counts = np.array(counts)/ITER
        
    return listL, counts
    
def statsSpacings(n, ITER = 1, method = "Uniform", w = None, seed = None):
    '''
    calculate the statistics of spacings
    of the largest cycle in a sample of ITER random meanders. Each of meanders 
    have length n
    parameters:
    n - length of the meanders. 
    returns:
    S array of spacings in all iterations
    Sp a matched array of spacings from randomly distributed points. 
    M mean of S
    Mp mean of Sp
    '''   
    if seed != None:
        np.random.seed(seed) 
    S = np.array([])
    Sp = np.array([])
    for count in range(ITER):
        if count % 1000 == 0:
            print("statsSpacings : iteration " + str(count))
        if method == "Uniform":
            mndr = Meander.randomMeander(n)
        elif method == "Semi":
            mndr = Meander.randomSemiMeander(n)
        elif method == "Weighted":
            mndr = Meander.randomMeander(n, w)
        elif method == "Comb":
            mndr = Meander.randomComb(n)
        else: 
            print("StatsLargestCycle says: Unknown type of a random meander")
            return
        #mndr.draw()
        (cycles, _) = mndr.findCycles()
        lengths = list(map(lambda x: len(x), cycles))
        L = max(lengths)
        largestC = cycles[lengths.index(L)]
        #print(largestC)
        support = np.sort(largestC)
        L = len(support)
        X = np.arange(2 * n)
        np.random.shuffle(X)
        #print(X)
        X = np.sort(X[:L])
        #print(X)
        spacings = np.diff(support)
        spacingsX = np.diff(X)
        #print(spacingsX)
        S = np.hstack([S, spacings])
        Sp = np.hstack([Sp, spacingsX])
    #calculate means
    M = np.mean(S)
    Mp = np.mean(Sp)
    return S, Sp, M, Mp

def plotMeanAndStdLargestCycle(Nmin, Nmax, ITER, ticks_step = 10, 
                               ymin = 1.6, ymax = 2.3, 
                               methods = ["Uniform"], seed = None):
    
    '''this is a program that creates plots for my meander paper.
    Namely, it creates the plots that show the mean and the std of the largest 
    cycle of a random meander system, normalized by n^\alpha
    parameters:
    Nmin - minimal length of the meander system
    Mmax - maximum length of the meander system
    ymin - lower limit for y-axis
    ymas - upper limit for y-axis
    ITER - number of sample points for meander systems of given length
    method - type of the random meander system
    seed - the seed for random generator if reproducibility is needed. 
    '''
    def normalizer(n):
        if method in ["Uniform", "Semi", "Weighted", "CrossSemi"]:
            return n ** alpha
        elif method == "Comb":
            return np.log2(n) * alpha
        else:
            print("normalizer says: unknown method")
            return 0
    
    '''
    alpha - parameter for normalization
    step - the step between length of meanders
    ticks_step - the step between ticks on the plot
    '''
    
    _, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.grid(True)
    ax1.xaxis.set_ticks(np.arange(Nmin,Nmax + 1,ticks_step))
    ax1.set_title("Normalized mean of the largest cycle length")
    ax1.set_xlabel("meander system half-length $n$")
    
    _, ax2 = plt.subplots(nrows=1, ncols=1)
    ax2.grid(True)
    ax2.xaxis.set_ticks(np.arange(Nmin, Nmax + 1,ticks_step))
    ax2.set_title("Normalized std of the largest cycle length")
    ax2.set_xlabel("meander system half-length $n$")   
    
    w = ([1,1,1], [1,1,1]) 
    
    for method in methods:
        step = 1
        if method == "Uniform":
            alpha = 4/5
            style = 'r-'
        elif method == "Semi":
            alpha = 4/5
            style = 'b--'
        elif method == "Weighted":
            alpha = 4/5
            step = 10
            style = 'g-.'
        elif method == "Comb":
            alpha = 1 #this is alpha for logarithm
            style = 'r-'
        elif method == "CrossSemi":
            alpha = 1
            style = 'm-'
        
        mLC = []
        sLC = []
        for n in range(Nmin, Nmax + 1, step):
            if n % 10 == 0:
                print(method + " : " + str(n))          
            (M, S, _, _) = statsLargestCycle(n, ITER = ITER, method = method, w = w, seed = seed)
            mLC.append(M/normalizer(n))
            sLC.append(S/normalizer(n))
        mLC = np.array(mLC)
        sLC = np.array(sLC)
        #print(mLC)
        #print(sLC)
    
        ax1.plot(np.arange(Nmin,Nmax + 1, step), mLC, style, label = method)
        ax1.yaxis.set_ticks(np.arange(ymin, ymax, 0.02))
        if method in ["Uniform", "Semi", "Weighted"]:
            ax1.set_ylabel("$\overline{L}/n^{4/5}$")
        elif method in ["CrossSemi"]:
            ax1.set_ylabel("$\overline{L}/n^{1}$")
        else: 
            ax1.set_ylabel("$\overline{L}/\log_2 n$")
        
        ax2.plot(np.arange(Nmin,Nmax + 1,step), sLC, style, label = method)
        if method in ["Uniform", "Semi", "Weighted"]:
            ax2.yaxis.set_ticks(np.arange(ymin - 1, ymax - 1, 0.02))
            ax2.set_ylabel("$\mathrm{std}(L)/n^{4/5}$")
        elif method in ["CrossSemi"]:
            ax2.set_ylabel("$\overline{L}/n^{1}$")
        else: 
            ax2.yaxis.set_ticks(np.arange(ymin - 1.5, ymax - 1.5, 0.02))
            ax2.set_ylabel("$\mathrm{std}(L)/\log_2 n$")
            
    ax1.legend()
    ax2.legend()

def plotLargestClusterSize(Nmin, Nmax, max_gap_size = 3, ITER = 1000,
                            step = 10, tick_step = 100):
    def normalizer(n):
            return np.log2(n)
    mLC = []
    for n in range(Nmin, Nmax + 1, step):
        if n % 100 == 0:
                print("plotLargestClusterSize: iteration " + str(n))          
        M = statsLargestClusterCycle(n, max_gap_size = max_gap_size, ITER = ITER)
        mLC.append(M/normalizer(n))
    mLC = np.array(mLC)
    _, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.grid(True)
    ax1.xaxis.set_ticks(np.arange(Nmin,Nmax + 1,tick_step))
    ax1.set_title("Normalized mean of the largest cluster cycle length")
    ax1.set_xlabel("meander system half-length $n$")
    ax1.plot(np.arange(Nmin,Nmax + 1, step), mLC)
    
    
def plotCycleSpectrum(n, ITER = 1000, method = "Uniform", seed = None):
    ''' plots the counts of cycle lengths in order to show the dependence of 
    counts on the cycle length
    '''

    lengths, counts = statsCycleSpectrum(n, method = method, ITER = ITER, seed = seed)
    print("Cycle lengths = " + str(lengths) + "\n and counts/n * 8 = " + str(counts * 8 /n))
    #normalize counts: 
    #counts_norm1 = np.log(10**(-7) + counts * 8 /n) #/np.log(np.arange(2, counts.shape[0] + 2))
    #counts_norm2 = np.log(10**(-7) + counts * 8 /n)/np.log(np.arange(2, counts.shape[0] + 2))
    L = counts.shape[0]
    counts_pred = 1.4/(np.arange(1, L + 1)**2)
    
    #plt.plot(counts * 8/n)
    
    _, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    ax1.grid(True)
    ax1.plot(counts * 8/n, label = "cycle counts")
    ax1.plot(counts_pred, label = "predicted cycle counts")
    ax1.set_yscale("log")
    #ax2.set_xscale("log", basex = 2)
    ax1.set_title("Counts of cycles with length k normalized by n/8")
    ax1.legend()
    ax1.set_xlabel("$k$")
    ax1.set_ylabel("$8 \overline{Y}/n$")
    
    ax2.grid(True)
    ax2.plot(counts * 8/n, label = "cycle counts")
    ax2.plot(counts_pred, label = "predicted cycle counts")
    ax2.set_yscale("log")
    ax2.set_xscale("log")
    #ax2.set_title("Counts of cycles with length k normalized by n/8")
    ax2.legend()
    ax2.set_xlabel("$k$")
    ax2.set_ylabel("$8 \overline{Y}/n$")
    
    #ax1.plot(counts_norm1) 
    #ax2.plot(counts_norm2)   
    
def histLargestCycleLength(n, ITER = 10000, bins = 30, 
                           method = "Uniform", seed = None):    
    '''plots the histogram of largest cycle length normalized by n^{4/5}'''
    M, S, skewness, lengths = statsLargestCycle(n, ITER = ITER, method = method,
                                                 seed = seed)
    
    print(" M = " + str(M/n**(4/5)) + "; S = " + str(S/n**(4/5)) + "; skewness = " + str(skewness))
    
    plt.hist(lengths/n**(4/5), bins = bins, density = True)
    plt.grid(True)
    plt.title("Density of the normalized largest cycle length")
    plt.xlabel("$L/n^{4/5}$")

def histLargestCycleSpacing(n, beta = 1, ITER = 10000, bins = 30, 
                            method = "Uniform", seed = None):   
    ''' plots the histogram of spacings in a large cycle in comparison 
    with spacings of uniformly distributed points. The spacings are 
    normalized by n^beta where n is the half-length of the meander system.'''
    S, Sp, _, _ = statsSpacings(n, ITER = ITER, method = method, seed = seed)
    #print(S)
    #print(Sp)
    #frequency of short spacings in largest cycle and random points spacings
    N1 = np.count_nonzero(S == 1)
    print("Percentage of spacings of length 1 in largest cycle = " + str(N1/len(S)))
    N3 = np.count_nonzero(S == 3)
    print("Percentage of spacings of length 3 in LC = " + str(N3/len(S)))   
    N5 = np.count_nonzero(S == 5)
    print("Percentage of spacings of length 5 in LC = " + str(N5/len(S)))   
    
    N1p = np.count_nonzero(Sp == 1)
    print("Percentage of spacings of length 1 in matching sample of uniform points = " 
          + str(N1p/len(S)))
    N3p = np.count_nonzero(Sp == 3)
    print("Percentage of spacings of length 3 in MSofUP = " + str(N3p/len(S)))   
    N5p = np.count_nonzero(Sp == 5)
    print("Percentage of spacings of length 5 in MSofUP = " + str(N5p/len(S)))  
    
    Snorm = S/(n ** beta)  
    Spnorm = Sp/(n ** beta)
    _, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.hist(Spnorm, bins = bins, density = True, label = "Random points spacings")
    ax1.hist(Snorm, bins = bins, density = True, alpha = 0.5, label = "Largest cycle spacings")
    ax1.set_title("Histogram of spacings in the largest cycle")
    ax1.set_xlabel("spacing size $/n$")
    ax1.set_yscale('log', nonposy='clip')
    #ax1.set_xscale('log')
    ax1.legend()
    '''
    ax2.hist(Spnorm, bins = 50, density = True, label = "Random points spacings")
    ax2.hist(Snorm, bins = 50, density = True, alpha = 0.5, label = "Largest cycle spacings")
    #ax2.set_title("Histogram of spacings in the largest cycle")
    ax2.set_xlabel("spacing size $/n^{1/5}$")
    ax2.set_yscale('log', nonposy='clip')
    #ax2.set_xscale('log')
    ax2.legend()
    ''' 
    
'''
For testing methods
'''
def main():
    
    
    '''Plotting a picture of growth in the length of the largest cycle 
    depending on meander half-size n'''
    Nmin = 10
    Nmax = 200  #target 2000
    ticks_step = 100
    ITER = 500  #target 4000
    #methods = ["Uniform", "Semi", "Weighted"]
    methods = ["CrossSemi"]
    
    plotMeanAndStdLargestCycle(Nmin, Nmax, ITER, ticks_step = ticks_step, methods = methods)
    
    '''Plotting the distribution of cycle lengths in a large meander system'''
    #n = 100000
    #ITER = 1000
    #method = "Uniform"
    #plotCycleSpectrum(n, ITER = ITER, method = method)  

    
      
    ''' Plotting the distribution of the largest cycle length in a large meander system'''
    #n = 2000 
    #ITER = 100000 #target 1000000
    #method = "Uniform"
    #bins = 50
    #histLargestCycleLength(n, ITER = ITER, bins = bins, method = method)
 
    
    '''Showing the histogram of the spacings in the largest cycle of a m.s.'''
    #n = 2000 #target 2000
    #ITER = 50000 #target 50000
    #bins = 50
    #histLargestCycleSpacing(n, ITER = ITER, bins = bins)
    
    '''
    #Now let us study how the average spacing grows with n
    Nmin = 100
    Nmax = 6000  #target 2000
    step = 100
    ITER = 400  #target 4000
    method = "Uniform"
    w = None
    seed = None
    ticks_step = 500
    ymin = 0.8
    ymax = 1.2
    style1 = 'r-'
    style2 = 'b--'
    
    _, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.grid(True)
    ax1.xaxis.set_ticks(np.arange(Nmin,Nmax + 1,ticks_step))
    ax1.set_title("Normalized mean of the largest cycle spacings")
    ax1.set_xlabel("meander system half-length $n$")
    mLC = []
    sLC = []
    for n in range(Nmin, Nmax + 1, step):
        if n % 100 == 0:
            print(method + " : " + str(n))          
        (_, _, M, Mp) = statsSpacings(n, ITER = ITER, method = method,
                                        w = w, seed = seed)
        mLC.append(M/n**(1/5))
        sLC.append(Mp/n**(1/5))
    mLC = np.array(mLC)
    sLC = np.array(sLC)
    #print(mLC)
    #print(sLC)

    ax1.plot(np.arange(Nmin,Nmax + 1, step), mLC, style1, label = "Largest Cycle")
    ax1.plot(np.arange(Nmin,Nmax + 1, step), sLC, style2, label = "Uniform Points")
    ax1.yaxis.set_ticks(np.arange(ymin, ymax, 0.02))
    if method in ["Uniform", "Semi", "Weighted"]:
        ax1.set_ylabel("$\overline{S}/n^{1/5}$")
    else: 
        ax1.set_ylabel("$\overline{S}/\log_2 n$")
    ax1.legend()
    '''
    
    '''
    plots the largest cluster cycle size (normalized)
    '''
    '''
    Nmin = 10
    Nmax = 2000
    ITER = 100
    max_gap_size = 5
    plotLargestClusterSize(Nmin, Nmax, max_gap_size = max_gap_size, 
                           ITER = ITER)
    '''
    
    plt.show()  


if __name__ == '__main__':
    main()