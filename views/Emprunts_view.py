# views/Emprunts_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from Controllers.Emprunts_controller import Emprunts_controller
from Controllers.Livres_controller import Livres_controller
from Controllers.Members_controller import Members_controller
from Controllers.Categories_controller import Categories_controller

class Emprunts_view:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        self.id_selectionne = None
        self.livres_dict = {}      # {display_text: id_livre}
        self.membres_dict = {}     # {display_text: id_membre}
        self.categories_dict = {}  # {nom_categorie: id_categorie}
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principale
        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titre
        title_label = tk.Label(main_frame, text="Gestion des Emprunts", 
                              font=('Arial', 16, 'bold'), fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # PanedWindow pour séparer formulaire et tableau
        paned = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Frame gauche (formulaire)
        left_frame = tk.Frame(paned, bg='#f5f6fa')
        paned.add(left_frame, width=400)
        
        # Frame droite (tableau)
        right_frame = tk.Frame(paned)
        paned.add(right_frame)
        
        # Formulaire
        self.setup_formulaire(left_frame)
        
        # Tableau
        self.setup_tableau(right_frame)
        
        # Boutons d'action
        self.setup_boutons(left_frame)
        
        # Filtres pour la recherche
        self.setup_filtres(left_frame)
    
    def setup_formulaire(self, parent):
        """Configure le formulaire avec améliorations"""
        form_frame = tk.LabelFrame(parent, text="Nouvel Emprunt / Retour", 
                                  font=('Arial', 12, 'bold'), bg='#f5f6fa',
                                  padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame pour les filtres de recherche de livre
        livre_frame = tk.LabelFrame(form_frame, text="Sélection du Livre", 
                                   font=('Arial', 10), bg='#f5f6fa',
                                   padx=10, pady=10)
        livre_frame.grid(row=0, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        
        # Filtre par catégorie pour les livres
        tk.Label(livre_frame, text="Filtrer par catégorie:", bg='#f5f6fa',
                font=('Arial', 9)).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.combo_categorie_filtre = ttk.Combobox(livre_frame, font=('Arial', 9), width=25, state='readonly')
        self.combo_categorie_filtre.grid(row=0, column=1, pady=5, padx=5)
        self.combo_categorie_filtre.bind('<<ComboboxSelected>>', self.filtrer_livres_par_categorie)
        
        # Livre - DROPDOWN AMÉLIORÉ
        tk.Label(livre_frame, text="Livre:", bg='#f5f6fa',
                font=('Arial', 9)).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.combo_livre = ttk.Combobox(livre_frame, font=('Arial', 10), width=30, state='readonly')
        self.combo_livre.grid(row=1, column=1, pady=5, padx=5)
        
        # Membre - DROPDOWN
        tk.Label(form_frame, text="Membre:", bg='#f5f6fa',
                font=('Arial', 11)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.combo_membre = ttk.Combobox(form_frame, font=('Arial', 11), width=35, state='readonly')
        self.combo_membre.grid(row=1, column=1, pady=10, padx=10)
        
        # Date d'emprunt
        tk.Label(form_frame, text="Date emprunt:", bg='#f5f6fa',
                font=('Arial', 11)).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.date_emprunt = DateEntry(form_frame, font=('Arial', 11), width=20,
                                     background='#3498db', foreground='white',
                                     borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_emprunt.grid(row=2, column=1, pady=10, padx=10, sticky=tk.W)
        self.date_emprunt.set_date(datetime.now())
        
        # Date retour prévue
        tk.Label(form_frame, text="Date retour prévue:", bg='#f5f6fa',
                font=('Arial', 11)).grid(row=3, column=0, sticky=tk.W, pady=10)
        self.date_retour_prevue = DateEntry(form_frame, font=('Arial', 11), width=20,
                                           background='#27ae60', foreground='white',
                                           borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_retour_prevue.grid(row=3, column=1, pady=10, padx=10, sticky=tk.W)
        self.date_retour_prevue.set_date(datetime.now() + timedelta(days=14))
        
        # Date retour effective (pour les retours)
        tk.Label(form_frame, text="Date retour effective:", bg='#f5f6fa',
                font=('Arial', 11)).grid(row=4, column=0, sticky=tk.W, pady=10)
        self.date_retour_effective = DateEntry(form_frame, font=('Arial', 11), width=20,
                                              background='#e74c3c', foreground='white',
                                              borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_retour_effective.grid(row=4, column=1, pady=10, padx=10, sticky=tk.W)
        self.date_retour_effective.set_date(datetime.now())
    
    def setup_filtres(self, parent):
        """Configure les filtres pour la recherche"""
        filtres_frame = tk.LabelFrame(parent, text="Filtres de Recherche", 
                                     font=('Arial', 10, 'bold'), bg='#f5f6fa',
                                     padx=10, pady=10)
        filtres_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Filtre par statut
        tk.Label(filtres_frame, text="Statut:", bg='#f5f6fa',
                font=('Arial', 9)).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.combo_statut_filtre = ttk.Combobox(filtres_frame, font=('Arial', 9), width=15, state='readonly')
        self.combo_statut_filtre['values'] = ['Tous', 'En cours', 'Retournés', 'En retard']
        self.combo_statut_filtre.set('Tous')
        self.combo_statut_filtre.grid(row=0, column=1, padx=5)
        self.combo_statut_filtre.bind('<<ComboboxSelected>>', self.filtrer_emprunts)
        
        # Filtre par membre
        tk.Label(filtres_frame, text="Membre:", bg='#f5f6fa',
                font=('Arial', 9)).grid(row=0, column=2, sticky=tk.W, padx=5)
        
        self.combo_membre_filtre = ttk.Combobox(filtres_frame, font=('Arial', 9), width=20, state='readonly')
        self.combo_membre_filtre.grid(row=0, column=3, padx=5)
        self.combo_membre_filtre.bind('<<ComboboxSelected>>', self.filtrer_emprunts)
        
        # Bouton pour réinitialiser les filtres
        tk.Button(filtres_frame, text="Réinitialiser Filtres", font=('Arial', 9),
                 bg='#95a5a6', fg='white', command=self.reinitialiser_filtres).grid(row=0, column=4, padx=10)
    
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
                                 columns=('ID', 'Livre', 'Catégorie', 'Membre', 
                                         'DateEmprunt', 'DateRetourPrevue', 'DateRetourEffective', 'Statut', 'Jours'),
                                 show='headings',
                                 yscrollcommand=scrollbar_y.set,
                                 xscrollcommand=scrollbar_x.set)
        
        # En-têtes
        self.table.heading('ID', text='ID')
        self.table.heading('Livre', text='Livre')
        self.table.heading('Catégorie', text='Catégorie')
        self.table.heading('Membre', text='Membre')
        self.table.heading('DateEmprunt', text='Date Emprunt')
        self.table.heading('DateRetourPrevue', text='Date Retour Prévue')
        self.table.heading('DateRetourEffective', text='Date Retour Réel')
        self.table.heading('Statut', text='Statut')
        self.table.heading('Jours', text='Jours Restants')
        
        # Colonnes
        self.table.column('ID', width=50, anchor=tk.CENTER)
        self.table.column('Livre', width=180)
        self.table.column('Catégorie', width=100)
        self.table.column('Membre', width=120)
        self.table.column('DateEmprunt', width=90)
        self.table.column('DateRetourPrevue', width=90)
        self.table.column('DateRetourEffective', width=90)
        self.table.column('Statut', width=80)
        self.table.column('Jours', width=80)
        
        self.table.pack(fill=tk.BOTH, expand=True)
        
        # Lier les scrollbars
        scrollbar_y.config(command=self.table.yview)
        scrollbar_x.config(command=self.table.xview)
        
        # Tags pour les couleurs
        self.table.tag_configure('en_cours', background='#fff9c4')
        self.table.tag_configure('retourne', background='#c8e6c9')
        self.table.tag_configure('retard', background='#ffccbc')
        
        # Lier l'événement de sélection
        self.table.bind('<<TreeviewSelect>>', self.selectionner_emprunt)
    
    def setup_boutons(self, parent):
        """Configure les boutons d'action"""
        btn_frame = tk.Frame(parent, bg='#f5f6fa')
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Boutons en grille
        buttons = [
            ('➕ Nouvel Emprunt', '#27ae60', self.ajouter_emprunt),
            ('📖 Enregistrer Retour', '#3498db', self.enregistrer_retour),
            ('🗑️ Supprimer Emprunt', '#e74c3c', self.supprimer_emprunt),
            ('🔄 Rafraîchir', '#f39c12', self.charger_tout),
            ('🗑️ Vider Formulaire', '#95a5a6', self.vider_formulaire),
            ('📊 Statistiques', '#9b59b6', self.afficher_statistiques)
        ]
        
        # 3 boutons par ligne
        for i, (text, color, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            btn = tk.Button(btn_frame, text=text, font=('Arial', 10, 'bold'),
                           bg=color, fg='white', width=20, command=command)
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Footer avec statistiques
        self.footer_label = tk.Label(btn_frame, text="", font=('Arial', 10),
                                    bg='#f5f6fa', fg='#2c3e50')
        self.footer_label.grid(row=3, column=0, columnspan=2, pady=10)
    
    def charger_tout(self):
        """Charge toutes les données"""
        self.charger_categories()
        self.charger_livres_disponibles()
        self.charger_membres()
        self.charger_emprunts()
    
    def charger_categories(self):
        """Charge la liste des catégories pour le filtre"""
        try:
            categories = Categories_controller.liste_categories()
            self.categories_dict = {}
            cat_list = ['Toutes']  # Option par défaut
            
            for cat in categories:
                cat_list.append(cat[1])
                self.categories_dict[cat[1]] = cat[0]
            
            self.combo_categorie_filtre['values'] = cat_list
            self.combo_categorie_filtre.set('Toutes')
            
        except Exception as e:
            print(f"Erreur chargement catégories: {e}")
    
    def charger_livres_disponibles(self, categorie_id=None):
        """Charge la liste des livres disponibles avec filtrage par catégorie"""
        try:
            # Obtenir tous les livres disponibles
            livres_disponibles = Emprunts_controller.get_livres_disponibles()
            
            # Filtrer par catégorie si spécifié
            if categorie_id:
                livres_disponibles = [livre for livre in livres_disponibles 
                                     if livre.get('id_categorie') == categorie_id]
            
            # Obtenir toutes les catégories pour afficher le nom
            categories = {}
            try:
                cat_list = Categories_controller.liste_categories()
                categories = {cat[0]: cat[1] for cat in cat_list}
            except:
                pass
            
            # Préparer la liste pour le dropdown
            self.livres_dict = {}
            livre_list = []
            
            for livre in livres_disponibles:
                # Obtenir le nom de la catégorie
                cat_nom = categories.get(livre.get('id_categorie'), 'Non catégorisé')
                
                # Format d'affichage: "Titre (ID: X) - Catégorie"
                display_text = f"{livre['titre_livre']} (ID: {livre['id_livre']}) - {cat_nom}"
                livre_list.append(display_text)
                self.livres_dict[display_text] = livre['id_livre']
            
            self.combo_livre['values'] = livre_list
            
            return len(livres_disponibles)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des livres: {str(e)}")
            return 0
    
    def charger_membres(self):
        """Charge la liste des membres"""
        try:
            membres = Members_controller.liste_membres()
            self.membres_dict = {}
            membre_list = ['Tous']  # Option pour le filtre
            
            for membre in membres:
                # Format pour le formulaire d'emprunt
                display_text_form = f"{membre['nom_membre']} (ID: {membre['id_membre']})"
                self.membres_dict[display_text_form] = membre['id_membre']
                
                # Format pour le filtre (juste le nom)
                display_text_filtre = membre['nom_membre']
                membre_list.append(display_text_filtre)
            
            self.combo_membre['values'] = list(self.membres_dict.keys())
            self.combo_membre_filtre['values'] = membre_list
            self.combo_membre_filtre.set('Tous')
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des membres: {str(e)}")
    
    def filtrer_livres_par_categorie(self, event=None):
        """Filtre les livres disponibles par catégorie"""
        categorie_nom = self.combo_categorie_filtre.get()
        
        if categorie_nom == 'Toutes' or not categorie_nom:
            # Afficher tous les livres disponibles
            self.charger_livres_disponibles()
        else:
            # Trouver l'ID de la catégorie
            categorie_id = self.categories_dict.get(categorie_nom)
            if categorie_id:
                self.charger_livres_disponibles(categorie_id)
            else:
                self.charger_livres_disponibles()
    
    def charger_emprunts(self, filtre_statut=None, filtre_membre=None):
        """Charge tous les emprunts avec filtres"""
        # Vider le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        try:
            emprunts = Emprunts_controller.liste_emprunts()
            
            # Appliquer les filtres
            emprunts_filtres = []
            for emp in emprunts:
                # Filtre par statut
                if filtre_statut and filtre_statut != 'Tous':
                    date_retour_effective = emp['date_retour_effective']
                    date_retour_prevue = datetime.strptime(str(emp['date_retour_prevue']), '%Y-%m-%d').date()
                    
                    statut_reel = "Retourné" if date_retour_effective else (
                        "En retard" if date_retour_prevue < datetime.now().date() else "En cours"
                    )
                    
                    if filtre_statut != statut_reel:
                        continue
                
                # Filtre par membre
                if filtre_membre and filtre_membre != 'Tous':
                    if emp['nom_membre'] != filtre_membre:
                        continue
                
                emprunts_filtres.append(emp)
            
            self.afficher_emprunts(emprunts_filtres)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def filtrer_emprunts(self, event=None):
        """Applique les filtres aux emprunts"""
        filtre_statut = self.combo_statut_filtre.get()
        filtre_membre = self.combo_membre_filtre.get()
        
        self.charger_emprunts(filtre_statut, filtre_membre)
    
    def reinitialiser_filtres(self):
        """Réinitialise tous les filtres"""
        self.combo_statut_filtre.set('Tous')
        self.combo_membre_filtre.set('Tous')
        self.combo_categorie_filtre.set('Toutes')
        self.charger_emprunts()
        self.charger_livres_disponibles()
    
    def afficher_emprunts(self, emprunts):
        """Affiche les emprunts dans le tableau"""
        total = len(emprunts)
        en_cours = 0
        retournes = 0
        en_retard = 0
        
        for emp in emprunts:
            id_emp = emp['id_emprunt']
            livre = emp['titre_livre']
            
            # Récupérer la catégorie du livre
            try:
                from Controllers.Livres_controller import Livres_controller
                livre_info = Livres_controller.get_livre(emp['id_livre'])
                categorie = livre_info.get('nom_categorie', 'Non catégorisé') if livre_info else 'Non catégorisé'
            except:
                categorie = 'Non catégorisé'
            
            membre = emp['nom_membre']
            date_emprunt = emp['date_emprunt']
            date_retour_prevue = emp['date_retour_prevue']
            date_retour_effective = emp['date_retour_effective']
            
            # Calculer les jours restants ou de retard
            jours_info = ""
            if not date_retour_effective:
                date_prevue = datetime.strptime(str(date_retour_prevue), '%Y-%m-%d').date()
                jours_diff = (date_prevue - datetime.now().date()).days
                
                if jours_diff >= 0:
                    jours_info = f"{jours_diff} jours"
                else:
                    jours_info = f"+{abs(jours_diff)} jours"
            
            # Déterminer le statut
            if date_retour_effective:
                statut = "Retourné"
                tag = 'retourne'
                retournes += 1
            else:
                date_prevue = datetime.strptime(str(date_retour_prevue), '%Y-%m-%d').date()
                if date_prevue < datetime.now().date():
                    statut = "En retard"
                    tag = 'retard'
                    en_retard += 1
                else:
                    statut = "En cours"
                    tag = 'en_cours'
                    en_cours += 1
            
            # Formater la date de retour effective
            date_retour_effective_display = date_retour_effective if date_retour_effective else "-"
            
            self.table.insert('', tk.END, values=(
                id_emp, livre, categorie, membre, date_emprunt,
                date_retour_prevue, date_retour_effective_display, statut, jours_info
            ), tags=(tag,))
        
        # Mettre à jour les statistiques
        stats_text = f"Total: {total} | En cours: {en_cours} | Retournés: {retournes} | En retard: {en_retard}"
        self.footer_label.config(text=stats_text)
    
    def afficher_statistiques(self):
        """Affiche des statistiques détaillées"""
        try:
            emprunts = Emprunts_controller.liste_emprunts()
            emprunts_en_cours = Emprunts_controller.liste_emprunts_en_cours()
            
            total = len(emprunts)
            en_cours = len(emprunts_en_cours)
            retournes = total - en_cours
            
            # Calculer les retards
            en_retard = 0
            for emp in emprunts_en_cours:
                date_prevue = datetime.strptime(str(emp['date_retour_prevue']), '%Y-%m-%d').date()
                if date_prevue < datetime.now().date():
                    en_retard += 1
            
            stats_msg = f"""
📊 STATISTIQUES DES EMPRUNTS 📊

Total des emprunts: {total}
• En cours: {en_cours}
• Retournés: {retournes}
• En retard: {en_retard}

📅 Emprunts cette année: {self.compter_emprunts_annee()}
📚 Livres les plus empruntés: {self.livres_plus_empruntes()}

Dernier emprunt: {self.dernier_emprunt()}
            """
            
            messagebox.showinfo("Statistiques", stats_msg)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul des statistiques: {str(e)}")
    
    def compter_emprunts_annee(self):
        """Compte les emprunts de l'année en cours"""
        try:
            emprunts = Emprunts_controller.liste_emprunts()
            annee_courante = datetime.now().year
            count = 0
            
            for emp in emprunts:
                date_emp = datetime.strptime(str(emp['date_emprunt']), '%Y-%m-%d')
                if date_emp.year == annee_courante:
                    count += 1
            
            return count
        except:
            return "N/A"
    
    def livres_plus_empruntes(self):
        """Trouve les livres les plus empruntés"""
        try:
            emprunts = Emprunts_controller.liste_emprunts()
            compteur = {}
            
            for emp in emprunts:
                livre_id = emp['id_livre']
                livre_titre = emp['titre_livre']
                cle = f"{livre_titre} (ID: {livre_id})"
                compteur[cle] = compteur.get(cle, 0) + 1
            
            # Trier par nombre d'emprunts
            livres_tries = sorted(compteur.items(), key=lambda x: x[1], reverse=True)
            
            if livres_tries:
                return f"{livres_tries[0][0]} ({livres_tries[0][1]} fois)"
            else:
                return "Aucun"
        except:
            return "N/A"
    
    def dernier_emprunt(self):
        """Trouve le dernier emprunt"""
        try:
            emprunts = Emprunts_controller.liste_emprunts()
            if emprunts:
                dernier = max(emprunts, key=lambda x: x['date_emprunt'])
                return f"{dernier['date_emprunt']} - {dernier['titre_livre']}"
            else:
                return "Aucun"
        except:
            return "N/A"
    
    def ajouter_emprunt(self):
        """Ajoute un nouvel emprunt"""
        livre_selectionne = self.combo_livre.get()
        membre_selectionne = self.combo_membre.get()
        
        if not livre_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre!")
            return
        if not membre_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner un membre!")
            return
        
        id_livre = self.livres_dict.get(livre_selectionne)
        id_membre = self.membres_dict.get(membre_selectionne)
        date_emprunt = self.date_emprunt.get_date().strftime('%Y-%m-%d')
        date_retour_prevue = self.date_retour_prevue.get_date().strftime('%Y-%m-%d')
        
        # Validation des dates
        if self.date_retour_prevue.get_date() <= self.date_emprunt.get_date():
            messagebox.showwarning("Attention", "La date de retour doit être après la date d'emprunt!")
            return
        
        try:
            Emprunts_controller.ajouter_emprunt(id_livre, id_membre, date_emprunt, date_retour_prevue)
            messagebox.showinfo("Succès", "Emprunt enregistré avec succès!")
            
            # Rafraîchir et vider
            self.charger_tout()
            self.vider_formulaire()
            
        except ValueError as e:
            messagebox.showwarning("Attention", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def enregistrer_retour(self):
        """Enregistre le retour d'un livre"""
        if not self.id_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner un emprunt!")
            return
        
        date_retour_effective = self.date_retour_effective.get_date().strftime('%Y-%m-%d')
        
        # Validation: la date de retour doit être après la date d'emprunt
        date_emprunt = self.date_emprunt.get_date()
        if self.date_retour_effective.get_date() < date_emprunt:
            messagebox.showwarning("Attention", "La date de retour ne peut pas être avant la date d'emprunt!")
            return
        
        try:
            message = Emprunts_controller.enregistrer_retour(self.id_selectionne, date_retour_effective)
            messagebox.showinfo("Succès", message)
            
            # Rafraîchir et vider
            self.charger_tout()
            self.vider_formulaire()
            
        except ValueError as e:
            messagebox.showwarning("Attention", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def supprimer_emprunt(self):
        """Supprime un emprunt"""
        if not self.id_selectionne:
            messagebox.showwarning("Attention", "Veuillez sélectionner un emprunt!")
            return
        
        confirmation = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer cet emprunt (ID: {self.id_selectionne})?"
        )
        
        if confirmation:
            try:
                Emprunts_controller.supprimer_emprunt(self.id_selectionne)
                messagebox.showinfo("Succès", "Emprunt supprimé avec succès!")
                
                # Rafraîchir et vider
                self.charger_tout()
                self.vider_formulaire()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def selectionner_emprunt(self, event):
        """Sélectionne un emprunt dans le tableau"""
        selection = self.table.selection()
        if selection:
            item = self.table.item(selection[0])
            values = item['values']
            
            self.id_selectionne = values[0]
            
            # Mettre à jour les champs du formulaire
            # Trouver le livre correspondant
            livre_titre = values[1]
            for display_text, livre_id in self.livres_dict.items():
                if livre_titre in display_text:
                    self.combo_livre.set(display_text)
                    break
            
            # Trouver le membre correspondant
            membre_nom = values[3]
            for display_text, membre_id in self.membres_dict.items():
                if membre_nom in display_text:
                    self.combo_membre.set(display_text)
                    break
            
            # Définir les dates
            if values[4]:
                self.date_emprunt.set_date(datetime.strptime(values[4], '%Y-%m-%d'))
            if values[5]:
                self.date_retour_prevue.set_date(datetime.strptime(values[5], '%Y-%m-%d'))
            if values[6] and values[6] != '-':
                self.date_retour_effective.set_date(datetime.strptime(values[6], '%Y-%m-%d'))
            else:
                self.date_retour_effective.set_date(datetime.now())
    
    def vider_formulaire(self):
        """Vide le formulaire"""
        self.combo_livre.set('')
        self.combo_membre.set('')
        self.date_emprunt.set_date(datetime.now())
        self.date_retour_prevue.set_date(datetime.now() + timedelta(days=14))
        self.date_retour_effective.set_date(datetime.now())
        self.id_selectionne = None
        
        # Désélectionner dans le tableau
        for item in self.table.selection():
            self.table.selection_remove(item)