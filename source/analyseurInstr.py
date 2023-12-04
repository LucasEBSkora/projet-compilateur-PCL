import noeud
from TypeToken import typeToken
from analyseurExpr import AnalyseurExpr

#parser instr

class AnalyseurInstr:

    def __init__(self, analyseurLexique, analyseurExpr):
        self.lexeur = analyseurLexique
        self.analyseurExpr = analyseurExpr

    
    def instr(self):
        
        #return <expr>? ;
        if (self.prochainToken(typeToken.RETURN)):
            self.lexeur.next()
            if (self.prochainToken(typeToken.SEMICOLON)):
                self.verification(typeToken.SEMICOLON)
                return noeud.Return(None)
            acces = self.analyseurExpr.expr()
            self.verification(typeToken.SEMICOLON)
            return noeud.Return(acces)
        
        #begin <instr>+ end;

        if (self.prochainToken(typeToken.BEGIN)):
            instrList = []
            self.lexeur.next()
            instrList = self.repetitionInstr(typeToken.END)
            self.verification(typeToken.END)
            self.verification(typeToken.SEMICOLON)
            return noeud.Begin(instrList)
            
        # if <expr> then <instr>+ (elsif <expr> then <instr>+)*
        #        (else <instr>+)? end if ;

        if (self.prochainToken(typeToken.IF)):
            instrList2 = []
            instrList3 = []
            instrList4 = []
            listTuples = []
            self.lexeur.next()
            x = self.analyseurExpr.expr()
            self.verification(typeToken.THEN)
            instrList2 = self.repetitionInstr(typeToken.ELSEIF, typeToken.ELSE, typeToken.END)
            if(self.prochainToken(typeToken.ELSEIF)):
                while(self.prochainToken(typeToken.ELSEIF)):
                    instrList3 = []
                    self.lexeur.next()
                    y = self.analyseurExpr.expr()
                    self.verification(typeToken.THEN)
                    instrList3 = self.repetitionInstr(typeToken.ELSE, typeToken.END, typeToken.ELSEIF)
                    listTuples.append((y, instrList3))
            else: y = None
            if(self.prochainToken(typeToken.ELSE)):
                self.lexeur.next()
                instrList4 = self.repetitionInstr(typeToken.END)
            if(self.prochainToken(typeToken.END)):
                self.verification(typeToken.END)
                self.verification(typeToken.IF)
                self.verification(typeToken.SEMICOLON)
            return noeud.If(x, instrList2, listTuples, instrList4)

        # | for <ident> in reverse? <expr> .. <expr>
        #   loop <instr>+ end loop ;
        if(self.prochainToken(typeToken.FOR)):
            instrList5 = []
            self.lexeur.next()
            if(self.prochainToken(typeToken.IDENTIFICATEUR)):
                ident = self.lexeur.peek().value
            self.verification(typeToken.IDENTIFICATEUR)
            self.verification(typeToken.IN)
            if(self.prochainToken(typeToken.REVERSE)):
                isReverse = True
                self.verification(typeToken.REVERSE)
            else: isReverse = False
            x = self.analyseurExpr.expr()
            self.verification(typeToken.DEUXPOINTS)
            y = self.analyseurExpr.expr()
            self.verification(typeToken.LOOP)
            instrList5 = self.repetitionInstr(typeToken.END)
            self.verification(typeToken.END)
            self.verification(typeToken.LOOP)
            self.verification(typeToken.SEMICOLON)
            return noeud.ForLoop(ident, isReverse, x, y, instrList5)


        # while <expr> loop <instr>+ end loop ;
        if(self.prochainToken(typeToken.WHILE)):
            instrList6 = []
            self.lexeur.next()
            g = self.analyseurExpr.expr()
            self.verification(typeToken.LOOP)
            instrList6 = self.repetitionInstr(typeToken.END)
            self.verification(typeToken.END)
            self.verification(typeToken.LOOP)
            self.verification(typeToken.SEMICOLON)
            return noeud.WhileLoop(g, instrList6)
        


        k = self.analyseurExpr.acces()

        # <accès> := <expr>;
        if(k is noeud.Binaire and k.operateur == "."):
            self.verification(typeToken.AFFECT)
            p = self.analyseurExpr.expr()
            self.verification(typeToken.SEMICOLON)
            return noeud.Affectation(k,p)
        elif(k is noeud.Appel): # <appel> ;
            self.verification(typeToken.SEMICOLON)
            return k
        elif(k is noeud.Ident):
            if(self.prochainToken(typeToken.SEMICOLON)): # ident ;
                return k
            else:  # ident := <expr>;
                self.verification(typeToken.AFFECT)
                q = self.analyseurExpr.expr()
                self.verification(typeToken.SEMICOLON)
                return  noeud.Affectation(k ,q)

    def repetitionInstr(self, *args):
        list = []
        while (self.lexeur.peek().type not in args):
            list.append(self.instr())
        return list
    

    def verification(self, type):
        id = self.lexeur.peek().type 
        if(id == type):
            self.lexeur.next()
        else:
            print(f"Error: expected token type {type} but got {id}")
            exit(1)

    def prochainToken(self, type):
        return self.lexeur.peek().type == type
    
