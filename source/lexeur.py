from Token import Token, mots_cles
from TypeToken import typeToken
import string
from ExceptionLexique import ExceptionLexique

class Lexeur:
    
  def __init__(self, source):
    # programme source
    self.source = source
    # tokens déjà identifiés
    self.tokens = []
    # position dans le vecteur de tokens identifiés
    self.indice = 0

    # position dans le fichier programme (pour debug)
    self.ligneCourant = 1
    self.colomneCourant = 1

    # position du debut du token actuel
    self.debut = 0
    # position actuellement lu du programme source
    self.courant = 0

    while not self._finSource():
      if self._prochainCaractereDans(' \r\t\n\0'):
        self._avancer()
      else:
        self._lireToken()

  def _lireToken(self):
    self.debut = self.courant
    self.ligneDebut = self.ligneCourant
    self.colomneDebut = self.colomneCourant
    char = self._avancer()

    lexemes = {
      '=': lambda : self._ajouterToken(typeToken.EQ),
      '/': lambda : self._siSouvantSinon('=', typeToken.NE, typeToken.DIV),
      '<': lambda : self._siSouvantSinon('=', typeToken.LE, typeToken.LT),
      '>': lambda : self._siSouvantSinon('=', typeToken.GE, typeToken.GT),
      '-': lambda : self._verifierCommentaire(),
      '+': lambda : self._ajouterToken(typeToken.PLUS),
      '*': lambda : self._ajouterToken(typeToken.MUL),
      '.': lambda : self._siSouvantSinon('.', typeToken.DEUXPOINTS, typeToken.POINT),
      ':': lambda : self._siSouvantSinon('=', typeToken.AFFECT, typeToken.COLON),
      ';': lambda : self._ajouterToken(typeToken.SEMICOLON),
      ',': lambda : self._ajouterToken(typeToken.COMMA),
      '(': lambda : self._ajouterToken(typeToken.PARENG),
      ')': lambda : self._ajouterToken(typeToken.PAREND),
      "'": lambda : self._caractere(),
    }

    if (char in lexemes):
      lexemes[char]()
      return
    

    if self._estChiffre(char):
      self._nombre()
      return

    if self._estDebutValideIdentifiantOuMotCle(char):
      self._identifiantOuMotCle()
      return 
        
    raise ExceptionLexique(f"caractere inattendu {char}", self.ligneDebut, self.colomneDebut)
    
  def _siSouvantSinon(self, char, si, sinon):
    if self._prochainCaractere() == char:
      self._avancer()
      self._ajouterToken(si)
    else:
      self._ajouterToken(sinon)

  def _caractere(self):
    if self._finSource():
      raise ExceptionLexique("literal de caractere pas fini", self.ligneCourant, self.colomneCourant)
    char = self._avancer()

    if char == '\\':
      if self._prochainCaractereDans("0ntr\\"):
        char += self._avancer()
      else:
        raise ExceptionLexique(f"caractère d'échappement invalide: \{self._prochainCaractere()}")

    if not self._match("'"):
      raise ExceptionLexique("literal de caractere pas fini", self.ligneCourant, self.colomneCourant)

    if len(char) == 1 and char not in string.printable:
      raise ExceptionLexique(f"literal de caractere invalide: caractere ASCII {ord(char)}", self.ligneCourant, self.colomneCourant)

    self._ajouterToken(typeToken.CARACTERE)

  def _nombre(self):
    while self._estChiffre(self._prochainCaractere()):
      self._avancer()
    
    self._ajouterToken(typeToken.ENTIER)
  
  def _identifiantOuMotCle(self):
    while self._estCaractereValideIdentifiantOuMotCle(self._prochainCaractere()):
      self._avancer()
    
    prefixe = self.source[self.debut:self.courant]

    if prefixe == "Ada":
      if self._prochainCaracteresSont('.Text_IO'):
        self._ajouterToken(typeToken.ADA)
        return
    elif prefixe == "character":
      if self._prochainCaracteresSont("'val"):
        self._ajouterToken(typeToken.CHARACTER_APOSTROFE_VAL)
        return
    elif prefixe in mots_cles:
      self._ajouterToken(mots_cles[prefixe])
      return
    
    self._ajouterToken(typeToken.IDENTIFICATEUR)
    
  def _verifierCommentaire(self):
    if not self._match('-'):
      self._ajouterToken(typeToken.MINUS)
      return
    char = self.source[self.courant]
    while not self._finSource() and self._avancer() != '\n':
      pass

  def _prochainCaracteresSont(self, chars):
    courant = self.courant
    for c in chars:
      if courant < len(self.source) and self.source[courant] == c:
        courant += 1
      else:
        return False
    for i in chars:
      self._avancer()
    return True

  def _avancer(self):
    if self._finSource():
      return None
    char = self.source[self.courant]
    self.courant += 1
    if char == '\n':
      self.ligneCourant += 1
      self.colomneCourant = 1
    else:
      self.colomneCourant += 1
    return char
  
  def _ajouterToken(self, type):
    texte = self.source[self.debut:self.courant]
    self.tokens.append(Token(type, texte, self.ligneDebut, self.colomneDebut))

  def _match(self, char):
    if not self._prochainCaractereEst(char):
      return False
    
    self._avancer()
    return True
  
  def _prochainCaractereEst(self, char):
    return self._prochainCaractere() == char

  def _prochainCaractereDans(self, chars):
    c = self._prochainCaractere()
    return c is not None and c in chars
  
  def _estChiffre(self, c):
    return c is not None and c in string.digits
  
  def _estDebutValideIdentifiantOuMotCle(self, c):
    return c is not None and  c in string.ascii_letters
  
  def _estCaractereValideIdentifiantOuMotCle(self, c):
    return self._estChiffre(c) or self._estDebutValideIdentifiantOuMotCle(c) or c == '_'
  
  def _finSource(self):
    return self.courant >= len(self.source)

  def _prochainCaractere(self):
    if self._finSource():
      return None
    return self.source[self.courant]

  def peek(self):
    if self.indice < len(self.tokens):
      return self.tokens[self.indice]
    return Token(typeToken.EOF, "end of file", self.ligneCourant, self.colomneCourant)

  def next(self):
      valeur = self.peek()
      self.indice += 1
      return valeur