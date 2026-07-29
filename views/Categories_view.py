# views/Categories_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.Categories_controller import Categories_controller

class Categories_view:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.id_selectionne = None
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principale
        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titre
        title_label = tk.Label(main_frame, text="Gestion des Catégories", 
                              font=('Arial', 16, 'bold'), fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Conteneur pour formulaire et tableau
        container = tk.Frame(main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Frame gauche (formulaire)
        left_frame = tk.Frame(container, bg='#f8f9fa')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Frame droite (tableau)
        right_frame = tk.Frame(container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Formulaire
        self.setup_formulaire(left_frame)
        
        # Tableau
        self.setup_tableau(right_frame)
        
        # Boutons d'action
        self.setup_boutons(left_frame)
    
    def setup_formulaire(self, parent):
        """Configure le formulaire"""
        form_frame = tk.LabelFrame(parent, text="Nouvelle Catégorie", 
                                  font=('Arial', 12, 'bold'), bg='#f8f9fa',
                                  padx=20, pady=20)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nom de la catégorie
        tk.Label(form_frame, text="Nom:", bg='#f8f9fa',
                font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W, pady=20)
        self.entry_nom = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.entry_nom.grid(row=0, column=1, pady=20, padx=10)
    
    def setup_tableau(self, parent):
        """Configure le tableau"""
        # Frame pour tableau avec scrollbars
        table_frame = tk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tableau
        self.table = ttk.Treeview(table_frame, 
                                 columns=('ID', 'Nom'),
                                 show='headings',
                                 yscrollcommand=scrollbar_y.set)
        
        # En-têtes
        self.table.heading('ID', text='ID')
        self.table.heading('Nom', text='Nom de la catégorie')
        
        # Colonnes
        self.table.column('ID', width=80, anchor=tk.CENTER)
        self.table.column('Nom', width=300)
        
        self.table.pack(fill=tk.BOTH, expand=True)
        
        # Lier la scrollbar
        scrollbar_y.config(command=self.table.yview)
        
        # Lier l'événement de sélection
        self.table.bind('<<TreeviewSelect>>', self.selectionner_categorie)
    
    def setup_boutons(self, parent):
        """Configure les boutons d'action"""
        btn_frame = tk.Frame(parent, bg='#f8f9fa')
        btn_frame.pack(fill=tk.X, padx=10, pady=20)
        
        # Boutons
        buttons = [
            ('➕ Ajouter', '#27ae60', self.ajouter_categorie),
            ('✏️ Modifier', '#3498db', self.modifier_categorie),
            ('🗑️ Supprimer', '#e74c3c', self.supprimer_categorie),
            ('🔄 Rafraîchir', '#f39c12', self.charger_categories),
            ('🗑️ Vider', '#95a5a6', self.vider_formulaire)
        ]
        
        for text, color, command in buttons:
            btn = tk.Button(btn_frame, text=text, font=('Arial', 10, 'bold'),
                           bg=color, fg='white', width=18, command=command)
            btn.pack(pady=5)
    
    def charger_categories(self):
        """Charge la liste des catégories"""
        # Vider le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        try:
            categories = Categories_controller.liste_categories()
            
            for categorie in categories:
                self.table.insert('', tk.END, values=(
                    categorie[0],  # ID
                    categorie[1]   # Nom
                ))
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def ajouter_categorie(self):
        """Ajoute une nouvelle catégorie"""
        nom = self.entry_nom.get().strip()
        
        if not nom:
            messagebox.showwarning("Attention", "Veuillez saisir un nom de catégorie!")
            return
        
        try:
            Categories_controller.ajouter_categorie(nom)
            messagebox.showinfo("Succès", "Catégorie ajoutée avec succès!")
            
            # Rafraîchir et vider
            self.charger_categories()
            self.vider_formulaire()
            
        except ValueError as e:
            messagebox.showwarning("Attention", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def modifier_categorie(self):
        """Modifie une catégorie existante"""
        if not self.id_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner une catégorie!")
            return
        
        nom = self.entry_nom.get().strip()
        
        if not nom:
            messagebox.showwarning("Attention", "Veuillez saisir un nom de catégorie!")
            return
        
        try:
            Categories_controller.modifier_categorie(self.id_selectionne, nom)
            messagebox.showinfo("Succès", "Catégorie modifiée avec succès!")
            
            # Rafraîchir et vider
            self.charger_categories()
            self.vider_formulaire()
            
        except ValueError as e:
            messagebox.showwarning("Attention", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def supprimer_categorie(self):
        """Supprime une catégorie"""
        if not self.id_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner une catégorie!")
            return
        
        # Vérifier si la catégorie est utilisée
        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer cette catégorie (ID: {self.id_selectionne})?\n"
            "Les livres utilisant cette catégorie n'auront plus de catégorie!"
        )
        
        if confirmation:
            try:
                Categories_controller.supprimer_categorie(self.id_selectionne)
                messagebox.showinfo("Succès", "Catégorie supprimée avec succès!")
                
                # Rafraîchir et vider
                self.charger_categories()
                self.vider_formulaire()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def selectionner_categorie(self, event):
        """Sélectionne une catégorie dans le tableau"""
        selection = self.table.selection()
        if selection:
            item = self.table.item(selection[0])
            values = item['values']
            
            self.id_selectionne = values[0]
            self.entry_nom.delete(0, tk.END)
            self.entry_nom.insert(0, values[1])
    
    def vider_formulaire(self):
        """Vide le formulaire"""
        self.entry_nom.delete(0, tk.END)
        self.id_selectionne = None
        
        # Désélectionner dans le tableau
        for item in self.table.selection():
            self.table.selection_remove(item)