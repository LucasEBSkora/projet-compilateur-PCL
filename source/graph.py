import tkinter as tk
import noeud as nd

class TreeDrawer:
    def __init__(self, root, tree):
        self.root = root
        self.tree = tree
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.draw_tree(tree, 400, 50, 400, 50)

    def draw_tree(self, node, x, y, dx, dy):
        if isinstance(node, (nd.Binaire, nd.Unaire, nd.Literal, nd.Ident, nd.New, nd.CharacterApostrofeVal, nd.Appel,
                             nd.Var, nd.Procedure, nd.Function, nd.Record, nd.AccessType, nd.Type, nd.Champs, nd.Mode, nd.Param,
                             nd.Return, nd.Block, nd.WhileLoop, nd.ForLoop, nd.If, nd.Affectation)):
            text = str(node)
        else:
            text = str(type(node).__name__)

        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, outline="black")
        self.canvas.create_text(x, y, text=text)

        if isinstance(node, (nd.Binaire, nd.Unaire, nd.Appel, nd.Var, nd.Procedure, nd.Function, nd.Record, nd.AccessType, nd.Type, nd.Champs, nd.Param, nd.Return)):
            if hasattr(node, 'params'):
                total_width = len(node.params) * dx
                current_x = x - total_width / 2
                current_y = y + dy
                for param in node.params:
                    self.draw_tree(param, current_x + dx / 2, current_y + dy, dx, dy)
                    current_x += dx
            elif hasattr(node, 'expr'):
                self.draw_tree(node.expr, x, y + dy, dx, dy)
            elif hasattr(node, 'instr'):
                self.draw_tree(node.instr, x, y + dy, dx, dy)
            elif hasattr(node, 'instrList'):
                current_x = x
                current_y = y + dy
                for instr in node.instrList:
                    self.draw_tree(instr, current_x, current_y, dx, dy)
                    current_y += dy

        elif isinstance(node, (nd.If)):
            self.draw_tree(node.expr1, x, y + dy, dx, dy)

            current_x = x - dx
            current_y = y + 2 * dy
            for instr in node.instrList1:
                self.draw_tree(instr, current_x, current_y, dx, dy)
                current_y += dy

            for elseif in node.listTuple:
                self.draw_tree(elseif[0], x, y + 2 * dy, dx, dy)
                current_x = x - dx
                current_y = y + 3 * dy
                for instr in elseif[1]:
                    self.draw_tree(instr, current_x, current_y, dx, dy)
                    current_y += dy

            if node.instrList3:
                current_x = x - dx
                current_y = y + 3 * dy
                for instr in node.instrList3:
                    self.draw_tree(instr, current_x, current_y, dx, dy)
                    current_y += dy

    def run(self):
        self.root.mainloop()