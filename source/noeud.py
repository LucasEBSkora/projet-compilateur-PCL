class Fichier:
  def __init__(self,ident,decl,instr):
    self.ident = ident
    self.decl = decl
    self.instr = instr

class Binaire:
  def __init__(self, gauche, operateur, droite):
    self.gauche = gauche
    self.operateur = operateur
    self.droite = droite

class Unaire:
  def __init__(self, operateur, operande):
    self.operateur = operateur
    self.operande = operande


class Var:
  def __init__(self,ident,type,expr):
    self.type = type
    self.ident = ident
    self.expr = expr
class Procedure:
  def __init__(self,ident,params,instr,decl):
    self.ident = ident
    self.params = params
    self.instr = instr
    self.decl = decl
class Function:
  def __init__(self,ident,params,type,instr,decl):
    self.ident = ident
    self.params = params
    self.type = type
    self.instr = instr
    self.decl = decl 
class Record:
  def __init__(self,ident,champs):
    self.ident = ident
    self.champs = champs
class Access:
  def __init__(self,ident1,ident2):
    self.ident1 = ident1
    self.ident2 = ident2

class Type:
  def __init__(self,isAccess,ident):
    self.ident = ident
    self.isAccess = isAccess

class Champs: 
  def __init__(self,ident,type):
    self.ident = ident
    self.type = type

class Mode:
  def __init__(self,isIn):
    self.isIn = isIn

class Param:
  def __init__(self,ident,mode,type):
    self.ident = ident
    self.mode = mode
    self.type = type

