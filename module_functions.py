
from tangle_ import Simple_Strand, StrandAlgebra,TANGLE,Strands, Idempotent, StrandDiagram
from utility import mod_helper, mod_between
import numpy as np


def m2_raw(gen, alg_gen):
    ''' m2 map that sends CT-(T) * I(-dRT) * A-(dRT) to CT-(T).
    gen is a generator in CT-(T)
    alg_gen is a generator of  A-(dRT)
    
    Returns a list of elements of the form ((s1, s2), d_plus_raw_term), where
    s1 < s2 are pairs of strands that d_plus is applied, and
        diff_term is a generator in d_plus() obtained by uncrossing these two
        strands. Together they specify all terms in gen.d_plus(). ''' 
    
#    if is_B: # apply to B_j
#        pass
#    else:# apply to A_j left
#        pass       

def del_l_raw(gen, is_B):
    ''' del_L map that sends CT-(T_i) to  A-(dRT) * I(-dRT) * CT-(T_i)
    gen is an element of CT-(T_i)
    gen is a generator in CT-(T_i)
    if is_B = True, apply it to B_j
    if is_B = False apply it to A_j'''
    
    if is_B: # apply to B_j
        pass
    else:# apply to A_j apply to A_j left
        pass
 
def d_plus_raw_B(gen):
    ''' d_+ map that smooths a black-black crossing of a generator `gen`
    of CT-(T_i)) contained in right halfs ( i- 1/2, i)
    Returns a list of elements of the form ((s1, s2), d_plus_raw_term), where
    s1 < s2 are pairs of strands that d_plus is applied, and
    diff_term is a generator in d_plus() obtained by uncrossing these two
    strands. Together they specify all terms in gen.d_plus(). ''' 
    
    # applying it to line Bj
    lst = []
    l_strands = gen.strands.left_converted 
    r_strands = gen.strands.right_converted
    types = mod_helper(l_strands, r_strands)
    t_r = gen.tangle.r_pairs_wc
    r_crossings = types[4] # type 4 : right crosisngs
    for s1, s2 in r_crossings: 
        is_crossed = False
        # check double black - black crossing
        for strands in r_strands: 
            if mod_between(strands, (s1[0],s2[0]),(s1[1],s2[1]), False) == 1:
                is_crossed = True
        # tangle double cross a strand
        for tangle in t_r:
            if mod_between(tangle, (s1[0],s2[0]),(s1[1],s2[1]), False) ==1:
                is_crossed = True
        if not is_crossed:
            sd_1 = gen.strands.get_strand_index(s1, False)
            sd_2 = gen.strands.get_strand_index(s2, False)
            new_strand = ((sd_1[0],sd_2[1]),(sd_2[0],sd_1[1]))
            lst.append((sd_1, sd_2), gen.replace((sd_1, sd_2), new_strand, False))
    return lst

def d_minus_raw(gen, is_B):
    '''d_- map that introduces a black-black crossing to a generator 'gen`
    of CT-(T_i) contained in left halfs, (i, i+1/2).
    if is_B == True, apply it to B_j
    if is_B == False apply it to A_j 
    
    Returns a list of elements of the form ((s1, s2), d_minus_raw_term), where
    s1 < s2 are pairs of strands that d_minus is applied, and
        diff_term is a generator in d_minus() obtained by crossing these two
        strands. Together they specify all terms in gen.d_minus(). ''' 
    # applying it to line Bj
    lst = []
    l_strands = gen.strands.left_converted 
    r_strands = gen.strands.right_converted
    types = mod_helper(l_strands, r_strands)
    t_l = gen.tangle.l_pairs_wc
    horizontals = types[1] # type 1 : left horizontals
    for s1, s2 in horizontals:
        is_crossed = False
        # check double black - black crossing 
        for strands in r_strands: 
            if mod_between(strands, (s1[0],s2[0]),(s1[1],s2[1]),True)==0:
                is_crossed = True
        # tangle double cross a strand
        for tangle in t_l:
            if mod_between(tangle, (s1[0],s2[0]),(s1[1],s2[1]),True) == 0:
                is_crossed = True
        if not is_crossed:
            sd_1 = gen.strands.get_strand_index(s1, True)
            sd_2 = gen.strands.get_strand_index(s2, True)
            new_strand = ((sd_1[0],sd_2[1]),(sd_2[0],sd_1[1]))
            lst.append((sd_1, sd_2), gen.replace((sd_1, sd_2), new_strand, True))
    return lst

