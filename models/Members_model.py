# models/Members_model.py
from .Connexion_base import *

class Members_model:
    def __init__(self, id_membre=None, nom_membre=None, contact_membre=None):
        self._id_membre = id_membre
        self._nom_membre = nom_membre
        self._contact_membre = contact_membre
    
    # Getters et Setters avec properties
    @property
    def id_membre(self):
        return self._id_membre
    
    @id_membre.setter
    def id_membre(self, value):
        self._id_membre = value
    
    @property
    def nom_membre(self):
        return self._nom_membre
    
    @nom_membre.setter
    def nom_membre(self, value):
        self._nom_membre = value
    
    @property
    def contact_membre(self):
        return self._contact_membre
    
    @contact_membre.setter
    def contact_membre(self, value):
        self._contact_membre = value
    
    def create(self):
        """Insère un nouveau membre"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "INSERT INTO membres (nom_membre, contact_membre) VALUES (%s, %s)"
            valeurs = (self.nom_membre, self.contact_membre)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
            self._id_membre = curseur.lastrowid
            return True
        except mysql.connector.IntegrityError:
            raise ValueError("Ce contact existe déjà!")
        except Exception as e:
            print(f"Erreur d'ajout de membre: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def read(self):
        """Lit un membre par son ID"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True)
            chaine_req = "SELECT * FROM membres WHERE id_membre = %s"
            curseur.execute(chaine_req, (self.id_membre,))
            result = curseur.fetchone()
            if result:
                self._nom_membre = result['nom_membre']
                self._contact_membre = result['contact_membre']
                return result
            return None
        except Exception as e:
            print(f"Erreur de lecture de membre: {e}")
            return None
        finally:
            if curseur:
                curseur.close()
    
    def read_all(self):
        """Lit tous les membres"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor(dictionary=True)
            chaine_req = "SELECT * FROM membres ORDER BY nom_membre"
            curseur.execute(chaine_req)
            return curseur.fetchall()
        except Exception as e:
            print(f"Erreur de lecture des membres: {e}")
            return []
        finally:
            if curseur:
                curseur.close()
    
    def update(self):
        """Met à jour un membre"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "UPDATE membres SET nom_membre = %s, contact_membre = %s WHERE id_membre = %s"
            valeurs = (self.nom_membre, self.contact_membre, self.id_membre)
            curseur.execute(chaine_req, valeurs)
            ma_connexion.commit()
            return curseur.rowcount > 0
        except mysql.connector.IntegrityError:
            raise ValueError("Ce contact existe déjà!")
        except Exception as e:
            print(f"Erreur de modification de membre: {e}")
            return False
        finally:
            if curseur:
                curseur.close()
    
    def delete(self):
        """Supprime un membre"""
        ma_connexion = None
        curseur = None
        try:
            ma_connexion = Connexion_base.get_connexion()
            curseur = ma_connexion.cursor()
            chaine_req = "DELETE FROM membres WHERE id_membre = %s"
            curseur.execute(chaine_req, (self.id_membre,))
            ma_connexion.commit()
            return curseur.rowcount > 0
        except Exception as e:
            print(f"Erreur de suppression de membre: {e}")
            return False
        finally:
            if curseur:
                curseur.close()