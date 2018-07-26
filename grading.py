'Handles grading groups and grading sets.'''

from fractions import Fraction, gcd
from numbers import number
from utility import flatten, grTypeStr, memorize, oppSide, sideStr, tolist
from utility import ACTION_LEFT, ACTION_RIGHT, BIG_GRADING, SMALL_GRADING

class Group:
    '''Represents a general group.'''
    
    def multiply(self,elt, elt2):
        ''' Returns the product of gen1 and gen2.'''
        raise NotImplementedError("Multiply not implemented.")
    
class GroupElement:
    ''' Represents an element of a group.'''
    
    def __init__(self,parent):
        '''Specifies which gropu this element is in.'''
        self.parent = parent
    
    def __mult__(self,other):
        ''' Multiplies this gropu element with other '''
        return self.parent.multiply(self, other)
    
class GradingGroup(Group):
    ''' Bi-Grading Group associated to a tangle.'''
    
    def __init__(self, tangle, maslov, alexander):
        self.tangle = tangle
        self.maslov = maslov
        self.alexander
    
    def __eq__(self, other):
        return self.tangle == other.tangle and self.maslov == other.maslov \
        and self.alexander == other.alexander

    def __ne__(self,other):
        return not (self == other)
    
    def multiply(self, elt1, elt2):
        if not isinstance(elt1, GroupElement):
            return NotImplemented
        if not isinstance(elt2, GroupElement):
            return NotImplemented
        assert elt1.parent == self and elt2.parent == self

        new_maslov = elt1.maslov + elt2. maslov # CB and compare with spinc
        new_alexander =  elt1.alexander + elt2.alexander
        
        return GradingGroup(self, new_maslov, new_alexander)

    def zero(self):
        ''' Returns the zero element of this grading group. '''
        return GradingElement(self, 0, 0)
    
    def central_m(self): #cb and remove if unncessary
        ''' returns the element with maslov = 1, alex = 0 of this grading group. '''
        return GradingElement(self, 1, 0)
    
    def central_a(self): # cb and remove if uncesary
        ''' dreturns the element with maslow = 0, alex = 1 of this grading group '''
        return GradingElement(self, 0, 1)

class GradingElement:
    ''' An element of this grading group.'''
    
    def __init__(self, parent, maslov, alexander):
        ''' Specifies the maslov and alexander component of the grading. '''
        
        GroupElement.__init__(self, parent)
        self.maslov = maslov
        self.alexander = alexander
    
    def __eq__(self, other):
        if isinstance(other, int) and other == 0:
            return self.maslov == 0 and self.alexander == 0
        
        return self.parent == other.parent and self.maslov == other.maslov \
                    and self.alexander == other.alexander
                    
    def __ne__(self,other):
        return not (self == other)
    
    def __hash__(self):
        return hash((self.parent, self.maslov, self.alexander))
    
    def __str__(self):
        return "[%s, %s]" %(str(self.maslov), str(self.alexander))
    
    def __repr__(self):
        return str(self)
    
    def __power(self, exp): # cb and remove if unncessary
        ''' Returns the grading element raised to the given power
        (basically multiplies the maslov and each spinc component by exp.'''
    
class Gradingset:
    ''' Represents a general grading set. Can specify an arbitrary number
        of group actions ( although only up to two is used).'''
    
    def __init__(self,actions):
        ''' actions is a list of tuples (group,side).
        Side must be either ACTION_LEFT or ACTION_RIGHT'''
    
        self.actions = actions
        self.type = self.actions[0][0].type # cb and fix
    
    def multiply(self, set_elt, grp_elt):
        ''' Returns the result of grp_elt acting on set_elt. 
        grp_elt is a list of grading group elements, whose length must equal 
        \ the number or group actions. ''' #cb ask akram
        
        raise NotImplementedError("Group action not implemented.")
    
class GradingSetElement:
    '''Represents an element of a grading set. '''
    # cb and ask akram
    
    def __init__(self, parent):
        ''' Specify which grading set this element is in.'''
        self.parent = parent
    
    def __mult__(self,other):
        ''' Returns the result of gropu action on self.'''
    