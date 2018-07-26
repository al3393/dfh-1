
from tangle_ import Simple_Strand, StrandAlgebra,TANGLE,Strands, Idempotent, StrandDiagram
from utility import mod_helper


def m2_raw(gen, alg_gen):
    ''' m2 map that sends CT-(T) * I(-dRT) * A-(dRT) to CT-(T).
    gen is a generator in CT-(T)
    alg_gen is a generator of  A-(dRT)
    
    Returns a list of elements of the form ((s1, s2), d_plus_raw_term), where
    s1 < s2 are pairs of strands that d_plus is applied, and
        diff_term is a generator in d_plus() obtained by uncrossing these two
        strands. Together they specify all terms in gen.d_plus(). ''' 
    
    if is_B: # apply to B_j
    

    else:# apply to A_j left
    

def del_l_raw(gen, is_B):
    ''' del_L map that sends CT-(T_i) to  A-(dRT) * I(-dRT) * CT-(T_i)
    gen is an element of CT-(T_i)
    gen is a generator in CT-(T_i)
    if is_B = True, apply it to B_j
    if is_B = False apply it to A_j'''
    
    if is_B: # apply to B_j
        
    else:# apply to A_j apply to A_j left
 
def d_plus_raw(gen, is_B ):
    ''' d_+ map that smooths a black-black crossing of a generator `gen`
    of CT-(T_i)) contained in right halfs ( i- 1/2, i)
    if is_B = True, apply it to B_j
    if is_B = False apply it to A_j
    
    Returns a list of elements of the form ((s1, s2), d_plus_raw_term), where
    s1 < s2 are pairs of strands that d_plus is applied, and
    diff_term is a generator in d_plus() obtained by uncrossing these two
    strands. Together they specify all terms in gen.d_plus(). ''' 
    
    if is_B: # apply to B_j
            
    else:# apply to A_j apply to A_j left


def d_minus_raw(gen, is_B):
    '''d_- map that introduces a black-black crossing to a generator 'gen`
    of CT-(T_i) contained in left halfs, (i, i+1/2).
    if is_B == True, apply it to B_j
    if is_B == False apply it to A_j 
    
    Returns a list of elements of the form ((s1, s2), d_minus_raw_term), where
    s1 < s2 are pairs of strands that d_minus is applied, and
        diff_term is a generator in d_minus() obtained by crossing these two
        strands. Together they specify all terms in gen.d_minus(). ''' 
        
    if is_B: # apply to B_j
        
    else:# apply to A_j apply to A_j left


def d_m_raw(gen, is_B):
    ''' dm map that picks two pair of points, given A_j or
    B_j. Exchanges two ends of the corresponding pair of black strands of generator
    `gen` in CT(Ti)
    if is_B = True, apply it to B_j
    if is_B = False apply it to A_j
    
        Returns a list of elements of the form ((s1, s2), d_m_raw_term), where
    s1 < s2 are pairs of strands that d_m is applied, and
        diff_term is a generator in d_plus() obtained by uncrossing or  crossing
        these two strands. Together they specify all terms in d_m(). '''
    if is_B:
        gen
         
    else:

def helper(tang_left, tang_right, pair_1, pair_2, pair_3, is_left, option):
    ''' Helper methods for diff methods. Assumes compatibility. Given a generator x, taking the is_left side, 
    exchanges pairs = (a,b), it seems whether the 
    whether it violates `option`. Refer to options.jpg
    for options.
    
    tang_left is dictionary object of pairs 
    tang_right is dictionary object of pairs 
    Pair_1 is the coordinate of two pairs of strand on the left
    Pair_2 is the coordinate of two pairs of strand in the middle
    Pair_3 is the coordinate of two pairs of strand in the middle.'''
    mod = False
    if is_left: # only check mod relations 1,2,3
        for k,v in tang_left.items():
            if option ==1:
                if mod_helper((k,v), pair_1, pair_2, is_left) == 1: 
                    mod = True
            elif option == 2:
                if mod_helper((k,v), pair_1, pair_2, is_left) == 0:
                    mod = True
            elif option == 3:
                if mod_helper((k,v), pair_1, pair_2, is_left) == -1: 
                    mod = True
            else:
                raise AssertionError("Something is wrong -- options arent either 1, 2 or 3 ")      
    else: # only check mod relations 4,5,6
        for k,v in tang_right.items():
            if option == 4:
                if mod_helper((k,v), pair_2, pair_3, is_left) == 1:
                    mod = True
            elif option ==5:
                if mod_helper((k,v), pair_2, pair_3, is_left) == 0: 
                    mod = True
            elif option == 6:
                if mod_helper((k,v), pair_2, pair_3, is_left) == -1: 
                    mod = True    
            else:
                raise AssertionError("Something is wrong about `is_left`-- options arent either 4, 5, 6" )
    return mod

p1 = ((1,0.5),(1,4.5))
p2 = ((1.5,1.5), (1.5, 3.5))
p3 = ((2,1.5),(2,4.5))
t_left = {(1,7):(1.5,3), (1,2):(1.5,3)}
t_right = {(1.5,3):(2,5)}

print(helper(t_left,t_right, p1, p2, p3, False, 6 ))
         