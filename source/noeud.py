class Fichier:
  def __init__(self,idents,decls,instrs):
    self.idents = idents
    self.decls = decls
    self.instrs = instrs

  def __str__(self):
    str = f"procedure({self.idents}, ["
    for decl in self.decls:
      str += f", {decl}"
    str += "], ["
    for instr in self.instrs:
      str += f", {instr}"
    return str + "])"

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
    str = f"appel({self.nom}"
    for param in self.params:
      str += f", {param}"
    return str + ")"
    

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
    str = f"procedure({self.idents}, ["
    for param in self.params:
      str += f", {param}"
    str += "], ["
    
    for decl in self.decls:
      str += f", {decl}"
    str += "], ["

    for instr in self.instrs:
      str += f", {instr}"
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
    for param in self.params:
      str += f", {param}"
    str += f"], {self.type}, ["
    
    for decl in self.decls:
      str += f", {decl}"
    str += "], ["

    for instr in self.instrs:
      str += f", {instr}"
    return str + "])"
  
class Record:
  def __init__(self,ident,champs):
    self.ident = ident
    self.champs = champs

  def __str__(self):
    str = f"Record({self.ident}, ["
    for champ in self.champs:
      str += f", {champ}"
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
    return f"({self.instr})"

class WhileLoop:
  def __init__(self,expr, instrList):
    self.expr = expr
    self.instrList = instrList
  def __str__(self):
    return f"while({self.expr}, {self.instrList})"
  
class ForLoop:
  def __init__(self, ident, isReverse, expr1, expr2, instrList):
    self.ident = ident
    self.isReverse = isReverse
    self.expr1 = expr1
    self.expr2 = expr2
    self.instrList = instrList
  def __str__(self):
    if self.isReverse:
      return f"for({self.ident}, reverse, {self.expr1}, {self.expr2}, {self.instrList})"
    return f"for({self.ident}, {self.expr1}, {self.expr2}, {self.instrList})"

class If:
  def __init__(self, expr, instrNoeud, elseNoeud):
    self.expr = expr
    self.instrNoeud = instrNoeud
    self.elseNoeud = elseNoeud
  """
  def __str__(self):
    str = f"if({self.expr1}, ["
    for instr in self.instrList1:
      str += f"{instr},"
    str += "]"
    for elseif in self.listTuple:
      str += ", elseif({elseif[0]}, ["
      for instr in elseif[1]:
        str += f"{instr},"
      str += "])"
    if self.instrList3:
      str += ", else(["
      for instr in self.instrList3:
        str += f"{instr},"
      str += "])"
    return str + ')'
  """

class Affectation:
  def __init__(self, acess, expr):
    self.acess = acess
    self.expr = expr
  def __str__(self):
    return f":=({self.acess}, {self.expr})"
    