import noeud
from TypeToken import typeToken
from ExceptionSyntatique import ExceptionSyntatique

#parser expr

class AnalyseurExpr:
  def __init__(self, analyseurLexique):
    self.lexeur = analyseurLexique

  def expr(self):
    gauche = self._and()

    while self._prochainTokenEst(typeToken.OR):
      labelNoeud = "or"
      self.lexeur.next()
      if self._prochainTokenEst(typeToken.ELSE):
        labelNoeud = "or else"
        self.lexeur.next()
      droite = self._and()
      gauche = noeud.Binaire(gauche, labelNoeud, droite)
    
    return gauche

  def _and(self):
    gauche = self._not()

    while self._prochainTokenEst(typeToken.AND):
      labelNoeud = "and"
      self.lexeur.next()
      if self._prochainTokenEst(typeToken.THEN):
        labelNoeud = "and then"
        self.lexeur.next()
      droite = self._not()
      gauche = noeud.Binaire(gauche, labelNoeud, droite)
    
    return gauche

  def _not(self):
    if self._prochainTokenEst(typeToken.NOT):
      self.lexeur.next()
      operande = self._not()
      return noeud.Unaire("not", operande)
    
    return self._egal()

  def _egal(self):
    gauche = self._comparaison()

    if self._prochainTokenDans([typeToken.NE, typeToken.EQ]):
        label = self.lexeur.next().value
        droite = self._comparaison()
        return noeud.Binaire(gauche, label, droite)
    return gauche

  def _comparaison(self):
    gauche = self._addition()

    if  self._prochainTokenDans([typeToken.GE, typeToken.GT, 
                                       typeToken.LE, typeToken.LT]):
        label = self.lexeur.next().value
        droite = self._addition()
        return noeud.Binaire(gauche, label, droite)
    return gauche

  def _addition(self):
    gauche = self._multiplication()

    while self._prochainTokenDans([typeToken.PLUS, typeToken.MINUS]):
      label = self.lexeur.next().value
      droite = self._multiplication()
      gauche = noeud.Binaire(gauche, label, droite)
    return gauche

  def _multiplication(self):
    gauche = self._negation()

    while self._prochainTokenDans([typeToken.MUL, typeToken.DIV, typeToken.REM]):
      label = self.lexeur.next().value
      droite = self._negation()
      gauche = noeud.Binaire(gauche, label, droite)
    return gauche

  def _negation(self):
    if self._prochainTokenEst(typeToken.MINUS):
      self.lexeur.next()
      operande = self._negation()
      return noeud.Unaire("-", operande)
    
    return self.acces()

  def acces(self):
    expr = self._primaire()

    while self._prochainTokenEst(typeToken.POINT):
      self.lexeur.next()

      id = self.lexeur.next()
      if id.type != typeToken.IDENTIFICATEUR:
        raise ExceptionSyntatique(f"expected identifier after ., got {id.value} instead", id.ligne, id.colomne)

      expr = noeud.Binaire(expr, '.', noeud.Ident(id.value))

    return expr

  def _primaire(self):
    literal = self._essayerLiteral()
    if literal is not None:
      return literal
    
    exprParenthese = self._essayerParenthese()
    if exprParenthese is not None:
      return exprParenthese
    
    newExpr = self._essayerNew()
    if newExpr is not None:
      return newExpr
    
    character_val = self._essayerCharacterVal()
    if character_val is not None:
      return character_val
    
    return self.appel()
    
  def _essayerLiteral(self):
    if self._prochainTokenDans([typeToken.ENTIER, typeToken.CARACTERE, typeToken.TRUE, typeToken.FALSE, typeToken.NULL]):
      return noeud.Literal(self.lexeur.next().value)
    return None
  
  def _essayerParenthese(self):
    if not self._prochainTokenEst(typeToken.PARENG):
      return None
    self.lexeur.next()
    expr = self.expr()
    if not self._prochainTokenEst(typeToken.PAREND):
      faux_token = self.lexeur.next()
      raise ExceptionSyntatique(f"expected ')' got {faux_token.value} instead", faux_token.ligne, faux_token.colomne)
    self.lexeur.next()
    return expr
  
  def _essayerNew(self):
    if not self._prochainTokenEst(typeToken.NEW):
      return None
    self.lexeur.next()
    id = self.lexeur.next()
    if id.type != typeToken.IDENTIFICATEUR:
      raise ExceptionSyntatique(f"expected new identifier instead of {id.value}", id.ligne, id.colomne)
    return noeud.New(id.value)
    
  def _essayerCharacterVal(self):
    if not self._prochainTokenEst(typeToken.CHARACTER_APOSTROFE_VAL):
      return None
    self.lexeur.next()

    if not self._prochainTokenEst(typeToken.PARENG):
      faux_token = self.lexeur.next()
      raise ExceptionSyntatique(f"expected '(', got {faux_token.value} instead", faux_token.ligne, faux_token.colomne)
    self.lexeur.next()

    expr = self.expr()

    if not self._prochainTokenEst(typeToken.PAREND):
      faux_token = self.lexeur.next()
      raise ExceptionSyntatique(f"expected ')', got {faux_token.value} instead", faux_token.ligne, faux_token.colomne)
    self.lexeur.next()
    
    return noeud.CharacterApostrofeVal(expr)
  
  def appel(self):
    id = self.lexeur.next()
    if id.type != typeToken.IDENTIFICATEUR:
      raise ExceptionSyntatique(f"unexpected {id.value}", id.ligne, id.colomne)

    if not self._prochainTokenEst(typeToken.PARENG):
      return noeud.Ident(id.value)
  
    self.lexeur.next()
    params = []
    while not self._prochainTokenEst(typeToken.PAREND):
      params.append(self.expr())
      if self._prochainTokenEst(typeToken.COMMA):
        self.lexeur.next()
      elif not self._prochainTokenEst(typeToken.PAREND):
        token = self.lexeur.next()
        raise ExceptionSyntatique(f"expected ')' or ',' after call parameter, got {token.value}", token.ligne, token.colomne)
    self.lexeur.next()
    return noeud.Appel(id.value, params)
    
  def _prochainTokenEst(self, type):
    return self.lexeur.peek().type == type

  def _prochainTokenDans(self, types):
    return self.lexeur.peek().type in types
