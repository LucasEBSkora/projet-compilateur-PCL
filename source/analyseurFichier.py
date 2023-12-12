import noeud
from TypeToken import typeToken
#parser fichier
class AnalyseurFichier:
    
    def __init__(self, analyseurLexique,analyseurInstr, analyseurExpr):
        self.lexeur = analyseurLexique
        self.analyseurInstr = analyseurInstr
        self.analyseurExpr = analyseurExpr

    def fichier(self):
        tokens = [typeToken.WITH, typeToken.ADA, typeToken.SEMICOLON, typeToken.USE, typeToken.ADA, typeToken.SEMICOLON, typeToken.PROCEDURE]
        #check if we have the begining of the code "with Ada.Text...."
        for token in tokens:
            self.check_token(token)
        identificateur = self.check_token(typeToken.IDENTIFICATEUR)
        self.check_token(typeToken.IS)
        decls = []
        while self.lexeur.peek().type != typeToken.BEGIN:
            decls.append(self.decl())
    
        self.check_token(typeToken.BEGIN)
        instrs = []
        while self.lexeur.peek().type != typeToken.END:
            instrs.append(self.analyseurInstr.instr())
        
        self.check_token(typeToken.END)
        if self.lexeur.peek().type == typeToken.IDENTIFICATEUR:
            if identificateur != self.lexeur.peek().value:
                return None
            self.lexeur.next()
        self.check_token(typeToken.SEMICOLON)
        if self.lexeur.peek().type != typeToken.EOF:
            return None
           
        return noeud.Procedure(identificateur,NULL,instr,decl)
    
    def decl(self):
         match self.lexeur.peek().type:
            case typeToken.TYPE:
                return self._type()
            case typeToken.IDENTIFICATEUR:
                return self.var()
            case typeToken.PROCEDURE:
                return self.procedure()
            case typeToken.FUNCTION:
                return self.function()
            case _:
                return None
    
    def champs(self):
        idents = []
        typage = None
        idents += [self.check_token(typeToken.IDENTIFICATEUR)]
        while self.lexeur.peek().type == typeToken.COMMA:
            self.check_token(typeToken.COMMA)
            idents.append(self.check_token(typeToken.IDENTIFICATEUR))
        self.check_token(typeToken.COLON)
        typage = self.typage()
        return noeud.Champs(idents,typage)
    
    def _type(self):
        self.check_token(typeToken.TYPE)
        identificateur = self.check_token(typeToken.IDENTIFICATEUR)
        if self.lexeur.peek().type == typeToken.SEMICOLON:
            self.check_token(typeToken.SEMICOLON)
            return noeud.Type(identificateur)
        self.check_token(typeToken.IS)
        if self.lexeur.peek().type == typeToken.ACCESS:
            self.check_token(typeToken.ACCESS)
            identificateur_access = self.check_token(typeToken.IDENTIFICATEUR)
            self.check_token(typeToken.SEMICOLON)
            return noeud.Access(identificateur, identificateur_access)
        elif self.lexeur.peek().type == typeToken.RECORD:
            self.check_token(typeToken.RECORD)
            champs = self.champs()
            self.check_token(typeToken.END)
            self.check_token(typeToken.RECORD)
            self.check_token(typeToken.SEMICOLON)
            return noeud.Record(identificateur, champs)
        return None

    
    def params(self):
        params = []
        self.check_token(typeToken.PARENG)
        params.append(self.param())
        while self.lexeur.peek().type == typeToken.SEMICOLON:
            self.check_token(typeToken.SEMICOLON)
            params.extend(self.param())
        self.check_token(typeToken.PAREND)
        return params
    
    def param(self):
        idents = []
        typage = None
        idents += [self.check_token(typeToken.IDENTIFICATEUR)]
        while self.lexeur.peek().type == typeToken.COMMA:
            self.check_token(typeToken.COMMA)
            idents.append(self.check_token(typeToken.IDENTIFICATEUR))
        self.check_token(typeToken.COLON)
        mode = self.mode()
        _mode = ""
        if mode :
            _mode = "in"
        else:
            _mode = "in out"
        typage = self.typage()
        params = []
        for ident in idents:
            params.append(noeud.Param(ident,_mode,typage))
        return params
    
    def mode(self):
        isIn = True
        self.check_token(typeToken.IN)
        if self.lexeur.peek() == typeToken.OUT:
            self.check_token(typeToken.OUT)
            isIn = False
        return isIn
  
    def var(self):
        idents = []
        typage = None
        idents += [self.check_token(typeToken.IDENTIFICATEUR)]
        while self.lexeur.peek().type == typeToken.COMMA:
            self.check_token(typeToken.COMMA)
            idents.append(self.check_token(typeToken.IDENTIFICATEUR))
        self.check_token(typeToken.COLON)
        typage = self.typage()
        if self.lexeur.peek().type == typeToken.AFFECT:
            self.check_token(typeToken.AFFECT)
            expr = self.analyseurExpr.expr()
        self.check_token(typeToken.SEMICOLON)
        return noeud.Var(idents,typage,expr)

    def typage(self):
        if self.lexeur.peek().type == typeToken.ACCESS:
            self.check_token(typeToken.ACCESS)
            identificateur_access = self.check_token(typeToken.IDENTIFICATEUR)
            typage = noeud.Type(True, identificateur_access)
        else :
            identificateur_type = self.check_token(typeToken.IDENTIFICATEUR)
            typage = noeud.Type(False,identificateur_type)
        return typage
        
    def procedure(self):
        identificateur = None
     
        self.check_token(typeToken.PROCEDURE)
        identificateur = self.check_token(typeToken.IDENTIFICATEUR)
        params = self.params() 
        self.check_token(typeToken.IS)
        decl = self.decl()
        self.check_token(typeToken.BEGIN)
        instr = self.analyseurInstr.instr()
        self.check_token(typeToken.END)
        if self.lexeur.peek().type == typeToken.IDENTIFICATEUR:
            if identificateur != self.lexeur.peek().value: 
                return None
            self.lexeur.next()
        self.check_token(typeToken.SEMICOLON)
        return noeud.Procedure(identificateur,params,instr,decl)
    
    def function(self):
        identificateur = None
     
        self.check_token(typeToken.FUNCTION)
        identificateur = self.check_token(typeToken.IDENTIFICATEUR)
        params = self.params() 
        self.check_token(typeToken.RETURN)
        typage = self.typage()
        self.check_token(typeToken.IS)
        decl = []
        while self.lexeur.peek().type != typeToken.BEGIN:
            decl = self.decl()
        self.check_token(typeToken.BEGIN)
        instr = self.analyseurInstr.instr()
        self.check_token(typeToken.END)
        if self.lexeur.peek().type == typeToken.IDENTIFICATEUR:
            if identificateur != self.lexeur.peek().value: 
                return None
        self.lexeur.next()
        self.check_token(typeToken.SEMICOLON)
        return noeud.Function(identificateur,params,typage,instr,decl)
    
        


  #check if the token is correct and return the value of the valid token   
    def check_token(self, type, required = True):
        value = None
        if self.lexeur.peek().type != type and required:
            raise ExceptionSyntatique(f"expected {type} instead of {self.lexeur.peek().value}", id.ligne, id.colomne)
          
        else:
            value = self.lexeur.peek().value
            self.lexeur.next()
        return value
