from sqlalchemy import exc

from models.api_caller import API
from models.api_data_cleaner import make_readable
from models.db_creation import *


class Control:
    def __init__(self, db):
        self.db = db
        self.run = True
        self.current_menu = None

    @staticmethod
    def validate_input(prompt=""):
        try:
            choice = int(input(prompt))
            return choice
        except ValueError:
            print("Votre requête n'a pas été comprise. Utilisez les chiffres du clavier pour naviguer")

    def reload_menu(self, *args, **kwargs):
        print("Il semblerait que vous ayez tapé un mauvais nombre, veuillez réessayer")
        self.current_menu(*args, **kwargs)

    def starting_menu(self):
        self.current_menu = self.starting_menu
        prompt = "1 - Réinitialiser la base de données \n" \
                 "2 - Créer un utilisateur \n" \
                 "3 - Accéder à un compte existant \n" \
                 "0 - Fermer le programme \n"
        choice = self.validate_input(prompt)
        if choice == 1:
            confirm_prompt = "Etes-vous sûr de vouloir tout réinitialiser? Les produits enregistrés et utilisateurs \n" \
                             "seront perdus \n" \
                             "1 - Réinitialiser \n" \
                             "0 - Revenir au menu d'accueil \n"
            confirm = self.validate_input(confirm_prompt)
            if confirm == 1:
                self.initialise_db()
            elif confirm == 0:
                self.starting_menu()
            else:
                self.reload_menu()
        elif choice == 2:
            self.create_user()
            self.main_menu()
        elif choice == 3:
            self.authenticate()
            self.main_menu()
        elif choice == 0:
            self.quit()
        else:
            self.reload_menu()

    def main_menu(self):
        self.current_menu = self.main_menu
        prompt = "1 - Trouver un aliment \n" \
                 "2 - Afficher vos produits subtitués \n" \
                 "0 - Fermer le programme \n"
        choice = self.validate_input(prompt)
        if choice == 1:
            self.find_product_menu()
        elif choice == 2:
            self.favourites_menu()
        elif choice == 0:
            self.quit()
        else:
            self.reload_menu()

    def favourites_menu(self):
        self.current_menu = self.favourites_menu
        prompt = "Voici la liste des produits que vous avez enregistrés. \n" \
                 "Entrez un numéro pour obtenir les détails de ce produit, \n" \
                 "1 pour revenir au menu principal, ou 0 pour fermer le programme: \n"
        print(prompt)
        favourites = self.db.get_favourites()
        for num, favourite in enumerate(favourites, start=2):
            print(f"{num} - {favourite.product.product_name_fr} - {favourite.product.brands} \n"
                  f"En remplacement de {[product.product_name_fr for product in self.db.session.query(Product).filter(Product.id.ilike(favourite.replaced_product))]}")
        choice = self.validate_input()
        if choice == 0:
            self.quit()
        elif choice == 1:
            self.main_menu()
        else:
            try:
                favourite = favourites[choice - 2]
                self.favourite_details_menu(favourite)
            except IndexError:
                self.reload_menu()

    def favourite_details_menu(self, favourite):
        self.current_menu = self.favourite_details_menu
        print("Voici les détails du favori que vous avez sélectionné: \n"
              f"{favourite.product.product_name_fr} - {favourite.product.brands} - Nutriscore: {favourite.product.nutriscore_grade} \n "
              "Il est disponible à l'achat dans ces magasins: \n"
              f"{favourite.product.stores} \n"
              f"Consultez https://fr.openfoodfacts.org/produit/{favourite.product.code} pour plus de renseignements")
        prompt = "Tapez 1 pour retourner au menu précédent, 2 pour le menu principal, 3 pour supprimer ce favori, " \
                 "ou 0 pour quitter: "
        choice = self.validate_input(prompt)
        if choice == 1:
            self.favourites_menu()
        elif choice == 2:
            self.main_menu()
        elif choice == 3:
            self.db.delete_favourite(favourite)
            self.favourites_menu()
        elif choice == 0:
            self.quit()
        else:
            self.reload_menu()

    def find_product_menu(self):
        self.current_menu = self.find_product_menu
        prompt = "1 - Sélectionner une catégorie \n" \
                 "2 - Revenir au menu précédent \n" \
                 "0 - Fermer le programme \n"
        choice = self.validate_input(prompt)
        if choice == 1:
            self.categories_menu()
        elif choice == 2:
            self.main_menu()
        elif choice == 0:
            self.quit()
        else:
            self.reload_menu()

    def categories_menu(self):
        self.current_menu = self.categories_menu
        prompt = "Entrez un numéro pour obtenir les produits faisant partie de cette catégorie, \n" \
                 "ou 0 pour fermer le programme: \n"
        print(prompt)
        categories = self.db.get_categories()
        for num, category in enumerate(categories, start=1):
            print(f"{num} - {category}")
        choice = self.validate_input()
        if choice == 0:
            self.quit()
        else:
            try:
                category = categories[choice - 1]
                self.products_menu(category)
            except IndexError:
                self.reload_menu()

    def products_menu(self, category):
        self.current_menu = self.products_menu
        prompt = "Entrez un numéro pour sélectionner un produit et obtenir des suggestions plus saines, \n" \
                 "ou 0 pour fermer le programme: \n"
        print(prompt)
        products = self.db.get_products_in_category(category)[:15]
        for num, product in enumerate(products, start=1):
            print(f"{num} - {product.product_name_fr} - {product.brands} - Nutriscore: {product.nutriscore_grade}")
        choice = self.validate_input()
        if choice == 0:
            self.quit()
        else:
            try:
                product = products[choice - 1]
                self.substitutes_menu(product, category)
            except IndexError:
                self.reload_menu(category)

    def substitutes_menu(self, product, category):
        self.current_menu = self.substitutes_menu
        prompt = "Entrez un numéro pour sélectionner un produit et afficher ses informations, \n" \
                 "ou 0 pour fermer le programme: \n"
        if product.nutriscore_grade == "A":
            prompt = "Le produit que vous avez choisi est excellent, mais voici quelques recommendations. \n" \
                     "Entrez un numéro pour sélectionner un produit et afficher ses informations, \n" \
                     "ou 0 pour fermer le programme: \n"
            substitutes = self.db.session.query(Product).filter(Product.nutriscore_grade == product.nutriscore_grade,
                                                                Product.categories.ilike(f"%{category}%"))
        else:
            substitutes = self.db.get_replacement(product, category)
        print(prompt)
        for num, sub in enumerate(substitutes, start=1):
            print(f"{num} - {sub.product_name_fr} - {sub.brands} - Nutriscore: {sub.nutriscore_grade}")
        choice = self.validate_input()
        if choice == 0:
            self.quit()
        else:
            try:
                substitute = substitutes[choice - 1]
                self.substitute_details_menu(product, substitute)
            except IndexError:
                self.reload_menu(product, category)

    def substitute_details_menu(self, product, substitute):
        self.current_menu = self.substitute_details_menu
        print("Voici le produit pour lequel vous vouliez trouver un substitut: \n"
              f"{product.product_name_fr} - {product.brands} - Nutriscore: {product.nutriscore_grade}")
        print("Voici le produit de remplacement que vous avez sélectionné: \n"
              f"{substitute.product_name_fr} - {substitute.brands} - Nutriscore: {substitute.nutriscore_grade} \n"
              "Il est disponible à l'achat dans ces magasins: \n"
              f"{substitute.stores} \n"
              f"Consultez https://fr.openfoodfacts.org/produit/{substitute.code} pour plus de renseignements"
              )
        prompt = "Voulez-vous enregistrer ce produit dans vos favoris? \n" \
                 "Tapez 1 pour l'enregister, 2 pour revenir au menu principal, ou 0 pour quitter"
        choice = self.validate_input(prompt)
        if choice == 1:
            self.add_favourite(substitute, product)
            self.main_menu()
        elif choice == 2:
            self.main_menu()
        elif choice == 0:
            self.quit()
        else:
            self.reload_menu(product, substitute)

    def add_favourite(self, replacement, replaced):
        try:
            self.db.add_favourite(replacement, replaced)
            self.db.session.commit()
            print("Le produit a été ajouté à vos favoris")
        except exc.IntegrityError:
            self.db.session.rollback()
            print("Le produit est déjà enregistré dans vos favoris")

    def initialise_db(self):
        print("Initialisation de la base de données...")
        create_db()
        print("Collecte des données...")
        api = API()
        api.get_data()
        print("Nettoyage des données...")
        api.cleaner()
        data = make_readable(api.cleaned_data)
        print("Remplissage de la base de données...")
        self.db.fill_db(data)
        print("Réussite, la base de données est prête!")

    def authenticate(self):
        while self.db.user is None:
            print("Entrez votre nom pour accéder à vos favoris:")
            users = self.db.get_user()
            if len([user for user in users]) == 1:
                self.db.user = [user for user in users][0]
                print(f"Bonjour, {self.db.user.username}!")
            elif len([user for user in users]) == 0:
                print("Aucun résultat trouvé; avez-vous fait une faute de frappe?")
                continue
            else:
                print("Plusieurs résultats correspondent à ce que vous avez entré:")
                print([user.username for user in users])
                continue

    def create_user(self):
        print("Entrez un nom d'utilisateur:")
        try:
            new_user = self.db.add_user(input())
            self.db.session.add(new_user)
            self.db.session.commit()
            self.db.user = new_user
            print(f"Le compte utilisateur de {new_user.username} a été créé!")
        except exc.IntegrityError:
            self.db.session.rollback()
            print("Ce nom d'utilisateur est déjà enregistré")
            self.create_user()

    def quit(self):
        print("Au revoir!")
        self.run = False
