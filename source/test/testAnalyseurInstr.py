import unittest

from incluire_parent import incluire_parent
incluire_parent()

from fauxLexer import FauxLexer
from analyseurExpr import AnalyseurExpr
from analyseurInstr import AnalyseurInstr
from TypeToken import typeToken
import noeud
from ExceptionSyntatique import ExceptionSyntatique


class TestAnalyseurInstr(unittest.TestCase):
    def test_prochain_token(self):
        lexer = FauxLexer.builder([(typeToken.RETURN, "return"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        instr = AnalyseurInstr(lexer, expr)
        self.assertEqual(True, instr.prochainToken(typeToken.RETURN))


    def test_verification(self):
        lexer = FauxLexer.builder([(typeToken.RETURN, "return"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        instr = AnalyseurInstr(lexer, expr)
        instr.verification(typeToken.RETURN)
        self.assertIs(typeToken.SEMICOLON ,lexer.peek().type)


    def test_repetitionInstr(self):
        lexer = FauxLexer.builder([(typeToken.RETURN, "return"), (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"),(typeToken.ENTIER, "10") ,
                                   (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"),(typeToken.ENTIER, "5") ,(typeToken.SEMICOLON, ";"), 
                                   (typeToken.END, "end")])
        expr = AnalyseurExpr(lexer)
        instr = AnalyseurInstr(lexer, expr)
        lista = instr.repetitionInstr(typeToken.END)
        self.assertEqual(3, len(lista))
        self.assertEqual(None, lista[0].expr)
        self.assertEqual("10", lista[1].expr.literal)
        self.assertEqual("5", lista[2].expr.literal)


    def test_return_without_expr(self):
        lexer = FauxLexer.builder([(typeToken.RETURN, "return"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.Return)
        self.assertEqual(None, result.expr)


    def test_return_expr(self):
        lexer = FauxLexer.builder([(typeToken.RETURN, "return"),(typeToken.ENTIER, "5") ,(typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.Return)
        self.assertEqual("5", result.expr.literal)


    def test_begin_instr_end(self):
        lexer = FauxLexer.builder([(typeToken.BEGIN, "begin"),(typeToken.RETURN, "return"),(typeToken.ENTIER, "5") ,(typeToken.SEMICOLON, ";"), 
                                   (typeToken.END, "end"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.Block)
        self.assertEqual(1, len(result.instr))
        self.assertEqual("5", result.instr[0].expr.literal)


    def test_begin_with_identificateur(self):
        lexer = FauxLexer.builder([(typeToken.BEGIN, "begin"),(typeToken.RETURN, "return"),(typeToken.ENTIER, "5") ,(typeToken.SEMICOLON, ";"), 
                                   (typeToken.END, "end"), (typeToken.IDENTIFICATEUR, "x"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        try:
            analyseur.block("y")
        except ExceptionSyntatique as e:
            self.assertEqual(f"Expected the second identificateur to be the same as the first one, but they are differents. First Identificateur: y. Second Identificateur: x", e.message)
            return
        self.assertTrue(False)


    def test_while(self):
        lexer = FauxLexer.builder([(typeToken.WHILE, "while"),(typeToken.IDENTIFICATEUR, "a") ,(typeToken.LOOP, "loop"), (typeToken.RETURN, "return"),
                                   (typeToken.ENTIER, "5") ,(typeToken.SEMICOLON, ";"), (typeToken.END, "end"), (typeToken.LOOP, "loop"), (typeToken.SEMICOLON, ";") ])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.WhileLoop)
        self.assertEqual(1, len(result.instrList))
        self.assertEqual("5", result.instrList[0].expr.literal)
        self.assertEqual("a", result.expr.nom)


    def test_for_without_reverse(self):
        lexer = FauxLexer.builder([(typeToken.FOR, "for"),(typeToken.IDENTIFICATEUR, "b"), (typeToken.IN, "in"), (typeToken.IDENTIFICATEUR, "a"),
                                   (typeToken.DEUXPOINTS, ".."), (typeToken.IDENTIFICATEUR, "c"), (typeToken.LOOP, "loop"), (typeToken.RETURN, "return"),
                                   (typeToken.ENTIER, "5") ,(typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), (typeToken.ENTIER, "7") ,
                                   (typeToken.SEMICOLON, ";"), (typeToken.END, "end"), (typeToken.LOOP, "loop"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.ForLoop)
        self.assertEqual("b", result.ident)
        self.assertFalse(result.isReverse)
        self.assertEqual("a", result.expr1.nom)
        self.assertEqual("c", result.expr2.nom)
        self.assertEqual(2, len(result.instrList))
        self.assertEqual("5", result.instrList[0].expr.literal)
        self.assertEqual("7", result.instrList[1].expr.literal)


    def test_for_avec_reverse(self):
        lexer = FauxLexer.builder([(typeToken.FOR, "for"),(typeToken.IDENTIFICATEUR, "b"), (typeToken.IN, "in"), (typeToken.REVERSE, "reverse"), 
                                   (typeToken.IDENTIFICATEUR, "a"), (typeToken.DEUXPOINTS, ".."), (typeToken.IDENTIFICATEUR, "c"), (typeToken.LOOP, "loop"), 
                                   (typeToken.RETURN, "return"), (typeToken.ENTIER, "5") ,(typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), 
                                   (typeToken.ENTIER, "7"), (typeToken.SEMICOLON, ";"), (typeToken.END, "end"), (typeToken.LOOP, "loop"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.ForLoop)
        self.assertEqual("b", result.ident)
        self.assertTrue(result.isReverse)
        self.assertEqual("a", result.expr1.nom)
        self.assertEqual("c", result.expr2.nom)
        self.assertEqual(2, len(result.instrList))
        self.assertEqual("5", result.instrList[0].expr.literal)
        self.assertEqual("7", result.instrList[1].expr.literal)

    
    def test_if_without_elseif_and_else(self):
        lexer = FauxLexer.builder([(typeToken.IF, "if"), (typeToken.ENTIER, "5"), (typeToken.THEN, "then"), (typeToken.RETURN, "return"), 
                                   (typeToken.IDENTIFICATEUR, "a"), (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), (typeToken.IDENTIFICATEUR, "b"), 
                                   (typeToken.SEMICOLON, ";"), (typeToken.END, "end"), (typeToken.IF, "if"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.If)
        self.assertEqual("5" , result.expr.literal)
        self.assertIsInstance(result.instrNoeud, noeud.Block)
        self.assertEqual(2, len(result.instrNoeud.instr))
        self.assertEqual("a", result.instrNoeud.instr[0].expr.nom)
        self.assertEqual("b", result.instrNoeud.instr[1].expr.nom)
        self.assertEqual(result.elseNoeud, None)


    def test_if_without_elseif_and_avec_else(self):
        lexer = FauxLexer.builder([(typeToken.IF, "if"), (typeToken.ENTIER, "5"), (typeToken.THEN, "then"), (typeToken.RETURN, "return"), 
                                   (typeToken.IDENTIFICATEUR, "a"), (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), (typeToken.IDENTIFICATEUR, "b"), 
                                   (typeToken.SEMICOLON, ";"), (typeToken.ELSE, "else"), (typeToken.RETURN, "return"), (typeToken.ENTIER, "2"), 
                                   (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), (typeToken.IDENTIFICATEUR, "g"), (typeToken.SEMICOLON, ";"), 
                                   (typeToken.END, "end"), (typeToken.IF, "if"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.If)
        self.assertEqual("5" , result.expr.literal)
        self.assertIsInstance(result.instrNoeud, noeud.Block)
        self.assertEqual(2, len(result.instrNoeud.instr))
        self.assertEqual("a", result.instrNoeud.instr[0].expr.nom)
        self.assertEqual("b", result.instrNoeud.instr[1].expr.nom)
        self.assertIsInstance(result.elseNoeud, noeud.Block)
        self.assertEqual(2, len(result.elseNoeud.instr))
        self.assertEqual("2", result.elseNoeud.instr[0].expr.literal)
        self.assertEqual("g", result.elseNoeud.instr[1].expr.nom)    
    

    def test_if_avec_elseif_and_without_else(self):
        lexer = FauxLexer.builder([(typeToken.IF, "if"), (typeToken.ENTIER, "5"), (typeToken.THEN, "then"), (typeToken.RETURN, "return"), 
                                   (typeToken.IDENTIFICATEUR, "a"), (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), (typeToken.IDENTIFICATEUR, "b"), 
                                   (typeToken.SEMICOLON, ";"), (typeToken.ELSEIF, "elseif"), (typeToken.IDENTIFICATEUR, "c"), (typeToken.THEN, "then"), 
                                   (typeToken.RETURN, "return"), (typeToken.IDENTIFICATEUR, "d"), (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), 
                                   (typeToken.IDENTIFICATEUR, "e"), (typeToken.SEMICOLON, ";"), (typeToken.ELSEIF, "elseif"), (typeToken.IDENTIFICATEUR, "f"), 
                                   (typeToken.THEN, "then"), (typeToken.RETURN, "return"), (typeToken.SEMICOLON, ";"), (typeToken.END, "end"), (typeToken.IF, "if"), 
                                   (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.If)
        self.assertEqual("5" , result.expr.literal)
        self.assertIsInstance(result.instrNoeud, noeud.Block)
        self.assertEqual(2, len(result.instrNoeud.instr))
        self.assertEqual("a", result.instrNoeud.instr[0].expr.nom)
        self.assertEqual("b", result.instrNoeud.instr[1].expr.nom)
        self.assertIsInstance(result.elseNoeud, noeud.If)
        self.assertEqual(2, len(result.elseNoeud.instrNoeud.instr))
        self.assertEqual("c", result.elseNoeud.expr.nom)
        self.assertEqual("d", result.elseNoeud.instrNoeud.instr[0].expr.nom)
        self.assertEqual("e", result.elseNoeud.instrNoeud.instr[1].expr.nom)
        self.assertIsInstance(result.elseNoeud.elseNoeud, noeud.If)
        self.assertEqual(1, len(result.elseNoeud.elseNoeud.instrNoeud.instr))
        self.assertEqual("f", result.elseNoeud.elseNoeud.expr.nom)
        self.assertEqual(None, result.elseNoeud.elseNoeud.instrNoeud.instr[0].expr)


    def test_if_avec_elseif_and_avec_else(self):
        lexer = FauxLexer.builder([(typeToken.IF, "if"), (typeToken.ENTIER, "5"), (typeToken.THEN, "then"), (typeToken.RETURN, "return"), 
                                   (typeToken.IDENTIFICATEUR, "a"), (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), (typeToken.IDENTIFICATEUR, "b"), 
                                   (typeToken.SEMICOLON, ";"), (typeToken.ELSEIF, "elseif"), (typeToken.IDENTIFICATEUR, "c"), (typeToken.THEN, "then"), 
                                   (typeToken.RETURN, "return"), (typeToken.IDENTIFICATEUR, "d"), (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), 
                                   (typeToken.IDENTIFICATEUR, "e"), (typeToken.SEMICOLON, ";"), (typeToken.ELSEIF, "elseif"), (typeToken.IDENTIFICATEUR, "f"), 
                                   (typeToken.THEN, "then"), (typeToken.RETURN, "return"), (typeToken.SEMICOLON, ";"), (typeToken.ELSE, "else"), 
                                   (typeToken.RETURN, "return"), (typeToken.ENTIER, "2"), (typeToken.SEMICOLON, ";"), (typeToken.RETURN, "return"), 
                                   (typeToken.IDENTIFICATEUR, "g"), (typeToken.SEMICOLON, ";"), (typeToken.END, "end"), (typeToken.IF, "if"), 
                                   (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.If)
        self.assertEqual("5" , result.expr.literal)
        self.assertIsInstance(result.instrNoeud, noeud.Block)
        self.assertEqual(2, len(result.instrNoeud.instr))
        self.assertEqual("a", result.instrNoeud.instr[0].expr.nom)
        self.assertEqual("b", result.instrNoeud.instr[1].expr.nom)
        self.assertIsInstance(result.elseNoeud, noeud.If)
        self.assertEqual(2, len(result.elseNoeud.instrNoeud.instr))
        self.assertEqual("c", result.elseNoeud.expr.nom)
        self.assertEqual("d", result.elseNoeud.instrNoeud.instr[0].expr.nom)
        self.assertEqual("e", result.elseNoeud.instrNoeud.instr[1].expr.nom)
        self.assertIsInstance(result.elseNoeud.elseNoeud, noeud.If)
        self.assertEqual(1, len(result.elseNoeud.elseNoeud.instrNoeud.instr))
        self.assertEqual("f", result.elseNoeud.elseNoeud.expr.nom)
        self.assertEqual(None, result.elseNoeud.elseNoeud.instrNoeud.instr[0].expr)
        self.assertIsInstance(result.elseNoeud.elseNoeud.elseNoeud, noeud.Block)
        self.assertEqual(2, len(result.elseNoeud.elseNoeud.elseNoeud.instr))
        self.assertEqual("2", result.elseNoeud.elseNoeud.elseNoeud.instr[0].expr.literal)
        self.assertEqual("g", result.elseNoeud.elseNoeud.elseNoeud.instr[1].expr.nom)


    def test_affectation(self):
        lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "a"),(typeToken.AFFECT, ":="), (typeToken.ENTIER, "5"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.Affectation)


    def test_appel(self):
        lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "a"), (typeToken.PARENG, "("), (typeToken.PAREND, ")"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.Appel)


    def test_ident(self):
        lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "a"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.Ident)


    def test_ident_expr(self):
        lexer = FauxLexer.builder([(typeToken.IDENTIFICATEUR, "a"), (typeToken.AFFECT, ":="), (typeToken.ENTIER, "5"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.Affectation)


if __name__ == '__main__':
    unittest.main()
