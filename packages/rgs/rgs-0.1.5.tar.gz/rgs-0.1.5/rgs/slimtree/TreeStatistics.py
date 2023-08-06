'''
Created on Sep 6, 2020

@author: vladislavkargin
'''

import numpy as np
import matplotlib.pyplot as plt

import pmaps.OrderedTree as ot
import pmaps.TreeUtility as tutil

'''
For testing methods
'''
def main():
    n = 200
    w = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #w = [1, 0, 1]
    
    '''
    #Calculate the Kolmogorov - Smirnov statistic
    ITER = 10000
    KSsample = []
    for count in range(ITER):
        if (count % 1000 == 0):
            print(count)
        path1 = tutil.randomBridge(n, w, SEED = 0)
        Mplus = max(np.cumsum(path1))
        Mmin = - min(np.cumsum(path1))
        KSsample.append(max([Mplus, Mmin])/np.sqrt(n))
    print(np.mean(KSsample)/np.sqrt(2))
    plt.plot(KSsample)
    '''
    
    '''calculating average height of the trees '''
    ITER = 100
    EHlist0 = [] #predicted expected height
    EHlist = [] #experimental average height
    alpha_range = np.linspace(0.1, 0.95, num = 20, endpoint = False)
    for alpha in alpha_range:
        print("alpha = ", alpha)
        EHlist0.append(np.sqrt((1-alpha)/alpha * np.pi * n))
        k = np.floor(n * alpha)
        H = []
        count = 0
        while count < ITER:
            if count % 100 == 0:
                print("count = ", count)
            try:
                tree = ot.randomSlimTree(k, n, w, SEED = 0)
                h = tree.height()
                H.append(h[0])
                count = count + 1
            except:
                print("there was an error in tree generation at step ", count)
        EH = np.average(H)
        print("EH = ", EH)
        EHlist.append(EH)        
    plt.plot(alpha_range, EHlist, label = "experimental")
    plt.plot(alpha_range, EHlist0, label = "predicted")
    plt.legend()
    plt.grid()
    plt.title("Average tree height, n = " + str(n))
    plt.xlabel("alpha")
    
    #plt.xkcd()
    #plt.xticks()
        #tree.draw()
    
    
    plt.show()
        

if __name__ == '__main__':
    main()