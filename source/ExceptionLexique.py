
class ExceptionLexique(BaseException):
  def __init__(self, message, ligne, colomne):
    self.message = message
    self.ligne = ligne
    self.colomne = colomne
  
  def __str__(self):
    return f"Erreur lexique {self.message} ({self.ligne}:{self.colomne})"