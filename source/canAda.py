from sys import argv
from lexeur import Lexeur
from analyseurExpr import AnalyseurExpr
from analyseurInstr import AnalyseurInstr
from analyseurFichier import AnalyseurFichier
from ExceptionLexique import ExceptionLexique
from ExceptionSyntatique import ExceptionSyntatique

if len(argv) == 1:
  print("misssing source file!")
  exit(1)

try:
  source = open(argv[1])
except ():
  print(f"source file {argv[1]} not found")
  exit(1)

source_string = source.read()
try:
  lexeur = Lexeur(source_string)
except ExceptionLexique as e:
  print(str(e))
  exit(-1)

# for token in lexeur.tokens:
#   print(token)

analyseurExpr = AnalyseurExpr(lexeur)
analyseurInstr = AnalyseurInstr(lexeur, analyseurExpr)
AnalyseurFichier = AnalyseurFichier(lexeur, analyseurInstr, analyseurExpr)
try:
  AST = AnalyseurFichier.fichier()
  print(AST)
except ExceptionSyntatique as e:
  print(str(e))
  exit(-1)
