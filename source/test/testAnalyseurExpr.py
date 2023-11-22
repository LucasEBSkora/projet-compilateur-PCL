import unittest

from incluire_parent import incluire_parent
incluire_parent()

from fauxLexer import FauxLexer
from analyseurExpr import AnalyseurExpr
from Token import Token
from TypeToken import typeToken
import noeud
class TestAnalyseurExpr(unittest.TestCase):
  def test_addition(self):
    lexer = FauxLexer([Token(typeToken.IDENTIFICATEUR, "a", 0), Token(typeToken.PLUS, "+", 1), Token(typeToken.ENTIER, "2", 2)])
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.expr()
    self.assertIs(expr, noeud.Binaire)
    self.asserEqual(expr.operateur, "+")
    self.assertIs(expr.gauche, noeud.Ident)
    self.assertEqual(expr.gauche.nom, "a")
    self.assertIs(expr.droite, noeud.Literal)
    self.assertEqual(expr.droite.literal, "2")

if __name__ == '__main__':
    unittest.main()