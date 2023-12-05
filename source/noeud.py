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

  def __str__(self):
    return f"{self.operateur}({self.gauche}, {self.droite})"

class Unaire:
  def __init__(self, operateur, operande):
    self.operateur = operateur
    self.operande = operande
  def __str__(self):
    return f"{self.operateur}({self.operande})"

class Literal:
  def __init__(self, literal):
    self.literal = literal
  def __str__(self):
    return str(self.literal)

class Ident:
  def __init__(self, nom):
    self.nom = nom
  def __str__(self):
    return str(self.nom)

class New:
  def __init__(self, nom):
    self.nom = nom
  def __str__(self):
    return f"new({self.nom})"

class CharacterApostrofeVal:
  def __init__(self, expr):
    self.expr = expr
  def __str__(self):
    return f"character'val({self.expr})"

class Appel:
  def __init__(self, nom, params):
    self.nom = nom
    self.params = params

  def __str__(self):
    return f"{self.ident}({self.params})"

class Var:
  def __init__(self,ident,type,expr):
    self.type = type
    self.ident = ident
    self.expr = expr
  
  def __str__(self):
    return f'Var({self.type}, {self.ident},{self.expr})'
  
class Procedure:
  def __init__(self,ident,params,instr,decl):
    self.ident = ident
    self.params = params
    self.instr = instr
    self.decl = decl
  
  def __str__(self):
    return f'Procedure({self.ident}, {self.params},{self.instr},{self.decl})'

class Function:
  def __init__(self,ident,params,type,instr,decl):
    self.ident = ident
    self.params = params
    self.type = type
    self.instr = instr
    self.decl = decl 
  
  def __str__(self):
    return f'Function({self.ident}, {self.params},{self.type},{self.instr},{self.decl})'

class Record:
  def __init__(self,ident,champs):
    self.ident = ident
    self.champs = champs

  def __str__(self):
    return f'Record({self.ident}, {self.champs})'

class Access:
  def __init__(self,ident1,ident2):
    self.ident1 = ident1
    self.ident2 = ident2

  def __str__(self):
    return f'Access({self.indent1}, {self.ident2})'

class Type:
  def __init__(self,isAccess,ident):
    self.ident = ident
    self.isAccess = isAccess
  
  def __str__(self):
    return f'Type({self.ident}, {self.isAccess})'

class Champs: 
  def __init__(self,ident,type):
    self.ident = ident
    self.type = type
  
  def __str__(self):
    return f'Champs({self.ident}, {self.type})'

class Mode:
  def __init__(self,isIn):
    self.isIn = isIn

  
  def __str__(self):
    return f'Mode({self.isIn})'

class Param:
  def __init__(self,ident,mode,type):
    self.ident = ident
    self.mode = mode
    self.type = type

  def __str__(self):
    return f'record({self.ident}, {self.mode},{self.type})'
  
class Return:
  def __init__(self, expr):
    self.expr = expr

class Begin:
  def __init__(self, instr):
    self.instr = instr

class Loop:
  def __init__(self, instr):
    self.instr = instr

class WhileLoop:
  def __init__(self,expr, instrList):
    self.expr = expr
    self.instrList = instrList

class ForLoop:
  def __init__(self, ident, isReverse, expr1, expr2, instrList):
    self.ident = ident
    self.isReverse = isReverse
    self.expr1 = expr1
    self.expr2 = expr2
    self.instrList = instrList

class If:
  def __init__(self, expr1, instrList1, listTuple, instrList3):
    self.expr1 = expr1
    self.instrList1 = instrList1
    self.listTuple = listTuple
    self.instrList3 = instrList3

class Affectation:
  def __init__(self, acess, expr):
    self.acess = acess
    self.expr = expr