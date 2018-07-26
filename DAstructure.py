'''Defines type DA Structures.'''

from algebra import DGAlgebra, FreeModule, Generator, Tensor, \
    TensorGenerator, TensorStarGenerator
from algebra import ChainComplex, E0, TensorDGAlgebra
from dstructure import DGenerator, SimpleDStructure
from ddstructure import DDGenerator, SimpleDDGenerator, SimpleDDStructure
from grading import GeneralGradingSet, GeneralGradingSetElement, \
    SimpleDbGradingSetElement
from hdiagram import getIdentityDiagram
from pmc import StrandDiagram
from utility import MorObject, NamedObject
from utility import sumColumns
from utility import ACTION_LEFT, ACTION_RIGHT, F2