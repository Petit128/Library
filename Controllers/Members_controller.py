# Controllers/Members_controller.py
from models.Members_model import Members_model

class Members_controller:
    
    @classmethod
    def ajouter_membre(cls, nom_membre, contact_membre):
        """Ajoute un nouveau membre"""
        if not nom_membre or not nom_membre.strip():
            raise ValueError("Le nom du membre est obligatoire")
        if not contact_membre or not contact_membre.strip():
            raise ValueError("Le contact du membre est obligatoire")
        
        membre = Members_model(nom_membre=nom_membre.strip(), 
                              contact_membre=contact_membre.strip())
        try:
            if membre.create():
                return "Membre ajouté avec succès!"
        except ValueError as e:
            raise ValueError(str(e))
        except Exception:
            raise Exception("Erreur lors de l'ajout du membre")
    
    @classmethod
    def modifier_membre(cls, id_membre, nom_membre, contact_membre):
        """Modifie un membre existant"""
        if not nom_membre or not nom_membre.strip():
            raise ValueError("Le nom du membre est obligatoire")
        if not contact_membre or not contact_membre.strip():
            raise ValueError("Le contact du membre est obligatoire")
        
        membre = Members_model(id_membre=id_membre, nom_membre=nom_membre.strip(),
                              contact_membre=contact_membre.strip())
        try:
            if membre.update():
                return "Membre modifié avec succès!"
        except ValueError as e:
            raise ValueError(str(e))
        except Exception:
            raise Exception("Erreur lors de la modification du membre")
    
    @classmethod
    def supprimer_membre(cls, id_membre):
        """Supprime un membre"""
        membre = Members_model(id_membre=id_membre)
        if membre.delete():
            return "Membre supprimé avec succès!"
        else:
            raise Exception("Erreur lors de la suppression du membre")
    
    @classmethod
    def liste_membres(cls):
        """Récupère la liste de tous les membres"""
        membre = Members_model()
        return membre.read_all()
    
    @classmethod
    def get_membre(cls, id_membre):
        """Récupère un membre spécifique"""
        membre = Members_model(id_membre=id_membre)
        return membre.read()