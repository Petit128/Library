# main.py
import tkinter as tk
from tkinter import messagebox
import sys
import traceback

def main():
    """
    Point d'entrée principal de l'application de gestion de bibliothèque
    """
    root = None
    try:
        # Créer la fenêtre principale
        root = tk.Tk()
        
        # Configuration de la fenêtre
        root.title("Gestion de Bibliothèque")
        root.geometry("1200x700")
        
        # Empêcher le redimensionnement trop petit
        root.minsize(1000, 600)
        
        # Initialiser l'application
        from views.main_view import MainView
        app = MainView(root)
        
        # Si l'application a été détruite à cause d'une erreur de connexion
        if not root.winfo_exists():
            return
        
        # Gestion de la fermeture de la fenêtre
        def on_closing():
            try:
                if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application?"):
                    # Fermer proprement la connexion à la base de données
                    from models.Connexion_base import Connexion_base
                    Connexion_base.close_connexion()
                    root.destroy()
            except:
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Lancer la boucle principale
        root.mainloop()
        
    except Exception as e:
        # Afficher l'erreur complète
        error_msg = f"Une erreur critique est survenue:\n\n{str(e)}\n\n"
        error_msg += "Traceback complet:\n" + traceback.format_exc()
        
        print(error_msg)
        
        if root and root.winfo_exists():
            messagebox.showerror("Erreur fatale", 
                f"Une erreur critique est survenue:\n\n{str(e)}\n\n"
                "L'application va se fermer.")
            root.destroy()
        else:
            messagebox.showerror("Erreur fatale", 
                f"Impossible de démarrer l'application:\n\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()