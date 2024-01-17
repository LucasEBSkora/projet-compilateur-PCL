from anytree import Node
from graph import *
from noeud import *




def build_anytree(node, parent=None):
    current_node = Node(str(node), parent=parent)

    if isinstance(node, Binaire):
        current_node = Node(node.operateur, parent=parent)
        build_anytree(node.gauche, current_node)
        build_anytree(node.droite, current_node)
    elif isinstance(node, Unaire):
        current_node = Node(node.operateur, parent=parent)
        build_anytree(node.operande, current_node)
    elif isinstance(node, Literal):
        current_node = Node(str(node.literal), parent=parent)
    elif isinstance(node, Ident):
        current_node = Node(node.nom, parent=parent)
    elif isinstance(node, New):
        current_node = Node("new", parent=parent)
        build_anytree(node.nom, current_node)
    elif isinstance(node, CharacterApostrofeVal):
        current_node = Node("Character'val", parent=parent)
        build_anytree(node.expr, current_node)

    elif isinstance(node, Appel):
        current_node = Node(f"appel {node.nom}", parent=parent)
        for param in node.params:
            build_anytree(param, current_node)
    elif isinstance(node, Var):
        current_node = Node(f"var {node.ident}", parent=parent)
        build_anytree(node.type, current_node)
        if node.expr is not None:
            build_anytree(node.expr, current_node)
    elif isinstance(node, Procedure):
        current_node = Node(f"procedure {node.ident}", parent=parent)
        for param in node.params:
            build_anytree(param, current_node)
        build_anytree(node.instr, current_node)
        for decl in node.decl:
            build_anytree(decl, current_node)
    elif isinstance(node, Function):
        current_node = Node(f"function {node.ident}", parent=parent)
        for param in node.params:
            build_anytree(param, current_node)
        for instr in node.instrs.instr:  # Accédez à la liste d'instructions
            build_anytree(instr, current_node)
        for decl in node.decls:
            build_anytree(decl, current_node)
    elif isinstance(node, Record):
        current_node = Node(f"record {node.ident}", parent=parent)
        for champ in node.champs:
            build_anytree(champ, current_node)
    elif isinstance(node, AccessType):
        current_node = Node(f"access type {node.ident1} {node.ident2}", parent=parent)
        pass  # Ajoutez le code pour la classe AccessType si nécessaire
    elif isinstance(node, Type):
        nom = f"type {node.ident}"
        if node.isAccess:
            nom = "access " + nom
        current_node = Node(nom, parent=parent)
    elif isinstance(node, Champs):
        current_node = Node(f"champ {node.ident}", parent=parent)
        build_anytree(node.type, current_node)
    elif isinstance(node, Param):
        build_anytree(node.type, current_node)
    elif isinstance(node, Return):
        build_anytree(node.expr, current_node)
    elif isinstance(node, Block):
        for instr in node.instr:  # Accédez à la liste d'instructions
            build_anytree(instr, current_node)
    elif isinstance(node, WhileLoop):
        build_anytree(node.expr, current_node)
        for instr in node.instrList:
            build_anytree(instr, current_node)
    elif isinstance(node, ForLoop):
        build_anytree(node.expr1, current_node)
        build_anytree(node.expr2, current_node)
        for instr in node.instrList:
            build_anytree(instr, current_node)
    elif isinstance(node, If):
        build_anytree(node.expr, current_node)
        for instr in node.instrNoeud.instr:  # Accédez à la liste d'instructions du bloc then
            build_anytree(instr, current_node)
        if node.elseNoeud is not None:
            build_anytree(node.elseNoeud, current_node) 
    elif isinstance(node, Affectation):
        build_anytree(node.acess, current_node)
        build_anytree(node.expr, current_node)

    return current_node
