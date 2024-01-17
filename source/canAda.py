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
from anytree.exporter import DotExporter
import os 


# os.environ["GRAPHIZ_DOT"] = '/Users/Diane/opt/anaconda3/lib/python3.9/site-packages/graphviz/dot.py'
#mettez le chemin de votre executable dot.exec (download la librairie graphviz sur vos pc svp)
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

   
  arbre_anytree = build_anytree(AST)
  for pre, fill, node in RenderTree(arbre_anytree):
        print(f"{pre}{node.name}")


  dot_data = DotExporter(arbre_anytree)
  dot_data.to_dotfile("arbre_syntaxique.dot")

  render('dot', 'png', 'arbre_syntaxique.dot')


except ExceptionSyntatique as e:
  print(str(e))
  exit(-1)
