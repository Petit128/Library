# models/Livres_model.py
from .Connexion_base import *

class Livres_model:
    def __init__(self, id_livre=None, titre_livre=None, id_categorie=None):
        self._id_livre = id_livre
        self._titre_livre = titre_livre
        self._id_categorie = id_categorie
    
    # Getters
    @property
    def id_livre(self):
        return self._id_livre
    
    @property
    def titre_livre(self):
        return self._titre_livre
    
    @property
    def id_categorie(self):
        return self._id_categorie
    
    # Setters
    @id_livre.setter
    def id_livre(self, value):
        self._id_livre = value
    
    @titre_livre.setter
    def titre_livre(self, value):
        self._titre_livre = value
    
    @id_categorie.setter
    def id_categorie(self, value):
        self._id_categorie = value
    
    def create(self):
        """Insère un nouveau livre dans la base de données"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO livres (titre_livre, id_categorie) VALUES (%s, %s)"
            valeurs = (self.titre_livre, self.id_categorie)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
            self._id_livre = curseur.lastrowid
            return True
        except Exception as e:
            print(f"Erreur d'ajout de livre: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def read(self):
        """Lit un livre par son ID"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True)
            chaine_req = "SELECT * FROM livres WHERE id_livre = %s"
            curseur.execute(chaine_req, (self.id_livre,))
            result = curseur.fetchone()
            if result:
                self._titre_livre = result['titre_livre']
                self._id_categorie = result['id_categorie']
                return result
            return None
        except Exception as e:
            print(f"Erreur de lecture de livre: {e}")
            return None
        finally:
            if curseur:
                curseur.close()
    
    def read_all(self):
        """Lit tous les livres"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True)
            chaine_req = """
            SELECT l.*, c.nom_categorie 
            FROM livres l 
            LEFT JOIN categories c ON l.id_categorie = c.id_categorie
            ORDER BY l.titre_livre
            """
            curseur.execute(chaine_req)
            return curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des livres: {e}")
            return []
        finally:
            if curseur:
                curseur.close()
    
    def update(self):
        """Met à jour un livre"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "UPDATE livres SET titre_livre = %s, id_categorie = %s WHERE id_livre = %s"
            valeurs = (self.titre_livre, self.id_categorie, self.id_livre)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
            return curseur.rowcount > 0
        except Exception as e:
            print(f"Erreur de modification de livre: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def delete(self):
        """Supprime un livre"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "DELETE FROM livres WHERE id_livre = %s"
            curseur.execute(chaine_req, (self.id_livre,))
            ma_connexion.commit()
            return curseur.rowcount > 0
        except Exception as e:
            print(f"Erreur de suppression de livre: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def rechercher(self, terme):
        """Recherche des livres par terme"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True)
            chaine_req = """
            SELECT l.*, c.nom_categorie 
            FROM livres l 
            LEFT JOIN categories c ON l.id_categorie = c.id_categorie
            WHERE l.titre_livre LIKE %s 
            OR c.nom_categorie LIKE %s
            ORDER BY l.titre_livre
            """
            curseur.execute(chaine_req, (f"%{terme}%", f"%{terme}%"))
            return curseur.fetchall()
        except Exception as e:
            print(f"Erreur de recherche de livres: {e}")
            return []
        finally:
            if curseur:
                curseur.close()