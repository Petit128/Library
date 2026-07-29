# Controllers/Emprunts_controller.py
from models.Emprunts_model import Emprunts_model
from models.Livres_model import Livres_model
from models.Members_model import Members_model
from datetime import datetime, timedelta

class Emprunts_controller:
    
    @classmethod
    def ajouter_emprunt(cls, id_livre, id_membre, date_emprunt=None, date_retour_prevue=None):
        """Ajoute un nouvel emprunt"""
        # Validation
        if not id_livre:
            raise ValueError("Veuillez sélectionner un livre")
        if not id_membre:
            raise ValueError("Veuillez sélectionner un membre")
        
        # Vérifier si le livre est disponible
        livre_disponible = cls.verifier_livre_disponible(id_livre)
        if not livre_disponible:
            raise ValueError("Ce livre est déjà emprunté")
        
        # Définir les dates par défaut si non fournies
        if not date_emprunt:
            date_emprunt = datetime.now().strftime('%Y-%m-%d')
        
        if not date_retour_prevue:
            date_retour_prevue = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        
        # Vérifier que la date de retour est après la date d'emprunt
        date_emp = datetime.strptime(date_emprunt, '%Y-%m-%d')
        date_ret = datetime.strptime(date_retour_prevue, '%Y-%m-%d')
        if date_ret <= date_emp:
            raise ValueError("La date de retour doit être après la date d'emprunt")
        
        # Créer l'emprunt
        emprunt = Emprunts_model(
            date_emprunt=date_emprunt,
            date_retour_prevue=date_retour_prevue,
            date_retour_effective=None,
            id_livre=id_livre,
            id_membre=id_membre
        )
        
        if emprunt.create():
            return "Emprunt enregistré avec succès!"
        else:
            raise Exception("Erreur lors de l'enregistrement de l'emprunt")
    
    @classmethod
    def enregistrer_retour(cls, id_emprunt, date_retour_effective=None):
        """Enregistre le retour d'un livre"""
        if not date_retour_effective:
            date_retour_effective = datetime.now().strftime('%Y-%m-%d')
        
        # Récupérer l'emprunt
        emprunt = Emprunts_model(id_emprunt=id_emprunt)
        emprunt_data = emprunt.read()
        
        if not emprunt_data:
            raise ValueError("Emprunt introuvable")
        
        # Vérifier si déjà retourné
        if emprunt_data['date_retour_effective']:
            raise ValueError("Ce livre a déjà été retourné")
        
        # Mettre à jour avec la date de retour
        emprunt.date_retour_effective = date_retour_effective
        emprunt.date_emprunt = emprunt_data['date_emprunt']
        emprunt.date_retour_prevue = emprunt_data['date_retour_prevue']
        emprunt.id_livre = emprunt_data['id_livre']
        emprunt.id_membre = emprunt_data['id_membre']
        
        if emprunt.update():
            # Calculer les jours de retard
            jours_retard = cls.calculer_retard(emprunt_data['date_retour_prevue'], 
                                              date_retour_effective)
            message = "Retour enregistré avec succès!"
            if jours_retard > 0:
                message += f"\n\nRetard: {jours_retard} jour(s)"
            return message
        else:
            raise Exception("Erreur lors de l'enregistrement du retour")
    
    @classmethod
    def supprimer_emprunt(cls, id_emprunt):
        """Supprime un emprunt"""
        emprunt = Emprunts_model(id_emprunt=id_emprunt)
        if emprunt.delete():
            return "Emprunt supprimé avec succès!"
        else:
            raise Exception("Erreur lors de la suppression de l'emprunt")
    
    @classmethod
    def liste_emprunts(cls):
        """Récupère la liste de tous les emprunts"""
        emprunt = Emprunts_model()
        return emprunt.read_all()
    
    @classmethod
    def liste_emprunts_en_cours(cls):
        """Récupère la liste des emprunts en cours"""
        emprunt = Emprunts_model()
        return emprunt.read_en_cours()
    
    @classmethod
    def verifier_livre_disponible(cls, id_livre):
        """Vérifie si un livre est disponible (non emprunté)"""
        emprunts_en_cours = cls.liste_emprunts_en_cours()
        for emp in emprunts_en_cours:
            if emp['id_livre'] == id_livre:
                return False
        return True
    
    @classmethod
    def calculer_retard(cls, date_retour_prevue, date_retour_effective):
        """Calcule le nombre de jours de retard"""
        date_prevue = datetime.strptime(str(date_retour_prevue), '%Y-%m-%d')
        date_effective = datetime.strptime(str(date_retour_effective), '%Y-%m-%d')
        
        if date_effective > date_prevue:
            return (date_effective - date_prevue).days
        return 0
    
    @classmethod
    def get_livres_disponibles(cls):
        """Récupère la liste des livres disponibles"""
        livre_model = Livres_model()
        tous_livres = livre_model.read_all()
        livres_disponibles = []
        
        for livre in tous_livres:
            if cls.verifier_livre_disponible(livre['id_livre']):
                livres_disponibles.append(livre)
        
        return livres_disponibles
    
    @classmethod
    def get_emprunt(cls, id_emprunt):
        """Récupère un emprunt spécifique"""
        emprunt = Emprunts_model(id_emprunt=id_emprunt)
        return emprunt.read()