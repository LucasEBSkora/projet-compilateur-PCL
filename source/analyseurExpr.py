import noeud
from TypeToken import typeToken
#parser expr
class AnalyseurExpr:
  def __init__(self, analyseurLexique):
    self.lexeur = analyseurLexique

  def expr(self):
    gauche = self._and()

    if self._prochainTokenEst(typeToken.OR):
      labelNoeud = "or"
      self.lexeur.next()
      if self._prochainTokenEst(typeToken.ELSE):
        labelNoeud = "or else"
        self.lexeur.next()
      droite = self.expr()
      return noeud.Binaire(gauche, labelNoeud, droite)
    
    return gauche

  def _and(self):
    gauche = self._not()

    if self._prochainTokenEst(typeToken.AND):
      labelNoeud = "and"
      self.lexeur.next()
      if self._prochainTokenEst(typeToken.THEN):
        labelNoeud = "and then"
        self.lexeur.next()
      droite = self._and()
      return noeud.Binaire(gauche, labelNoeud, droite)
    
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

    if self._prochainTokenDans([typeToken.PLUS, typeToken.MINUS]):
      label = self.lexeur.next().value
      droite = self._addition()
      return noeud.Binaire(gauche, label, droite)
    return gauche

  def _multiplication(self):
    gauche = self._negation()

    if self._prochainTokenDans([typeToken.MUL, typeToken.DIV, typeToken.REM]):
      label = self.lexeur.next().value
      droite = self._multiplication()
      return noeud.Binaire(gauche, label, droite)
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
      if not self._prochainTokenEst(typeToken.IDENTIFICATEUR):
        print(f"expected identifier after . at {id.position}, got {id.value} instead")

      expr = noeud.Access(expr, id)

    return expr

  def _primaire(self):
    literal = self._essayerLiteral()
    if not (literal is None):
      return literal
    
    exprParenthese = self._essayerParenthese()
    if not (exprParenthese is None):
      return exprParenthese
    
    newExpr = self._essayerNew()
    if not (newExpr is None):
      return newExpr
    
    character_val = self._essayerCharacterVal()
    if not (character_val is None):
      return character_val
    
    return self.appel()
    
  def _essayerLiteral(self):
    if self._prochainTokenDans([typeToken.ENTIER, typeToken.CARACTERE, typeToken.TRUE, typeToken.FALSE, typeToken.NULL]):
      return noeud.Literal(self.lexeur.next())
    return None
  
  def _essayerParenthese(self):
    if not self._prochainTokenEst(typeToken.PARENG):
      return None
    self.lexeur.next()
    expr = self.expr()
    if not self._prochainTokenEst(typeToken.PAREND):
      faux_token = self.lexeur.next()
      print(f"expected ')' at ${faux_token.position}, got {faux_token.value} instead")
      exit(1)
    self.lexeur.next()
    return expr
  
  def _essayerNew(self):
    if not self._prochainTokenEst(typeToken.NEW):
      return None
    id = self.lexeur.next()
    if id.type != typeToken.IDENTIFICATEUR:
      print(f"expected new identifier at ${id.position}, got {id.value} instead")
      exit(1)
    return id
    
  def _essayerCharacterVal(self):
    if not self._prochainTokenEst(typeToken.CHARACTER_APOSTROFE_VAL):
      return None
    self.lexeur.next()

    expr = self.expr()
    return noeud.CharacterApostrofeVal(expr)
  
  def appel(self, id):
    id = self.lexeur.peek()
    if id.type != typeToken.IDENTIFICATEUR:
      print(f"unexpected '{id.value}' at {id.position}")
      exit(1)

    if not self._prochainTokenEst(typeToken.PARENG):
      return id
  
    self.lexeur.next()
    params = []
    while not self._prochainTokenEst(typeToken.PAREND):
      params.append(self.expr())
      if self._prochainTokenEst(typeToken.COMMA):
        self.lexeur.next()
      elif not self._prochainTokenEst(typeToken.PAREND):
        token = self.lexeur.next()
        print(f"expected ')' or ',' after call parameter, got {token.value} instead")
        exit(1)
    self.lexeur.next()
    return noeud.Appel(id, params)
    
  def _prochainTokenEst(self, type):
    return self.lexeur.peek().type == type

  def _prochainTokenDans(self, types):
    return self.lexeur.peek().type in types
