'''
Created on Feb 12, 2021

@author: vladislavkargin
'''

''' This is a file for various experiments with Temperley-Lieb algebra '''
import scipy.special as special
import matplotlib.pyplot as plt

import rgs.mndrpy.Pairing as pr
import rgs.mndrpy.ElementTL as tl
import rgs.mndrpy.Utility as ut

def simplify(prng):
    ''' This is the first step to write the pairing in a normal form when 
    we think about the pairing as an element of the Temperley - Lieb algebra
    (see paper of Di Francesco about meander determinant.
    Arguments: prng - a pairing
    Returns: a 3-tuple that consists from index of e_i (which is associated
    with a ringlet, depth of the ringlet 
    (which is needed if we want
    to use this pairing as an encoding of a basis 2 element), and 
    the simplified pairing.
    '''
    N = len(prng.prng)
    #find all ringlets
    ringlets = []
    for i in range(N):
        if prng.prng[i] == i + 1:
            ringlets.append(i)
    #find depths of ringlets (it is easier to do it using the path 
    #representation of the pairing
    path = pr.prng2path(prng)
    x = 0
    y = 0
    S = [(x, y)] #these are the points on the Dyck path.
    for i in range(N):
        if path[i] == 1:
            y += 1
        else:
            x += 1
        S.append((x,y))
    depths = [0] * len(ringlets)
    for i in range(len(ringlets)):
        s = ringlets[i]
        depths[i] = S[s + 1][1] - S[s + 1][0] - 1
    #print("Depths are ", depths)
    #find the first ringlet with the largest depth
    max_depth = max(depths)
    i = depths.index(max_depth)
    x = ringlets[i]
    '''
    depth = 0
    for i in range(len(ringlets)):
        if i == 0 and ringlets[i] > 0:
            x = ringlets[i]
            depth = ringlets[i]
            break
        elif i > 0 and ringlets[i] - ringlets[i - 1] > 2:
            #print(ringlets[i - 1], ringlets[i])
            x = ringlets[i]
            depth = ringlets[i] - ringlets[i-1] - 2
            break
        else: 
            continue
    '''
    #now we calculate the simplified pairing, assuming that 
    #there is a ringlet with positive depth
    if max_depth > 0:
        prng_copy = list(prng.prng)
        y = prng.prng[x - 1]
        prng_copy[x - 1] = x 
        prng_copy[x] = x - 1
        prng_copy[x + 1] = y
        prng_copy[y] = x + 1
        prngS = pr.Pairing(prngArray = prng_copy)
    else:
        prngS = None  
    
    return (ringlets, x, max_depth, prngS)

def normalForm(prng):
    ''' calculate the normal form of the pairing as defined in the 
    paper by DiFrancesco about meander determinants.
    returns: the sequence of the indices of e_i (which is the position of 
    an actionable ringlet) and the depths of the corresponding
    ringlets. The positions are  '''
    nf = []
    prngS = pr.Pairing(prngArray = prng.prng)
    while prngS != None:
        _, x, depth, prngS = simplify(prngS)
        #print(x, depth, prngS)
        if prngS != None:
            nf.append((x,depth))
    return nf

def act(x, prng):
    ''' Acts by e_x on prng. In the picture with Dyck paths this corresponds 
    to adding a square in a valley. A sequence of these actions corresponding
    to the normal form  builds a pairing from the standard pairing.
    Arguments: x - position to act
    prng - prng to act on
    returns: new pairing 
    '''
    #first we need to check that the action is possible 
    N = len(prng.prng)
    if x <= 0 or x >= N - 1:
        print("act says: x should be between 1 and 2n - 2")
        return 
    if prng.prng[x] > x or prng.prng[x + 1] < x + 1:
        print("act says: cannot act by ", x, "on pairing ", str(prng))
        print("x is not a valley in the corresponding Dyck path")
        return 
    prng0 = list(prng.prng)
    y = prng0[x]
    z = prng0[x + 1]
    prng0[y] = z 
    prng0[z] = y
    prng0[x] = x + 1
    prng0[x + 1] = x 
    p = pr.Pairing(prngArray = prng0)
    return p

def act2(x, k, q, el):
    ''' Acts by e_x on an element of TL algebra in the ideal considered
    by Di Francesco.
    In the picture with Dyck paths this corresponds 
    to adding a square in a valley. 
    This is a second variant of the action used by Di Francesco in
     orthogonalization
    Arguments: x - position to act
    k - height at which to act
    q - parameter of the TL algebra
    prng - prng to act on
    returns: an element of a left ideal in TL algebra (see Di Francesco.
    '''
    #TODO
    mu_k = special.eval_chebyu(k - 1, q/2)/special.eval_chebyu(k, q/2)
    #print(mu_k)
    el_new = tl.ElementTL({})
    if isinstance(el, pr.Pairing):
        prng1 = act(x, el)
        el_new = tl.ElementTL({prng1:1}) + tl.ElementTL({el:mu_k})
    elif isinstance(el, tl.ElementTL):
        for prng in el.S.keys():
            el_new = el_new + act2(x,k,q,prng) * el.S[prng]
    else:
        print("act2 says: wrong type of the element")
    return el_new
    


def nf2pairing(nf, n):
    '''takes a normal form and recovers the pairing
    Normal form can be either a sequence of x (locations of valleys in
    the Dyck path representation where we insert a square), or 
    sequence of (x, h_x) where  and h_x is the height of 
    the squares that we insert. In this algorithm we use only 
    the sequence of x-ses.
    arguments: nf - normal form
    n - half-length of the resulting pairing
    returns: the resulting pairing '''
    prng = pr.standardPairing(n)
    if type(nf[-1]) == tuple:
        Xs = list(zip(*nf))[0]
    else:
        Xs = nf
    for x in reversed(Xs):
        prng = act(x, prng)
    return prng


'''
For testing methods
'''
def main():
    pass
    
    widths = [3, 1, 4]
    n = sum(widths)
    prng = pr.rainbows(widths)
    prng.draw()
    print(prng)
    
    path = pr.prng2path(prng)
    ut.plotDyckPath(path)
    '''
    y = 0
    S = [(x, y)]
    for i in range(2 * n):
        if path[i] == 1:
            y += 1
        else:
            x += 1
        S.append((x,y))
    print(S)
    '''    
    ringlets, x, depth, prng1 = simplify(prng)
    print(ringlets, x, depth, prng1)
    if prng1 != None:
        prng1.draw()
    
    
    nf = normalForm(prng)
    print(nf)
    
    
    
    prng = nf2pairing(nf, n)
    
    prng.draw()
    

    
    n = 3 #size of the pairing
    q = 2 #parameter of the algebra
    x = 3 #place to act
    m = 1 
    #vacuum element:
    prng = pr.standardPairing(n) 
    #another element created by acting with e_x on the vacuum element
    prng1 = act(x,prng)
    prng1.draw(asPath = True)
    
    
    '''
    el1 = tl.ElementTL({prng:1}, q = q) #basis element as a part of the TL algebra
    #now we create another element by acting by a different version of e_x on 
    #the vacuum vector. 
    el2 = act2(x, m, q, el1)
    print("Vacuum element: ", el1)
    print(el2)
    #I think the idea is that el2 is orthogonal to el1 and we can also 
    #calculate the norm of el2
    print(el2 | el1) #Problem this is not zero. Have to do it by hands
    print(el2 | el2)
    
    
    #yet another element
    el3 = act2(x - 2, m, q, el2)
    print(el3)

    '''
    plt.show()


if __name__ == '__main__':
    main()