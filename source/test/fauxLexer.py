from incluire_parent import incluire_parent

incluire_parent()

from Token import Token
from TypeToken import typeToken
class FauxLexer:
  def __init__(self, tokens):
    self.tokens = tokens
    self.indice = 0
  def peek(self):
    if self.indice < len(self.tokens):
      return self.tokens[self.indice]
    return Token(typeToken.EOF, "end of file", 0, 0)
  def next(self):
      valeur = self.peek()
      self.indice += 1
      return valeur