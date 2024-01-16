from sys import argv
from lexeur import Lexeur
from analyseurExpr import AnalyseurExpr
from analyseurInstr import AnalyseurInstr
from analyseurFichier import AnalyseurFichier
from ExceptionLexique import ExceptionLexique
from ExceptionSyntatique import ExceptionSyntatique
from graph import *

if len(argv) == 1:
  print("missing source file!")
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

analyseurExpr = AnalyseurExpr(lexeur)
analyseurInstr = AnalyseurInstr(lexeur, analyseurExpr)
AnalyseurFichier = AnalyseurFichier(lexeur, analyseurInstr, analyseurExpr)
try:
  AST = AnalyseurFichier.fichier()
  # Construire l'arbre syntaxique en utilisant la fonction build_anytree
  arbre_anytree = build_anytree(AST)

# Affichage de l'arbre avec des traits
  for pre, fill, node in RenderTree(arbre_anytree):
    print(f"{pre}{node.name}")
  print(AST)

except ExceptionSyntatique as e:
  print(str(e))
  exit(-1)
