# Controllers/Categories_controller.py
from models.Categories_model import Categories_model

class Categories_controller:
    
    @classmethod
    def ajouter_categorie(cls, nom_categorie):
        """Ajoute une nouvelle catégorie"""
        if not nom_categorie or not nom_categorie.strip():
            raise ValueError("Le nom de la catégorie est obligatoire")
        
        categorie = Categories_model(nom_categorie=nom_categorie.strip())
        if categorie.create():
            return "Catégorie ajoutée avec succès!"
        else:
            raise Exception("Erreur lors de l'ajout de la catégorie")
    
    @classmethod
    def modifier_categorie(cls, id_categorie, nom_categorie):
        """Modifie une catégorie existante"""
        if not nom_categorie or not nom_categorie.strip():
            raise ValueError("Le nom de la catégorie est obligatoire")
        
        categorie = Categories_model(id_categorie=id_categorie, 
                                   nom_categorie=nom_categorie.strip())
        if categorie.update():
            return "Catégorie modifiée avec succès!"
        else:
            raise Exception("Erreur lors de la modification de la catégorie")
    
    @classmethod
    def supprimer_categorie(cls, id_categorie):
        """Supprime une catégorie"""
        categorie = Categories_model(id_categorie=id_categorie)
        if categorie.delete():
            return "Catégorie supprimée avec succès!"
        else:
            raise Exception("Erreur lors de la suppression de la catégorie")
    
    @classmethod
    def liste_categories(cls):
        """Récupère la liste de toutes les catégories"""
        categorie = Categories_model()
        return categorie.read_all()
    
    @classmethod
    def get_categorie(cls, id_categorie):
        """Récupère une catégorie spécifique"""
        categorie = Categories_model(id_categorie=id_categorie)
        if categorie.read():
            return categorie
        return None