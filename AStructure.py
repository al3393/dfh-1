'''Defines type A structures.'''

from fractions import Fraction
from algebra import DGAlgebra, FreeModule, Generator, SimpleChainComplex, \
    Tensor, TensorGenerator
from algebra import simplifyComplex
from algebra import E0
from grading import GeneralGradingSet, GeneralGradingSetElement
#from hdiagram import getZeroFrameDiagram, getInfFrameDiagram, getPlatDiagram
from tangle_new import Idempotent, Strands, StrandDiagram
from pmc import connectSumPMC, splitPMC, linearPMC
from utility import MorObject, NamedObject
from utility import memorize
from utility import ACTION_LEFT, DEFAULT_GRADING, F2, SMALL_GRADING
