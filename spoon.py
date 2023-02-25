
import numpy as np
import pandas as pd
import requests
import json
import sys
import spoonacular as sp
from bs4 import BeautifulSoup as bs
api = sp.API("31361112cdbe4c7aad28f3ca2879b6a7")


ingredients=sys.argv[0]
for i in range(1,len(sys.argv)):
    ingredients+=",+"+sys.argv[i]
url="https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&ignorePantry=true&ranking=2&apiKey=31361112cdbe4c7aad28f3ca2879b6a7"
response=api.search_recipes_by_ingredients(ingredients, fillIngredients=False, ranking=2)
data=response.json()
data = [{k: v for k, v in x.items() if k in ['title','id', 'missedIngredients']} for x in data]
df=pd.DataFrame(data)
rows=len(df.index)
#df=pd.json_normalize(data, record_path=['missedIngredients'], meta=['name'])
str=""
missed=[""]*rows
for i in range(len(df['missedIngredients'])):
    for j in df['missedIngredients'][i]:
        str+=j['name']+", "
    missed[i]=str[:-2]
    str=""
df=df.drop('missedIngredients', axis=1)
df['missedIngredients']=missed
print(df)