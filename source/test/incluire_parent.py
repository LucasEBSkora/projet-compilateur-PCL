import sys
import os

#petit hack pour incluire les fichiers dans le repertoire pere
def incluire_parent():
  current = os.path.dirname(os.path.realpath(__file__))
  parent = os.path.dirname(current)
  sys.path.insert(0, parent)
