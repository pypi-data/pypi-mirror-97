'''
Created on Aug 2, 2020

@author: vladislavkargin
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
from scipy.optimize import minimize_scalar

import rgs.mndrpy.Meander as mr

''' A couple of functions and plots for the paper about meanders '''

def entropy(x):
    ''' calculates the (binary) entropy function'''
    H = -x * np.log2(x) - (1 - x) * np.log2(1 - x)
    return H

def growthClusterRate(x, meanderRate = 8):
    ''' This function is supposed to calculate the growth in the 
    expected number of cluster-like cycles in a random meander.
    arguments:
    x -- the ratio of ringlets inside the cycle support to the half-length of
    the cycle. Can be between 0 and infty. Can be an array
    meanderRate (M) is the parameter for the growth of meanders (number of meanders of 
    half-length n is = M^n) It is known that it is between 7  a 13.
    returns:
    the growth rate for each choice of x
    '''
    
    R = 16/meanderRate
    #This is unfortunately a wrong expression
    y = - np.log2(R) - 4 * x + entropy(1/(1 + 2 * x)) * (2 + x) 
    
    return y

def maxGrowth(M, bounds = (0.001, 2), precision = 0.001):
    ''' finds the maximum growth rate in the expected 
    number of cluster-like cycles 
    arguments: M - the growth rate in the number of proper meanders 
    (M_n = M^n + error term)
    returns:
     maxG - the maximum growth where the maximum is over ratio of the ringlets 
    to the size of the proper meander
    maximizer - the maximizing ratio of the number of ringlets to the
    size of the meander'''
    x = np.array(np.arange(bounds[0], bounds[1], precision))
    y = growthClusterRate(x, meanderRate = M)
    maxG = np.max(y)
    maximizer = x[np.argmax(y)]
    return maxG, maximizer
    
def findBoundGrowth():    
    ''' finds the upper bound on the growth in the number of proper meanders.
    It is the rate such that the growth rate in the expected number
    of cluster-like meanders is 0.
    returns: 
    criticalM - the bound on the growth rate in the number of proper meanders.
    '''
    criticalM = root_scalar(lambda M: maxGrowth(M)[0], bracket=(7,9))
    return criticalM.root


def upperBound(x):
    '''
    This is a different realization of the same method to bound the growth rate 
    in the number of proper meander.
    parameter: x - ratio of the number of ringlets to the half-size of meander
    returns: the bound on the growth rate lambda for this choice of x. 
        (Here lambda = log2(M), where
        M is the other definition of the growth rate.)  
    '''   
    #this is unfortunately a mistaken expression 
    #y = 4 * (1+x) - (2 + x) * entropy(1/(1 + 2 * x)) 
    #The correct one is  here (note the division by x instead of multiplication
    def f(t):
        if t <= 0:
            z = 10**8
        else:
            z = 4 * (1+t) - (2 + t) * entropy(1/(1 + 2/t)) 
        return z
    try:
        y = list(map(f, x))
    except:
        y = f(x)
    return y

def plotUpperBound():
    '''
    This plots a picture for paper. It plots an upper bound on 
    the meander growth number for various alpha (ratio of number of 
    ringlets to the length of the proper meander)'''
    _, ax = plt.subplots(nrows=1, ncols=1)
    x = np.array(np.arange(0.01, 0.8, 0.01))
    z = upperBound(x)
    ax.plot(x, z)
    ax.grid(True)
    ax.set_xticks(np.arange(0,0.8,0.05))
    ax.tick_params(labelrotation = 90)
    ax.set_xlabel("alpha")
    ax.set_title("An upper bound on the (logarithmic) meander growth rate")
 
def calcCriticalM():   
    #finds the optimal bound on the meander rate M
    maxG = minimize_scalar(upperBound,bounds = (0.01, 1), method = "Brent")
    print(maxG)   
    rateGamma = maxG.fun
    rateM = 2 ** rateGamma  
    print("rate M = ", rateM)
    return rateM

def plotPictureQuasiCluster():
    ''' This is a picture of meanders that have one cycle of half-length 2
    and 2 ringlets'''
    _, ((ax1, ax2, ax3, ax4, ax5), (ax6, ax7, ax8, ax9, ax10),
        (ax11, ax12, ax13, ax14, ax15)) = plt.subplots(nrows=3, ncols=5)
        
    
    mndr = mr.Meander(None, None, uprngArray = [1,0,3,2,7,6,5,4], 
                        dprngArray = [1,0,3,2,5,4,7,6])
    mndr.draw(ax1)
    ax1.set_xticks([])
    ax1.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [1,0,7,4,3,6,5,2], 
                        dprngArray = [1,0,5,4,3,2,7,6])
    mndr.draw(ax2)
    ax2.set_xticks([])
    ax2.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [1,0,7,6,5,4,3,2], 
                        dprngArray = [1,0,3,2,5,4,7,6])
    mndr.draw(ax3)
    ax3.set_xticks([])
    ax3.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [1,0,7,4,3,6,5,2], 
                        dprngArray = [1,0,3,2,7,6,5,4])
    mndr.draw(ax4)
    ax4.set_xticks([])
    ax4.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [1,0,5,4,3,2,7,6], 
                        dprngArray = [1,0,3,2,5,4,7,6])
    mndr.draw(ax5)
    ax5.set_xticks([])
    ax5.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [7,2,1,4,3,6,5,0], 
                        dprngArray = [5,2,1,4,3,0,7,6])

    mndr.draw(ax6)
    ax6.set_xticks([])
    ax6.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [7,2,1,6,5,4,3,0], 
                        dprngArray = [3,2,1,0,5,4,7,6])
    mndr.draw(ax7)
    ax7.set_xticks([])
    ax7.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [7,2,1,4,3,6,5,0], 
                        dprngArray = [3,2,1,0,7,6,5,4])
    mndr.draw(ax8)
    ax8.set_xticks([])
    ax8.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [5,2,1,4,3,0,7,6], 
                        dprngArray = [3,2,1,0,5,4,7,6])
    mndr.draw(ax9)
    ax9.set_xticks([])
    ax9.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [7,6,3,2,5,4,1,0], 
                        dprngArray = [1,0,3,2,5,4,7,6])
    mndr.draw(ax10)
    ax10.set_xticks([])
    ax10.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [7,4,3,2,1,6,5,0], 
                        dprngArray = [1,0,3,2,7,6,5,4])
    mndr.draw(ax11)
    ax11.set_xticks([])
    ax11.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [7,2,1,4,3,6,5,0], 
                        dprngArray = [1,0,7,4,3,6,5,2])
    mndr = mr.Meander(None, None, uprngArray = [5,4,3,2,1,0,7,6], 
                        dprngArray = [1,0,3,2,5,4,7,6])
    mndr.draw(ax12)
    ax12.set_xticks([])
    ax12.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [7,2,1,4,3,6,5,0], 
                        dprngArray = [1,0,7,4,3,6,5,2])
    mndr.draw(ax13)
    ax13.set_xticks([])
    ax13.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [5,2,1,4,3,0,7,6], 
                        dprngArray = [1,0,5,4,3,2,7,6])
    mndr.draw(ax14)
    ax14.set_xticks([])
    ax14.set_yticks([])
    mndr = mr.Meander(None, None, uprngArray = [3,2,1,0,5,4,7,6], 
                        dprngArray = [1,0,3,2,5,4,7,6])
    mndr.draw(ax15)
    ax15.set_xticks([])
    ax15.set_yticks([])
    

#meander numbers from a paper by Jensen and Guttmann [up to M_{22}] 
#they coincide with numbers in the main entry of OEIS - which stops at
#this number
Mnumbers = [1, 1, 2, 8, 42, 262, 1828, 13820 ,110954, 933458, 8152860, 
            73424650, 678390116, 6405031050, 61606881612, 602188541928, 
            5969806669034, 59923200729046, 608188709574124, 6234277838531806,
            64477712119584604, 672265814872772972, 7060941974458061392, 
            74661728661167809752, 794337831754564188184]


#Meander numbers from a note in OEIS. The discrepancy with the previous 
#starts at M24
Mnumbers2 = [1, 1, 2, 8, 42, 262, 1828, 13820 ,110954, 933458, 8152860, 
            73424650, 678390116, 6405031050, 61606881612, 602188541928, 
            5969806669034, 59923200729046, 608188709574124, 6234277838531806,
            64477712119584604, 672265814872772972, 7060941974458061392,
            74661728661167809752, 794337831754570367812, 8499066628515413229282,
            91412898898828176826244, 987975910996038555989486, 
            10726008363361842734385644]

#Number of irreducible meanders
IrrNumbers = [1, 1, 2, 8, 46, 322, 2546, 21870, 199494, 1904624, 
              18846714, 191955370, 2002141126, 21303422480, 
              230553207346, 2531848587534, 28159614749270, 
              316713536035464, 3597509926531778, 41225699113145888, 
              476180721050626814, 5539597373695447322, 
              64863295574835126394, 763984568163192551672, 
              9047263176444565467566, 107672779595584140350702]

'''
Main Calculations
'''
if __name__ == '__main__':
    
    
    '''
    This seems to be wrong because of the mistake in growth cluster rate
    M = 7.467
    x = np.array(np.arange(0.01, 0.8, 0.01))
    y = growthClusterRate(x, meanderRate = M)
    
    fig1, ax1 = plt.subplots(nrows=1, ncols=1)
    ax1.plot(x, y)
    ax1.grid(True)
    
    (maxG, maximizer) = maxGrowth(M)
    print("Maximum growth in cluster probability is ", maxG)
    print("Reached at ", maximizer)     
    criticalM = findBoundGrowth() 
    print("Upper bound on the growth rate in the number of proper meanders:")
    print(criticalM)
    '''
    
    plotUpperBound()
    calcCriticalM()

    k = 24
    print(Mnumbers[k])
    print(Mnumbers[k]**(1/k))
    
    '''
    lengths = np.arange(len(Mnumbers))
    rateM = calcCriticalM()
    n = len(Mnumbers)
    prediction = rateM ** np.arange(n)
    z = np.array(Mnumbers)/prediction
    plt.figure()
    plt.plot(z)
    plt.yscale("log")
    #plt.xscale("log")
    '''
    
    plotPictureQuasiCluster()
    
    plt.figure()
    plt.plot(np.array(Mnumbers)/np.array(IrrNumbers[:25]))
    plt.yscale('log')
    plt.grid(True)
    
    R = (IrrNumbers[24]/Mnumbers[24])**(1/24)
    print(13.39408 - R)
    
    plt.show()
    

    
    pass