# Controllers/Livres_controller.py
from models.Livres_model import Livres_model
from models.Categories_model import Categories_model

class Livres_controller:
    
    @classmethod
    def ajouter_livre(cls, titre_livre, id_categorie):
        """Ajoute un nouveau livre"""
        if not titre_livre or not titre_livre.strip():
            raise ValueError("Le titre du livre est obligatoire")
        
        livre = Livres_model(titre_livre=titre_livre.strip(), id_categorie=id_categorie)
        if livre.create():
            return "Livre ajouté avec succès!"
        else:
            raise Exception("Erreur lors de l'ajout du livre")
    
    @classmethod
    def modifier_livre(cls, id_livre, titre_livre, id_categorie):
        """Modifie un livre existant"""
        if not titre_livre or not titre_livre.strip():
            raise ValueError("Le titre du livre est obligatoire")
        
        livre = Livres_model(id_livre=id_livre, titre_livre=titre_livre.strip(), 
                            id_categorie=id_categorie)
        if livre.update():
            return "Livre modifié avec succès!"
        else:
            raise Exception("Erreur lors de la modification du livre")
    
    @classmethod
    def supprimer_livre(cls, id_livre):
        """Supprime un livre"""
        livre = Livres_model(id_livre=id_livre)
        if livre.delete():
            return "Livre supprimé avec succès!"
        else:
            raise Exception("Erreur lors de la suppression du livre")
    
    @classmethod
    def liste_livres(cls):
        """Récupère la liste de tous les livres"""
        livre = Livres_model()
        return livre.read_all()
    
    @classmethod
    def rechercher_livres(cls, terme):
        """Recherche des livres par terme"""
        livre = Livres_model()
        return livre.rechercher(terme)
    
    @classmethod
    def get_livre(cls, id_livre):
        """Récupère un livre spécifique"""
        livre = Livres_model(id_livre=id_livre)
        return livre.read()
    
    @classmethod
    def liste_categories(cls):
        """Récupère la liste des catégories"""
        categorie = Categories_model()
        return categorie.read_all()

        # Ajoutez cette méthode à la classe Livres_controller dans Controllers/Livres_controller.py

    @classmethod
    def get_livre_avec_categorie(cls, id_livre):
        """Récupère un livre avec les informations de sa catégorie"""
        livre = Livres_model(id_livre=id_livre)
        result = livre.read()
        if result:
            return result
        return Noness