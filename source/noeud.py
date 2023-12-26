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
    str = f"appel({self.nom}, "
    str += _list_as_string(self.params)
    str += ')'
    return str

class Var:
  def __init__(self,ident,type,expr):
    self.type = type
    self.ident = ident
    self.expr = expr
  
  def __str__(self):
    str = f'Var({self.type}, {self.ident}'
    if self.expr is not None:
      str += ', {self.expr}'
    return str + ')'
  
class Procedure:
  def __init__(self,ident,params,instr,decl):
    self.ident = ident
    self.params = params
    self.instr = instr
    self.decl = decl
  
  def __str__(self):
    str = f"procedure({self.ident}, ["
    str += _list_as_string(self.params)
    str += "], ["
    
    str += _list_as_string(self.decl)
    str += "], ["

    str += _list_as_string(self.instr)
    return str + "])"

class Function:
  def __init__(self,ident,params,type,instrs,decls):
    self.ident = ident
    self.params = params
    self.type = type
    self.instrs = instrs
    self.decls = decls

  def __str__(self):
    str = f"function({self.ident}, ["
    str += _list_as_string(self.params)
    str += f"], {self.type}, ["
    
    str += _list_as_string(self.decls)
    str += "], ["

    str += _list_as_string(self.instrs)
    return str + "])"
  
class Record:
  def __init__(self,ident,champs):
    self.ident = ident
    self.champs = champs

  def __str__(self):
    str = f"Record({self.ident}, ["
    str += _list_as_string(self.champs)
    str += f"])"
    return str    

class Access:
  def __init__(self,ident1,ident2):
    self.ident1 = ident1
    self.ident2 = ident2

  def __str__(self):
    return f'Access({self.ident1}, {self.ident2})'

class Type:
  def __init__(self,isAccess,ident):
    self.ident = ident
    self.isAccess = isAccess
  
  def __str__(self):
    if self.isAccess:
      return f'accessType({self.ident})'
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
    return f'Param({self.ident}, {self.mode},{self.type})'
  
class Return:
  def __init__(self, expr):
    self.expr = expr
  
  def __str__(self):
    return f"return({self.expr})"

class Block:
  def __init__(self, instr):
    self.instr = instr
  def __str__(self):
    str = '('
    str += _list_as_string(self.instr)
    str += ')'
    return str

class WhileLoop:
  def __init__(self,expr, instrList):
    self.expr = expr
    self.instrList = instrList
  def __str__(self):
    str = f"while({self.expr}, ["
    str += _list_as_string(self.instrList)
    str += "])"
    return str
  
class ForLoop:
  def __init__(self, ident, isReverse, expr1, expr2, instrList):
    self.ident = ident
    self.isReverse = isReverse
    self.expr1 = expr1
    self.expr2 = expr2
    self.instrList = instrList
  def __str__(self):
    str = f"for({self.ident}, "

    if self.isReverse:
      str += "reverse, "
    
    str += f"{self.expr1}, {self.expr2}, ["
    str += _list_as_string(self.instrList)
    str += "])"
    return str

class If:
  def __init__(self, expr1, instrList1, listTuple, instrList3):
    self.expr1 = expr1
    self.instrList1 = instrList1
    self.listTuple = listTuple
    self.instrList3 = instrList3
  def __str__(self):
    str = f"if({self.expr1}, ["
    _list_as_string(self.instrList1)
    str += "]"
    for elseif in self.listTuple:
      str += f", elseif({elseif[0]}, ["
      str += _list_as_string(elseif[1])
      str += "])"
    if self.instrList3:
      str += ", else(["
      str += _list_as_string(self.instrList3)
      str += "])"
    return str + ')'

class Affectation:
  def __init__(self, acess, expr):
    self.acess = acess
    self.expr = expr
  def __str__(self):
    return f":=({self.acess}, {self.expr})"
    

def _list_as_string(list):
  str = ""
  if list:
    str += f"{list[0]}"
    for i in list[1:]:
      str += f", {i}"
  return str