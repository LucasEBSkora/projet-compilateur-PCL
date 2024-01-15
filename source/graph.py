import tkinter as tk
import noeud as nd

class TreeDrawer:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.draw_tree(tree, 400, 50, 200, 50)

    def draw_tree(self, node, x, y, dx, dy):
        if isinstance(node, (nd.Binaire, nd.Unaire, nd.Literal, nd.Ident, nd.New, nd.CharacterApostrofeVal, nd.Appel,
                             nd.Var, nd.Procedure, nd.Function, nd.Record, nd.AccessType, nd.Type, nd.Champs, nd.Mode, nd.Param,
                             nd.Return, nd.Block, nd.WhileLoop, nd.ForLoop, nd.If, nd.Affectation)):
            text = str(node)
        else:
            text = str(type(node).__name__)

        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, outline="black")
        self.canvas.create_text(x, y, text=text)

        if isinstance(node, (nd.Binaire, nd.Unaire, nd.Appel, nd.Var, nd.Procedure, nd.Function, nd.Record, nd.AccessType, nd.Type, nd.Champs, nd.Param, nd.Return)):
            if hasattr(node, 'params'):
                total_width = len(node.params) * dx
                current_x = x - total_width / 2
                current_y = y + dy
                for param in node.params:
                    child_x = current_x + dx / 2
                    child_y = current_y + dy
                    self.draw_tree(param, child_x, child_y, dx, dy)
                    self.canvas.create_line(x, y + 10, child_x, child_y - 10, fill="black")
                    current_x += dx
            elif hasattr(node, 'expr'):
                child_x = x
                child_y = y + dy
                self.draw_tree(node.expr, child_x, child_y, dx, dy)
                self.canvas.create_line(x, y + 10, child_x, child_y - 10, fill="black")
            elif hasattr(node, 'instr'):
                child_x = x
                child_y = y + dy
                self.draw_tree(node.instr, child_x, child_y, dx, dy)
                self.canvas.create_line(x, y + 10, child_x, child_y - 10, fill="black")
            elif hasattr(node, 'instrList'):
                total_width = len(node.instrList) * dx
                current_x = x - total_width / 2
                current_y = y + dy
                for instr in node.instrList:
                    child_x = current_x + dx / 2
                    child_y = current_y + dy
                    self.draw_tree(instr, child_x, child_y, dx, dy)
                    self.canvas.create_line(x, y + 10, child_x, child_y - 10, fill="black")
                    current_x += dx

        elif isinstance(node, (nd.If)):
            child_x = x
            child_y = y + dy
            self.draw_tree(node.expr1, child_x, child_y, dx, dy)
            self.canvas.create_line(x, y + 10, child_x, child_y - 10, fill="black")

            current_x = x - dx
            current_y = y + 2 * dy
            for instr in node.instrList1:
                child_x = current_x + dx / 2
                child_y = current_y + dy
                self.draw_tree(instr, child_x, child_y, dx, dy)
                self.canvas.create_line(x, y + 10, child_x, child_y - 10, fill="black")
                current_x += dx

            for elseif in node.listTuple:
                child_x = x
                child_y = y + 2 * dy
                self.draw_tree(elseif[0], child_x, child_y, dx, dy)
                self.canvas.create_line(x, y + 10, child_x, child_y - 10, fill="black")
                current_x = x - dx
                current_y = y + 3 * dy
                for instr in elseif[1]:
                    child_x = current_x + dx / 2
                    child_y = current_y + dy
                    self.draw_tree(instr, child_x, child_y, dx, dy)
                    self.canvas.create_line(x, y + 10, child_x, child_y - 10, fill="black")
                    current_x += dx

            if node.instrList3:
                child_x = x
                child_y = y + 3 * dy
                for instr in node.instrList3:
                    child_x += dx / 2  # Mise à jour de current_x
                    child_y = current_y + dy
                    self.draw_tree(instr, child_x, child_y, dx, dy)
                    self.canvas.create_line(x, y + 10, child_x, child_y - 10, fill="black")
                    current_x += dx

    def run(self):
        self.root.mainloop()

# Exemple d'utilisation avec un arbre fictif (remplacez-le par votre AST réel)
