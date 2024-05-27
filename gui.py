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
        dessinMolecule (DessinMolecule): L'objet Molecule représentant la molécule dessinée.
    """

    def __init__(self, master=None):
        """
        Initialise un objet HulisInterface.

        Args:
            master (tkinter.Tk): La fenêtre principale de l'application.
        """
        super().__init__(master)
        self.master = master
        self.pack(fill='both', expand=True)
        self.create_panels()
        self.bind_events()
        self.dessinMolecule = DessinMolecule(self.canvas_molecule)
        self.drag_atom_at_startingpoint = None
        self.drag_atom_at_endpoint = None
        self.canvas_molecule = None

    def create_panels(self):
        """
        Crée les panneaux de l'interface.
        """
        self.panneau_huckel   = tk.Frame(self, bg='blue',   width=int(self.master.winfo_width() * 0.1))
        self.panneau_molecule = tk.Frame(self, bg='black')
        self.panneau_spectre  = tk.Frame(self, bg='green',  width=int(self.master.winfo_width() * 0.1))
        self.panneau_lewis    = tk.Frame(self, bg='orange', width=int(self.master.winfo_width() * 0.1))

        self.canvas_huckel   = tk.Canvas(self.panneau_huckel,   bg='lightblue')
        self.canvas_molecule = tk.Canvas(self.panneau_molecule, bg='white')
        self.canvas_spectre  = tk.Canvas(self.panneau_spectre,  bg='lightgreen')
        self.canvas_lewis    = tk.Canvas(self.panneau_lewis,    bg='yellow')

        self.panneau_huckel.pack(  side=tk.LEFT, fill=tk.BOTH)
        self.panneau_molecule.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.panneau_spectre.pack( side=tk.LEFT, fill=tk.BOTH)
        self.panneau_lewis.pack(   side=tk.LEFT, fill=tk.BOTH)

        self.canvas_huckel.pack(  fill=tk.BOTH, expand=True)        
        self.canvas_molecule.pack(fill=tk.BOTH, expand=True)
        self.canvas_spectre.pack( fill=tk.BOTH, expand=True)
        self.canvas_lewis.pack(   fill=tk.BOTH, expand=True)

    def bind_events(self):
        """
        Lie l'événement de touche 'l' pour afficher/masquer les labels des atomes.
        """
        self.canvas_molecule.bind('<Button-1>', self.add_carbon_atom)
        self.canvas_molecule.bind('<ButtonPress-1>', self.drag_start)
        self.canvas_molecule.bind('<ButtonRelease-1>', self.drag_stop)
        self.canvas_molecule.bind('<B1-Motion>', self.dragging)
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
        """
        Ajoute un lien entre deux atomes de la molécule.

        Args:
            atome1: Le premier atome.
            atome2: Le deuxième atome.
        """
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
    root.minsize(400, 300)
    root.geometry('800x600')
    root.mainloop()

if __name__ == '__main__':
    main()