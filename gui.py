import tkinter as tk
from tkinter import colorchooser
import numpy as np
from dessinMolecule import DessinMolecule

from params import params

class HulisInterface(tk.Frame):
    """
    Classe représentant l'interface graphique pour dessiner des molécules.

    Attributs:
        master (tkinter.Tk): La fenêtre principale de l'application.
        left_panel (tkinter.Canvas): Le panneau gauche de l'interface.
        center_panel (tkinter.Frame): Le panneau central de l'interface contenant le canvas de dessin.
        right_panel (tkinter.Canvas): Le panneau droit de l'interface.
        canvas (tkinter.Canvas): Le canvas de dessin des molécules.
        molecule (Molecule): L'objet Molecule représentant la molécule dessinée.
    """

    def __init__(self, master=None):
        """
        Initialise un objet MoleculeDrawer.

        Args:
            master (tkinter.Tk): La fenêtre principale de l'application.
        """
        super().__init__(master)
        self.master = master
        self.pack(fill='both', expand=True)
        self.create_panels()
        self.create_canvas()
        self.bind_events()
        self.dessinMolecule = DessinMolecule(self.canvas)
        self.drag_atom_at_startingpoint = None

    def create_panels(self):
        """
        Crée les panneaux gauche, central et droit de l'interface.
        """
        self.left_panel = tk.Canvas(self, bg='blue', width=int(self.master.winfo_width() * 0.2))
        self.left_panel.pack(side='left', fill='both', expand=True)
        
        self.center_panel = tk.Frame(self)
        self.center_panel.pack(side='left', fill='both', expand=True)
        
        self.right_panel = tk.Canvas(self, bg='orange', width=int(self.master.winfo_width() * 0.2))
        self.right_panel.pack(side='left', fill='both', expand=True)

    def create_canvas(self):
        """
        Crée le canvas de dessin des molécules et lie les événements de clic.
        """
        self.canvas = tk.Canvas(self.center_panel, bg='white')
        self.canvas.pack(fill='both', expand=True)

    def bind_events(self):
        """
        Lie l'événement de touche 'l' pour afficher/masquer les labels des atomes.
        """
        self.canvas.bind('<Button-1>', self.add_carbon_atom)
        self.canvas.bind('<ButtonPress-1>', self.drag_start)
        self.canvas.bind('<ButtonRelease-1>', self.drag_stop)
        self.canvas.bind('<B1-Motion>', self.dragging)
        self.master.bind('l', self.toggle_symbols)
        self.master.bind('q', self.quit_app)

    def drag_start(self, event):
        x = event.x
        y = event.y
        self.drag_atom_at_startingpoint = self.dessinMolecule.get_atom_at_position(x,y)
        print(self.drag_atom_at_startingpoint)
        if self.drag_atom_at_startingpoint == None:
            print('beging dragging')
            self.drag_atom_at_startingpoint = self.add_carbon_atom(event)

    def dragging(self, event):
        print("Dragging "+str(event.x)+" "+str(event.y))
        return

    def drag_stop(self, event):
        x = event.x
        y = event.y
        self.drag_atom_at_endpoint = self.dessinMolecule.get_atom_at_position(x,y)
        print(self.drag_atom_at_endpoint)
        if self.drag_atom_at_endpoint == None:
            print('end dragging')
            self.drag_atom_at_endpoint = self.add_carbon_atom(event)
        self.add_bond(self.drag_atom_at_startingpoint, self.drag_atom_at_endpoint)
        return

    def add_carbon_atom(self, event):
        """
        Ajoute un atome de carbone à la molécule aux coordonnées du clic gauche.

        Args:
            event (tkinter.Event): L'événement de clic gauche.
        """
        x, y = event.x, event.y
        return self.dessinMolecule.add_carbon_atom(x, y)
    
    def add_bond(self, atome1, atome2):
        self.dessinMolecule.add_bond(atome1, atome2)

    def toggle_symbols(self, event):
        """
        Affiche ou masque les labels des atomes de la molécule.

        Args:
            event (tkinter.Event): L'événement de touche 'l'.
        """
        self.dessinMolecule.toggle_symbols()

    def quit_app(self, event):
        """
        Quitte l'application.

        Args:
            event (tkinter.Event): L'événement de touche 'q'.
        """
        self.master.quit()

          
def main():
    """
    Fonction principale pour lancer l'application.
    """
    root = tk.Tk()
    app = HulisInterface(root)
    root.geometry('800x600')
    root.mainloop()

if __name__ == '__main__':
    main()