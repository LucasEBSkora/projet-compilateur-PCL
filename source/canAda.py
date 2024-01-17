from sys import argv
from lexeur import Lexeur
from analyseurExpr import AnalyseurExpr
from analyseurInstr import AnalyseurInstr
from analyseurFichier import AnalyseurFichier
from ExceptionLexique import ExceptionLexique
from ExceptionSyntatique import ExceptionSyntatique
from graph import *
from anytree import RenderTree
from graphviz import render
from subprocess import run
from anytree.exporter import UniqueDotExporter
import os 


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

except ExceptionSyntatique as e:
  print(str(e))
  exit(-1)

arbre_anytree = build_anytree(AST)
# print(AST)
print(RenderTree(arbre_anytree))

UniqueDotExporter(arbre_anytree).to_picture("arbre_syntaxique.png")