# PurBeurre

Hi! Welcome to this GitHub page!
Here is our quickstart guide and user friendly documentation.


# *Philosophy*

The goal of this application is simple: 

 - Select a product you would like a healthy substitute for
 - The app works with OpenFoodFacts' API to return you a list of choices, based on Nutriscore
 - Compare the options, and save them in a database should you want to, for easy access down the line


## **Design and Development**

PurBeurre is built using the MVC architecture
Made with Python 3, MySQL, Open Food Facts' API

## **Requirements**

*Libraries and requirements: Include a pip freeze*


## **Developer Manual** 

*Installation walkthrough, setup and config - include screenshots*

 This version works with French data; to change to the language of your liking, change the URL to include the country code you want:
  ``` python 
def get_data(self):  
	url = "https://fr.openfoodfacts.org/cgi/search.pl?"  
```

For more information about search options and parameters:
> https://world.openfoodfacts.org/data

## **User Manual** 

Quick start guide, complete manual

The user is on the command prompt. They're being asked to choose between:

 - 1 - Replace a product
 - 2 - Access the products saved in the DB
 - 3 - Quit

If 1 is selected:
 - User is asked to select a category (Several numbers, each number associated with a category)
 - User chooses a product (Several numbers, each of them associated with a product)
 - App returns a substitute; with a description, where this product is sold, and a link to OFF
 - User can save their choice on the database

If 2 is selected:
 - User can see their favourite products 


## **Features**

 - All product data comes from [Open Food Facts](https://world.openfoodfacts.org)
 - This version makes use of the good ol' command prompt
 - Use only numbers to navigate in the app
 



