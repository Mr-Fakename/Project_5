from controller import Control
from models.db_manipulation import Database


if __name__ == '__main__':

    db = Database()
    controller = Control(db)

    while controller.run:
        controller.starting_menu()
