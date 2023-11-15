from sys import argv
from lexer import lexer
from analyseurExpr import AnalyseurExpr
from analyseurFichier import AnalyseurFichier


analyseurExpr = AnalyseurExpr(None)
AnalyseurFichier = AnalyseurFichier(None, analyseurExpr)
print(argv)

if len(argv) == 1:
  print("misssing source file!")
  exit(1)

try:
  source = open(argv[1])
except ():
  print(f"source file {argv[1]} not found")
  exit(1)

source_string = source.read()
# print (source_string)

tokens, _ = lexer(source_string)

print(tokens)