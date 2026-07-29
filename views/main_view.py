# views/main_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from views.Livres_view import Livres_view
from views.Members_view import Members_view
from views.Categories_view import Categories_view
from views.Emprunts_view import Emprunts_view
from models.Connexion_base import Connexion_base

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Bibliothèque")
        
        # Vérifier la connexion à la base de données AVANT de créer l'interface
        try:
            if not self.verifier_connexion():
                messagebox.showerror("Erreur", 
                    "Impossible de se connecter à la base de données!\n\n"
                    "Veuillez vérifier:\n"
                    "1. Que MySQL est démarré\n"
                    "2. Les paramètres de connexion dans Connexion_base.py\n"
                    "3. Que la base de données 'library' existe")
                root.destroy()
                return
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la connexion: {str(e)}")
            root.destroy()
            return
        
        # Configuration de la fenêtre
        try:
            self.setup_styles()
            
            # Frame principal
            main_frame = tk.Frame(root)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # Header
            self.create_header(main_frame)
            
            # Notebook (onglets)
            self.create_notebook(main_frame)
            
            # Footer
            self.create_footer(main_frame)
            
            # Initialiser les vues
            self.initialize_views()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'initialisation: {str(e)}")
            root.destroy()
    
    def setup_styles(self):
        """Configure les styles de l'interface"""
        try:
            style = ttk.Style()
            style.theme_use('clam')
            
            # Personnalisation des onglets
            style.configure('TNotebook', background='#f0f0f0')
            style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 11))
            style.map('TNotebook.Tab', background=[('selected', '#3498db')])
        except:
            pass  # Si les styles échouent, on continue sans
    
    def create_header(self, parent):
        """Crée l'en-tête de l'application"""
        try:
            header_frame = tk.Frame(parent, bg='#2c3e50', height=80)
            header_frame.pack(fill=tk.X)
            header_frame.pack_propagate(False)
            
            # Titre
            title_label = tk.Label(
                header_frame,
                text="📚 Gestion de Bibliothèque",
                font=('Arial', 24, 'bold'),
                fg='white',
                bg='#2c3e50'
            )
            title_label.pack(side=tk.LEFT, padx=30, pady=20)
            
            # Bouton de rafraîchissement
            refresh_btn = tk.Button(
                header_frame,
                text="🔄 Rafraîchir",
                font=('Arial', 10),
                bg='#3498db',
                fg='white',
                command=self.refresh_all
            )
            refresh_btn.pack(side=tk.RIGHT, padx=20, pady=20)
        except Exception as e:
            print(f"Erreur création header: {e}")
    
    def create_notebook(self, parent):
        """Crée le notebook avec les onglets"""
        try:
            self.notebook = ttk.Notebook(parent)
            self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Créer les frames pour chaque onglet
            self.livres_frame = ttk.Frame(self.notebook)
            self.membres_frame = ttk.Frame(self.notebook)
            self.categories_frame = ttk.Frame(self.notebook)
            self.emprunts_frame = ttk.Frame(self.notebook)
            
            # Ajouter les onglets
            self.notebook.add(self.livres_frame, text='📖 Livres')
            self.notebook.add(self.membres_frame, text='👥 Membres')
            self.notebook.add(self.categories_frame, text='🏷️ Catégories')
            self.notebook.add(self.emprunts_frame, text='📋 Emprunts')
            
            # Associer l'événement de changement d'onglet
            self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        except Exception as e:
            print(f"Erreur création notebook: {e}")
            raise
    
    def create_footer(self, parent):
        """Crée le pied de page"""
        try:
            footer_frame = tk.Frame(parent, bg='#ecf0f1', height=40)
            footer_frame.pack(fill=tk.X)
            footer_frame.pack_propagate(False)
            
            # Statut de connexion
            self.status_label = tk.Label(
                footer_frame,
                text="● Connecté à la base de données",
                font=('Arial', 10),
                fg='#27ae60',
                bg='#ecf0f1'
            )
            self.status_label.pack(side=tk.LEFT, padx=20)
            
            # Version
            version_label = tk.Label(
                footer_frame,
                text="Version 1.0.0",
                font=('Arial', 10),
                fg='#7f8c8d',
                bg='#ecf0f1'
            )
            version_label.pack(side=tk.RIGHT, padx=20)
        except Exception as e:
            print(f"Erreur création footer: {e}")
    
    # Modifiez la méthode initialize_views dans views/main_view.py

   # Dans la méthode initialize_views de views/main_view.py
# Assurez-vous d'appeler charger_tout() pour emprunts_view

    def initialize_views(self):
        """Initialise toutes les vues"""
        try:
            # Créer les instances des vues
            self.livres_view = Livres_view(self.livres_frame)
            self.membres_view = Members_view(self.membres_frame)
            self.categories_view = Categories_view(self.categories_frame)
            self.emprunts_view = Emprunts_view(self.emprunts_frame)
            
            # Charger les données initiales
            self.livres_view.charger_livres()
            self.membres_view.charger_membres()
            self.categories_view.charger_categories()
            
            # Pour emprunts, charger tout (inclut membres pour autocomplétion)
            self.emprunts_view.charger_tout()
            
        except Exception as e:
            messagebox.showwarning("Avertissement", 
                f"Certaines données n'ont pas pu être chargées:\n{str(e)}")

    def on_tab_changed(self, event):
        """Gère le changement d'onglet"""
        try:
            tab_index = self.notebook.index(self.notebook.select())
            tab_names = ['Livres', 'Membres', 'Catégories', 'Emprunts']
            current_tab = tab_names[tab_index]
            
            # Rafraîchir les données de l'onglet actif
            if current_tab == 'Livres':
                self.livres_view.charger_livres()
            elif current_tab == 'Membres':
                self.membres_view.charger_membres()
            elif current_tab == 'Catégories':
                self.categories_view.charger_categories()
            elif current_tab == 'Emprunts':
                self.emprunts_view.charger_emprunts()
                self.emprunts_view.charger_livres_disponibles()
        except Exception as e:
            print(f"Erreur changement onglet: {e}")
    
    def refresh_all(self):
        """Rafraîchit toutes les vues"""
        try:
            # Rafraîchir toutes les vues
            self.livres_view.charger_livres()
            self.membres_view.charger_membres()
            self.categories_view.charger_categories()
            self.emprunts_view.charger_emprunts()
            self.emprunts_view.charger_livres_disponibles()
            
            messagebox.showinfo("Rafraîchissement", "Données rafraîchies avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du rafraîchissement: {str(e)}")
    
    def verifier_connexion(self):
        """Vérifie la connexion à la base de données"""
        try:
            # Test simple de connexion
            return Connexion_base.test_connexion()
        except Exception as e:
            print(f"Erreur de vérification de connexion: {e}")
            return False