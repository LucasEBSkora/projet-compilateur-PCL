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

    def test_prochain_token(self):
        lexer = FauxLexer([Token(typeToken.RETURN, "return", 0), Token(typeToken.SEMICOLON, ";", 1)])
        instr = AnalyseurInstr(lexer)
        self.assertEqual(True, instr.prochainToken(typeToken.RETURN))


    def test_verification(self):
        lexer = FauxLexer([Token(typeToken.RETURN, "return", 0), Token(typeToken.SEMICOLON, ";", 1)])
        instr = AnalyseurInstr(lexer)
        instr.verification(typeToken.RETURN)
        self.assertIs(typeToken.SEMICOLON ,lexer.peek().type)

    
    def test_return_expr(self):
        lexer = FauxLexer([Token(typeToken.RETURN, "return", 0), Token(typeToken.SEMICOLON, ";", 1)])
        analyseur = AnalyseurInstr(lexer)
        result = analyseur.instr()
        self.assertIs(result, noeud.Return)



if __name__ == '__main__':
    unittest.main()
