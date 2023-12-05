
class ExceptionSyntatique(BaseException):
  def __init__(self, message, ligne, colomne):
    self.message = message
    self.ligne = ligne
    self.colomne = colomne
  
  def __str__(self):
    return f"Syntatic error at ({self.ligne}:{self.colomne}:{self.message})"