import noeud
from TypeToken import typeToken

class AnalyseurExpr:
  def __init__(self, analyseurLexique):
    self.lexeur = analyseurLexique

  def expr(self):
    gauche = self._and()

    if self.lexeur.peek().type == typeToken.OR:
      labelNoeud = "or"
      self.lexeur.next()
      if self.lexeur.peek().type == typeToken.ELSE:
        labelNoeud = "or else"
        self.lexeur.next()
      droite = self.expr()
      return noeud.Binaire(gauche, labelNoeud, droite)
    
    return gauche

  def _and(self):
    gauche = self._not()

    if self.lexeur.peek().type == typeToken.AND:
      labelNoeud = "and"
      self.lexeur.next()
      if self.lexeur.peek().type == typeToken.THEN:
        labelNoeud = "and then"
        self.lexeur.next()
      droite = self._and()
      return noeud.Binaire(gauche, labelNoeud, droite)
    
    return gauche

  def _not(self):
    if self.lexeur.peek().type == typeToken.NOT:
      self.lexeur.next()
      operande = self._not()
      return noeud.Unaire("not", operande)
    return self._egal()

  def _egal(self):
    None

  def _comparaison(self):
    None

  def _addition(self):
    None

  def _multiplication(self):
    None

  def _negation(self):
    None

  def acces(self):
    None

  def _acces_embrique(self):
    None

  def _primaire(self):
    None

