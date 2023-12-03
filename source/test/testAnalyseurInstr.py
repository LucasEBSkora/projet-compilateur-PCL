import unittest

from incluire_parent import incluire_parent
incluire_parent()

from fauxLexer import FauxLexer
from analyseurExpr import AnalyseurExpr
from analyseurInstr import AnalyseurInstr
from Token import Token
from TypeToken import typeToken
import noeud

class TestAnalyseurInstr(unittest.TestCase):
    def test(self):
        pass



if __name__ == '__main__':
    unittest.main()
