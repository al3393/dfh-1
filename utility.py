# Adapted from Bzhan Code are as follows: 
#NamedObject, SummableDict, fracToInt, memorize, memorizeHash, safeMultiply, F2

from fractions import gcd
from numbers import Number
import itertools as it
from numpy import *
import numpy as np

class Ring:
    def convert(self, data):
        """Try to convert data to an element of this ring."""
        raise NotImplementedError("convert function not specified for ring.")

class RingElement(Number):
    pass

class ModNRing(Ring):
    """The ring Z/nZ."""
    def __init__(self, n):
        self.n = n
        self.zero = self.convert(0)
        self.one = self.convert(1)

    def add(self, elt1, elt2):
        elt1, elt2 = self.convert(elt1), self.convert(elt2)
        if elt1 is NotImplemented or elt2 is NotImplemented:
            return NotImplemented
        return ModNElement(self, (elt1.val+elt2.val)%self.n)

    def multiply(self, elt1, elt2):
        elt1, elt2 = self.convert(elt1), self.convert(elt2)
        if elt1 is NotImplemented or elt2 is NotImplemented:
            return NotImplemented
        return ModNElement(self, (elt1.val*elt2.val)%self.n)

    def __eq__(self, other):
        return self.n == other.n

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.n, "ModNRing"))

    def convert(self, data):
        """Try to convert data to an element of this ring."""
        if isinstance(data, ModNElement) and data.parent == self:
            return data
        if isinstance(data, int):
            return ModNElement(self, data % self.n)
        return NotImplemented

class ModNElement(RingElement):
    """An element in a ring Z/nZ."""
    def __init__(self, parent, val):
        self.parent = parent
        self.val = val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)

    def __add__(self, other):
        return self.parent.add(self, other)

    def __radd__(self, other):
        return self.parent.add(self, other)

    def __mul__(self, other):
        return self.parent.multiply(self, other)

    def __rmul__(self, other):
        return self.parent.multiply(self, other)

    def __eq__(self, other):
        """Can compare to integer 0 or 1."""
        if isinstance(other, int) and (other == 0 or other == 1):
            return self.val == other
        else:
            return self.val == other.val

    def invertible(self):
        """Returns whether this element is invertible in the ring."""
        return gcd(self.val, self.parent.n) == 1

    def inverse(self):
        """Returns the inverse of this element. Must be invertible"""
        # Currently only implemented for n = 2
        assert self.parent.n == 2
        return self

class Integer(Ring):
    """The ring Z."""
    def convert(self, data):
        """Try to convert data to an element of this ring."""
        assert isinstance(data, int)
        return data

class IntegerElement(RingElement, int):
    """An element in a ring Z."""
    def __new__(cls, parent, val):
        return int.__new__(cls, val)

    def __init__(self, parent, val):
        self.parent = parent


F2 = ModNRing(2)
ZZ = Integer()

# Constants for positive and negative orientation
POS, NEG = 1, -1

class NamedObject:
    """Provides functionality for an object to be described by name. If this is
    listed as a parent class, an object will use name in equality comparisons,
    hash functions, and string outputs.
    """
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


#an analogous version Free Modules by extending dictionary data structure
class SummableDict(dict):
    ''' An extension of Dictionary class that supports sum and multiplication:
        Works like free module with generators as keys, and coefficients as values. 
        Zeros are automatically thrown away'''
        
    def __add__(self, other):
        ''' does not modify the invoking object '''
        return _dictAddTo(type(self)(), [self, other])
    
    def __iadd__(self, other):
        '''typical add operation for dictionaries: add other onto self
              modifies the invoking object.'''
        return _dictAddTo(self, other)
    
    def __sub__(self, other):
        
        # ORIGINAL : return _dictAddTo(type(self)(), [self, -1*other])
        return _dictAddTo(type(self)(), [self, _dictMult(other, -1)])
    
    def __isub__(self, other):
        '''typical subtract operation for dictionaries: subtract other from self'''
        #ORIGINAL return _dictAddTo(self, -1*other)
        return _dictAddTo(self, _dictMult(other, -1))
    
    def accumulate(self, lst):
        """Similar to +=, except returns the sum."""
        return _dictAddTo(self, lst)
       
    def __mul__(self, other):
        '''multiply by scalar'''
        return _dictMult(self, other)
    
    def __rmul__(self, other): #useless?
        # dk what the difference is against _mult # cb
        return _dictMult(self, other)
    
    def __eq__(self, other):
        ''' Comparison to 0 is a test for empty dictionary.'''
        if isinstance(other, int) and other == 0:
            return len(self) == 0
        else:
            return dict.__eq__(self, other)
    
    def __ne__(self, other): 
        '''returns whether self is equal to other'''
        return not (self == other)
    
    def copy(self): #useless?
        '''Copy function that preserves type.'''
        return type(self)(self)
        
    def translateKey(self, key_map):
        '''Translate keys of self using key_map. 
        keys in self must appear in key_map and key named will be changed to the 
        corresponding values (i.e the new key names) in key_map dictionary'''
        
        return type(self)([(key_map[k], v) for k, v in self.items()])
    
    def getElt(self):
        """Returns an arbitrary key from this dictionary. Must be non-empty."""
        #return iter(self).next() # in python 2
        return iter(self).__next__() # in python 3 

