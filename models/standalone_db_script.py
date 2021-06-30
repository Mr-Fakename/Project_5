from models.db_creation import create_db
from models.api_caller import API
from models.api_data_cleaner import make_readable
from models.db_manipulation import Database


print("\n---------------------------------------------------------------")
print("Initialisation de la base de données...")
create_db()
print("Collecte des données...")
api = API()
api.get_data()
print("Nettoyage des données...")
api.cleaner()
data = make_readable(api.cleaned_data)
print("Remplissage de la base de données...")
db = Database()
db.fill_db(data)
print("Réussite, la base de données est prête!")
print("---------------------------------------------------------------\n")
