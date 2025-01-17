# Cook-n-Cart

models.py
- Sisältää datamalli-luokat tietokannan taulukoiden mukaan
- Mahdollistaa tietojen lisäämisen tietokantaan helposti luokista tehtyjen olioiden avulla
- Luokat: Product, Recipe, RecipeIngredient, ShoppingList, ShoppingListItem

database.py
- Imports: models.py
- Hoitaa keskustelun sqlite tietokannan kanssa
- Sisältää metodit tietokannan muutoksiin tai hakuihin esim. add_recipe(), add_product(), add_shopping_list()

controllers.py
- Imports: models.py, database.py
- Sisältää kontrollerit eri osa-alueille esim. reseptit, tuotteet ja ostoslistat

views.py
- Sisältää UI-koodin

app.py
- Juoksutettava koodi
