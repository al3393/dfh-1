""" Unit Test for latex.py"""

from Latex import *
from tangle_new import TANGLE, StrandDiagram, Simple_Strand, Idempotent, StrandAlgebra, TangleModule
import unittest
from utility import F2
from b_e_tangle import braid_to_tangle

class LatexTest(unittest.TestCase):
    def testPrintDAStructure(self):
        braid_dic = braid_to_tangle()
        f = open("braid_latex_output.txt", "w")
        f.write(beginDoc())
        for i in range(1,len(braid_dic)+1):
            tang = TANGLE(braid_dic[i])
            f.write(showTangle(tang))
        f.write(endDoc())
        f.close()

if __name__ == "__main__":
    unittest.main()
    

