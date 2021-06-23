from sqlalchemy import exc

from models.api_caller import API
from models.api_data_cleaner import make_readable
from models.db_creation import create_db
from views import Colors


class Control:
    """
    This class bridges the gap between user input and SQLAlchemy's ORM
    """

    def __init__(self, db):
        self.db = db
        self.run = True

        # self.current_menu is updated with every "menu" class method. It keeps track of where the user is in the
        # program, so reloading functions don't send them back at the beginning
        self.current_menu = None

        self.upper_separator = f"{Colors.BLACK}\n---------------------------------------------------------------{Colors.NORMAL}"
        self.lower_separator = f"{Colors.BLACK}---------------------------------------------------------------{Colors.NORMAL} \n"

    def validate_input(self, prompt="", *args, **kwargs):
        """ Makes sure that the user's input is a number
        Returns the choice if valid, or outputs an error message and reloads the current menu
        *args and **kwargs keep the relevant previous inputs so the user doesn't have to
        restart when the menu reloads
        """
        try:
            choice = int(input(prompt))
            return choice
        except ValueError:
            print(self.upper_separator)
            print(
                f"{Colors.YELLOW}Votre requête n'a pas été comprise. Utilisez les chiffres du clavier pour naviguer{Colors.NORMAL}")
            print(self.lower_separator)
            self.current_menu(*args, **kwargs)

    def reload_menu(self, *args, **kwargs):
        """ Function that's called when the user types a number out of range
        Displays an error message, then reloads the current menu
        *args and **kwargs keep the relevant previous inputs so the user doesn't have to
        restart when the menu reloads
        """
        print(self.upper_separator)
        print(f"{Colors.YELLOW}Il semblerait que vous ayez tapé un mauvais nombre, veuillez réessayer{Colors.NORMAL}")
        print(self.lower_separator)
        self.current_menu(*args, **kwargs)

    def starting_menu(self):
        """ Where the program begins, from there flow control is done with validated numbers"""
        self.current_menu = self.starting_menu
        prompt = f"{Colors.PURPLE}1 - Réinitialiser la base de données \n" \
                 f"{Colors.BLUE}2 - Créer un utilisateur \n" \
                 f"{Colors.CYAN}3 - Accéder à un compte existant \n" \
                 f"{Colors.RED}0 - Fermer le programme {Colors.NORMAL}\n"
        choice = self.validate_input(self.upper_separator + "\n" + prompt + self.lower_separator)
        if choice == 1:
            confirm_prompt = f"{Colors.YELLOW}Etes-vous sûr de vouloir tout réinitialiser? Les produits enregistrés " \
                             f"et utilisateurs \n" \
                             f"seront perdus: {Colors.NORMAL}\n" \
                             f"{Colors.RED}1 - Réinitialiser {Colors.NORMAL}\n" \
                             f"{Colors.GREEN}0 - Revenir au menu d'accueil {Colors.NORMAL}\n"
            confirm = self.validate_input(self.upper_separator + "\n" + confirm_prompt + self.lower_separator)
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
        prompt = f"{Colors.BLUE}1 - Trouver un aliment{Colors.NORMAL} \n" \
                 f"{Colors.CYAN}2 - Afficher vos produits subtitués{Colors.NORMAL} \n" \
                 f"{Colors.RED}0 - Fermer le programme{Colors.NORMAL} \n"
        choice = self.validate_input(self.upper_separator + "\n" + prompt + self.lower_separator)
        if choice == 1:
            self.find_product_menu()
        elif choice == 2:
            self.favourites_menu()
        elif choice == 0:
            self.quit()
        else:
            self.reload_menu()

    def favourites_menu(self):
        """ This menu gets a list of Favourite objects associated with the User, then displays selected data on screen
        The user is given the option to choose a favourite, using a list index
        If so, the chosen favourite object is passed to the favourite_details_menu
        """
        self.current_menu = self.favourites_menu
        prompt = "Voici la liste des produits que vous avez enregistrés. \n" \
                 "Entrez un numéro pour obtenir les détails de ce produit, \n" \
                 f"{Colors.BLUE}1 pour revenir au menu principal{Colors.NORMAL}, {Colors.RED}ou 0 pour fermer le programme{Colors.NORMAL}: \n"
        print(self.upper_separator + "\n" + prompt + self.lower_separator)
        favourites = self.db.get_favourites()
        for num, favourite in enumerate(favourites, start=2):
            print(f"{num} - {Colors.BLUE}{favourite.product.product_name_fr}{Colors.NORMAL} - {favourite.product.brands} \n"
                  f"    En remplacement de {Colors.CYAN}{[product.product_name_fr for product in self.db.session.query(Product).filter(Product.id.ilike(favourite.replaced_product))]}{Colors.NORMAL}")
        print(self.lower_separator)
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
        """ Takes a Favourite object as input, passed from the favourite_menu() function
        Chosen data is displayed by accessing attributes: favourite.product.KEY
        The user can then move on to another menu or delete this favourite
        """
        self.current_menu = self.favourite_details_menu
        print(self.upper_separator)
        print(f"{Colors.BLACK}Voici les détails du favori que vous avez sélectionné:{Colors.NORMAL} \n"
              f"{Colors.BLUE}{favourite.product.product_name_fr}{Colors.NORMAL} - {favourite.product.brands} - Nutriscore: {Colors.PURPLE}{favourite.product.nutriscore_grade}{Colors.NORMAL} \n"
              f"{Colors.BLACK}Il est disponible à l'achat dans ces magasins:{Colors.NORMAL} \n"
              f"{favourite.product.stores} \n"
              f"{Colors.BLACK}Consultez https://fr.openfoodfacts.org/produit/{favourite.product.code} pour plus de renseignements{Colors.NORMAL}")
        print(self.lower_separator)
        prompt = f"{Colors.BLUE}Tapez 1 pour retourner au menu précédent{Colors.NORMAL}, {Colors.CYAN}2 pour le menu principal{Colors.NORMAL}, {Colors.YELLOW}3 pour supprimer ce favori{Colors.NORMAL}, "\
                 f"{Colors.RED}ou 0 pour quitter{Colors.NORMAL}: \n"
        choice = self.validate_input(self.upper_separator + "\n" + prompt + self.lower_separator)
        if choice == 1:
            self.favourites_menu()
        elif choice == 2:
            self.main_menu()
        elif choice == 3:
            self.db.delete_favourite(favourite)
            print(self.upper_separator)
            print(f"{Colors.YELLOW}Le favori a été supprimé{Colors.NORMAL}")
            print(self.lower_separator)
            self.favourites_menu()
        elif choice == 0:
            self.quit()
        else:
            self.reload_menu()

    def find_product_menu(self):
        self.current_menu = self.find_product_menu
        prompt = f"{Colors.BLUE}1 - Sélectionner une catégorie {Colors.NORMAL}\n" \
                 f"{Colors.CYAN}2 - Revenir au menu précédent {Colors.NORMAL}\n" \
                 f"{Colors.RED}0 - Fermer le programme{Colors.NORMAL} \n"
        choice = self.validate_input(self.upper_separator + "\n" + prompt + self.lower_separator)
        if choice == 1:
            self.categories_menu()
        elif choice == 2:
            self.main_menu()
        elif choice == 0:
            self.quit()
        else:
            self.reload_menu()

    def categories_menu(self):
        """ This menu maps category names obtained in db_manipulation.get_categories() with numbers
        The user can then select a category by its number, which is passed to products_menu() to run
        a SQL SELECT statement
        """
        self.current_menu = self.categories_menu
        prompt = "Entrez un numéro pour obtenir les produits faisant partie de cette catégorie, \n" \
                 f"{Colors.RED}ou 0 pour fermer le programme{Colors.NORMAL}: \n"
        print(self.upper_separator + "\n" + prompt + self.lower_separator)
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
        """ This menu makes use of the "category" parameter passed from categories_menu() to obtain
        Product objects belonging to this category
        15 of them are kept using a list slice, and displayed with a number that the user can choose
        Chosen product is passed to substitutes_menu(), along with the category
        """
        self.current_menu = self.products_menu
        prompt = "Entrez un numéro pour sélectionner un produit et obtenir des suggestions plus saines, \n" \
                 f"{Colors.RED}ou 0 pour fermer le programme{Colors.NORMAL}: \n"
        print(self.upper_separator + "\n" + prompt + self.lower_separator)
        products = self.db.get_products_in_category(category)[:15]
        for num, product in enumerate(products, start=1):
            print(f"{num} - {Colors.BLUE}{product.product_name_fr}{Colors.NORMAL} - {product.brands} - Nutriscore: {Colors.PURPLE}{product.nutriscore_grade}{Colors.NORMAL}")
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
        """ This menu uses the product and category parameters to run a SQL statement, selecting
        Product objects with a better nutriscore, belonging to the same category as the product

        If the chosen product has a nutriscore of "A", a custom message is displayed, and the
        SQLAlchemy comparison filter changes from "<" to "==" to avoid a comparison error

        20 of the Product objects are kept using a list slice, and displayed with a number that the user can choose
        Chosen replacement product is passed to substitute_details_menu(), along with the initially chosen product
        """
        self.current_menu = self.substitutes_menu
        prompt = "Entrez un numéro pour sélectionner un produit et afficher ses informations, \n" \
                 "ou 0 pour fermer le programme: \n"
        if product.nutriscore_grade == "A":
            prompt = f"{Colors.GREEN}Le produit que vous avez choisi est excellent, mais voici quelques recommendations.{Colors.NORMAL} \n" \
                     "Entrez un numéro pour sélectionner un produit et afficher ses informations, \n" \
                     f"{Colors.RED}ou 0 pour fermer le programme{Colors.NORMAL}: \n"
            substitutes = self.db.session.query(Product).filter(Product.nutriscore_grade == product.nutriscore_grade,
                                                                Product.categories.ilike(f"%{category}%"))[:20]
        else:
            substitutes = self.db.get_replacement(product, category)[:20]
        print(self.upper_separator + "\n" + prompt + self.lower_separator)
        for num, sub in enumerate(substitutes, start=1):
            print(f"{num} - {Colors.BLUE}{sub.product_name_fr}{Colors.NORMAL} - {sub.brands} - Nutriscore: {Colors.PURPLE}{sub.nutriscore_grade}{Colors.NORMAL}")
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
        """ This menu compares the two Product object passed as parameters
        If the user chooses to register the substitute in their favourites, a new Favourite object is
        created, and added to the User's Favourite collection
        The substituted product is kept in the relationship as well, for reference
        """

        self.current_menu = self.substitute_details_menu
        print(self.upper_separator)
        print(f"{Colors.BLACK}Voici le produit pour lequel vous vouliez trouver un substitut: {Colors.NORMAL}\n"
              f"{Colors.BLUE}{product.product_name_fr}{Colors.NORMAL} - {product.brands} - Nutriscore: {Colors.PURPLE}{product.nutriscore_grade}{Colors.NORMAL}")
        print(f"{Colors.BLACK}Voici le produit de remplacement que vous avez sélectionné: {Colors.NORMAL}\n"
              f"{Colors.BLUE}{substitute.product_name_fr}{Colors.NORMAL} - {substitute.brands} - Nutriscore: {Colors.PURPLE}{substitute.nutriscore_grade}{Colors.NORMAL} \n"
              f"{Colors.BLACK}Il est disponible à l'achat dans ces magasins:{Colors.NORMAL} \n"
              f"{substitute.stores} \n"
              f"{Colors.BLACK}Consultez https://fr.openfoodfacts.org/produit/{substitute.code} pour plus de renseignements{Colors.NORMAL}"
              )
        print(self.lower_separator)
        prompt = "Voulez-vous enregistrer ce produit dans vos favoris? \n" \
                 f"{Colors.BLACK}Tapez 1 pour l'enregister{Colors.NORMAL}, {Colors.CYAN}2 pour revenir au menu principal{Colors.NORMAL}, ou {Colors.RED}0 pour quitter{Colors.NORMAL} \n"
        choice = self.validate_input(self.upper_separator + "\n" + prompt + self.lower_separator)
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
        """ See db_manipulation.add_favourite()
        If the action is successful, a Favourite object is created and a message is displayed
        If the Favourite object already exists, SQLAlchemy throws an IntegrityError, and the session reverts back
        """

        try:
            self.db.add_favourite(replacement, replaced)
            self.db.session.commit()
            print(self.upper_separator)
            print(f"{Colors.GREEN}Le produit a été ajouté à vos favoris{Colors.NORMAL}")
            print(self.lower_separator)
        except exc.IntegrityError:
            self.db.session.rollback()
            print(self.upper_separator)
            print(f"{Colors.YELLOW}Le produit est déjà enregistré dans vos favoris{Colors.NORMAL}")
            print(self.lower_separator)

    def initialise_db(self):
        """ See in models"""

        print(self.upper_separator)
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
        print(f"{Colors.GREEN}Réussite, la base de données est prête!{Colors.NORMAL}")
        print(self.lower_separator)

    def authenticate(self):
        """ Associates a User object to the session, to retrieve their favourites, and make
        Favourite creation possible
        User is found by matching a SQL query in the user table with an input()

        If 1 object is returned, this object becomes the User
        If 2 are returned, options are displayed and the user is asked to select the corresponding one
        If 0 are returned, the user is asked to check for spelling errors
        """

        while self.db.user is None:
            print(self.upper_separator)
            print("Entrez votre nom pour accéder à vos favoris:")
            print(self.lower_separator)
            users = self.db.get_user()
            if len([user for user in users]) == 1:
                self.db.user = [user for user in users][0]
                print(self.upper_separator)
                print(f"Bonjour, {Colors.CYAN}{self.db.user.username}{Colors.NORMAL}!")
                print(self.lower_separator)
            elif len([user for user in users]) == 0:
                print(self.upper_separator)
                print(f"{Colors.YELLOW}Aucun résultat trouvé; avez-vous fait une faute de frappe?{Colors.NORMAL}")
                print(self.lower_separator)
                continue
            else:
                print(self.upper_separator)
                print(f"{Colors.YELLOW}Plusieurs résultats correspondent à ce que vous avez entré:{Colors.NORMAL}")
                print([user.username for user in users])
                print(self.lower_separator)
                continue

    def create_user(self):
        """ User is asked to input a name, that the function attempts to register as a new User object's username
        If the action is successful, a User object is created and a message is displayed, the new User
        becomes the user for the session
        If a User with this name already exists, SQLAlchemy throws an IntegrityError, and the session reverts back
        """

        print(self.upper_separator)
        print("Entrez un nom d'utilisateur:")
        print(self.lower_separator)
        try:
            new_user = self.db.add_user(input())
            self.db.session.add(new_user)
            self.db.session.commit()
            self.db.user = new_user
            print(self.upper_separator)
            print(f"{Colors.GREEN}Le compte utilisateur de {new_user.username} a été créé!")
            print(self.lower_separator)
        except exc.IntegrityError:
            self.db.session.rollback()
            print(self.upper_separator)
            print(f"{Colors.RED}Ce nom d'utilisateur est déjà enregistré")
            print(self.lower_separator)
            self.create_user()

    def quit(self):
        print(self.upper_separator)
        print(f"{Colors.PURPLE}Au revoir!")
        print(self.lower_separator)
        self.run = False
