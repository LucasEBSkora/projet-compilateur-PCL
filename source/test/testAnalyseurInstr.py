import unittest

from incluire_parent import incluire_parent
incluire_parent()

from fauxLexer import FauxLexer
from analyseurExpr import AnalyseurExpr
from analyseurInstr import AnalyseurInstr
from Token import Token
from TypeToken import typeToken
import noeud

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
        lexer = FauxLexer.builder([(typeToken.BEGIN, "begin"),(typeToken.RETURN, "return"),(typeToken.ENTIER, "5") ,(typeToken.SEMICOLON, ";"), (typeToken.END, "end"), (typeToken.SEMICOLON, ";")])
        expr = AnalyseurExpr(lexer)
        analyseur = AnalyseurInstr(lexer, expr)
        result = analyseur.instr()
        self.assertIsInstance(result, noeud.Begin)
        self.assertEqual(1, len(result.instr))
        self.assertEqual("5", result.instr[0].expr.literal)



if __name__ == '__main__':
    unittest.main()
