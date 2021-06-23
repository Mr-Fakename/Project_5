# PurBeurre

Welcome to this GitHub page!
Here is our quickstart guide and documentation.


# *Philosophy*

The goal of this application is simple: 

 - Select a product you would like a healthy substitute for
 - The app works with OpenFoodFacts' API to return you a list of choices, based on Nutriscore
 - Compare the options, and save them in a database should you want to, for easy access down the line


## **Design and Development**

PurBeurre is built using the MVC architecture
Made with Python 3.8, [SQLAlchemy](https://www.sqlalchemy.org) and [Open Food Facts' API](https://world.openfoodfacts.org)

## **Requirements**

*certifi==2021.5.30*
*chardet==4.0.0*
*flake8==3.9.2*
*greenlet==1.1.0*
*idna==2.10*
*mccabe==0.6.1*
*pycodestyle==2.7.0*
*pyflakes==2.3.1*
*requests==2.25.1*
*SQLAlchemy==1.4.17*
*urllib3==1.26.5*
*Werkzeug==2.0.1*


## **Developer Manual** 


 This version works with French data; to change to the language of your liking, change the URL to include the country code you want:
 >In api_caller.py
 
``` python 
def get_data(self):  
	url = "https://fr.openfoodfacts.org/cgi/search.pl?"  
```

For more information about search options and parameters:
> https://world.openfoodfacts.org/data

It is also possible to change the data that will be stored in the database by changing items in the list:

``` python 
tags = ['brands', 'categories', 'code', 'nutriscore_grade', 'product_name_fr', 'stores']  
```

They correspond to keys in the JSON doc returned by the API.

---
To change of database management system, database name or location, modify the parameters passed to SQLAlchemy's *create_engine()* function:

> In models/db_creation.py

``` python 
def  create_db():
	 engine  =  create_engine("sqlite:///models/project_5_db")
```

> In models/db_manipulation.py

``` python 
class  Database:
	def __init__(self):
		self.engine = create_engine("sqlite:///models/project_5_db")
```
e.g., 
```python
create_engine("mysql:///folder/thisisadbname")
```

## **User Manual** 

As this is a pretty simple program, usage is very straightforward.

Interaction with the program is done on the Python console, using numbers.

The starting menu asks the user to choose between initialising the database, creating/connecting to a user account, or quitting.

**If this is the first time you're using the app, please create the database before proceeding further.**

Creating a user will allow you to save a favourite in the database, and retrieve it in a dedicated menu.
To access your favourites, just type the username you have chosen when starting the program.

---
The main scenario is as follows:
 - User is asked to select a category (Several numbers, each number associated with a category)
 - User chooses a product belonging to this category (Several numbers, each of them associated with a product)
 - App returns a list of possible substitutes, belonging to the same category, with a better nutriscore than the original product 
 (Several numbers, each of them associated with a product)
 - User selects a substitute, its info is displayed on screen
 - User can save their choice in the database



## **Others**

- Link to [Trello](https://trello.com/b/KTZ2iu0e/project-5) board for this project
