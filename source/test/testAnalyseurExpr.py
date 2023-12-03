import unittest

from incluire_parent import incluire_parent
incluire_parent()

from fauxLexer import FauxLexer
from analyseurExpr import AnalyseurExpr
from Token import Token
from TypeToken import typeToken
import noeud
from ExceptionSyntatique import ExceptionSyntatique

class TestAnalyseurExpr(unittest.TestCase):

  def test_appelSansIdentifier(self):
    lexer = FauxLexer([Token(typeToken.ENTIER, "1", 0, 0)]) 
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur.appel()
    except ExceptionSyntatique as e:
      self.assertEqual("unexpected 1", e.message)
      return
    self.assertTrue(False)

  def test_appelRetourneIdent(self):
    lexer = FauxLexer([Token(typeToken.IDENTIFICATEUR, "a", 0, 0), Token(typeToken.PLUS, "+", 0, 1)]) 
    analyseur = AnalyseurExpr(lexer)
    expr =  analyseur.appel()
    self.assertIsInstance(expr, noeud.Ident)
    self.assertEqual("a", expr.nom)
  
  def test_appelSansParentheseDroite(self):
    lexer = FauxLexer([Token(typeToken.IDENTIFICATEUR, "a", 0, 0), Token(typeToken.PARENG, "+", 0, 1), Token(typeToken.CARACTERE, "'a'", 0, 2)]) 
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur.appel()
    except ExceptionSyntatique as e:
      self.assertEqual("expected ')' or ',' after call parameter, got end of file", e.message)
      return
    self.assertTrue(False)

  def test_appelSansParamettres(self):
    lexer = FauxLexer([Token(typeToken.IDENTIFICATEUR, "abcd", 0, 0), Token(typeToken.PARENG, "+", 0, 1), Token(typeToken.PAREND, ")", 0, 2)]) 
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.appel()

    self.assertIsInstance(expr, noeud.Appel)
    self.assertEqual("abcd", expr.nom)
    self.assertListEqual([], expr.params)

  def test_appelAvecDeuxParamettres(self):
    lexer = FauxLexer([Token(typeToken.IDENTIFICATEUR, "abcd", 0, 0), Token(typeToken.PARENG, "+", 0, 1),  Token(typeToken.ENTIER, "5", 0, 2), Token(typeToken.COMMA, ",", 0, 3), Token(typeToken.CARACTERE, "'f'", 0, 4), Token(typeToken.PAREND, ")", 0, 2)]) 
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.appel()

    self.assertIsInstance(expr, noeud.Appel)
    self.assertEqual("abcd", expr.nom)
    self.assertEqual(2, len(expr.params))
    self.assertIsInstance(expr.params[0], noeud.Literal)
    self.assertEqual(expr.params[0].literal, "5")
    self.assertIsInstance(expr.params[1], noeud.Literal)
    self.assertEqual(expr.params[1].literal, "'f'")

  def test_appelVirguleManquante(self):
    lexer = FauxLexer([Token(typeToken.IDENTIFICATEUR, "abcd", 0, 0), Token(typeToken.PARENG, "+", 0, 1),  Token(typeToken.ENTIER, "5", 0, 2), Token(typeToken.CARACTERE, "'f'", 0, 4), Token(typeToken.PAREND, ")", 0, 2)]) 
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur.appel()
    except ExceptionSyntatique as e:
      self.assertEqual("expected ')' or ',' after call parameter, got 'f'", e.message)
      return
    self.assertTrue(False)


  def test_addition(self):
    lexer = FauxLexer([Token(typeToken.IDENTIFICATEUR, "a", 0, 0), Token(typeToken.PLUS, "+", 0, 1), Token(typeToken.ENTIER, "2", 0, 2)])
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur._addition()
    self.assertIsInstance(expr, noeud.Binaire)
    self.assertEqual(expr.operateur, "+")
    self.assertIsInstance(expr.gauche, noeud.Ident)
    self.assertEqual(expr.gauche.nom, "a")
    self.assertIsInstance(expr.droite, noeud.Literal)
    self.assertEqual(expr.droite.literal, "2")

if __name__ == '__main__':
    unittest.main()