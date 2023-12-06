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

  def test_prochainTokenEstFalse(self):
    lexer = FauxLexer.builder([(typeToken.ENTIER, "1")])
    analyseur = AnalyseurExpr(lexer)
    self.assertFalse(analyseur._prochainTokenEst(typeToken.AFFECT))

  def test_prochainTokenEstTrue(self):
    lexer = FauxLexer.builder([(typeToken.CARACTERE, "'c'")])
    analyseur = AnalyseurExpr(lexer)
    self.assertTrue(analyseur._prochainTokenEst(typeToken.CARACTERE))

  def test_prochainTokenDansFalse(self):
    lexer = FauxLexer.builder([(typeToken.ENTIER, "1")])
    analyseur = AnalyseurExpr(lexer)
    self.assertFalse(analyseur._prochainTokenDans([typeToken.DEUXPOINTS, typeToken.DIV]))

  def test_prochainTokenDansTrue(self):
    lexer = FauxLexer.builder([(typeToken.CARACTERE, "'c'")])
    analyseur = AnalyseurExpr(lexer)
    self.assertTrue(analyseur._prochainTokenDans([typeToken.CARACTERE, typeToken.COLON]))

  def test_appelSansIdentifier(self):
    lexer = FauxLexer.builder([(typeToken.ENTIER, "1")])
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur.appel()
    except ExceptionSyntatique as e:
      self.assertEqual("unexpected 1", e.message)
      return
    self.assertTrue(False)

  def test_appelRetourneIdent(self):
    lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "a"), (typeToken.PLUS, "+")]) 
    analyseur = AnalyseurExpr(lexer)
    expr =  analyseur.appel()
    self.assertIsInstance(expr, noeud.Ident)
    self.assertEqual("a", expr.nom)
    self.assertEqual(lexer.peek().type, typeToken.PLUS)
  
  def test_appelSansParentheseDroite(self):
    lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "a"), (typeToken.PARENG, "+"), (typeToken.CARACTERE, "'a'")]) 
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur.appel()
    except ExceptionSyntatique as e:
      self.assertEqual("expected ')' or ',' after call parameter, got end of file", e.message)
      return
    self.assertTrue(False)

  def test_appelSansParamettres(self):
    lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "abcd"), (typeToken.PARENG, "+"), (typeToken.PAREND, ")")]) 
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.appel()

    self.assertIsInstance(expr, noeud.Appel)
    self.assertEqual("abcd", expr.nom)
    self.assertListEqual([], expr.params)
    self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_appelAvecDeuxParamettres(self):
    lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "abcd"), (typeToken.PARENG, "+"),  (typeToken.ENTIER, "5"), (typeToken.COMMA, ","), (typeToken.CARACTERE, "'f'"), (typeToken.PAREND, ")")]) 
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.appel()

    self.assertIsInstance(expr, noeud.Appel)
    self.assertEqual("abcd", expr.nom)
    self.assertEqual(2, len(expr.params))
    self.assertIsInstance(expr.params[0], noeud.Literal)
    self.assertEqual(expr.params[0].literal, "5")
    self.assertIsInstance(expr.params[1], noeud.Literal)
    self.assertEqual(expr.params[1].literal, "'f'")
    self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_appelVirguleManquante(self):
    lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "abcd"), (typeToken.PARENG, "+"),  (typeToken.ENTIER, "5"), (typeToken.CARACTERE, "'f'"), (typeToken.PAREND, ")")]) 
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur.appel()
    except ExceptionSyntatique as e:
      self.assertEqual("expected ')' or ',' after call parameter, got 'f'", e.message)
      return
    self.assertTrue(False)

  def test_essayerCharacterValNon(self):
    lexer = FauxLexer.builder([(typeToken.ENTIER, "12")])
    analyseur = AnalyseurExpr(lexer)
    self.assertEqual(analyseur._essayerCharacterVal(), None)
    self.assertEqual(lexer.peek().type, typeToken.ENTIER)

  def test_essayerCharacterValOui(self):
    lexer = FauxLexer.builder([(typeToken.CHARACTER_APOSTROFE_VAL, ""), (typeToken.PARENG, "("), (typeToken.CARACTERE, "'a'"), (typeToken.PAREND, "("),])
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur._essayerCharacterVal()
    self.assertIsInstance(expr, noeud.CharacterApostrofeVal)
    self.assertIsInstance(expr.expr, noeud.Literal)
    self.assertEqual(expr.expr.literal, "'a'")
    self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_essayerCharacterValSansParentheseGauche(self):
    lexer = FauxLexer.builder([(typeToken.CHARACTER_APOSTROFE_VAL, ""), (typeToken.CARACTERE, "'a'")])
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur._essayerCharacterVal()
    except ExceptionSyntatique as e:
      self.assertEqual("expected '(', got 'a' instead", e.message)
      return
    self.assertTrue(False)

  def test_essayerCharacterValSansParentheseDroite(self):
    lexer = FauxLexer.builder([(typeToken.CHARACTER_APOSTROFE_VAL, ""), (typeToken.PARENG, "("), (typeToken.CARACTERE, "'a'")])
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur._essayerCharacterVal()
    except ExceptionSyntatique as e:
      self.assertEqual("expected ')', got end of file instead", e.message)
      return
    self.assertTrue(False)

  def test_essayerNewNon(self):
    lexer = FauxLexer.builder([(typeToken.PLUS, "+")])
    analyseur = AnalyseurExpr(lexer)
    self.assertEqual(analyseur._essayerNew(), None)
    self.assertEqual(lexer.peek().type, typeToken.PLUS)

  def test_essayerNewSansIdentificateur(self):
    lexer = FauxLexer.builder([(typeToken.NEW, "new"), (typeToken.PARENG, "(")]) 
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur._essayerNew()
    except ExceptionSyntatique as e:
      self.assertEqual("expected new identifier instead of (", e.message)
      return
    self.assertTrue(False)

  def test_essayerNew(self):
    lexer = FauxLexer.builder([(typeToken.NEW, "new"), (typeToken.IDENTIFICATEUR, "a_B")]) 
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur._essayerNew()
    self.assertIsInstance(expr, noeud.New)
    self.assertEqual(expr.nom, "a_B")
    self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_essayeParentheseNon(self):
    lexer = FauxLexer.builder([(typeToken.DEUXPOINTS, "..")])
    analyseur = AnalyseurExpr(lexer)
    self.assertEqual(analyseur._essayerNew(), None)
    self.assertEqual(lexer.peek().type, typeToken.DEUXPOINTS)

  def test_essayerParentheseSansParentheseFerme(self):
    lexer = FauxLexer.builder([(typeToken.PARENG, "("), (typeToken.CARACTERE, "'a'")]) 
    analyseur = AnalyseurExpr(lexer)
    try:
      analyseur._essayerParenthese()
    except ExceptionSyntatique as e:
      self.assertEqual(f"expected ')' got end of file instead", e.message)
      return
    self.assertTrue(False)

  def test_essayerParenthese(self):
    lexer = FauxLexer.builder([(typeToken.PARENG, "("), (typeToken.CARACTERE, "'a'"), (typeToken.PLUS, "+"), (typeToken.CARACTERE, "b"), (typeToken.PAREND, ")")]) 
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur._essayerParenthese()
    self.assertIsInstance(expr, noeud.Binaire)
    self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_essayerLiteralNon(self):
    lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "ab")])
    analyseur = AnalyseurExpr(lexer)
    self.assertEqual(analyseur._essayerLiteral(), None)
    self.assertEqual(lexer.peek().type, typeToken.IDENTIFICATEUR)

  def test_esssayerLiteral(self):
    types_literales = {
      typeToken.ENTIER: Token(typeToken.ENTIER, "23", 1, 1),
      typeToken.CARACTERE: Token(typeToken.CARACTERE, "'\r'", 1, 1),
      typeToken.TRUE: Token(typeToken.TRUE, "true", 1, 1),
      typeToken.FALSE: Token(typeToken.FALSE, "false", 1, 1),
      typeToken.NULL: Token(typeToken.NULL, "null", 1, 1)
    }
    for type in types_literales.keys():
       with self.subTest(i=types_literales[type].value): 
         lexer = FauxLexer([types_literales[type]])
         analyseur = AnalyseurExpr(lexer)
         expr = analyseur._essayerLiteral()
         self.assertIsInstance(expr, noeud.Literal)
         self.assertEqual(types_literales[type].value, expr.literal)
         self.assertEqual(lexer.peek().type, typeToken.EOF)
    
  def test_primaire(self):
    expressions_primaires = {
      noeud.Literal: [(typeToken.ENTIER, "23")],
      noeud.Unaire: [(typeToken.PARENG, "("), (typeToken.MINUS, "-"), (typeToken.ENTIER, "2"), (typeToken.PAREND, ")")],
      noeud.New: [(typeToken.NEW, "new"), (typeToken.IDENTIFICATEUR, "a")],
      noeud.CharacterApostrofeVal: [(typeToken.CHARACTER_APOSTROFE_VAL, "character'val"), (typeToken.PARENG, "("), (typeToken.CARACTERE, "'b'"), (typeToken.PAREND, ")")],
      noeud.Ident: [(typeToken.IDENTIFICATEUR, "abc")]
    }
    for type in expressions_primaires:
      with self.subTest(i=type):
        lexer = FauxLexer.builder(expressions_primaires[type])
        analyseur = AnalyseurExpr(lexer)
        expr = analyseur._primaire()
        self.assertIsInstance(expr, type)
        self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_descendreRecursive(self):
    analyseur = AnalyseurExpr(None)
    fonctions = [analyseur.expr, analyseur._and, analyseur._not, analyseur._egal, analyseur._comparaison,
                 analyseur._addition, analyseur._multiplication, analyseur._negation, analyseur.acces]
    for fonction in fonctions:
      with self.subTest(i=fonction):
        analyseur.lexeur = FauxLexer.builder([(typeToken.IDENTIFICATEUR, 'a')])
        expr = fonction()
        self.assertIsInstance(expr, noeud.Ident)
        self.assertEqual(analyseur.lexeur.peek().type, typeToken.EOF)

  def test_acces(self):
    lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, 'a'), (typeToken.POINT, '.'), (typeToken.IDENTIFICATEUR, 'b'), (typeToken.POINT, '.'), (typeToken.IDENTIFICATEUR, 'c')])
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.acces()
    self.assertIsInstance(expr, noeud.Binaire)
    self.assertEqual(expr.operateur, '.')
    self.assertIsInstance(expr.droite, noeud.Ident)
    self.assertEqual(expr.droite.nom, 'c')
    subExpr = expr.gauche
    self.assertIsInstance(subExpr, noeud.Binaire)
    self.assertEqual(subExpr.operateur, '.')
    self.assertIsInstance(subExpr.gauche, noeud.Ident)
    self.assertEqual(subExpr.gauche.nom, 'a')
    self.assertIsInstance(subExpr.droite, noeud.Ident)
    self.assertEqual(subExpr.droite.nom, 'b')
    self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_accesSansIdentificateur(self):
    analyseur = AnalyseurExpr(FauxLexer.builder([(typeToken.IDENTIFICATEUR, 'a'), (typeToken.POINT, '.'), (typeToken.IDENTIFICATEUR, 'b'), (typeToken.POINT, '.'), (typeToken.CARACTERE, "'c'")]))
    try:
      analyseur.acces()
    except ExceptionSyntatique as e:
      self.assertEqual(f"expected identifier after ., got 'c' instead", e.message)
      return
    self.assertTrue(False)

  def test_unaire(self):
    for token in [(typeToken.MINUS, '-'), (typeToken.NOT, 'not')]:
      with self.subTest(i=token[1]):
        lexer = FauxLexer.builder([token, (typeToken.IDENTIFICATEUR, 'a')])
        analyseur = AnalyseurExpr(lexer)
        expr = analyseur.expr()
        self.assertIsInstance(expr, noeud.Unaire)
        self.assertEqual(expr.operateur, token[1])
        self.assertIsInstance(expr.operande, noeud.Ident)
        self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_unaireDouble(self):
    for token in [(typeToken.MINUS, '-'), (typeToken.NOT, 'not')]:
      with self.subTest(i=token[1]):
        lexer = FauxLexer.builder([token, token, (typeToken.IDENTIFICATEUR, 'a')])
        analyseur = AnalyseurExpr(lexer)
        expr = analyseur.expr()
        self.assertIsInstance(expr, noeud.Unaire)
        self.assertEqual(expr.operateur, token[1])
        self.assertIsInstance(expr.operande, noeud.Unaire)
        self.assertEqual(expr.operande.operateur, token[1])
        self.assertIsInstance(expr.operande.operande, noeud.Ident)
        self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_binaire(self):
    operateurs = {
      "or": [(typeToken.OR, 'or')],
      "or else": [(typeToken.OR, 'or'), (typeToken.ELSE, 'else')],
      "and": [(typeToken.AND, 'and')],
      "and then": [(typeToken.AND, 'and'), (typeToken.THEN, 'then')],
      "=": [(typeToken.EQ, '=')],
      "\=": [(typeToken.NE, '\=')],
      ">": [(typeToken.GT, '>')],
      ">=": [(typeToken.GE, '>=')],
      "<": [(typeToken.LT, '<')],
      "<=": [(typeToken.LE, '<=')],
      "+": [(typeToken.PLUS, '+')],
      "-": [(typeToken.MINUS, '-')],
      "*": [(typeToken.MUL, '*')],
      "/": [(typeToken.DIV, '/')],
      "rem": [(typeToken.REM, 'rem')],
    }
    for test in operateurs.keys():
      with self.subTest(i=test):
        tokens = operateurs[test]
        tokens.insert(0, (typeToken.IDENTIFICATEUR, 'a'))
        tokens.append((typeToken.IDENTIFICATEUR, 'b'))
        lexer = FauxLexer.builder(tokens)
        analyseur = AnalyseurExpr(lexer)
        expr = analyseur.expr()
        self.assertIsInstance(expr, noeud.Binaire)
        self.assertEqual(expr.operateur, test)
        self.assertIsInstance(expr.gauche, noeud.Ident)
        self.assertEqual(expr.gauche.nom, 'a')
        self.assertIsInstance(expr.droite, noeud.Ident)
        self.assertEqual(expr.droite.nom, 'b')
        self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_associativite(self):
    operateurs = {
      "or": [(typeToken.OR, 'or')],
      "or else": [(typeToken.OR, 'or'), (typeToken.ELSE, 'else')],
      "and": [(typeToken.AND, 'and')],
      "and then": [(typeToken.AND, 'and'), (typeToken.THEN, 'then')],
      "+": [(typeToken.PLUS, '+')],
      "-": [(typeToken.MINUS, '-')],
      "*": [(typeToken.MUL, '*')],
      "/": [(typeToken.DIV, '/')],
      "rem": [(typeToken.REM, 'rem')],
    }
    for test in operateurs.keys():
      with self.subTest(i=test):
        tokens = list(operateurs[test])
        tokens.insert(0, (typeToken.IDENTIFICATEUR, 'a'))
        tokens.append((typeToken.IDENTIFICATEUR, 'b'))
        tokens = tokens + operateurs[test]
        tokens.append((typeToken.IDENTIFICATEUR, 'c'))
        lexer = FauxLexer.builder(tokens)
        analyseur = AnalyseurExpr(lexer)
        expr = analyseur.expr()
        self.assertIsInstance(expr, noeud.Binaire)
        self.assertEqual(expr.operateur, test)
        
        self.assertIsInstance(expr.gauche, noeud.Binaire)
        self.assertEqual(expr.gauche.operateur, test)

        self.assertIsInstance(expr.gauche.gauche, noeud.Ident)
        self.assertEqual(expr.gauche.gauche.nom, 'a')
        self.assertIsInstance(expr.gauche.droite, noeud.Ident)
        self.assertEqual(expr.gauche.droite.nom, 'b')

        self.assertIsInstance(expr.droite, noeud.Ident)

        self.assertEqual(expr.droite.nom, 'c')
        self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_precedenceBinaires(self):
    paires = [ 
      ("or", (typeToken.OR, 'or')),
      ("and", (typeToken.AND, 'and')),
      ("=", (typeToken.EQ, '=')),
      ("<", (typeToken.LT, '<')),
      ("+", (typeToken.PLUS, '+')),
      ("*", (typeToken.MUL, '*')),
      (".", (typeToken.POINT, '.')),
    ]
    for i in range(0, len(paires) - 1):
      with self.subTest(i=f"priorite {paires[i][0]} avec {paires[i+1][0]}"):
        faible = paires[i][0]
        forte = paires[i+1][0]
        tokens = [(typeToken.IDENTIFICATEUR, 'a'), 
                  paires[i][1],
                  (typeToken.IDENTIFICATEUR, 'b'),
                  paires[i+1][1],
                  (typeToken.IDENTIFICATEUR, 'c')
                  ]
        lexer = FauxLexer.builder(tokens)
        analyseur = AnalyseurExpr(lexer)
        expr = analyseur.expr()
        self.assertIsInstance(expr, noeud.Binaire)
        self.assertEqual(expr.operateur, faible)
        
        self.assertIsInstance(expr.gauche, noeud.Ident)
        self.assertEqual(expr.gauche.nom, 'a')

        self.assertIsInstance(expr.droite, noeud.Binaire)
        self.assertEqual(expr.droite.operateur, forte)

        self.assertIsInstance(expr.droite.gauche, noeud.Ident)
        self.assertEqual(expr.droite.gauche.nom, 'b')
        self.assertIsInstance(expr.droite.droite, noeud.Ident)
        self.assertEqual(expr.droite.droite.nom, 'c')

        self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_AssociativiteNegationAcces(self):
    tokens = [(typeToken.MINUS, '-'), 
              (typeToken.IDENTIFICATEUR, 'a'), 
              (typeToken.POINT, '.'),
              (typeToken.IDENTIFICATEUR, 'b'),
              ]
    lexer = FauxLexer.builder(tokens)
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.expr()
    self.assertIsInstance(expr, noeud.Unaire)
    self.assertEqual(expr.operateur, '-')
    
    self.assertIsInstance(expr.operande, noeud.Binaire)
    self.assertEqual(expr.operande.operateur, '.')

    self.assertIsInstance(expr.operande.gauche, noeud.Ident)
    self.assertEqual(expr.operande.gauche.nom, 'a')
    self.assertIsInstance(expr.operande.droite, noeud.Ident)
    self.assertEqual(expr.operande.droite.nom, 'b')

  def test_AssociativiteNegationAddition(self):
    tokens = [(typeToken.IDENTIFICATEUR, 'a'), 
              (typeToken.PLUS, '+'),
              (typeToken.MINUS, '-'), 
              (typeToken.IDENTIFICATEUR, 'b'),
              ]
    lexer = FauxLexer.builder(tokens)
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.expr()
    self.assertIsInstance(expr, noeud.Binaire)
    self.assertEqual(expr.operateur, '+')
    
    self.assertIsInstance(expr.gauche, noeud.Ident)
    self.assertEqual(expr.gauche.nom, 'a')

    self.assertIsInstance(expr.droite, noeud.Unaire)
    self.assertEqual(expr.droite.operateur, '-')

    self.assertIsInstance(expr.droite.operande, noeud.Ident)
    self.assertEqual(expr.droite.operande.nom, 'b')
    
    self.assertEqual(lexer.peek().type, typeToken.EOF)

  def test_AssociativiteNotEgal(self):
    tokens = [(typeToken.NOT, 'not'), 
              (typeToken.IDENTIFICATEUR, 'a'), 
              (typeToken.EQ, '='),
              (typeToken.IDENTIFICATEUR, 'b'),
              ]
    lexer = FauxLexer.builder(tokens)
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.expr()
    self.assertIsInstance(expr, noeud.Unaire)
    self.assertEqual(expr.operateur, 'not')
    
    self.assertIsInstance(expr.operande, noeud.Binaire)
    self.assertEqual(expr.operande.operateur, '=')

    self.assertIsInstance(expr.operande.gauche, noeud.Ident)
    self.assertEqual(expr.operande.gauche.nom, 'a')
    self.assertIsInstance(expr.operande.droite, noeud.Ident)
    self.assertEqual(expr.operande.droite.nom, 'b')

  def test_AssociativiteNotAnd(self):
    tokens = [(typeToken.IDENTIFICATEUR, 'a'), 
              (typeToken.AND, 'and'),
              (typeToken.NOT, 'not'), 
              (typeToken.IDENTIFICATEUR, 'b'),
              ]
    lexer = FauxLexer.builder(tokens)
    analyseur = AnalyseurExpr(lexer)
    expr = analyseur.expr()
    self.assertIsInstance(expr, noeud.Binaire)
    self.assertEqual(expr.operateur, 'and')
    
    self.assertIsInstance(expr.gauche, noeud.Ident)
    self.assertEqual(expr.gauche.nom, 'a')

    self.assertIsInstance(expr.droite, noeud.Unaire)
    self.assertEqual(expr.droite.operateur, 'not')

    self.assertIsInstance(expr.droite.operande, noeud.Ident)
    self.assertEqual(expr.droite.operande.nom, 'b')
    
    self.assertEqual(lexer.peek().type, typeToken.EOF)

if __name__ == '__main__':
    unittest.main()