import unittest

import string

from incluire_parent import incluire_parent
incluire_parent()

from lexer import Tokens
from Token import mots_cles, Token
from TypeToken import typeToken

class TestLexer(unittest.TestCase):
  def creerObjetEtTesterUnSeuleToken(self, tokenAttendu, text):
    lexer = Tokens()
    lexer.lexer(text)
    token = lexer.next()
    self.assertEqual(tokenAttendu.type, token.type)
    self.assertEqual(tokenAttendu.value, token.value)
    self.assertEqual(tokenAttendu.ligne, token.ligne)
    self.assertEqual(tokenAttendu.colomne, token.colomne)
    return lexer 

  def test_identifieChaqueMotCle(self):
    for mot_cle in mots_cles.keys():
      with self.subTest(msg=mot_cle):
        self.creerObjetEtTesterUnSeuleToken(Token(mots_cles[mot_cle], mot_cle, 1, 1), mot_cle)

  def test_identifieChaqueOperateur(self):
    operateurs = {
      "=": typeToken.EQ,
     "/=": typeToken.NE,
     "<": typeToken.LT,
     "<=": typeToken.LE,
     ">=": typeToken.GE,
     ">": typeToken.GT,
     "-": typeToken.MINUS,
     "+": typeToken.PLUS,
     "*": typeToken.MUL,
     "/": typeToken.DIV,
     ".": typeToken.POINT,
     ":=": typeToken.AFFECT,
     ";": typeToken.SEMICOLON,
     ",": typeToken.COMMA,
     ":": typeToken.COLON,
      "(": typeToken.PARENG,
      ")": typeToken.PAREND,
      "..":typeToken.DEUXPOINTS,
    }
    for operateur in operateurs.keys():
      with self.subTest(msg=operateur):
        self.creerObjetEtTesterUnSeuleToken(Token(operateurs[operateur], operateur, 1, 1), operateur)

  def test_identifieChaqueEntier(self):
    for i in range(0, 10):
      text = str(i)
      with self.subTest(msg=text):
        self.creerObjetEtTesterUnSeuleToken(Token(typeToken.ENTIER, text, 1, 1), text)
        
  def test_identifieEntiersPlusiersChiffres(self):
    text = "1258102842194"
    lexer = self.creerObjetEtTesterUnSeuleToken(Token(typeToken.ENTIER, text, 1, 1) , text)
    self.assertEqual(typeToken.EOF, lexer.peek().next())

  def test_identifieChaqueCaractere(self):
    for c in string.printable:
      str = f"'{c}'"
      with self.subTest(msg=str):
        self.creerObjetEtTesterUnSeuleToken(Token(typeToken.CARACTERE, str, 1, 1), str)

  def test_identifieChaqueIdentificateurUnSeuleCaractere(self):
    for c in string.ascii_letters:
      with self.subtest(msg=c):
        self.creerObjetEtTesterUnSeuleToken(Token(typeToken.IDENTIFICATEUR, c, 1, 1), c)

  def test_identifieidentificateurAvecUnderline(self):
    text = "a_"
    self.creerObjetEtTesterUnSeuleToken(Token(typeToken.IDENTIFICATEUR, text, 1, 1), text)

  def test_identifieIdentificateursAvecChaqueChiffre(self):
    for i in range(0, 10):
      text = f"a{i}"
      with self.subtest(msg=text):
        self.creerObjetEtTesterUnSeuleToken(Token(typeToken.IDENTIFICATEUR, text, 1, 1), text)

  def test_identifieIdentificateursPlusLonges(self):
    text = "abcd_00XYZ_W23"
    self.creerObjetEtTesterUnSeuleToken(Token(typeToken.IDENTIFICATEUR, text, 1, 1), text)

  def test_IdentifieADA(self):
    text = "Ada.Text_IO"
    self.creerObjetEtTesterUnSeuleToken(Token(typeToken.ADA, text, 1, 1), text)

  def test_IdentifieCharacterApostrofeVal(self):
    text= "character'val"
    self.creerObjetEtTesterUnSeuleToken(Token(typeToken.CHARACTER_APOSTROFE_VAL, text, 1, 1), text)

  def test_enleveCaracteresBlancs(self):
    text = "    \r\t\t\na            \n"
    lexer = Tokens()
    lexer.lexer(text)
    token = lexer.next()
    self.assertEqual(typeToken.IDENTIFICATEUR, token.type)
    self.assertEqual("a", token.value)
    self.assertEqual(2, token.ligne)
    self.assertEqual(9, token.colomne)

  def creerObjetEtTesterPlusiersTokens(self, tokensAttendus, text):
    lexer = Tokens()
    lexer.lexer(text)
    token = lexer.next()
    for tokenAttendu in tokensAttendus:
      token = lexer.next()
      self.assertEqual(tokenAttendu.type, token.type)
      self.assertEqual(tokenAttendu.value, token.value)
      self.assertEqual(tokenAttendu.ligne, token.ligne)
      self.assertEqual(tokenAttendu.colomne, token.colomne)

    return lexer 


  def test_trouvePositionDebutTokensCorrectement(self):
    text = "   aa\t\n\n\n\n 1234 + \n'c'"
    tokensAttendus = [ Token(typeToken.IDENTIFICATEUR, "aa", 1, 3),
      Token(typeToken.ENTIER, "1234", 5, 2),
      Token(typeToken.PLUS, "+", 5, 6),
      Token(typeToken.CARACTERE, "'c'", 6, 1)
      Token(typeToken.EOF, "", 6, 4)
    ]
    self.creerObjetEtTesterPlusiersTokens(tokensAttendus, text)

  def test_comprendPlusiersTokensEnsemble(self):
    text = "'a'+bbb-23/c"
    tokensAttendus = [ Token(typeToken.CARACTERE, "'a'", 1, 1),
      Token(typeToken.PLUS, "+", 1, 4),
      Token(typeToken.IDENTIFICATEUR, "bbb", 1, 5),
      Token(typeToken.MINUS, "-", 1, 8),
      Token(typeToken.ENTIER, "23", 1, 9),
      Token(typeToken.DIV, "/", 1, 11),
      Token(typeToken.IDENTIFICATEUR, "c", 1, 12),
      Token(typeToken.EOF, "", 1, 13)
    ]
    self.creerObjetEtTesterPlusiersTokens(tokensAttendus, text)

  def test_partageIdentificateursEtChiffresAvecCaracteresBlancs(self):
    text = "aa bb 12\t34\r56 cc\ndd"
    tokensAttendus = [Token(typeToken.IDENTIFICATEUR, "aa", 1, 1),
      Token(typeToken.IDENTIFICATEUR, "bb", 1, 4),
      Token(typeToken.ENTIER, "12", 1, 7),
      Token(typeToken.ENTIER, "34", 1, 10),
      Token(typeToken.ENTIER, "56", 1, 13),
      Token(typeToken.IDENTIFICATEUR, "cc", 1, 16),
      Token(typeToken.IDENTIFICATEUR, "dd", 1, 19),
      Token(typeToken.EOF, "", 1, 13)
    ]
    self.creerObjetEtTesterPlusiersTokens(tokensAttendus, text)

  def test_peekEtNext(self):
    text = "a b c d"
    lexer = Tokens()
    lexer.lexer(text)
    self.assertEqual("a", lexer.next().value)
    self.assertEqual("b", lexer.peek().value)
    self.assertEqual("b", lexer.peek().value)
    self.assertEqual("c", lexer.next().value)
    

if __name__ == '__main__':
    unittest.main()