#dictionary helper methods:
def tolist(obj):
    """Force obj into a list."""
    if isinstance(obj, list):
        return obj
    else:
        return [obj]    
#adding dictionaries
def _dictAddTo(dict1, dict2):
    """Add dict2 onto dict1 in place. If dict2 is a list of dictionaries,
    add each element of
    dict2 on dict1 in place.
    """
    dict2 = [curdict.copy() for curdict in tolist(dict2) if curdict != 0] # removes all empty dictionary
    if dict1 == 0:
        if len(dict2) == 0:
            return dict1
        else:
            dict1 = dict2[0]
            dict2 = dict2[1:]
    for curdict in dict2:
        assert type(dict1) == type(curdict), "Incompatible types: %s, %s" % \
            (str(type(dict1)), str(type(curdict)))
        for k, v in curdict.items():
            #if dict1.has_key(k): 
                # has key is removed in python 3
            if k in dict1:
                dict1[k] += v
                if dict1[k] == 0:
                    del dict1[k]
            else:
                dict1[k] = v
    return dict1
    
#multiplying dictionaries
def _dictMult(dict1, scalar):
    '''Return a new dictionary with same type as self, the same keyes, and each value mlutiplied by scalar'''   
    if not isinstance(scalar, Number):
        return NotImplemented
    
    result = type(dict1)((k, scalar * v) for k, v in dict1.items() if
                             scalar * v != 0)
    return result

def safeMultiply(a, b):
    '''multiply two sides using __mul__ and __rmul__. 
    Return NotImplemented if both fails.'''
    try:
        prod = a.__mul__(b)
    except TypeError:
        prod = NotImplemented
        
    if prod is NotImplemented:
        try:
            prod = b.__rmul__(a)
        except TypeError:
            prod = NotImplemented
    return prod

# ------- practice ------- dict codes
def __add__(self, other):
    '''typical add operation for dictionaries: add other onto self'''
    print("THIS IS WHAT IT MEANS")
    a = type(self)()
    print(a)
    print(type(a))
    return _dictAddTo(type(self)(), [self, other])

def __iadd__(self, other):
    '''like __add__ but other can be a list of dictionaries.'''
    return _dictAddTo(self, other)

def __sub__(self, other):
    '''typical subtract operation for dictionaries: subtract other from self'''
    return _dictAddTo(type(self)(), [self, _dictMult(other, -1)])#diff

def __isub__(self, other):
    '''like __sub__ but other can be a list of dictionaries.'''
    return _dictAddTo(self, _dictMult(other, -1)) #? diff

def accumulate(self, lst):
    """Similar to +=, except returns the sum."""
    return _dictAddTo(self, lst)
   
def __mul__(self, other):
    '''multiply by scalar''' #?
    return _dictMult(self, other)

def __rmul__(self, other): #useless?
    # dk what the difference is against _mult #?
    return _dictMult(self, other)

def __ne__(self, other):
    '''returns whether self is equal to other'''
    return not (self == other)

def copy(self): #useless?
    '''Copy function that preserves type.'''
    return type(self)(self)
    
def translateKey(self, key_map):
    '''Translate keys of self using key_map. 
    keys in self must appear in key_map and key named will be changed to the 
    corresponding values (i.e the new key names) in key_map dictionary'''
    return type(self)([(key_map[k], v) for k, v in self.items()])

def getElt(self):
    """Returns an arbitrary key from this dictionary. Must be non-empty."""
    #return iter(self).next() # in python 2
    return iter(self).__next__() # in python 3 

def complement(tup1, tup2):
    ''' Given ordered tup1 = [n] and returns the tup1 \ tup2,
    given that tup2 is contained in tup1''' 
    return tuple(set(tup1).difference(set(tup2)))


def orientation(pair, left_half = True):
    ''' Given a pair of coordinates ((x_1,y_1), (x_2,y_2)), returns 
    list {1} if from left to right 
    list {-1} if  right to left
    (1, -1) or (1,1) depending on cup or cap ''' 
    # left_half is `True` if is left half of the tangle i to i+1/2
    # left_half is `False` if it is right half of the tangle i+1/2 to i+1
    x_1,y_1 = pair[0]
    x_2,y_2 = pair[1]   
    if x_1 < x_2: # going left to right
        return (1)
    elif x_1 > x_2:
        return (-1)
    else: # cups or caps 
        if left_half == True:
            if y_1 > y_2:
                return (-1, 1)
            else:
                return (1, -1)
        else:#right half
            if y_1 > y_2:
                return (1, -1)
            else:
                return (-1, 1)
            
