from sys import argv
from lexer import Tokens
from analyseurExpr import AnalyseurExpr
from analyseurInstr import AnalyseurInstr
from analyseurFichier import AnalyseurFichier

if len(argv) == 1:
  print("misssing source file!")
  exit(1)

try:
  source = open(argv[1])
except ():
  print(f"source file {argv[1]} not found")
  exit(1)

source_string = source.read()

tokens = Tokens()
tokens.lexer(source_string)

analyseurExpr = AnalyseurExpr(tokens)
AnalyseurInstr = AnalyseurInstr(tokens, analyseurExpr)
AnalyseurFichier = AnalyseurFichier(tokens, AnalyseurInstr, analyseurExpr)

AST = AnalyseurFichier.fichier()

print(AST)
