
import numpy as np
import pandas as pd
import requests
import json
import sys
import spoonacular as sp
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests

def spoon_df():
    api = sp.API("31361112cdbe4c7aad28f3ca2879b6a7")


    ingredients=sys.argv[0]
    for i in range(1,len(sys.argv)):
        ingredients+=",+"+sys.argv[i]
    url="https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&ignorePantry=true&ranking=2&apiKey=31361112cdbe4c7aad28f3ca2879b6a7"
    response=api.search_recipes_by_ingredients(ingredients, fillIngredients=False, ranking=2)
    data=response.json()
    data = [{k: v for k, v in x.items() if k in ['title','id', 'missedIngredients']} for x in data]
    dff=pd.DataFrame(data)
    df=dff.head(5)
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
    df['calories'],df['carbs'],df['fat'],df['protein']=[""]*rows,[""]*rows,[""]*rows,[""]*rows
    for i in range(0,rows):
        u=f"https://api.spoonacular.com/recipes/{df['id'][i]}/nutritionWidget.json?apiKey=31361112cdbe4c7aad28f3ca2879b6a7"
        resp = requests.get(url=u)
        data2 = resp.json()
        str=json.dumps(data2)[0:(json.dumps(data2).index("bad")-3)]+"}"
        res = json.loads(str)
        for k in res.keys():
            df[k][i]=res[k][0:-1]
    print(df.drop(columns='id'))
    return df.drop(columns='id')
spoon_df()    