def orientation_i(pair, left_half = True):
     ''' Improved version of `orientation` method above, but actually returns 
     a dictionary object {(x1,y1): +1, (x2, y2): +- 1,'''
     x_1,y_1 = pair[0]
     x_2,y_2 = pair[1]
     pair_0 = (x_1,y_1)
     pair_1 = (x_2,y_2)
    # IF LEFT HALF    
     if left_half == True:
        if x_1 < x_2: # going left to right
             return {pair_0 :1} # cb
        elif x_1 > x_2:
            return {pair_1 :-1}
        else: # caps
            if y_1 > y_2:
                return {pair_1: -1, pair_0: 1}
            else:
                return {pair_0: 1, pair_1: -1} 
    # IF RIGHT HALF
     else:
        assert left_half == False # assert error if not right half
        if x_1 < x_2: # going left to right
             return {pair_1 :1} # cb
        elif x_1 > x_2:
            return {pair_0 :-1}
        else : #caps
            if y_1 > y_2:
                 return {pair_1: 1, pair_0: -1}
            else:
                 return {pair_0: -1, pair_1: 1}    


def doescross_simple(left,right):
    '''given a pair of points left = (a_1, b_1),right = (a_2, b_2)
    it does tells us whether they intersect''' 
    
    a = ((1, left[0]),(2,left[1]))
    b = ((1, right[0]),(2, right[1]))  
    def line(p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C    
    def intersection(L1, L2):
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return x,y
        else:
            return False
        
    L1 = line(a[0],a[1])
    L2 = line(b[0],b[1])
    
    if left != right:
        R = intersection(L1, L2)
    else:
        R = None
  
    if R == False:
        R = None
    elif R[0] < 1 or R[0] > 2: 
        R = None
    elif not(in_between(left[0], left[1],R[1]) and in_between(right[0], right[1], R[1])): # Check Y coordinates
        R = None
    else:
        pass
    
    if R != None:
        return True
    else:
        return False

def doescross_simple_rc(left,right):
    '''given a pair of points left = (a_1, b_1),right = (a_2, b_2)
    it does tells us whether they intersect and RETURNS coordinates''' 
    
    a = ((1, left[0]),(2,left[1]))
    b = ((1, right[0]),(2, right[1]))
    
    def line(p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C
    
    def intersection(L1, L2):
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return x,y
        else:
            return False
        
    L1 = line(a[0],a[1])
    L2 = line(b[0],b[1])
    
    if left != right:
        R = intersection(L1, L2)
    else:
        R = None
 
    if R == False:
        R = None
    elif R[0] < 1 or R[0] > 2: 
        R = None
    elif not(in_between(left[0], left[1],R[1]) and in_between(right[0], right[1], R[1])): # Check Y coordinates
        R = None
    else:
        pass
    
    return R


def in_between(a,b, x):
    ''' returns True if x is in between a and b. 
        a > b or b < a may happen. Error returned if a = b'''
        
    #if a==b and a != x: CB AND FIX IT
#        raise ValueError("a = b. Something is wrong.")
    if a == b and a == x:
        return True
    elif a>b:
        return b < x and x < a
    else:
        return a < x and x < b
    
def in_between_list(arr, x):
    ''' Given an array `arr`, returns true if there exists two values a1, a2 
    in `arr` such that x is in between arr
    if arr size is one, returns type error'''
    if not isinstance(arr,list):
        return TypeError("`arr` is not an array. Wrong type of input")
    elif len(arr) == 1:
        return TypeError("`arr` is of size 1. cannot use this method.")
    else:
        arr.sort()
        maximum = max(arr)
        minimum = min(arr)
        if x > maximum or x < minimum:
            return False
        else:
            return True
        
def reorganize_sign(cross):
    '''returns [a1, a2, b1, b2]
    Reorient points such that a1 is top left, then b1, a2, b2 in counter-
    clockwise orientation'''
    
    # ex if cross = ((4,2),(1,3))
    s1 = cross[0][0] #4
    s2 = cross[1][0] #1
    
    if s1 > s2:
        a1 = cross[0][0]
        a2 = cross[0][1]
        b1 = cross[1][0]
        b2 = cross[1][1]
    
    else: # s1 < s2
        a1 = cross[1][0]
        a2 = cross[1][1]
        b1 = cross[0][0]
        b2 = cross[0][1]
    
    return [a1,a2,b1,b2]

#dic = {(1,3):((1.5,1.5),(2,3.5)),
#        (4,2): ((1.5, 4.5),(2,2.5))}
#cross = ((4,2),(1,3))

def reorganize_sign_2(cross, dic):
    '''reorganizes the point like `reorganize_sign_2()` but with coordinates
    taken from `dic` object'''

    s1 = dic[cross[0]][0][1] # 4.5
    s2 = dic[cross[1]][0][1] # 1.5
    
    if s1> s2:
        a1 = dic[cross[0]][0] #(1.5, 4.5)
        b1 = dic[cross[1]][0] #((1.5,1.5)
        a2 = dic[cross[0]][1] #(2,2.5))
        b2 = dic[cross[1]][1] #3(2,3.5))
       
    else:
        a1 = dic[cross[1]][0] #(1.5, 4.5)
        b1 = dic[cross[0]][0] #((1.5,1.5)
        a2 = dic[cross[1]][1] #(2,2.5))
        b2 = dic[cross[0]][1] #3(2,3.5))
    
    return [a1,a2,b1,b2]

def doescross(a,b):
    '''given a pair of lines = ((x_1, y_1), (x_2, y_2)), ((x_3, y_3), (x_4, y_4))
    goes the intersection point, if one exists between, if not return None''' 
    
    def line(p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C
    
    def intersection(L1, L2):
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return x,y
        else:
            return False
        
    L1 = line(a[0],a[1])
    L2 = line(b[0],b[1])       
    if a != b:
        R = intersection(L1, L2)
    else:   R = None
    x_1, y_1 = a[0]
    x_2, y_2 = a[1]
    x_3, y_3 = b[0]
    x_4, y_4 = b[1]
    if R == False:
        R = None
    elif not(in_between(x_1, x_2, R[0]) and in_between(x_3, x_4, R[0]) and \
           in_between(y_1, y_2, R[1]) and in_between(y_3, y_4, R[1])):
        R = None
    else:
        pass

    return R

def doescross_bool(a,b):
    '''given a pair of lines = ((x_1, y_1), (x_2, y_2)), ((x_3, y_3), (x_4, y_4))
    goes the intersection point, if one exists between, if not return None''' 
    
    def line(p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        return A, B, -C
    
    def intersection(L1, L2):
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return x,y
        else:
            return False
        
    L1 = line(a[0],a[1])
    L2 = line(b[0],b[1])
    
        
    if a != b:
        R = intersection(L1, L2)
    else:   R = None

    x_1, y_1 = a[0]
    x_2, y_2 = a[1]
    x_3, y_3 = b[0]
    x_4, y_4 = b[1]

    if R == False:
        R = None
    elif not(in_between(x_1, x_2, R[0]) and in_between(x_3, x_4, R[0]) and \
            in_between(y_1, y_2, R[1]) and in_between(y_3, y_4, R[1])):
        R = None
    else:
        pass

    if R != None:
        return True
    else:
        return False

def combinations(n, m):
    ''' retyrbs an array of all possible combinations of n and m
    for example, if n = 1 , m = 2, returns, if WLOG n < m
    [ (0,0),(0,1),.....(n, m-1 ), (n,m)]'''
    ran1 = [k for k in range(0, n+1)] # = [0,1,....n]
    ran2 = [k for k in range(0, m+1)] # = [0,1,....m]
    combo = []
    for i in ran1:
        for j in ran2:
            combo.append((i,j))
    return combo
    
def generate_subset(n, num):
    '''given range [n] = [0,1,2,...n], returns the list of subsets
    of size num of [n]'''
    return list(it.combinations(range(n+1), num))

def generate_bijections(n):
    ''' given n, gives a list of possible 'subsets'of n, including 0 and n
    , EXCLUDING empty set. Used for generating idempotents'''
    
    lst = []
    for size in range(1,n+2):
        lst += generate_subset(n, size) 
    return lst

def generate_bijections_m(n,m): #WRONG CB
    ''' Given n and m, it gives bijections from [n] and [m] with [n] and [m] 
    that may have different size:
        [n] = [0, 1, 2, 3....n]
        [m] = [0, 1, 2, 3,...m]
        '''
    app = []
    if n > m:
        bij = generate_bijections_same(m,m)
        diff = n - m 
        for b in bij:
            arr = []
            for pair in b:
                arr.append((pair[0] + diff, pair[1]))
            app.append(arr)
    
    if n < m:
        bij = generate_bijections_same(n,n)
        diff = m - n
        for b in bij:
            arr = []
            for pair in b:
                arr.append((pair[0], pair[1] + diff))
            app.append(arr)
    set1 = set(bij)        
    return list(set1.union(set(app)))

def generate_bijections_3(n,m,k): # checked
    ''' Used for generating `Strand Diagrams`. 
    n = number of left alpha arcs
    m = number of beta arcs
    k = number of right alpha ars.
    WLOG assume m < n + k. 
    i.e possible injections between [n] , [m] , and [k] such that every element from
    Beta arcs are mapped. [n] = {0,1,2,...n}
    
    return type like 
[[[(0, 0), (1, 1)], []], [[(1, 0), (0, 1)], []], [[(0, 0)], [(1, 0)]], [[(0, 1)], [(0, 0)]], [[(0, 0)], [(1, 1)]], [[(0, 1)], [(0, 1)]], [[(1, 0)], [(1, 0)]], [[(1, 1)], [(0, 0)]], [[(1, 0)], [(1, 1)]], [[(1, 1)], [(0, 1)]], [[], [(0, 0), (1, 1)]], [[], [(0, 1), (1, 0)]]]'''
    ran1 = [k for k in range(0, n+1)]
    ran2 = [k for k in range(0, m+1)]
    ran3 = [j for j in range(0, k+1)]  
    ran_total = [k for k in range(0,n+k+2)]       # total arcs possible left or right 
    combinations = generate_subset(n+k+1, m + 1)
    arr = []
#    print("ran total: {0}".format(ran_total))
    for combo in combinations:
        ran =  [] # range
        for c in combo:
            ran.append(ran_total[c]) # combinations of indxes
        l = []
#        print("ran2 here : {0}".format(ran2))
#        print("ran here : {0}".format(ran))
        for p in it.permutations(ran):
            l.append(list(zip(ran2,p)))
#        print(l)
        l_new = []
        for bijections in l:
#            print("current bijection: {0}".format(bijections))
            bijections_left = []
            bijections_right = []
            for elt in bijections:
                if elt[1] > n:
                    bijections_right.append((elt[0],elt[1] - (n+1)))
                else:
                    bijections_left.append((elt[1],elt[0]))
#            print("bijection_left:{0}".format(bijections_left))
#            print("bijection_right:{0}".format(bijections_right))
#            print("+++++++++")
            l_new.append([bijections_left, bijections_right])
        arr += l_new
    return arr

def generate_bijections_same(n): # checked
    ''' Given n and m, it gives bijections from [n] and [m] with [n] and [m] size the same'''
    m = n
    ran1 = [k for k in range(0, n+1)] # = [0,1,....n]
    ran2 = [k for k in range(0, m+1)] # = [0,1,....m]
    bij = []
    for i in range(1, n+2): # i goes from 1 to n
        for set1 in it.combinations(ran1, i):
            for set2 in it.combinations(ran2, i):
                for p in it.permutations(set2):
                    bij.append(list(zip(set1,p)))
    return bij

def intersections( dict1, dict2, itself = False):
    ''' given dict1, and dict2, returns dictionary `intersection`that contains
     unique intersection points. 
    If itself = True, it means dict1 = dict2, and need to use a diff method
    If itself = False, we assume dict 1 and dict2 are distinct(no shared
    pairs).
    
    For example, if the intersection between (1,1):(1.5,2)(in dict1
                 and (1,2):(1.5,1) in dict2
    is (1.25,1.5) then, `intersection` will contain 
    (((1,1),(1.5,2)),((1,2),(1.5,1))) : (1.25, 1.5)
    
    i.e : The Key is the pair that causes intersection points
          The Value is the intersection points
    ''' 
    intersections = {}
    
    if itself == False:
        for key_1, value_1 in dict1.items():
            pair_1 = (key_1, value_1)
            for key_2, value_2 in dict2.items():
                pair_2 = (key_2, value_2)
                intersect = doescross(pair_1, pair_2)
                if intersect != None:
                    intersections.update({(pair_1, pair_2): intersect})
    else: # dict1 = dict2
        intersections = same_set_intersections(dict1)
    return intersections
                
def same_set_intersections(dict1):
    '''Given pairs by dict1, it gives the list of intersections by pairs in
    dict1 themselves.'''
    
    intersections = {}
    
    n = len(dict1)
    pairs = list(dict1.items())
    combinations = generate_subset(n-1,2) # generate combinations of [0,1,...n-1] with size 2
    
    
    for combo in combinations:
        if combo[0] == combo[1]:
            print("something is wrong, tuple has duplicate values")
        i = combo[0]
        j = combo[1]
        intersect = doescross(pairs[i],pairs[j])
        if intersect != None:
            intersections.update({(pairs[i],pairs[j]): intersect})
    
    return intersections
                
def simple_intersections( dict1, dict2, itself = False): # cb and fix positional arguments
    ''' given dict1, and dict2, returns number of unique intersection points 
    
    ''' 
    return len(intersections(dict1, dict2, itself))

def get_domain(tup):
    '''given a tuple of pairs(injective), it returns list of domains
    For example, if tup = ((1,2), (2,3), (4,2)), 
    then this method returns [1,2,4]'''    
    dom = []
    for pair in tup:
        dom.append(pair[0])
    return tuple(dom)
    
def get_range(tup):
    '''given a tuple of pairs(injective), it returns list of domains
    For example, if tup = ((1,2), (2,3), (4,4)), 
    then this method returns [2,3,4]'''
    
    ran = []
    for pair in tup:
        ran.append(pair[1])
    return tuple(ran)

def get_domain_dict(dic):
    ''' either takes a dictionary object or a list of dictionary objects
    and return the domain.'''
    dom = set()
    if isinstance(dic,list):
        for cur_dic in dic:
            dom.update(set(cur_dic.keys()))
    else:
        dom = set(dic.keys())
    return dom

def get_range_dict(dic):
    ''' either takes a dictionary object or a list of dictionary objects
    and return the range.'''
    
    ran= set()
    if isinstance(dic,list):
        for cur_dic in dic:
            ran.update(set(cur_dic.values()))
    else:
        ran = set(dic.values())
    return ran

def get_start_dict(tup):
    '''given tuple such as tup = (((4, 4.5), (4.5, 5.5)), ((4, 5.5), (4.5, 3.5)))
    returns set = {(4, 4.5),(4, 5.5)}.
    used for method cross_twice'''
    
    start = set()
    for pair in tup:
        start.add(pair[0])
    return start

def get_end_dict(tup):
    '''given tuple such as tup = (((4, 4.5), (4.5, 5.5)), ((4, 5.5), (4.5, 3.5)))
    returns set = {(4, 5.5), (4.5,3.5)}
     used for method cross_twice'''
    end = set()
    for pair in tup:
        end.add(pair[1])
    return end

#a = (((4, 4.5), (4.5, 5.5)), ((4, 5.5), (4.5, 3.5)))
#
#print(get_start_dict(a))
#print(get_end_dict(a))

def dict_shift(dic, shift_left = False):
    '''given a dictionary object `dic` shifts everything every x coord by 0.5'''
    
    new_dic = {}
    if shift_left:
        for k,v in dic.items():
            new_v1 = (k[0] - 0.5, k[1])
            new_v2 = (v[0] - 0.5, v[1])
            new_dic.update({new_v1 : new_v2})
    else:
        for k,v in dic.items():
            new_v1 = (k[0] + 0.5, k[1])
            new_v2 = (v[0] + 0.5, v[1])
            new_dic.update({new_v1 : new_v2})
    
    return new_dic

def dict_shift_double(dic, shift_left = False):
    '''(upgraded version of dict_shift, given a dictionary object `dic` shifts everything every x coord by 0.5
    For example : if, dic = {((4, 4.5), (4.5, 5.5)): ((4, 5.5), (4.5, 4.5))}
    returns {((4.5, 4.5), (5, 5.5)): ((4.5, 5.5), (5, 4.5))}'''
    
    new_dic = {}
    if shift_left:
        for k,v in dic.items():
            a_1 = k[0] #(4, 4.5)
            a_2 = k[1] #(4.5, 5.5)
            b_1 = v[0] #((4, 5.5)
            b_2 = v[1] #(4.5, 4.5)
    
            a_1 = tuple(np.subtract(a_1,(0.5,0)))
            a_2 = tuple(np.subtract(a_2,(0.5,0)))
            b_1 = tuple(np.subtract(b_1,(0.5,0)))
            b_2 = tuple(np.subtract(b_2,(0.5,0)))
            new_dic.update({(a_1,a_2):(b_1, b_2)})
    else:
        for k,v in dic.items():
            a_1 = k[0] #(4, 4.5)
            a_2 = k[1] #(4.5, 5.5)
            b_1 = v[0] #((4, 5.5)
            b_2 = v[1] #(4.5, 4.5)
    
            a_1 = tuple(np.add(a_1,(0.5,0)))
            a_2 = tuple(np.add(a_2,(0.5,0)))
            b_1 = tuple(np.add(b_1,(0.5,0)))
            b_2 = tuple(np.add(b_2,(0.5,0)))
            new_dic.update({(a_1,a_2):(b_1, b_2)})
    
    return new_dic

#dic = {((4, 4.5), (4.5, 5.5)): ((4, 5.5), (4.5, 4.5))}
#print(dict_shift_double(dic,True))
#print(dict_shift_double(dic,False))

def is_bijection(tup):
    ''' given a tuple of pairs, it returns whether the given tuple is 
    is an idempotent
    For example, 
    1. if tup = ((1,2),(2,1)) then returns false
    2. if tup = ((1,1), (2,2)) then returns true
    '''


def mod_helper(left_strand, right_strand):
    ''' Helper method used for dm, d+, d-.
    left_strands, right_strands, are coordinates.
    Given left_strands, and right strands, consists of strand pairs
    such as [((x_1, y_1),(x_2, y_2))....]
    
    Returns an dictionary object `types` whose value is a list of such 
    stair strands
    
    Option #1: left horizontal ( no cross)
    Option #2: left cross ( cross)
    Option #3: right horizontal strands ( no cross)
    Option #4: right cross( cross)
    Option #5: left below right
    Option #6: left above right
    '''    
    n = len(left_strand)
    m = len(right_strand)
    if not isinstance(left_strand, list):
        if isinstance(left_strand, tuple):
            left_strand = list(left_strand) 
        elif isinstance(left_strand, dict):
            left_strand = list(left_strand.items())
        else:
            raise TypeError("Something is wrong -- Not a list, dict, or tuple")
    if not isinstance(right_strand, list):
        if isinstance(right_strand, tuple):
            right_strand = list(right_strand)
        elif isinstance(right_strand, dict):
            right_strand = list(right_strand.items())
        else:
            raise TypeError("Something is wrong -- Not a list, dict, or tuple")
    types = {1:[],2:[],3:[],4:[],5:[],6:[]}
    #left half
    combin = generate_subset(n -1, 2)
    for combo in combin:
        strand_1 = left_strand[combo[0]]
        strand_2 = left_strand[combo[1]]
        if doescross_bool(strand_1, strand_2):
            types[2].append((strand_1, strand_2))
        else:
            types[1].append((strand_1, strand_2)) 
    #right_half
    combin = generate_subset(m-1, 2)
    for combo in combin:
        strand_1 = right_strand[combo[0]]
        strand_2 = right_strand[combo[1]]
        if doescross_bool(strand_1, strand_2):
            types[4].append((strand_1, strand_2))
        else:
            types[3].append((strand_1, strand_2))      
    # Calculate option#5 and #6
    combin = combinations(n-1,m-1) 
    for combo in combin:
        l_strand  = left_strand[combo[0]]
        r_strand = right_strand[combo[1]]
#        print("Comparison between {0} vs {1}:".format(l_strand, r_strand))
        if l_strand[1][1] < r_strand[0][1]: # left above right, Option 5
            types[5].append((l_strand,r_strand))
        else:
            if not l_strand[1][1] > r_strand[0][1]:
                raise TypeError("Something is wrong.")
            types[6].append((l_strand, r_strand))   
    return types

def mod_between(tangle, pair_left, pair_right, is_left):
    '''given a `tangle` coordinate pair ((x_1, y_1),(x_2, y_2)), 
    with any orientation left to right, tells us whether it hits up(1) down(-1) or middle (0). 
    if is_left is true:
        it means pair_right is the middle strand pair
    if is_right is true:
        it means pair_left is the middle strand pair.
    Assumes that the x coordinates line up well. return 2, if it doesn't even hit. '''
    
    t_1 = tangle[0]
    t_2 = tangle[1]
    if t_2[0] < t_1[0]:
        temp= t_1
        t_1 = t_2
        t_2 = temp      
    y_left_1 = pair_left[0][1]
    y_left_2 = pair_left[1][1]
    y_right_1 = pair_right[0][1]
    y_right_2 = pair_right[1][1]   
    if is_left:
        if in_between(y_right_1, y_right_2, t_2[1]):
            if in_between(y_left_1, y_left_2, t_1[1]): # Mod Relation 2
                return 0
            if t_1[1]> y_left_1 and t_1[1]> y_left_2:# Mod Relation 1
                return 1
            else:
                return -1 # Mod Relation 3
        else:
            return -2
    else:
        if in_between(y_left_1, y_left_2, t_1[1]):
            if in_between(y_right_1, y_right_2,t_2[1]): # Mod Relation 5
                return 0
            if t_2[1] > y_right_1 and t_2[1] > y_right_2:  # Mod Relation 4
                return 1
            else:  # Mod Relation 6
                return -1 
        else:
            return -2

def conc_strands(pair1, pair2):
    ''' Given two tuples, that consists of pairs, say from strand 1, stand 2,
    concantenates the strand and returns the new tuple
    for example, if pair1 = ((1,2), (4,2)...)
    pair2 = ((2,3),(2,1)... 
    This method will return tuple object, ((1,3), (4,1)...'''
     
    new = []                                  
    left = list(pair1)
    right = list(pair2)                                      
    for l in left:
        for r in right:
            if l[1] == r[0]:
                new.append((l[0],r[1]))
    return tuple(new)

def replace_sd_1(raw, old,new, is_left):
        ''' helper method for `replace` in Stand Diagram Class. Replaces the corresponding 
        strand on the `is_left` side. '''
        if is_left:
            new_left = list(raw[0])
            for index, o_pair in enumerate(old):
                new_left.remove(o_pair)
                new_left.append(new[index])
            mod = (tuple(new_left), raw[1])
        else:
            new_right = list(raw[1])
            for index, o_pair in enumerate(old):
                new_right.remove(o_pair)
                new_right.append(new[index])
            mod = (raw[0], tuple(new_right))
        return mod

#def replace_sd_2(raw, old, new):
#    ''' helper method for `replace` in Stand Diagram Class.
#    if old and new are tuples, call :
#        replace_sd_2(raw,((0,1),()), ((10,10),()))
#    If old and new are list objects, call:
#     replace_sd_2(raw,[[(0,1)], []], [[(10,10)],[]])'''
#    if len(old) != len(new):
#        raise TypeError("The number of old pairs to be replaced do not equal that of new_strands.")
#    if not((isinstance(old, list) and isinstance(new, list)) or \
#         (isinstance(old, tuple) and isinstance(new, tuple))):
#        raise TypeError(" Type Error: The given input `old` and `new` is not even in tuple or list format." )       
#    old = list(old)
#    new = list(new)
#    
#    print("Raw:{0}".format(raw))
#    print("old:{0}".format(old))
#    print("New:{0}".format(new))
#    print("old[0]:{0}".format(old[0]))
#    print("old[1]:{0}".format(old[1]))
#    print("New[0]:{0}".format(new[0]))
#    print("New[1]:{0}".format(new[1]))
#    new_left = list(raw[0])
#    new_right = list(raw[1])
#    for index, value in enumerate(old[0]):   #change left half
#        print("+++++++++cur val ++:{0}".format(value))
#        new_left.remove(value)
#        new_left.append(new[0][index])
#    for index, value in enumerate(old[1]): #change right half
#        new_right.remove(value)
#        new_right.append(new[1][index])           
#    return (tuple(new_left),tuple(new_right))
    
def replace_sd_2(raw, old, new):
    ''' helper method for `replace` in Stand Diagram Class.
    if old and new are tuples, by default change only one values, call :
        replace_sd_2(raw,((0,1),()), ((10,10),()))
    If old and new are list objects, call:
     replace_sd_2(raw,[[(0,1)], []], [[(10,10)],[]])'''
    if len(old) != len(new):
        raise TypeError("The number of old pairs to be replaced do not equal that of new_strands.")
    # if replace single pair ( -- when converting it to a "list" it takes off two tuple parenthesis, thats why
    if isinstance(old, tuple) and isinstance(new, tuple): 
        #replaces old[0] on the left with new_pair[0], and old[1] on the right with new_pair[1])
        new_left = list(raw[0])
        new_right = list(raw[1])
        if old[0] != ():
            new_left.remove(old[0])
            new_left.append(new[0])
        if old[1] !=():
            new_right.remove(old[1])
            new_right.append(new[1])
        return (tuple(new_left),tuple(new_right)) 
    elif isinstance(old, list) and isinstance(new, list):
        new_left = list(raw[0])
        new_right = list(raw[1])
        for index, value in enumerate(old[0]):   #change left half
            new_left.remove(value)
            new_left.append(new[0][index])
        for index, value in enumerate(old[1]): #change right half
            new_right.remove(value)
            new_right.append(new[1][index])           
        return (tuple(new_left),tuple(new_right))
    else:
        raise TypeError(" Type Error: The given input `old` and `new` is not even in tuple or list format." )       
# Constants for left and right action
ACTION_LEFT, ACTION_RIGHT = 0, 1
def sideStr(side):
    if side == ACTION_LEFT: return "LEFT"
    else: return "RIGHT"
    

#print(orientation_i(((1,3),(2,2)),False))
#print("----1")
#print(orientation_i(((1,2),(2,3)),False))
#print("----2")
#print(orientation_i(((0,3),(1,3)),True))
#print("----3")
#print(orientation_i(((0,2),(1,2)),True))
#print("-----4")
#print(orientation_i(((2,1),(2,0)),False))
#print("----5")
#
#

#print("--------------")
#print(orientation(((0,0),(1,1)),True))
#print("--------------")
#print(orientation(((0,0),(0,1)),True))
#print("----")
#print(orientation(((0,0),(0,1)),False))
#print("----")
#print(orientation_i(((0,0),(0,1)),True))
#print("----")
#print(orientation_i(((0,0),(0,1)),False))

#print("----dictionary test starts.----")
#dict1=    {
#  "x": 0,
#  "y": 1,
#  "z": 2
#}
#
#dict2=    {
#  "x": 1,
#  "y": 1,
#  "z": 2
#}


#test code
#
##print(__add__(dict1, [dict2, dict2]))  #has error
#print(__iadd__(dict1,dict2))
##print(__sub__(dict1,[dict2,dict2]))
#print(__isub__(dict1,dict2))
#print(accumulate(dict1,[dict2, dict2]))
#print(_dictMult(dict2, dict2))
#
#print(iter(dict1).__next__())
##F2 = ModNRing(2)
##ZZ = Integer()

#print({1,3,4} not in {1,2,3,4,5})
#a = (1,2,3,4,5)
#b = (1,3,4)
#print(complement(a,b))

dict1= SummableDict({
  "x": 1,
  "y": 2,
  "z": 1
})

dict2=   SummableDict({
  "x": 1,
  "y": 4,
  "z": 1
})

dict3=   SummableDict({
  "x": 1,
  "y": 4,
  "z": 1
})
#
#raw  = (((0,1),(2,2),(3,3)),((3,3),(1,5),(2,0)))
##d = replace_sd_1(raw,[(3,3),(2,0)], [(0,0),(1,1)], False)
##print(d)
##a = conc_strands(raw[0],raw[1])
#c = replace_sd_2(raw,(((0,1),(2,2)),()), (((10,10),(20,20)),()))
#print(c)
#c = replace_sd_2(raw,[[(0,1)], []], [[(10,10)],[]])
#print("HERE")
#print(c)
#c = replace_sd_2(raw,[[(0,1)], []], [[(10,10)],[]] )
#print(c)

#a = generate_bijections_2(2,3)
#print(a)
##
#print(type([dict2, dict2]))
#
## Note that add and sub is only for two, and i means 'other' is a list 
#print("___add___")
#print(__add__(dict1,dict2))
#print("___iadd___")
#print(__iadd__(dict1,[dict2, dict3]))
#print("___sub___")
#print(__sub__(dict1,dict2))
#print("____isub____")
#print(__isub__(dict1,dict2))
#
##a = generate_subset(5,2)
##print(a)
##
#dict11 = {(1,1):(1.5,2),(1,2):(1.5,1), (1,3):(1.5,3)}
#i = intersections(dict11, dict11, True)
#print(i)
#
#print(doescross_simple((4, 3), (3, 4)))

#lst = generate_bijections(3)
#
#print(lst)
#print(len(lst))

#print(generate_bijections(2))
#print(generate_bijections_2(1,2))
#print(len(generate_bijections_2(1,2)))

#print(len(combinations(2, 3)))
#
#a = generate_bijections_same(1)
#print(a)

a = generate_bijections_3(1,1,1)
for bij in a:
    print(tuple(bij[0]))
#print(a)