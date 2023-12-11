from sys import argv
from lexeur import Lexeur
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

lexeur = Lexeur(source_string)

analyseurExpr = AnalyseurExpr(lexeur)
AnalyseurInstr = AnalyseurInstr(lexeur, analyseurExpr)
AnalyseurFichier = AnalyseurFichier(lexeur, AnalyseurInstr, analyseurExpr)

AST = AnalyseurFichier.fichier()

print(AST)