def d_m_raw(is_B, gen, gen2 = None):
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
        lst = []
        l_strands = gen.strands.left_converted 
        r_strands = gen.strands.right_converted
        types = mod_helper(l_strands, r_strands)
        t_l = gen.tangle.l_pairs_wc 
        t_r = gen.tangle.r_pairs_wc 
        
  
        # right no cross strands
        r_horizontals = types[3]
        for s1,s2 in r_horizontals:
            is_crossed = False
            for tangle in t_r: # right half tangles
                if abs(mod_between(tangle, (s1[0],s2[0]),(s1[1],s2[1]),False)) == 1:
                    is_crossed = True
            for tangle in t_l: #left half tangles
                x = (tuple(np.subtract(s1[1],(1,0))), tuple(np.subtract(s2[1],(1,0))))
                if mod_between(tangle, x,(s1[0],s2[0]), True) != -2:
                    is_crossed = True
            if not is_crossed:
                lst.append(mod_helper_2(gen, s1, s2, is_crossed))
        # left cross strands
        l_cross = types[2]
        for s1,s2 in l_cross:
            is_crossed = False
            for tangle in t_l: #left half tangles
                if abs(mod_between(tangle, (s1[0],s2[0]),(s1[1],s2[1]),True)) == 1:
                    is_crossed = True
            for tangle in t_r:
                x = (tuple(np.add(s1[0],(1,0))), tuple(np.add(s2[0],(1,0))))
                if mod_between(tangle,(s1[1],s2[1]),x, False) != -2:
                    is_crossed = True  
            if not is_crossed:
                lst.append(mod_helper_2(gen, s1, s2, is_crossed))
        # left above right strands
        l_above_r = types[6]
        for s1, s2 in l_above_r:
            is_crossed = False
            left_pair = (tuple(np.subtract(s2[0],(0.5,0))), s1[0])
            mid_pair = (s2[0],s1[1])
            right_pair = (tuple(np.add(s1[1],(0.5,0))),s2[1])
            for tangle in t_l: # left half triangles
                if mod_between(tangle, left_pair, mid_pair, True) < 1:
                    is_crossed = True
            for tangle in t_r: # right_half tangles
                if mod_between(tangle, mid_pair, right_pair, False) == -1:
                    is_crossed = True
            if not is_crossed:
                lst.append(mod_helper_2(gen, s1, s2, is_crossed))
            
        # left below  right strands
        l_below_r = types[5]
        
        for s1,s2 in l_below_r: #s1 on the left, s2 on the right
            is_crossed = False
            left_pair = (tuple(np.subtract(s2[0],(0.5,0))), s1[0])
            mid_pair = (s2[0],s1[1])
            right_pair = (tuple(np.add(s1[1],(0.5,0))),s2[1])
            for tangle in t_l: # left half tangles
                if mod_between(tangle, left_pair, mid_pair, True) > -1 :
                    is_crossed = True
            for tangle in t_r:
                if mod_between(tangle, mid_pair, right_pair, False) == 0:
                    is_crossed = True
            if not is_crossed:
                lst.append(mod_helper_2(gen, s1, s2, is_crossed))
    else: # apply to Aj
            pass
    
def mod_helper_2(gen,s1, s2, is_crossed):
    '''returns the new generator if is_crossed is false '''
    if not is_crossed:
        if isinstance(s1[0][0], int):
            sd_1 = gen.strands.get_strand_index(s1, True)
            sd1_left = True
        else:
            sd_1 = gen.strands.get_strand_index(s1, False)
            sd1_left = False  
        if isinstance(s2[0][0], int):
            sd_2 = gen.strands.get_strand_index(s2, True)
            sd2_left = True
        else:
            sd_2 = gen.strands.get_strand_index(s2, False)
            sd2_left = False    

        if sd1_left and sd2_left:
            new_strand = ((sd_1[0],sd_2[1]),(sd_2[0],sd_1[1]))
            return (sd_1, sd_2), gen.replace((sd_1, sd_2), new_strand, True)
        elif not sd1_left and not sd2_left:
            new_strand = ((sd_1[0],sd_2[1]),(sd_2[0],sd_1[1]))
            return ((sd_1, sd_2), gen.replace((sd_1, sd_2), new_strand, False))
        elif sd1_left and not sd2_left:
            new_strand = ((sd_1[0],sd_2[0]),(sd_1[1],sd_2[1]))
            return ((sd_1, sd_2), gen.replace_2((sd_1, sd_2), new_strand))
        else:
            new_strand = ((sd_1[0],sd_2[0]),(sd_1[1],sd_2[1]))
            return ((sd_1, sd_2, gen.replace_2((sd_1, sd_2), new_strand)))
    
    else:
        return None

def helper(tang_left, tang_right, pair_1, pair_2, pair_3, is_left, option):
    ''' Helper methods for diff methods. Assumes compatibility. Given a generator x, taking the is_left side, 
    exchanges pairs = (a,b), it seems whether the 
    whether it violates `option`. Refer to options.jpg
    for options.  
    * tang_left is dictionary object of pairs 
    * tang_right is dictionary object of pairs 
    * Pair_1 is the coordinate of two pairs of strand on the left
    * Pair_2 is the coordinate of two pairs of strand in the middle
    * Pair_3 is the coordinate of two pairs of strand in the middle.'''
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
         