from anytree import Node, RenderTree
from noeud import *

class Binaire:
    def __init__(self, gauche, operateur, droite):
        self.gauche = gauche
        self.operateur = operateur
        self.droite = droite

    def __str__(self):
        return f"{self.operateur}({self.gauche}, {self.droite})"

class Unaire:
    def __init__(self, operateur, operande):
        self.operateur = operateur
        self.operande = operande

    def __str__(self):
        return f"{self.operateur}({self.operande})"

# ... Ajoutez des nœuds pour d'autres classes de nœuds

def build_anytree(node):
    root = Node(str(node))

    if isinstance(node, Binaire):
        root.children = [build_anytree(node.gauche), build_anytree(node.droite)]
    elif isinstance(node, Unaire):
        root.children = [build_anytree(node.operande)]
    # Ajoutez des conditions pour d'autres classes de nœuds

    return root

# Utilisation avec un exemple de nœud
exemple_noeud = Binaire(Ident("a"), "+", Literal(5))
arbre_anytree = build_anytree(exemple_noeud)

# Affichage de l'arbre avec des traits
for pre, fill, node in RenderTree(arbre_anytree):
    print(f"{pre}{node.name}")

