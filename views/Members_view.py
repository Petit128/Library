# views/Members_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.Members_controller import Members_controller

class Members_view:
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
        title_label = tk.Label(main_frame, text="Gestion des Membres", 
                              font=('Arial', 16, 'bold'), fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # PanedWindow pour séparer formulaire et tableau
        paned = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Frame gauche (formulaire)
        left_frame = tk.Frame(paned, bg='#f5f6fa')
        paned.add(left_frame, width=350)
        
        # Frame droite (tableau)
        right_frame = tk.Frame(paned)
        paned.add(right_frame)
        
        # Formulaire
        self.setup_formulaire(left_frame)
        
        # Tableau
        self.setup_tableau(right_frame)
        
        # Boutons d'action
        self.setup_boutons(left_frame)
    
    def setup_formulaire(self, parent):
        """Configure le formulaire"""
        form_frame = tk.LabelFrame(parent, text="Informations Membre", 
                                  font=('Arial', 12, 'bold'), bg='#f5f6fa',
                                  padx=20, pady=20)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nom
        tk.Label(form_frame, text="Nom complet:", bg='#f5f6fa',
                font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W, pady=15)
        self.entry_nom = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.entry_nom.grid(row=0, column=1, pady=15, padx=10)
        
        # Contact
        tk.Label(form_frame, text="Contact:", bg='#f5f6fa',
                font=('Arial', 11)).grid(row=1, column=0, sticky=tk.W, pady=15)
        self.entry_contact = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.entry_contact.grid(row=1, column=1, pady=15, padx=10)
    
    def setup_tableau(self, parent):
        """Configure le tableau"""
        # Frame pour tableau avec scrollbars
        table_frame = tk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(table_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Tableau
        self.table = ttk.Treeview(table_frame, 
                                 columns=('ID', 'Nom', 'Contact'),
                                 show='headings',
                                 yscrollcommand=scrollbar_y.set,
                                 xscrollcommand=scrollbar_x.set)
        
        # En-têtes
        self.table.heading('ID', text='ID')
        self.table.heading('Nom', text='Nom complet')
        self.table.heading('Contact', text='Contact')
        
        # Colonnes
        self.table.column('ID', width=50, anchor=tk.CENTER)
        self.table.column('Nom', width=250)
        self.table.column('Contact', width=200)
        
        self.table.pack(fill=tk.BOTH, expand=True)
        
        # Lier les scrollbars
        scrollbar_y.config(command=self.table.yview)
        scrollbar_x.config(command=self.table.xview)
        
        # Lier l'événement de sélection
        self.table.bind('<<TreeviewSelect>>', self.selectionner_membre)
    
    def setup_boutons(self, parent):
        """Configure les boutons d'action"""
        btn_frame = tk.Frame(parent, bg='#f5f6fa')
        btn_frame.pack(fill=tk.X, padx=10, pady=20)
        
        # Boutons en grille
        buttons = [
            ('➕ Ajouter', '#27ae60', self.ajouter_membre),
            ('✏️ Modifier', '#3498db', self.modifier_membre),
            ('🗑️ Supprimer', '#e74c3c', self.supprimer_membre),
            ('🔄 Rafraîchir', '#f39c12', self.charger_membres),
            ('🗑️ Vider', '#95a5a6', self.vider_formulaire)
        ]
        
        # Première ligne (3 boutons)
        for i, (text, color, command) in enumerate(buttons[:3]):
            btn = tk.Button(btn_frame, text=text, font=('Arial', 10, 'bold'),
                           bg=color, fg='white', width=15, command=command)
            btn.grid(row=0, column=i, padx=5, pady=5)
        
        # Deuxième ligne (2 boutons)
        for i, (text, color, command) in enumerate(buttons[3:]):
            btn = tk.Button(btn_frame, text=text, font=('Arial', 10, 'bold'),
                           bg=color, fg='white', width=15, command=command)
            btn.grid(row=1, column=i, padx=5, pady=5)
    
    def charger_membres(self):
        """Charge la liste des membres"""
        # Vider le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        try:
            membres = Members_controller.liste_membres()
            
            for membre in membres:
                self.table.insert('', tk.END, values=(
                    membre.get('id_membre', ''),
                    membre.get('nom_membre', ''),
                    membre.get('contact_membre', '')
                ))
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def ajouter_membre(self):
        """Ajoute un nouveau membre"""
        nom = self.entry_nom.get().strip()
        contact = self.entry_contact.get().strip()
        
        if not nom:
            messagebox.showwarning("Attention", "Veuillez saisir un nom!")
            return
        if not contact:
            messagebox.showwarning("Attention", "Veuillez saisir un contact!")
            return
        
        try:
            Members_controller.ajouter_membre(nom, contact)
            messagebox.showinfo("Succès", "Membre ajouté avec succès!")
            
            # Rafraîchir et vider
            self.charger_membres()
            self.vider_formulaire()
            
        except ValueError as e:
            messagebox.showwarning("Attention", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def modifier_membre(self):
        """Modifie un membre existant"""
        if not self.id_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner un membre!")
            return
        
        nom = self.entry_nom.get().strip()
        contact = self.entry_contact.get().strip()
        
        if not nom:
            messagebox.showwarning("Attention", "Veuillez saisir un nom!")
            return
        if not contact:
            messagebox.showwarning("Attention", "Veuillez saisir un contact!")
            return
        
        try:
            Members_controller.modifier_membre(self.id_selectionne, nom, contact)
            messagebox.showinfo("Succès", "Membre modifié avec succès!")
            
            # Rafraîchir et vider
            self.charger_membres()
            self.vider_formulaire()
            
        except ValueError as e:
            messagebox.showwarning("Attention", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def supprimer_membre(self):
        """Supprime un membre"""
        if not self.id_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner un membre!")
            return
        
        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer ce membre (ID: {self.id_selectionne})?\n"
            "Tous ses emprunts seront également supprimés!"
        )
        
        if confirmation:
            try:
                Members_controller.supprimer_membre(self.id_selectionne)
                messagebox.showinfo("Succès", "Membre supprimé avec succès!")
                
                # Rafraîchir et vider
                self.charger_membres()
                self.vider_formulaire()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def selectionner_membre(self, event):
        """Sélectionne un membre dans le tableau"""
        selection = self.table.selection()
        if selection:
            item = self.table.item(selection[0])
            values = item['values']
            
            self.id_selectionne = values[0]
            self.entry_nom.delete(0, tk.END)
            self.entry_nom.insert(0, values[1])
            self.entry_contact.delete(0, tk.END)
            self.entry_contact.insert(0, values[2])
    
    def vider_formulaire(self):
        """Vide le formulaire"""
        self.entry_nom.delete(0, tk.END)
        self.entry_contact.delete(0, tk.END)
        self.id_selectionne = None
        
        # Désélectionner dans le tableau
        for item in self.table.selection():
            self.tasble.selection_remove(item)