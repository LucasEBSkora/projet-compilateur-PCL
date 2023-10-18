
class Binaire:
  def __init__(self, gauche, operateur, droite):
    self.gauche = gauche
    self.operateur = operateur
    self.droite = droite

class Unaire:
  def __init__(self, operateur, operande):
    self.operateur = operateur
    self.operande = operande 