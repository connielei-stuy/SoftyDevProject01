from flask import Flask, render_template, request
from utils.recipe_func import *
from utils.nutri_func import *
import requests
import json

app = Flask(__name__)

def findRecipes(item):
	recipes=search_json(item)
       # print recipes
	if request.form["carb"] == "":
		  carbamount = 0
	else:
		  carbamount = float(request.form["carb"])
	if request.form["protein"] == "":
		  proteinamount = 0
	else:
		  proteinamount = float(request.form["protein"])
	if request.form["fat"] == "":
		  fatamount = 0
	else:
		  fatamount = float(request.form["fat"])
	recipeIDs = []
	for recipe in recipes:
		  recipeIDs.append(recipe_id(recipe))
	differences = []
	for recipeID in recipeIDs:
		#print recipeID
		nutrient_info = sumNutri(get_ingredients_dict(recipeID))
		differences.append(abs(nutrient_info[0] - carbamount) + abs(nutrient_info[1] - proteinamount) + abs(nutrient_info[2] - fatamount))
		#print differences
	#print differences
	chosen = []
	chosen1 = recipeIDs[differences.index(min(differences))]
	chosen.append(chosen1)
	differences.pop(differences.index(min(differences)))
	chosen2 = recipeIDs[differences.index(min(differences))]
	chosen.append(chosen2)
	differences.pop(differences.index(min(differences)))
	chosen3 = recipeIDs[differences.index(min(differences))]
	chosen.append(chosen3)
	differences.pop(differences.index(min(differences)))
	return chosen

@app.route('/', methods=['GET','POST'])
def root():
	#r = requests.get("https://api.nasa.gov/planetary/apod?api_key=CJIKeQKz4nuOpRSiMmW2qWB7qylNrE717O2q30Va")
	#dictionary = r.json()
       if request.method == 'POST':
              thechosen = findRecipes(request.form["food"])
              return render_template('recipes.html', recipe_one = recipe_title(recipe_json(thechosen[0])), recipe1url = recipe_source_url(recipe_json(thechosen[0])), recipe_two = recipe_title(recipe_json(thechosen[1])), recipe2url = recipe_source_url(recipe_json(thechosen[1])), recipe_three = recipe_title(recipe_json(thechosen[2])), recipe3url = recipe_source_url(recipe_json(thechosen[2])))
       else:
              return render_template('index.html')

	
if __name__ == '__main__':
	app.run(debug = True)
