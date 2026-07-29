# models/Connexion_base.py
import mysql.connector
from mysql.connector import Error
import threading

class Connexion_base:
    """Classe singleton pour gérer les connexions à la base de données"""
    _instance = None
    _lock = threading.Lock()
    _connection = None
    
    # Configuration de la base de données
    _config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',  # À modifier selon votre configuration
        'password': '',  # À modifier selon votre configuration
        'database': 'library',
        'charset': 'utf8mb4',
        'autocommit': True
    }
    
    @staticmethod
    def get_connexion():
        """Retourne une connexion à la base de données"""
        with Connexion_base._lock:
            try:
                if Connexion_base._connection is None or not Connexion_base._connection.is_connected():
                    Connexion_base._connection = mysql.connector.connect(
                        **Connexion_base._config
                    )
                return Connexion_base._connection
            except Error as err:
                print(f"Erreur de connexion à la base de données: {err}")
                raise
    
    @staticmethod
    def close_connexion():
        """Ferme la connexion à la base de données"""
        with Connexion_base._lock:
            if Connexion_base._connection and Connexion_base._connection.is_connected():
                Connexion_base._connection.close()
                Connexion_base._connection = None
    
    @staticmethod
    def test_connexion():
        """Teste la connexion à la base de données"""
        try:
            conn = Connexion_base.get_connexion()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchall()  # Lire tous les résultats pour éviter "Unread result found"
            cursor.close()
            return True
        except Exception as e:
            print(f"Erreur de test de connexion: {e}")
            return False