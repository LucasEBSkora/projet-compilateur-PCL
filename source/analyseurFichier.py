import noeud
from TypeToken import typeToken
from ExceptionSyntatique import ExceptionSyntatique

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
    
       
        instrs = self.analyseurInstr.block(identificateur)

        if self.lexeur.peek().type != typeToken.EOF:
            raise ExceptionSyntatique("Erreur de syntaxe dans la déclaration du fichier", self.lexeur.peek().ligne, self.lexeur.peek().colonne)

           
        return noeud.Procedure(identificateur,[],instrs,decls)
    
    def decl(self):
       
        token_type = self.lexeur.peek().type

        if token_type == typeToken.TYPE:
            return self._type()
        elif token_type == typeToken.IDENTIFICATEUR:
            return self.var()
        elif token_type == typeToken.PROCEDURE:
            return self.procedure()
        elif token_type == typeToken.FUNCTION:
            return self.function()
        else:
            raise ExceptionSyntatique("Erreur de syntaxe dans la déclaration ", self.lexeur.peek().ligne, self.lexeur.peek().colonne)

    
    def champs(self):
        idents = []
        typage = None
        idents += [self.check_token(typeToken.IDENTIFICATEUR)]
        while self.lexeur.peek().type == typeToken.COMMA:
            self.check_token(typeToken.COMMA)
            idents.append(self.check_token(typeToken.IDENTIFICATEUR))
        self.check_token(typeToken.COLON)
        typage = self.typage()
        self.check_token(typeToken.SEMICOLON)
        return noeud.Champs(idents,typage)
    
    def _type(self):
        self.check_token(typeToken.TYPE)
        identificateur = self.check_token(typeToken.IDENTIFICATEUR)
        if self.lexeur.peek().type == typeToken.SEMICOLON:
            self.check_token(typeToken.SEMICOLON)
            return noeud.Type(False, identificateur)
        self.check_token(typeToken.IS)
        if self.lexeur.peek().type == typeToken.ACCESS:
            self.check_token(typeToken.ACCESS)
            identificateur_access = self.check_token(typeToken.IDENTIFICATEUR)
            self.check_token(typeToken.SEMICOLON)
            return noeud.AccessType(identificateur, identificateur_access)
        elif self.lexeur.peek().type == typeToken.RECORD:
            self.check_token(typeToken.RECORD)
            champs = [self.champs()]
            while self.lexeur.peek().type == typeToken.IDENTIFICATEUR:
                champs.append(self.champs())
            self.check_token(typeToken.END)
            self.check_token(typeToken.RECORD)
            self.check_token(typeToken.SEMICOLON)
            return noeud.Record(identificateur, champs)
        
        raise ExceptionSyntatique("Erreur de syntaxe dans la déclaration de type", self.lexeur.peek().ligne, self.lexeur.peek().colonne)


    
    def params(self):
        params = []
        self.check_token(typeToken.PARENG)
        params.extend(self.param())
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
        if self.lexeur.peek().type == typeToken.IN:
            self.check_token(typeToken.IN)
            if self.lexeur.peek().type == typeToken.OUT:
                self.check_token(typeToken.OUT)
                isIn = False
        return isIn
  
    def var(self):
        idents = []
        vars = []
        typage = None
        idents += [self.check_token(typeToken.IDENTIFICATEUR)]
        while self.lexeur.peek().type == typeToken.COMMA:
            self.check_token(typeToken.COMMA)
            idents.append(self.check_token(typeToken.IDENTIFICATEUR))
        self.check_token(typeToken.COLON)
        typage = self.typage()
        expr = None
        if self.lexeur.peek().type == typeToken.AFFECT:
            self.check_token(typeToken.AFFECT)
            expr = self.analyseurExpr.expr()
        self.check_token(typeToken.SEMICOLON)
        for ident in idents:
            vars.append(noeud.Var(ident,typage,expr))
        return vars

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
        if self.lexeur.peek().type == typeToken.PARENG:
            params = self.params() 
        else:
            params = []
        self.check_token(typeToken.IS)
        decl = []
       
        while self.lexeur.peek().type != typeToken.BEGIN:
            decl.append(self.decl())

        instrs = self.analyseurInstr.block(identificateur)
        return noeud.Procedure(identificateur,params,instrs,decl)
    
    def function(self):
        identificateur = None
     
        self.check_token(typeToken.FUNCTION)
        identificateur = self.check_token(typeToken.IDENTIFICATEUR)
        if self.lexeur.peek().type == typeToken.PARENG:
            params = self.params() 
        else:
            params = []
        self.check_token(typeToken.RETURN)
        typage = self.typage()
        self.check_token(typeToken.IS)
        decls = []
        while self.lexeur.peek().type != typeToken.BEGIN:
            decls.append(self.decl())
       
     
      
        instrs = self.analyseurInstr.block(identificateur)
        return noeud.Function(identificateur,params,typage,instrs,decls)
    
        


  #check if the token is correct and return the value of the valid token   
    def check_token(self, type, required = True):
        value = None
        if self.lexeur.peek().type != type and required:
            raise ExceptionSyntatique(f"expected {type} instead of {self.lexeur.peek().value}", self.lexeur.peek().ligne, self.lexeur.peek().colomne)
          
        else:
            value = self.lexeur.peek().value
            self.lexeur.next()
        return value
