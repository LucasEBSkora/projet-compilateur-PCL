from anytree import Node
from graph import *
from noeud import *

def create_node(nom, parent):
    return Node(nom, parent=parent)

def build_anytree(node, parent=None):
    if isinstance(node, Binaire):
        current_node = create_node(node.operateur, parent)
        build_anytree(node.gauche, current_node)
        build_anytree(node.droite, current_node)
    elif isinstance(node, Unaire):
        current_node = create_node(node.operateur, parent)
        build_anytree(node.operande, current_node)
    elif isinstance(node, Literal):
        current_node = create_node(str(node.literal), parent)
    elif isinstance(node, Ident):
        current_node = create_node(node.nom, parent)
    elif isinstance(node, New):
        current_node = create_node("new", parent)
        build_anytree(node.nom, current_node)
    elif isinstance(node, CharacterApostrofeVal):
        current_node = create_node("Character'val", parent)
        build_anytree(node.expr, current_node)
    elif isinstance(node, Appel):
        current_node = create_node(f"appel {node.nom}", parent)
        for param in node.params:
            build_anytree(param, current_node)
    elif isinstance(node, Var):
        current_node = create_node(f"var {node.ident}", parent)
        build_anytree(node.type, current_node)
        if node.expr is not None:
            build_anytree(node.expr, current_node)
    elif isinstance(node, Procedure):
        current_node = create_node(f"procedure {node.ident}", parent)
        for param in node.params:
            build_anytree(param, current_node)
        for decl in node.decl:
            build_anytree(decl, current_node)
        build_anytree(node.instr, current_node)

    elif isinstance(node, Function):
        current_node = create_node(f"function {node.ident}", parent)
        for param in node.params:
            build_anytree(param, current_node)
        for instr in node.instrs.instr:  # Accédez à la liste d'instructions
            build_anytree(instr, current_node)
        for decl in node.decls:
            build_anytree(decl, current_node)
    elif isinstance(node, Record):
        current_node = create_node(f"record {node.ident}", parent)
        for champ in node.champs:
            build_anytree(champ, current_node)
    elif isinstance(node, AccessType):
        current_node = create_node(f"access type {node.ident1} {node.ident2}", parent)
    elif isinstance(node, Type):
        nom = f"type {node.ident}"
        if node.isAccess:
            nom = "access " + nom
        current_node = create_node(nom, parent)
    elif isinstance(node, Champs):
        current_node = create_node(f"champ {node.ident}", parent)
        build_anytree(node.type, current_node)
    elif isinstance(node, Param):
        current_node = create_node(f"param {node.mode} {node.ident}", parent)
        build_anytree(node.type, current_node)
    elif isinstance(node, Return):
        current_node = create_node("return", parent)
        build_anytree(node.expr, current_node)
    elif isinstance(node, Block):
        current_node = create_node("block", parent)
        for instr in node.instr:  # Accédez à la liste d'instructions
            build_anytree(instr, current_node)
    elif isinstance(node, WhileLoop):
        current_node = create_node("while", parent)
        build_anytree(node.expr, current_node)
        for instr in node.instrList:
            build_anytree(instr, current_node)
    elif isinstance(node, ForLoop):
        nom = "for"
        if node.isReverse:
            nom += " reverse"
        current_node = create_node(nom, parent)
        build_anytree(node.expr1, current_node)
        build_anytree(node.expr2, current_node)
        for instr in node.instrList:
            build_anytree(instr, current_node)
    elif isinstance(node, If):
        current_node = create_node("if", parent)
        build_anytree(node.expr, current_node)
        build_anytree(node.instrNoeud, current_node)
        if node.elseNoeud is not None:
            build_anytree(node.elseNoeud, current_node) 
    elif isinstance(node, Affectation):
        current_node = create_node(":=", parent)
        build_anytree(node.acess, current_node)
        build_anytree(node.expr, current_node)
    else:
        raise f"{node}"

    return current_node
