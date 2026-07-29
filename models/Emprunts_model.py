# models/Emprunts_model.py
from .Connexion_base import *

class Emprunts_model:
    def __init__(self, id_emprunt=None, date_emprunt=None, date_retour_prevue=None, 
                 date_retour_effective=None, id_livre=None, id_membre=None):
        self._id_emprunt = id_emprunt
        self._date_emprunt = date_emprunt
        self._date_retour_prevue = date_retour_prevue
        self._date_retour_effective = date_retour_effective
        self._id_livre = id_livre
        self._id_membre = id_membre
    
    # Getters et Setters
    @property
    def id_emprunt(self):
        return self._id_emprunt
    
    @id_emprunt.setter
    def id_emprunt(self, value):
        self._id_emprunt = value
    
    @property
    def date_emprunt(self):
        return self._date_emprunt
    
    @date_emprunt.setter
    def date_emprunt(self, value):
        self._date_emprunt = value
    
    @property
    def date_retour_prevue(self):
        return self._date_retour_prevue
    
    @date_retour_prevue.setter
    def date_retour_prevue(self, value):
        self._date_retour_prevue = value
    
    @property
    def date_retour_effective(self):
        return self._date_retour_effective
    
    @date_retour_effective.setter
    def date_retour_effective(self, value):
        self._date_retour_effective = value
    
    @property
    def id_livre(self):
        return self._id_livre
    
    @id_livre.setter
    def id_livre(self, value):
        self._id_livre = value
    
    @property
    def id_membre(self):
        return self._id_membre
    
    @id_membre.setter
    def id_membre(self, value):
        self._id_membre = value
    
    def create(self):
        """Insère un nouvel emprunt"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            # CORRECTION: Ordre correct des colonnes
            chaine_req = """
            INSERT INTO emprunts 
            (date_emprunt, date_retour_prevue, date_retour_effective, id_livre, id_membre) 
            VALUES (%s, %s, %s, %s, %s)
            """
            valeurs = (self.date_emprunt, self.date_retour_prevue, 
                      self.date_retour_effective, self.id_livre, self.id_membre)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
            self._id_emprunt = curseur.lastrowid
            return True
        except Exception as e:
            print(f"Erreur d'ajout d'emprunt: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def read(self):
        """Lit un emprunt par son ID"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True)
            chaine_req = """
            SELECT e.*, l.titre_livre, m.nom_membre 
            FROM emprunts e
            JOIN livres l ON e.id_livre = l.id_livre
            JOIN membres m ON e.id_membre = m.id_membre
            WHERE e.id_emprunt = %s
            """
            curseur.execute(chaine_req, (self.id_emprunt,))
            result = curseur.fetchone()
            if result:
                self._date_emprunt = result['date_emprunt']
                self._date_retour_prevue = result['date_retour_prevue']
                self._date_retour_effective = result['date_retour_effective']
                self._id_livre = result['id_livre']
                self._id_membre = result['id_membre']
                return result
            return None
        except Exception as e:
            print(f"Erreur de lecture d'emprunt: {e}")
            return None
        finally:
            if curseur:
                curseur.close()
    
    def read_all(self):
        """Lit tous les emprunts"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True)
            chaine_req = """
            SELECT e.*, l.titre_livre, m.nom_membre 
            FROM emprunts e
            JOIN livres l ON e.id_livre = l.id_livre
            JOIN membres m ON e.id_membre = m.id_membre
            ORDER BY e.date_emprunt DESC
            """
            curseur.execute(chaine_req)
            return curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des emprunts: {e}")
            return []
        finally:
            if curseur:
                curseur.close()
    
    def read_en_cours(self):
        """Lit les emprunts en cours (non retournés)"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True)
            chaine_req = """
            SELECT e.*, l.titre_livre, m.nom_membre 
            FROM emprunts e
            JOIN livres l ON e.id_livre = l.id_livre
            JOIN membres m ON e.id_membre = m.id_membre
            WHERE e.date_retour_effective IS NULL
            ORDER BY e.date_retour_prevue
            """
            curseur.execute(chaine_req)
            return curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des emprunts en cours: {e}")
            return []
        finally:
            if curseur:
                curseur.close()
    
    def update(self):
        """Met à jour un emprunt"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = """
            UPDATE emprunts 
            SET date_emprunt = %s, date_retour_prevue = %s, 
                date_retour_effective = %s, id_livre = %s, id_membre = %s 
            WHERE id_emprunt = %s
            """
            valeurs = (self.date_emprunt, self.date_retour_prevue, 
                      self.date_retour_effective, self.id_livre, 
                      self.id_membre, self.id_emprunt)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
            return curseur.rowcount > 0
        except Exception as e:
            print(f"Erreur de modification d'emprunt: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def delete(self):
        """Supprime un emprunt"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "DELETE FROM emprunts WHERE id_emprunt = %s"
            curseur.execute(chaine_req, (self.id_emprunt,))
            ma_connexion.commit()
            return curseur.rowcount > 0
        except Exception as e:
            print(f"Erreur de suppression d'emprunt: {e}")
            return False
        finally:
            if curseur:
                curseur.close()