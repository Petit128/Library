# models/Categories_model.py
from .Connexion_base import *

class Categories_model:
    def __init__(self, id_categorie=None, nom_categorie=None):
        self._id_categorie = id_categorie
        self._nom_categorie = nom_categorie
    
    # Getters et Setters
    @property
    def id_categorie(self):
        return self._id_categorie
    
    @id_categorie.setter
    def id_categorie(self, value):
        self._id_categorie = value
    
    @property
    def nom_categorie(self):
        return self._nom_categorie
    
    @nom_categorie.setter
    def nom_categorie(self, value):
        self._nom_categorie = value
    
    def create(self):
        """Insère une nouvelle catégorie"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO categories (nom_categorie) VALUES (%s)"
            curseur.execute(chaine_req, (self.nom_categorie,))
            ma_connexion.commit()
            self._id_categorie = curseur.lastrowid
            return True
        except Exception as e:
            print(f"Erreur d'ajout de catégorie: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def read(self):
        """Lit une catégorie par son ID"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "SELECT * FROM categories WHERE id_categorie = %s"
            curseur.execute(chaine_req, (self.id_categorie,))
            result = curseur.fetchone()
            if result:
                self._nom_categorie = result[1]
                return True
            return False
        except Exception as e:
            print(f"Erreur de lecture de catégorie: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def read_all(self):
        """Lit toutes les catégories"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "SELECT * FROM categories ORDER BY nom_categorie"
            curseur.execute(chaine_req)
            return curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des catégories: {e}")
            return []
        finally:
            if curseur:
                curseur.close()
    
    def update(self):
        """Met à jour une catégorie"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "UPDATE categories SET nom_categorie = %s WHERE id_categorie = %s"
            valeurs = (self.nom_categorie, self.id_categorie)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
            return curseur.rowcount > 0
        except Exception as e:
            print(f"Erreur de modification de catégorie: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def delete(self):
        """Supprime une catégorie"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "DELETE FROM categories WHERE id_categorie = %s"
            curseur.execute(chaine_req, (self.id_categorie,))
            ma_connexion.commit()
            return curseur.rowcount > 0
        except Exception as e:
            print(f"Erreur de suppression de catégorie: {e}")
            return False
        finally:
            if curseur:
                curseur.close()