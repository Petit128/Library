# views/Livres_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.Livres_controller import Livres_controller

class Livres_view:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.id_selectionne = None
        self.categories_dict = {}  # Dictionnaire pour stocker les catégories
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principale avec panedwindow
        main_paned = tk.PanedWindow(self.parent, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame gauche (formulaire)
        left_frame = tk.Frame(main_paned, bg='#f8f9fa')
        main_paned.add(left_frame, width=350)
        
        # Frame droit (tableau)
        right_frame = tk.Frame(main_paned)
        main_paned.add(right_frame)
        
        # Configuration du formulaire
        self.setup_formulaire(left_frame)
        
        # Configuration du tableau
        self.setup_tableau(right_frame)
        
        # Boutons d'action
        self.setup_boutons(left_frame)
    
    def setup_formulaire(self, parent):
        """Configure le formulaire avec dropdown pour catégorie"""
        form_frame = tk.LabelFrame(parent, text="Formulaire Livre", font=('Arial', 12, 'bold'),
                                  bg='#f8f9fa', padx=15, pady=15)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Titre
        tk.Label(form_frame, text="Titre:", bg='#f8f9fa', 
                font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.entry_titre = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.entry_titre.grid(row=0, column=1, pady=10, padx=10)
        
        # Catégorie - DROPDOWN
        tk.Label(form_frame, text="Catégorie:", bg='#f8f9fa',
                font=('Arial', 11)).grid(row=1, column=0, sticky=tk.W, pady=10)
        
        # Frame pour le dropdown et bouton d'ajout
        categorie_frame = tk.Frame(form_frame, bg='#f8f9fa')
        categorie_frame.grid(row=1, column=1, pady=10, padx=10, sticky=tk.W)
        
        self.combo_categorie = ttk.Combobox(categorie_frame, font=('Arial', 11), width=25, state='readonly')
        self.combo_categorie.pack(side=tk.LEFT)
        
        # Bouton pour ajouter une nouvelle catégorie
        btn_ajout_cat = tk.Button(categorie_frame, text="➕", font=('Arial', 9),
                                 bg='#3498db', fg='white', width=3,
                                 command=self.ouvrir_ajout_categorie)
        btn_ajout_cat.pack(side=tk.LEFT, padx=(5, 0))
        
        # Recherche
        tk.Label(form_frame, text="Recherche:", bg='#f8f9fa',
                font=('Arial', 11)).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.entry_recherche = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.entry_recherche.grid(row=2, column=1, pady=10, padx=10)
        self.entry_recherche.bind('<KeyRelease>', self.rechercher_livres)
    
    def setup_tableau(self, parent):
        """Configure le tableau"""
        # Frame pour le tableau avec scrollbars
        table_frame = tk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Tableau
        self.table = ttk.Treeview(table_frame, columns=('ID', 'Titre', 'Catégorie'),
                                 show='headings', yscrollcommand=scrollbar_y.set,
                                 xscrollcommand=scrollbar_x.set)
        
        # En-têtes
        self.table.heading('ID', text='ID')
        self.table.heading('Titre', text='Titre')
        self.table.heading('Catégorie', text='Catégorie')
        
        # Colonnes
        self.table.column('ID', width=50, anchor=tk.CENTER)
        self.table.column('Titre', width=300)
        self.table.column('Catégorie', width=150)
        
        self.table.pack(fill=tk.BOTH, expand=True)
        
        # Lier les scrollbars
        scrollbar_y.config(command=self.table.yview)
        scrollbar_x.config(command=self.table.xview)
        
        # Lier l'événement de sélection
        self.table.bind('<<TreeviewSelect>>', self.selectionner_livre)
    
    def setup_boutons(self, parent):
        """Configure les boutons d'action"""
        btn_frame = tk.Frame(parent, bg='#f8f9fa')
        btn_frame.pack(fill=tk.X, padx=10, pady=20)
        
        # Boutons
        buttons = [
            ('➕ Ajouter', '#27ae60', self.ajouter_livre),
            ('✏️ Modifier', '#3498db', self.modifier_livre),
            ('🗑️ Supprimer', '#e74c3c', self.supprimer_livre),
            ('🔄 Rafraîchir', '#f39c12', self.charger_livres),
            ('🗑️ Vider', '#95a5a6', self.vider_formulaire)
        ]
        
        for text, color, command in buttons:
            btn = tk.Button(btn_frame, text=text, font=('Arial', 10, 'bold'),
                           bg=color, fg='white', width=15, command=command)
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def ouvrir_ajout_categorie(self):
        """Ouvre une fenêtre pour ajouter une nouvelle catégorie"""
        popup = tk.Toplevel(self.parent)
        popup.title("Nouvelle Catégorie")
        popup.geometry("400x200")
        popup.transient(self.parent)
        popup.grab_set()
        
        # Centrer la fenêtre
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f'{width}x{height}+{x}+{y}')
        
        # Formulaire
        tk.Label(popup, text="Nom de la nouvelle catégorie:", 
                font=('Arial', 11)).pack(pady=20)
        
        entry_cat = tk.Entry(popup, font=('Arial', 11), width=30)
        entry_cat.pack(pady=10)
        entry_cat.focus_set()
        
        def ajouter():
            nom = entry_cat.get().strip()
            if not nom:
                messagebox.showwarning("Attention", "Veuillez saisir un nom de catégorie!")
                return
            
            try:
                from Controllers.Categories_controller import Categories_controller
                Categories_controller.ajouter_categorie(nom)
                messagebox.showinfo("Succès", "Catégorie ajoutée avec succès!")
                
                # Recharger les catégories
                self.charger_categories()
                popup.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
        
        # Boutons
        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Ajouter", bg='#27ae60', fg='white',
                 font=('Arial', 10, 'bold'), command=ajouter).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Annuler", bg='#95a5a6', fg='white',
                 font=('Arial', 10, 'bold'), command=popup.destroy).pack(side=tk.LEFT, padx=10)
    
    def charger_livres(self):
        """Charge la liste des livres"""
        # Vider le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        try:
            # Charger les livres
            livres = Livres_controller.liste_livres()
            
            for livre in livres:
                self.table.insert('', tk.END, values=(
                    livre.get('id_livre', ''),
                    livre.get('titre_livre', ''),
                    livre.get('nom_categorie', 'Non catégorisé')
                ))
            
            # Charger les catégories dans le combobox
            self.charger_categories()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def charger_categories(self):
        """Charge la liste des catégories dans le dropdown"""
        try:
            categories = Livres_controller.liste_categories()
            self.categories_dict = {}
            cat_list = ['']  # Option vide par défaut
            
            for cat in categories:
                cat_list.append(cat[1])
                self.categories_dict[cat[1]] = cat[0]  # nom -> id
            
            self.combo_categorie['values'] = cat_list
            
        except Exception as e:
            print(f"Erreur chargement catégories: {e}")
            self.combo_categorie['values'] = ['']
    
    def ajouter_livre(self):
        """Ajoute un nouveau livre"""
        titre = self.entry_titre.get().strip()
        categorie_nom = self.combo_categorie.get()
        
        if not titre:
            messagebox.showwarning("Attention", "Veuillez saisir un titre!")
            return
        
        try:
            # Trouver l'ID de la catégorie
            id_categorie = None
            if categorie_nom and categorie_nom in self.categories_dict:
                id_categorie = self.categories_dict[categorie_nom]
            
            # Appeler le contrôleur
            Livres_controller.ajouter_livre(titre, id_categorie)
            messagebox.showinfo("Succès", "Livre ajouté avec succès!")
            
            # Rafraîchir et vider
            self.charger_livres()
            self.vider_formulaire()
            
        except ValueError as e:
            messagebox.showwarning("Attention", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def modifier_livre(self):
        """Modifie un livre existant"""
        if not self.id_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre!")
            return
        
        titre = self.entry_titre.get().strip()
        categorie_nom = self.combo_categorie.get()
        
        if not titre:
            messagebox.showwarning("Attention", "Veuillez saisir un titre!")
            return
        
        try:
            # Trouver l'ID de la catégorie
            id_categorie = None
            if categorie_nom and categorie_nom in self.categories_dict:
                id_categorie = self.categories_dict[categorie_nom]
            
            # Appeler le contrôleur
            Livres_controller.modifier_livre(self.id_selectionne, titre, id_categorie)
            messagebox.showinfo("Succès", "Livre modifié avec succès!")
            
            # Rafraîchir et vider
            self.charger_livres()
            self.vider_formulaire()
            
        except ValueError as e:
            messagebox.showwarning("Attention", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def supprimer_livre(self):
        """Supprime un livre"""
        if not self.id_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre!")
            return
        
        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer ce livre (ID: {self.id_selectionne})?"
        )
        
        if confirmation:
            try:
                Livres_controller.supprimer_livre(self.id_selectionne)
                messagebox.showinfo("Succès", "Livre supprimé avec succès!")
                
                # Rafraîchir et vider
                self.charger_livres()
                self.vider_formulaire()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def rechercher_livres(self, event=None):
        """Recherche des livres"""
        terme = self.entry_recherche.get().strip()
        
        # Vider le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        if not terme:
            self.charger_livres()
            return
        
        try:
            livres = Livres_controller.rechercher_livres(terme)
            
            for livre in livres:
                self.table.insert('', tk.END, values=(
                    livre.get('id_livre', ''),
                    livre.get('titre_livre', ''),
                    livre.get('nom_categorie', 'Non catégorisé')
                ))
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche: {str(e)}")
    
    def selectionner_livre(self, event):
        """Sélectionne un livre dans le tableau"""
        selection = self.table.selection()
        if selection:
            item = self.table.item(selection[0])
            values = item['values']
            
            self.id_selectionne = values[0]
            self.entry_titre.delete(0, tk.END)
            self.entry_titre.insert(0, values[1])
            
            # Définir la catégorie dans le dropdown
            if values[2] != 'Non catégorisé':
                self.combo_categorie.set(values[2])
            else:
                self.combo_categorie.set('')
    
    def vider_formulaire(self):
        """Vide le formulaire"""
        self.entry_titre.delete(0, tk.END)
        self.combo_categorie.set('')
        self.entry_recherche.delete(0, tk.END)
        self.id_selectionne = None
        
        # Désélectionner dans le tableau
        for item in self.table.selection():
            self.table.selection_remove(item)